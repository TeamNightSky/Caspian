import os

from postgrest import AsyncPostgrestClient
from storage3 import AsyncStorageClient


class DB:
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
