import discord
import random
import io
from datetime import timezone
from discord.ext import commands
from anvi.db.guild_config import get_guild_config, set_modlog_channel


class Moderation(commands.Cog, name="Moderation"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ============================ ADD ROLE ============================

    @commands.hybrid_command(
        name="addrole",
        description="Add a role to a member! Usage: ,addrole @member role_name",
        aliases=["ar"],
    )
    async def addrole(
        self,
        ctx,
        member: discord.Member,
        *,
        role_arg: str,
    ):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("❌ You don't have permission to manage roles.")
            return

        try:
            role_arg_lower = role_arg.lower()

            role = discord.utils.find(
                lambda r: r.name.lower() == role_arg_lower,
                ctx.guild.roles,
            )

            if not role and ctx.message.role_mentions:
                role = ctx.message.role_mentions[0]

            if not role:
                await ctx.send(f"❌ Role '{role_arg}' not found.")
                return

            await member.add_roles(role)

            embed = discord.Embed(
                title="Role Added",
                description=(
                    f"✅ {ctx.author.mention} added the role "
                    f"**{role.name}** to {member.mention}."
                ),
                color=discord.Color.random(),
            )

            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(
                "❌ I don't have permission to add roles to that member."
            )
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to add role: {e}")

    # ============================ MOD LOG ============================

    @commands.hybrid_command(
        name="setmodlog",
        description="Set the moderation log channel for this server",
    )
    @commands.has_permissions(administrator=True)
    async def setmodlog(
        self,
        ctx,
        channel: discord.TextChannel,
    ):
        set_modlog_channel(ctx.guild.id, channel.id)
        await ctx.send(f"✅ Mod log channel set to {channel.mention}")

    # ============================ PURGE ============================

    @commands.hybrid_command(
        name="purge",
        description="Delete messages (all / user / bots)",
    )
    @commands.has_permissions(manage_messages=True)
    async def purge(
        self,
        ctx,
        amount: int,
        user: discord.Member | None = None,
        bots: bool = False,
    ):
        if amount < 1:
            return

        if amount > 1000:
            amount = 1000

        def check(message: discord.Message):
            if user:
                return message.author.id == user.id
            if bots:
                return message.author.bot
            return True

        deleted = await ctx.channel.purge(
            limit=amount + 1,  # remove command message too
            check=check,
            bulk=True,
        )

        deleted_messages = [
            m for m in deleted if m.id != ctx.message.id
        ]

        if not deleted_messages:
            return

        # ===== create purge.txt in memory =====
        buffer = io.StringIO()

        for msg in reversed(deleted_messages):
            timestamp = msg.created_at.astimezone(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
            content = msg.content or "[NO TEXT]"
            buffer.write(
                f"[{timestamp}] {msg.author} ({msg.author.id}):\n{content}\n\n"
            )

        buffer.seek(0)
        file = discord.File(
            fp=io.BytesIO(buffer.read().encode("utf-8")),
            filename="purge.txt",
        )

        config = get_guild_config(ctx.guild.id)
        if not config:
            return

        channel_id = config.get("modlog_channel_id")
        if not channel_id:
            return

        log_channel = ctx.guild.get_channel(channel_id)
        if not log_channel:
            return

        await log_channel.send(
            content=(
                f"🧹 **Purge**\n"
                f"Moderator: {ctx.author.mention}\n"
                f"Channel: {ctx.channel.mention}\n"
                f"Messages deleted: {len(deleted_messages)}"
            ),
            file=file,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
