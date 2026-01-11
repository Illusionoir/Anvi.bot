import discord
from discord.ext import commands
from discord import app_commands
from difflib import get_close_matches

from anvi.cogs.help_view import HelpView


class Core(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ===================== EVENTS =====================

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"[CORE] Ready as {self.bot.user}")

    # ===================== COMMANDS =====================

    @commands.hybrid_command(name="ping", description="Show bot latency")
    async def ping(self, ctx: commands.Context) -> None:
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! `{latency}ms`")

    @commands.hybrid_command(name="info", description="Show bot information")
    async def info(self, ctx: commands.Context) -> None:
        """Display information about the bot."""
        guild = ctx.guild
        bot = self.bot.user

        embed = discord.Embed(
            title=f"✨ {bot.name}'s Info",
            color=discord.Color.magenta(),
        )
        embed.set_thumbnail(url=bot.display_avatar.url)

        if guild:
            roles = [r.mention for r in guild.me.roles if r != guild.default_role]
            embed.add_field(
                name="🌸 Nickname",
                value=f"`{guild.me.display_name}`",
                inline=False,
            )
            embed.add_field(
                name="🎗️ Roles",
                value=", ".join(roles) or "None",
                inline=False,
            )

        embed.add_field(name="🎨 Creator", value="`Illusion`", inline=True)
        embed.add_field(name="🦋 Co-creator", value="`ChatGPT`", inline=True)
        embed.add_field(
            name="⚡ Ping",
            value=f"`{round(self.bot.latency * 1000)}ms`",
            inline=False,
        )

        embed.set_footer(text="Made with 💟")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="help", description="Show all commands")
    async def help_command(self, ctx: commands.Context):
        embed = discord.Embed(
            title="📬 Anvi Help Menu",
            description="Select a category from the dropdown below.",
            color=discord.Color.blurple(),
        )

        try:
            await ctx.author.send(embed=embed, view=HelpView(self.bot))
            await ctx.send("📬 I’ve sent you a DM with all my commands!")
        except discord.Forbidden:
            await ctx.send("❌ I can’t DM you. Please enable DMs from server members.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Core(bot))
