from fastapi import APIRouter, BackgroundTasks, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.db import DB
from api.scrapers import Scraper, SpotifyScraper, YoutubeScraper

DOWNLOAD_TIMEOUT = 6 * 60 * 60  # 6 hours


router = APIRouter(prefix="/import")


@router.post("/youtube")
async def youtube_scraper(url: str, background_tasks: BackgroundTasks):
    """
    Scrape a song from Youtube
    """
    scraper = YoutubeScraper(url)
    background_tasks.add_task(scraper.run, DOWNLOAD_TIMEOUT)
    return {"download_id": scraper.job_id, "url": scraper.url, "status": "ok"}


@router.post("/spotify")
async def spotify_scraper(url: str, background_tasks: BackgroundTasks):
    """
    Scrape a song from Spotify
    """
    scraper = SpotifyScraper(url)
    background_tasks.add_task(scraper.run, DOWNLOAD_TIMEOUT)
    return {"download_id": scraper.job_id, "url": scraper.url, "status": "ok"}


@router.post("/upload")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Manually upload song
    """
    background_tasks.add_task(DB.upload_song, file.read(), "manual")
    return {"status": "ok"}


@router.get("/active-jobs")
async def downloads_lists() -> dict[str, str]:
    """
    Get active download jobs
    """
    return {
        scraper.download_dir: scraper.url
        for scraper in Scraper.active_scrapers.values()
    }


@router.get("/active-jobs/{job_id}")
async def download_status(job_id: str):
    """
    Get status of active download job
    """
    if job_id not in Scraper.active_scrapers:
        return {"message": "Download job not found"}
    scraper = Scraper.active_scrapers[job_id]
    return {"job_id": scraper.job_id, "status": scraper.process.returncode}


@router.get("/active-jobs/{download_id}/log")
async def download_log(download_id: str):
    """
    Get log of active download job
    """
    if download_id not in Scraper.active_scrapers:
        return {"message": "Download not found"}
    scraper = Scraper.active_scrapers[download_id]
    return FileResponse(scraper.log_file, media_type="text/plain")
