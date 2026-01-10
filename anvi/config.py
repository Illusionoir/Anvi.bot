import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    PREFIX: str = os.getenv("COMMAND_PREFIX", ",")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    def validate(self) -> None:
        if not self.DISCORD_TOKEN:
            raise RuntimeError("DISCORD_TOKEN is missing")

config = Config()
config.validate()

