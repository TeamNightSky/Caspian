import os
import io

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

    files = storage.get_bucket("files")


class DB(RawDB):
    """
    Wrapper class for RawDB which implements basic functions.
    """
    async def upload_song(self, f: io.FileIO, source: str):
        """
        Upload a song to the database.
        """
        await self.files.upload(f"files/{source}/{f.name}", f)
        # Potentially autogenerate a uuid to store it under
