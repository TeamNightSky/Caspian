"""Celery app for scraping and saving data to database."""

import glob
import os
from pathlib import Path
import tempfile
from typing import Any
import audio_metadata
from celery import Celery
import urllib.parse
import shutil
from storage3 import create_client

from unittest import mock
import argparse

import yt_dlp
from spotdl.console import console_entry_point as spotdl

from .models import Song, Artist, Session

app = Celery(
    "scraper",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_BACKEND_URL"],
)
app.conf.result_backend = os.environ["CELERY_RESULT_BACKEND_URL"]

headers = {
    "apiKey": os.environ["SUPABASE_KEY"],
    "Authorization": f"Bearer {os.environ['SUPABASE_KEY']}",
}
storage_client = create_client(
    os.environ["SUPABASE_URL"] + "/storage/v1/", headers, is_async=False
)
# TODO: Switch to async


def get_metadata(download: bytes) -> dict[str, Any]:
    """Return the metadata for the downloaded mp3 file."""
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(download)
        tmp.flush()
        song = audio_metadata.load(tmp.name)
    return {
        "title": song.tags.title[0] if song.tags.get("title", []) else None,
        "artist": song.tags.artist[0] if song.tags.get("artist", []) else None,
        # "album": song.tags.album[0] if song.tags.get("album", []) else None,
        # "album_artist": song.tags.album_artist[0]
        # if song.tags.get("album_artist", [])
        # else None,
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
            scheme="https",  # Force HTTPS
            fragment="",  # Remove fragment
        )
        .geturl()
    )


@app.task
def scrape_youtube(url: str, user_id: str):
    """Scrape a YouTube video."""
    with tempfile.TemporaryDirectory() as tmp:
        try:
            yt_dlp.main(
                [
                    "--add-metadata",
                    "--yes-playlist",
                    "--write-thumbnail",
                    "-x",
                    "--audio-format=mp3",
                    "--audio-quality=0",
                    "--retries=infinite",
                    "--socket-timeout=30",
                    "--prefer-ffmpeg",
                    "--no-call-home",
                    "-i",
                    f"--output={tmp}/%(channel)s - %(title)s.%(ext)s",
                    prepare_url(url),
                ]
            )
        except SystemExit:
            pass
        for file in Path(tmp).glob("*.mp3"):
            with open(file, "rb") as mp3:
                coverpath = Path(str(file).replace(".mp3", ".jpg"))
                with open(coverpath, "rb") as cover:
                    upload_download.delay(mp3.read(), user_id, cover.read())
        return [file.name for file in Path(tmp).glob("*.mp3")]


@app.task
def scrape_spotify(url: str, user_id: str):
    with tempfile.TemporaryDirectory() as tmp:
        try:
            with mock.patch(
                "argparse.ArgumentParser.parse_args",
                return_value=argparse.Namespace(
                    operation="download",
                    query=[prepare_url(url)],
                    output=f"{tmp}",
                    output_format="mp3",
                    ffmpeg=shutil.which("ffmpeg"),
                    ignore_ffmpeg_version=False,
                    user_auth=None,
                    debug_termination=False,
                    use_youtube=True,
                    generate_m3u=False,
                    lyrics_provider="genius",
                    search_threads=5,
                ),
            ):
                spotdl()
        except SystemExit:
            pass
        for file in Path(tmp).glob("*.mp3"):
            with open(file, "rb") as mp3:
                upload_download.delay(mp3.read(), user_id)
        return [file.name for file in Path(tmp).glob("*.mp3")]


@app.task
def upload_download(file: bytes, user_id: str, cover: bytes = None) -> None:
    """Upload a file to the database."""
    metadata = get_metadata(file)
    with Session() as db:
        title = metadata["title"]
        artist = metadata["artist"]
        year = metadata["year"]
        genre = metadata["genre"]
        duration = metadata["duration"]
        if cover is None:
            cover = metadata["cover"]

        song = Song(
            title=title,
            artist=Artist(name=artist),
            year=year,
            genre=genre,
            duration=duration,
            uploaded_by=user_id,
        )
        db.add(song)
        db.commit()

        if "files" not in storage_client.list_buckets():
            storage_client.create_bucket("files")

        if cover is not None:
            storage_client.from_("files").upload(
                f"cover/{song.id}.jpg", cover, {"content-type": "image/jpg"}
            )
        # TODO: Default cover

        storage_client.from_("files").upload(
            f"song/{song.id}.mp3", file, {"content-type": "audio/mpeg"}
        )
        return song.id, song.title, song.artist.name
