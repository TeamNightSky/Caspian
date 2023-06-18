"""Celery app for scraping and saving data to database."""

import io
import os
from typing import Any
import uuid
import audio_metadata
from celery import Celery
import urllib.parse


app = Celery(
    "scraper",
    broker=os.environ["CELERY_BROKER_URL"],
    backend=os.environ["CELERY_BACKEND_URL"],
)
app.conf.result_backend = os.environ["CELERY_RESULT_BACKEND_URL"]



def get_metadata(download: io.BytesIO) -> dict[str, Any]:
    """Return the metadata for the downloaded mp3 file."""
    song = audio_metadata.load(download)
    return {
        "title": song.tags.title[0] if song.tags.get("title", []) else None,
        "artist": song.tags.artist[0] if song.tags.get("artist", []) else None,
        "album": song.tags.album[0] if song.tags.get("album", []) else None,
        "album_artist": song.tags.album_artist[0]
        if song.tags.get("album_artist", [])
        else None,
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


@app.task
def scrape_youtube(url: str):
    pass


@app.task
def scrape_spotify(url: str):
    pass


@app.task
def upload_download(file: io.BytesIO) -> None:
    pass