import os
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db import DB
from .routes import scrapers_router, db_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/api", scrapers_router)
app.mount("/api", db_router)


@app.on_event("startup")
async def startup():
    """
    Initialize the storage buckets
    """
    while True:
        try:
            for bucket in await DB.storage.list_buckets():
                if bucket.name == "files":
                    print("Bucket found.")
                    return
            await DB.storage.create_bucket("files")
            print("Created bucket.")
            break
        except:  # If you are gonna complain, fix it yourself
            print("Storage not launched. Retrying...")
            await asyncio.sleep(1)
