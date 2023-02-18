import os
import io
import asyncio
import yaml

from postgrest import AsyncPostgrestClient
from storage3 import AsyncStorageClient


class RawDB:
    """
    Base class for the DB, contains headers and clients.
    """
    headers = {
        "Authorization": f"Bearer {os.environ['SUPABASE_KEY']}",
        "apiKey": os.environ["SUPABASE_KEY"],
    }

    postgrest = AsyncPostgrestClient(
        os.environ["POSTGREST_URL"],
        headers=headers,
    )

    storage = AsyncStorageClient(
        os.environ["STORAGE_URL"],
        headers=headers,
    )

    files_ = None

    @classmethod
    @property
    def files(cls):
        """
        Get files bucket
        """
        if cls.files_:
            return cls.files_
        cls._files = asyncio.run(cls.storage.get_bucket("files"))
        return cls.files

    public_key = yaml.safe_load(
        open("/var/lib/kong/kong.yml", "r").read()
    )["consumers"][1]["keyauth_credentials"][0]["key"]


class DB(RawDB):
    """
    Wrapper class for RawDB which implements basic functions.
    """
    async def upload_song(self, f: io.FileIO, source: str):
        """
        Upload a song to the database.
        """
        # No metadata moment
        await self.files.upload(f"files/{source}/{f.name}", f)
