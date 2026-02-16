import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()  # <-- this loads the .env file

_pool = None

async def get_pool():
    global _pool
    if not _pool:
        db_url = os.getenv("SUPABASE_DB_URL")
        print("Connecting to DB:", db_url)  # Debug line
        _pool = await asyncpg.create_pool(
            db_url,
            min_size=2,
            max_size=10
        )
    return _pool
