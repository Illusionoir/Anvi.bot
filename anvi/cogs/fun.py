import random
import requests
import discord
from discord.ext import commands
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        with open(DATA_DIR / "roasts.json", "r", encoding="utf-8") as f:
            self.insults = f.readlines()

        with open(DATA_DIR / "lines.json", "r", encoding="utf-8") as f:
            self.pickup_lines = f.readlines()

    # =============================== WAIFU API ===============================

    def fetch_waifu_image(self, category, nsfw=False):
        base = "https://api.waifu.pics/nsfw" if nsfw else "https://api.waifu.pics/sfw"
        url = f"{base}/{category}"
        res = requests.get(url)
        return res.json().get("url")

    @commands.hybrid_command(
        name="waifu",
        description="Get a random waifu image (SFW)",
        aliases=["w"],
    )
    async def waifu(self, ctx):
        try:
            category = random.choice(["waifu", "neko", "shinobu", "megumin"])
            image_url = self.fetch_waifu_image(category)

            embed = discord.Embed(color=discord.Color.random())
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.hybrid_command(
        name="nsfw",
        description="Get a random waifu image (NSFW)",
    )
    async def nsfw(self, ctx):
        if not ctx.channel.is_nsfw():
            await ctx.send("🚫 This command can only be used in NSFW channels.")
            return

        try:
            category = random.choice(["waifu", "neko", "trap", "blowjob"])
            image_url = self.fetch_waifu_image(category, nsfw=True)

            embed = discord.Embed(color=discord.Color.random())
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    # =============================== ACTION COMMAND FACTORY ===============================

    def make_action_command(self, name, emoji, categories):
        @commands.hybrid_command(
            name=name,
            description=f"{name.title()} someone",
        )
        async def _action(ctx, user: discord.User):
            image_url = self.fetch_waifu_image(random.choice(categories))
            embed = discord.Embed(
                description=f"{ctx.author.mention} {name}s {user.mention} {emoji}",
                color=discord.Color.random(),
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=embed)

        return _action

    # =============================== 8 BALL ===============================

    @commands.hybrid_command(
        name="8ball",
        description="Ask the Magic 8-Ball a question.",
        aliases=["8b"],
    )
    async def _8ball(self, ctx, *, question: str):
        icon_url = "https://i.imgur.com/XhNqADi.png"
        responses = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes - definitely.',
            'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
            'Do not count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'no... (╯°□°）╯︵ ┻━┻',
            'senpai, pls no ;-;', 'no... baka', 'Very doubtful.'
        ]

        fortune = random.choice(responses)
        embed = discord.Embed(colour=discord.Colour.purple())
        embed.set_author(name='Magic 8-Ball', icon_url=icon_url)
        embed.add_field(name=f'{ctx.author.name} asks:', value=f'"{question}"', inline=False)
        embed.add_field(name="The Magic 8-Ball says:", value=f'**{fortune}**', inline=False)
        await ctx.send(embed=embed)

    # =============================== GAYDAR ===============================

    @commands.hybrid_command(
        name="gaydar",
        description="Measure someone's gayness! Just for fun!",
    )
    async def gaydar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        percentage = random.randint(0, 100)

        embed = discord.Embed(
            title="Gaydar",
            description=f"`{member.display_name}` is **{percentage}%** gay!",
            color=random.randint(0, 0xFFFFFF),
        )
        embed.set_thumbnail(
            url="https://static01.nyt.com/images/2013/05/27/booming/27mystory-booming-gaydar1/27mystory-booming-gaydar1-superJumbo.jpg"
        )
        await ctx.send(embed=embed)

    # =============================== FEMBOY ===============================

    @commands.hybrid_command(
        name="femboy",
        description="Are you an femboy ??",
    )
    async def femboy(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        percentage = random.randint(0, 100)

        embed = discord.Embed(
            title="Femboy Rating",
            description=f"`{member.display_name}` is **{percentage}%** femboy!",
            color=random.randint(0, 0xFFFFFF),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    # =============================== ROAST ===============================

    @commands.hybrid_command(
        name="roast",
        description="Roast a user",
    )
    async def roast(self, ctx, target: discord.Member):
        insult = random.choice(self.insults).strip()
        await ctx.send(f"{target.mention}, {insult}")

    # =============================== PICKUP ===============================

    @commands.hybrid_command(
        name="pickup",
        description="you looks delicious",
    )
    async def pickup(self, ctx, target: discord.Member):
        line = random.choice(self.pickup_lines).strip()
        await ctx.send(f"{target.mention}, {line}")

    # =============================== ROLL DICE ===============================

    @commands.hybrid_command(
        name="roll_dice",
        description="Roll two dice",
        aliases=["roll"],
    )
    async def roll_dice(self, ctx):
        icon_url = 'https://i.imgur.com/rkfXx3q.png'
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='Dice Roller', icon_url=icon_url)
        embed.add_field(
            name=f'*{ctx.author.name} rolls the dice...*',
            value=f'**{die1}** and **{die2}** for a total of **{total}**'
        )
        await ctx.send(embed=embed)

    # =============================== COIN FLIP ===============================

    @commands.hybrid_command(
        name="coin",
        description="Flip a coin",
        aliases=["cf"],
    )
    async def coin(self, ctx):
        icon_url = 'https://cdn-0.emojis.wiki/emoji-pics/whatsapp/coin-whatsapp.png'
        faces = ['Heads!', 'Tails!']
        outcome = random.choice(faces)

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='Coin Flip', icon_url=icon_url)
        embed.add_field(
            name=f'*{ctx.author.name}, the coin lands...*',
            value=f'**{outcome}**'
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    cog = Fun(bot)

    actions = [
        ("lick", "😳😳", ["lick"]),
        ("kiss", "😚😘", ["kiss"]),
        ("bully", "😈", ["bully"]),
        ("cuddle", "🥰", ["cuddle"]),
        ("hug", "🫂", ["hug", "glomp"]),
        ("pat", "🥰", ["pat"]),
        ("bonk", "🥴", ["bonk"]),
        ("yeet", "😵", ["yeet"]),
        ("wave", "👋", ["wave"]),
        ("highfive", "😄", ["highfive"]),
        ("handhold", "🫣", ["handhold"]),
        ("bite", "🫢", ["bite"]),
        ("slap", "🥶", ["slap"]),
        ("kill", "😮", ["kill"]),
        ("kicks", "😱", ["kick"]),
    ]

    for name, emoji, categories in actions:
        bot.add_command(cog.make_action_command(name, emoji, categories))

    await bot.add_cog(cog)
