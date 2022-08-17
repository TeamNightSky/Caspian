from fastapi import FastAPI
from api.scrapers.routes import router as scraping_router

from api.db import DB


app = FastAPI()
app.mount("/api", scraping_router)

