import discord
import random
from discord.ext import commands


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
        ctx: commands.Context,
        member: discord.Member,
        *,
        role_arg: str,
    ):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("❌ You don't have permission to manage roles.")
            return

        try:
            role_arg_lower = role_arg.lower()

            # Find role by name (case-insensitive)
            role = discord.utils.find(
                lambda r: r.name.lower() == role_arg_lower,
                ctx.guild.roles,
            )

            # Fallback: role mention
            if not role and ctx.message.role_mentions:
                role = ctx.message.role_mentions[0]

            if not role:
                await ctx.send(f"❌ Role '{role_arg}' not found.")
                return

            await member.add_roles(role)

            color = discord.Color(random.randint(0, 0xFFFFFF))
            embed = discord.Embed(
                title="Role Added",
                description=(
                    f"✅ {ctx.author.mention} added the role "
                    f"**{role.name}** to {member.mention}."
                ),
                color=color,
            )

            await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(
                "❌ I don't have permission to add roles to that member."
            )
        except discord.HTTPException as e:
            await ctx.send(f"❌ Failed to add role: {e}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
