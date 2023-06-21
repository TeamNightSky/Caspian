from fastapi import APIRouter, BackgroundTasks, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.worker import scrape_spotify, scrape_youtube, upload_download

router = APIRouter(prefix="/import")


@router.post("/youtube")
async def youtube_scraper(url: str):
    """
    Scrape a song from Youtube
    """
    # TODO: Add user_id to scrape_youtube
    scrape_youtube.delay(url, None)


@router.post("/spotify")
async def spotify_scraper(url: str):
    """
    Scrape a song from Spotify
    """
    # TODO: Add user_id to scrape_spotify
    scrape_spotify.delay(url, None)


@router.post("/upload")
async def upload_file(file: UploadFile):
    """
    Manually upload song
    """
    # TODO: Add user_id to upload_download
    upload_download.delay(file.file.read(), None)

