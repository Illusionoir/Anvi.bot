import discord
from discord.ext import commands
from anvi.config import config
from anvi.web import start_web

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True
INTENTS.presences = True
INTENTS.guilds = True
INTENTS.reactions = True

class AnviBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=config.PREFIX,
            intents=INTENTS,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        # cogs will be loaded here later
        pass

bot = AnviBot()

@bot.event
async def on_ready() -> None:
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"[WARN] Slash sync failed: {e}")

    print(f"[READY] Logged in as {bot.user} ({bot.user.id})")

def main() -> None:
    start_web()        # Render keep-alive
    bot.run(config.DISCORD_TOKEN)

if __name__ == "__main__":
    main()

