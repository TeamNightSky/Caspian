from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import scrapers_router, db_router

from api import DEBUG


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
