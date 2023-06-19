from fastapi import APIRouter, BackgroundTasks, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse


router = APIRouter(prefix="/import")


@router.post("/youtube")
async def youtube_scraper(url: str):
    """
    Scrape a song from Youtube
    """

@router.post("/spotify")
async def spotify_scraper(url: str):
    """
    Scrape a song from Spotify
    """

@router.post("/upload")
async def upload_file(file: UploadFile):
    """
    Manually upload song
    """


@router.get("/active-jobs")
async def downloads_lists() -> dict[str, str]:
    """
    Get active download jobs
    """


@router.get("/active-jobs/{job_id}")
async def download_status(job_id: str):
    """
    Get status of active download job
    """

@router.get("/active-jobs/{download_id}/log")
async def download_log(download_id: str):
    """
    Get log of active download job
    """
