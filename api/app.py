from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import scrapers_router, db_router
from .models import Session, Base

from api import DEBUG


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(scrapers_router)
app.include_router(db_router)


@app.on_event("startup")
async def initialize_models():
    with Session() as db:
        if DEBUG:
            Base.metadata.drop_all(db.bind)
        Base.metadata.create_all(db.bind)
