from fastapi import FastAPI
from caspian.api.routes.scraping import router as scraping_router

from caspian.db import DB


app = FastAPI()
app.mount("/api", scraping_router)

