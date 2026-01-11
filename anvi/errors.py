from discord.ext import commands
import discord


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx: commands.Context,
        error: commands.CommandError,
    ):
        # Ignore if command has local error handler
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You do not have permission to use this command.")
            return

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I do not have the required permissions.")
            return

        if isinstance(error, commands.BadArgument):
            await ctx.send("❌ Invalid argument.")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Missing required argument.")
            return

        if isinstance(error, commands.CommandNotFound):
            # silently ignore (matches your current UX)
            return

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"⏳ Try again in {round(error.retry_after, 1)} seconds."
            )
            return

        # Unknown / unexpected error → re-raise (important)
        raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(CommandErrorHandler(bot))
