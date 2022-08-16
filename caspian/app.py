from fastapi import FastAPI
from caspian.api.routes.scraping import router as scraping_router

from caspian.db import DB


app = FastAPI()
app.mount("/api", scraping_router)


@app.get("/")
async def root():
    DB.client.table
    return {"message": "Hello World"}
