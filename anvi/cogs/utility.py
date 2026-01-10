import discord
import random
from discord.ext import commands


class Utility(commands.Cog, name="Utility"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # ============================ SERVER INFO ============================

    @commands.hybrid_command(
        name="server",
        description="Show information about the current server",
        aliases=["sv"],
    )
    async def server(self, ctx: commands.Context):
        guild = ctx.guild
        created_date = guild.created_at.strftime("%d/%m/%y")
        thumbnail = guild.icon.url if guild.icon else None

        color = discord.Color(random.randint(0, 0xFFFFFF))
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        embed = discord.Embed(title="ℹ️ Server Information", color=color)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        embed.add_field(name="🛸 Server Name", value=guild.name, inline=False)
        embed.add_field(name="🆔 Server ID", value=guild.id, inline=False)
        embed.add_field(name="👑 Owner", value=guild.owner, inline=False)
        embed.add_field(name="📅 Server Created", value=created_date, inline=False)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="🍀 Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="💬 Text Channels", value=text_channels, inline=True)
        embed.add_field(name="📚 Categories", value=categories, inline=True)
        embed.add_field(name="🔊 Voice Channels", value=voice_channels, inline=True)

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.send(embed=embed)

    # ============================ ROLE LIST ============================

    @commands.hybrid_command(
        name="rolelist",
        description="Displays a list of all roles in the server",
        aliases=["rl"],
    )
    async def rolelist(self, ctx: commands.Context):
        roles = ctx.guild.roles
        role_names = [role.name for role in roles]

        embed = discord.Embed(
            title="List of Roles",
            description="\n".join(role_names),
            color=discord.Color.blue(),
        )

        await ctx.send(embed=embed)

    # ============================ ROLE INFO ============================

    @commands.hybrid_command(
        name="roleinfo",
        description="info abt a role. use : ,roleinfo role name or ,ri rolename",
        aliases=["ri"],
    )
    async def roleinfo(self, ctx: commands.Context, *, role_name: str):
        role_name_lower = role_name.lower()
        role = next(
            (r for r in ctx.guild.roles if r.name.lower() == role_name_lower),
            None,
        )

        if role is None:
            await ctx.send(f"Role '{role_name}' does not exist.")
            return

        embed_color = (
            role.color if role.color.value != 0 else discord.Color.random()
        )

        embed = discord.Embed(title=role.name, color=embed_color)

        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        else:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        embed.add_field(name="Role Color", value=str(role.color), inline=False)
        embed.add_field(name="Members", value=len(role.members), inline=False)
        embed.add_field(
            name="Permissions",
            value=", ".join(
                perm.replace("_", " ").title()
                for perm, value in role.permissions
                if value
            ),
            inline=False,
        )

        embed.set_footer(text="Sent with 💟 ")
        await ctx.send(embed=embed)

    # ============================ PROFILE (NO GIF) ============================

    @commands.hybrid_command(
        name="profile",
        description="Display profile info",
    )
    async def profile(self, ctx: commands.Context, member: discord.Member | None = None):
        member = member or ctx.author
        guild = ctx.guild

        colored_roles = [
            r
            for r in member.roles
            if r != guild.default_role and r.color != discord.Color.default()
        ]
        roles = [r for r in member.roles if r != guild.default_role]
        role_color = colored_roles[-1].color if colored_roles else discord.Color.blue()

        embed = discord.Embed(
            title=f"ℹ️ {member.name}'s Info",
            color=role_color,
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="", value=member.mention, inline=False)

        embed.add_field(
            name="🏷️ Roles:",
            value=", ".join(f"<@&{r.id}>" for r in roles),
            inline=False,
        )

        embed.add_field(
            name="🧭 Joined Server & Account Created:",
            value=(
                f"Joined: `{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}`\n"
                f"Created: `{member.created_at.strftime('%Y-%m-%d %H:%M:%S')}`"
            ),
            inline=False,
        )

        important_perms = [
            "administrator",
            "manage_guild",
            "manage_roles",
            "manage_channels",
            "manage_messages",
            "manage_webhooks",
            "manage_nicknames",
            "manage_emojis",
            "kick_members",
            "ban_members",
            "mention_everyone",
            "mute_members",
            "create_instant_invite",
        ]

        enabled = [
            perm.replace("_", " ").title()
            for perm, val in member.guild_permissions
            if val and perm in important_perms
        ]

        embed.add_field(
            name="🔐 Key Permissions:",
            value=", ".join(enabled) or "`None`",
            inline=False,
        )

        acknowledgements = []
        if member == guild.owner:
            acknowledgements.append("*Server Owner* 👑")
        if (
            guild.me.guild_permissions.administrator
            and member.guild_permissions.administrator
        ):
            acknowledgements.append("*Server Admin* 🛡️")

        if acknowledgements:
            embed.add_field(
                name="📜 Acknowledgements:",
                value="\n".join(acknowledgements),
                inline=False,
            )

        embed.set_footer(
            text=f"🆔 User ID: {member.id} | Sent with 💟"
        )

        await ctx.send(embed=embed)

    # ============================ AVATAR ============================

    @commands.hybrid_command(
        name="av",
        description="Display profile picture of a user",
    )
    async def av(self, ctx: commands.Context, user: discord.Member | None = None):
        user = user or ctx.author
        color = discord.Color(random.randint(0, 0xFFFFFF))

        embed = discord.Embed(
            title=f"Avatar of {user.display_name}",
            color=color,
        )

        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url,
        )

        await ctx.send(embed=embed)

    # ============================ NICKNAME ============================

    @commands.hybrid_command(
        name="nickname",
        description="Change a nickname of user in server",
        aliases=["nick"],
    )
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        new_nickname: str,
    ):
        try:
            await member.edit(nick=new_nickname)
            await ctx.send(
                f"Nickname changed for {member.mention} to {new_nickname}"
            )
        except discord.Forbidden:
            await ctx.send(
                "I do not have permission to change nicknames for this user."
            )
        except discord.HTTPException as e:
            await ctx.send(f"Failed to change nickname: {e}")

    @nickname.error
    async def nickname_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Utility(bot))

