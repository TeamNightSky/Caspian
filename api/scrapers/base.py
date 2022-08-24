"""Module for Scraper protocol."""

import asyncio
import contextlib
import os
import pathlib
import tempfile
import urllib.parse
import uuid
from typing import Any, Generator

import audio_metadata
from storage3._async.bucket import AsyncBucket

from api.db import DB


def get_metadata(download: pathlib.Path) -> dict[str, Any]:
    """Return the metadata for the downloaded mp3 file."""
    song = audio_metadata.load(download)
    return {
        "title": song.tags.title[0] if song.tags.get("title", []) else None,
        "artist": song.tags.artist[0] if song.tags.get("artist", []) else None,
        "album": song.tags.album[0] if song.tags.get("album", []) else None,
        "album_artist": song.tags.album_artist[0] if song.tags.get("album_artist", []) else None,
        "year": song.tags.year[0] if song.tags.get("year", []) else None,
        "genre": song.tags.genre[0] if song.tags.get("genre", []) else None,
        "duration": float(song.streaminfo.get("duration", "0.0")),
        "cover": song.pictures[0].data if song.get("pictures", []) else None,
    }


def prepare_url(url: str) -> str:
    """Prepares URL for scraping."""
    return (
        urllib.parse.urlparse(url)
        ._replace(
            scheme="https",
            fragment="",
        )
        .geturl()
    )


class Scraper:
    """Base class for scrapers."""

    LOGS_DIR = pathlib.Path("logs")
    DOWNLOAD_DIR = pathlib.Path("downloads")

    active_scrapers: dict[str, "Scraper"] = {}

    def __init__(self, url: str):
        self.url = prepare_url(url)
        self.download_id = f"download-{uuid.uuid4()}"
        self.process: asyncio.subprocess.Process | None = None

    def __init_subclass__(cls, source: str) -> None:
        cls.source = source

    @property
    def log_id(self) -> str:
        """Return the log id."""
        return f"{self.download_id}.log"

    @property
    def log_file(self) -> pathlib.Path:
        """Return the log file."""
        path = self.LOGS_DIR / self.log_id
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        return path

    @property
    def download_dir(self) -> pathlib.Path:
        """Return the download path."""
        path = self.DOWNLOAD_DIR / self.download_id
        if not path.exists():
            path.mkdir(parents=True)
        return path

    async def start(
        self,
        stdout: Any,
        stderr: Any,
        stdin: Any,
    ) -> asyncio.subprocess.Process:  # pylint: disable=no-member
        """Starts the scraper subprocess."""
        raise NotImplementedError()

    def downloads(self) -> Generator[pathlib.Path, None, None]:
        """Return the list of downloaded mp3 files."""
        return self.download_dir.glob("*.mp3")

    @contextlib.contextmanager
    def active(self):
        """Context manager for an active scraper."""
        Scraper.active_scrapers[self.download_id] = self
        try:
            yield
        finally:
            del Scraper.active_scrapers[self.download_id]

    async def run(self, timeout: int) -> None:
        """Run the scraper."""
        print("Downloading...", self.url)
        with self.active():
            self.process = await self.start(
                self.log_file.open("wb"),
                asyncio.subprocess.STDOUT,
                None,
            )
            try:
                await asyncio.wait_for(self.process.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                self.process.kill()
            except Exception as exc:
                self.process.kill()
                raise exc from None
            finally:
                await self.upload()

    async def upload(self) -> None:
        """Upload the downloaded mp3 files and logs to the database."""
        bucket = await DB.storage.get_bucket("files")
        for path in self.downloads():
            await self.upload_download(bucket, path)
            os.remove(path)
        await self.upload_log(bucket)
        os.rmdir(self.download_dir)

    async def upload_download(self, bucket: AsyncBucket, path: pathlib.Path) -> None:
        """Upload the downloaded mp3 file to the database."""
        audio_path, cover_path, metadata = (
            f"songs/{uuid.uuid4()}.mp3",
            f"covers/{uuid.uuid4()}.jpg",
            get_metadata(path),
        )
        if cover_data := metadata.pop("cover"):
            with tempfile.NamedTemporaryFile() as tmp:
                tmp.write(cover_data)
                tmp.flush()
                await bucket.upload(cover_path, tmp.name)
        else:
            cover_path = None
        metadata.update(
            source=self.source,
            audio_path=audio_path,
            cover_path=cover_path,
        )
        await bucket.upload(audio_path, path)
        await DB.postgrest.from_("song_metadata").insert(metadata).execute()

    async def upload_log(self, bucket: AsyncBucket) -> None:
        """Upload the log file to the database."""
        log_path = f"logs/{self.log_id}"
        await bucket.upload(log_path, self.log_file)
        await DB.postgrest.from_("scraper_logs").insert(
            {
                "source": self.source,
                "content_path": log_path,
                "exit_code": self.process.returncode,
            }
        ).execute()
