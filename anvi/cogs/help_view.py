import discord
from discord.ext import commands


class HelpSelect(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        options = [
            discord.SelectOption(
                label=cog_name,
                description=f"{cog_name} commands",
            )
            for cog_name in sorted(bot.cogs.keys())
        ]

        super().__init__(
            placeholder="Choose a command category...",
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        cog = self.bot.cogs.get(self.values[0])

        embed = discord.Embed(
            title=f"📂 {self.values[0]} Commands",
            color=discord.Color.blurple(),
        )

        for cmd in cog.get_commands():
            description = cmd.description or "No description"
            aliases = ", ".join(cmd.aliases) if cmd.aliases else "None"

            embed.add_field(
                name=f"/{cmd.name}",
                value=(
                    f"**Description:** {description}\n"
                    f"**Aliases:** {aliases}"
                ),
                inline=False,
            )

        await interaction.response.edit_message(embed=embed, view=self.view)


class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=120)
        self.add_item(HelpSelect(bot))
