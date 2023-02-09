from fastapi import APIRouter, BackgroundTasks, FastAPI, UploadFile
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
    return {"download_id": scraper.download_id, "url": scraper.url, "status": "ok"}


@router.post("/spotify")
async def spotify_scraper(url: str, background_tasks: BackgroundTasks):
    """
    Scrape a song from Spotify
    """
    scraper = SpotifyScraper(url)
    background_tasks.add_task(scraper.run, DOWNLOAD_TIMEOUT)
    return {"download_id": scraper.download_id, "url": scraper.url, "status": "ok"}


@router.post("/upload")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Manually upload song
    """
    background_tasks.add_task(DB.upload_song, file.read(), "manual")
    return {"status": "ok"}


@router.get("/active-downloads")
async def downloads_lists() -> dict[str, str]:
    """
    Get active downloads
    """
    return {scraper.download_dir:scraper.url for scraper in Scraper.active_scrapers.values()}


@router.get("/active-downloads/{download_id}")
async def download_status(download_id: str):
    """
    Get status of active download
    """
    if download_id not in Scraper.active_scrapers:
        return {"message": "Download not found"}
    scraper = Scraper.active_scrapers[download_id]
    return {"download_id": scraper.download_id, "status": scraper.process.returncode}


@router.get("/active-downloads/{download_id}/log")
async def download_log(download_id: str):
    """
    Get log of active download
    """
    if download_id not in Scraper.active_scrapers:
        return {"message": "Download not found"}
    scraper = Scraper.active_scrapers[download_id]
    return FileResponse(scraper.log_file, media_type="text/plain")


app = FastAPI()
app.mount("/api", router)


@app.on_event("startup")
async def startup():
    """
    Initialize the storage buckets
    """
    for bucket in await DB.storage.list_buckets():
        if bucket.name == "files":
            return
    await DB.storage.create_bucket("files")
