import os

from fastapi import APIRouter, Request


router = APIRouter(prefix="/db")


@router.get("/credentials")
async def getkey():
    """
    Method for client to get public db credentials
    """
    return {"URL": os.environ["CASPIAN_DOMAIN"], "KEY": os.environ["ANON_KEY"]}
