import os
from supabase import create_client, Client


class DB:
    client: Client = create_client(
        "0.0.0.0",
        os.environ["SUPABASE_KEY"],
    )
