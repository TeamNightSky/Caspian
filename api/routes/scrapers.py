from fastapi import APIRouter, BackgroundTasks, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import jwt
import os

from api.worker import scrape_spotify, scrape_youtube, upload_download

router = APIRouter(prefix="/import")

PUBLIC = bool(os.environ.get("CASPIAN_PUBLIC", "false").strip().lower() == "true")

def verify(auth: str):
    if PUBLIC:
        return True, None  # TODO: Create anonymous and superuser users
    try:
        payload = jwt.decode(auth, os.environ['JWT_SECRET'], algorithms=['HS256'])
        if role == 'service_role':
            return True, None
        return True, payload['sub']
    except jwt.exceptions.InvalidTokenError:
        return False, None

@router.post("/youtube")
async def youtube_scraper(url: str, authorization: str = None):
    """
    Scrape a song from Youtube
    """
    valid, user_id = verify(authorization)
    if valid:
        scrape_youtube.delay(url, user_id)


@router.post("/spotify")
async def spotify_scraper(url: str, authorization: str = None):
    """
    Scrape a song from Spotify
    """
    valid, user_id = verify(authorization)
    if valid:
        scrape_spotify.delay(url, user_id)


@router.post("/upload")
async def upload_file(file: UploadFile, authorization: str = None):
    """
    Manually upload song
    """
    valid, user_id = verify(authorization)
    if valid:
        upload_download.delay(file.file.read(), user_id)

