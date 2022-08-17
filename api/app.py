from fastapi import APIRouter, BackgroundTasks, FastAPI, UploadFile
from fastapi.responses import FileResponse

from api.db import DB
from api.scrapers import Scraper, SpotifyScraper, YoutubeScraper

DOWNLOAD_TIMEOUT = 6 * 60 * 60  # 6 hours


router = APIRouter(prefix="/import")


@router.post("/youtube")
async def youtube_scraper(url: str, background_tasks: BackgroundTasks):
    scraper = YoutubeScraper(url)
    background_tasks.add_task(scraper.run(DOWNLOAD_TIMEOUT))
    return {"download_id": scraper.download_id}


@router.post("/spotify")
async def spotify_scraper(url: str, background_tasks: BackgroundTasks):
    scraper = SpotifyScraper(url)
    background_tasks.add_task(scraper.run(DOWNLOAD_TIMEOUT))
    return {"download_id": scraper.download_id}


@router.post("/upload")
async def upload_file(file: UploadFile):
    ...  # TODO: upload file to database


@router.get("/active-downloads")
async def downloads_lists() -> dict[str, str]:
    return {scraper.url: scraper.download_dir for scraper in Scraper.active_scrapers}


@router.get("/active-downloads/{download_id}")
async def download_status(download_id: str):
    if download_id not in Scraper.active_scrapers:
        return {"message": "Download not found"}
    scraper = Scraper.active_scrapers[download_id]
    return {"download_id": scraper.download_id, "status": scraper.process.returncode}


@router.get("/active-downloads/{download_id}/log")
async def download_log(download_id: str):
    if download_id not in Scraper.active_scrapers:
        return {"message": "Download not found"}
    scraper = Scraper.active_scrapers[download_id]
    return FileResponse(scraper.log_file, media_type="text/plain")


app = FastAPI()
app.mount("/api", router)
