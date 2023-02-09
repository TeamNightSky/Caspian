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


class DB(RawDB):
    """
    Wrapper class for RawDB which implements basic functions.
    """
    async def upload_song(self, f: io.BytesIO, source: str):
        """
        Upload a song to the database.
        """
        # Gonna have to implement uploads in storage-py
        self.storage._request("POST", f"/object/files/{source}--{f.name}")
