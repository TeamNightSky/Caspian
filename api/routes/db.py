import os

from fastapi import APIRouter

from api.db import DB

router = APIRouter(prefix="/db")


@router.get("/credentials")
async def getkey():
    """
    Method for client to get public db credentials
    """
    return {"URL": os.getenv("CASPIAN_DOMAIN"), "KEY": DB.public_key}
