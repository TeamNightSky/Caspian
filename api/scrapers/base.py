"""Module for Scraper protocol."""

import asyncio
import contextlib
import pathlib
import urllib.parse
import uuid
from typing import Any, Generator

from api.db import DB


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
    def active_scraper(self):
        """Context manager for an active scraper."""
        self.active_scrapers[self.download_id] = self
        try:
            yield
        finally:
            del self.active_scrapers[self.download_id]

    async def run(self, timeout: int) -> None:
        """Run the scraper."""
        with self.active_scraper():
            self.process = await self.start(
                self.log_file.open("wb"),
                asyncio.subprocess.STDOUT,
                None,
            )
            try:
                await asyncio.wait_for(self.process.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                self.process.kill()
            for download in self.downloads():
                print(download[:50])  # TODO: add upload song file to database
