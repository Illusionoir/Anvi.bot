import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_supabase = None

def get_db():
    global _supabase
    if _supabase is None:
        _supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY"),
        )
    return _supabase
