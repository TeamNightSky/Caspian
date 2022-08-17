import os

from supabase import Client, create_client


class DB:
    client: Client = create_client(
        "0.0.0.0",
        os.environ["SUPABASE_KEY"],
    )
