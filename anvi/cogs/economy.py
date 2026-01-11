from datetime import datetime, timezone, timedelta

import asyncio
import discord
from discord.ext import commands

from anvi.db.economy import (
    get_wallet_balance,
    add_wallet_balance,
    get_bank_balance,
    add_bank_balance,
    apply_bank_interest,
    get_last_daily,
    set_last_daily,
)


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # =======================
    # /balance
    # =======================
    @commands.hybrid_command(
        name="balance",
        description="Check your or another user's balance",
        aliases=["bal"],
    )
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author

        balance = get_wallet_balance(member.id)

        await ctx.send(f"💰 {member.display_name}'s balance: `{balance}` Quarks")

    # =======================
    # /daily
    # =======================
    @commands.hybrid_command(name="daily", description="Claim your daily reward")
    async def daily(self, ctx):
        user_id = ctx.author.id
        now = datetime.now(timezone.utc)

        last_daily = get_last_daily(user_id)

        # If user already claimed within 24 hours
        if last_daily and now - last_daily < timedelta(hours=24):
            next_time = last_daily + timedelta(hours=24)
            remaining = next_time - now

            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60

            await ctx.send(f"🕒 Already claimed. Try again in `{hours}h {minutes}m`.")
            return

        # Reward logic (same as old bot)
        reward = 500

        add_wallet_balance(user_id, reward)
        set_last_daily(user_id)

        await ctx.send(f"🎉 You claimed your daily `{reward}` Quarks!")

    # =======================
    # /bank
    # =======================

    @commands.hybrid_command(name="bank", description="Check your banked Quarks")
    async def bank(self, ctx):
        await ctx.defer()
        user_id = ctx.author.id

        interest = await asyncio.to_thread(apply_bank_interest, user_id)
        balance = await asyncio.to_thread(get_bank_balance, user_id)

        embed = discord.Embed(title="🏦 Bank Account", color=discord.Color.teal())

        embed.add_field(
            name="💰 Vault Balance", value=f"`{balance}` Quarks", inline=False
        )

        if interest > 0:
            embed.add_field(
                name="📈 Interest Earned", value=f"`+{interest}` Quarks", inline=False
            )

        embed.set_footer(text="Use /deposit and /withdraw to manage funds.")

        await ctx.send(embed=embed)

    # =======================
    # /deposit
    # =======================

    @commands.hybrid_command(name="deposit", description="Deposit coins into your bank")
    async def deposit(self, ctx, amount: str):
        await ctx.defer()
        user_id = ctx.author.id
        await asyncio.to_thread(apply_bank_interest, user_id)
        wallet = await asyncio.to_thread(get_wallet_balance, user_id)

        if amount.lower() == "all":
            amount = wallet
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("Enter a number or `all`.")
                return

        if amount <= 0:
            await ctx.send("Deposit amount must be positive.")
            return

        if wallet < amount:
            await ctx.send("💸 Not enough Quarks in wallet.")
            return

        add_wallet_balance(user_id, -amount)
        add_bank_balance(user_id, amount)

        await ctx.send(f"✅ Deposited `{amount}` Quarks into your bank.")

    # =======================
    # /withdraw
    # ======================

    @commands.hybrid_command(
        name="withdraw", description="Withdraw coins from your bank"
    )
    async def withdraw(self, ctx, amount: str):
        user_id = ctx.author.id
        await ctx.defer()
        await asyncio.to_thread(apply_bank_interest, user_id)
        bank_balance = await asyncio.to_thread(get_bank_balance, user_id)

        if amount.lower() == "all":
            amount = bank_balance
        else:
            try:
                amount = int(amount)
            except ValueError:
                await ctx.send("Enter a number or `all`.")
                return

        if amount <= 0:
            await ctx.send("Withdraw amount must be positive.")
            return

        if bank_balance < amount:
            await ctx.send("🏦 Not enough Quarks in bank.")
            return

        add_bank_balance(user_id, -amount)
        add_wallet_balance(user_id, amount)

        await ctx.send(f"💵 Withdrew `{amount}` Quarks from your bank.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
