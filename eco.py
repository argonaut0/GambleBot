import discord
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.ext.commands import command

from typing import Dict


##
# Eco Cog
#
# Represents the wallets and bank accounts of Users
##
class Eco(Cog):
    NO_BAL_STR: str = ", You don't have enough money!"
    INIT_WALLET_BAL: int = 1000

    def __init__(self, bot: discord.Client) -> None:
        self.bot: discord.Client = bot
        self.wallets: Dict[int, Eco.Wallet] = {}
        self.bank: Dict[int, Eco.Account] = {}

    ##
    # COMMANDS
    ##

    ##
    # bal
    #   Prints the user's balance
    ##
    @command()
    async def bal(self, ctx: Context) -> None:
        await self.print_bal(ctx)

    ##
    # pay [target user] [amount]
    #   Transfers money from user's wallet to target user
    ##
    @command()
    async def pay(self, ctx: Context, usr: discord.Member, amt: int) -> bool:
        await self._check_wallet(ctx.author.id)
        await self._check_wallet(usr.id)
        if await self.spend(ctx, amt):
            await self.wallets[usr.id].add(amt)
            await ctx.channel.send(str(ctx.author) + " gave " + str(usr) + " $" + str(amt))

    ##
    # PUBLIC API
    ##

    ##
    # Prints the user's balance
    ##
    async def print_bal(self, ctx: Context) -> None:
        await self._check_wallet(ctx.author.id)
        wal = self.wallets[ctx.author.id].bal
        # TODO bank
        bal = 0  # self.bank[ctx.author.id].bal
        await ctx.channel.send(str(ctx.author) + " you have: \n   Wallet: $" + str(wal) + "\n   Bank: $" + str(bal))

    ##
    # Deducts an amount from the user's wallet
    #   Return: True if successful
    ##
    async def spend(self, ctx: Context, amt: int) -> bool:
        await self._check_wallet(ctx.author.id)
        if not await self.wallets[ctx.author.id].use(amt):
            await ctx.channel.send(str(ctx.author) + Eco.NO_BAL_STR)
            return False
        return True

    ##
    # Adds an amount to the user's wallet
    ##
    async def earn(self, ctx: Context, amt: int):
        await self._check_wallet(ctx.author.id)
        await self.wallets[ctx.author.id].add(amt)
        await self.print_bal(ctx)

    ##
    # PRIVATE METHODS
    ##
    async def _check_wallet(self, uid: int) -> None:
        if uid not in self.wallets:
            await self._add_wallet(uid)

    #
    async def _add_wallet(self, uid: int) -> None:
        self.wallets[uid] = Eco.Wallet(Eco.INIT_WALLET_BAL)

    class Wallet:
        def __init__(self, bal: int) -> None:
            self.bal = bal

        async def use(self, i: int) -> bool:
            if self.bal >= i and i > 0:
                self.bal -= i
                return True
            else:
                return False

        async def add(self, i: int) -> None:
            self.bal += i

    # TODO Unimplemented
    class Account:
        def __init__(self, bal: int) -> None:
            self.bal = bal

        async def withdraw(self, i: int) -> bool:
            if self.bal >= i and i > 0:
                self.bal -= i
                return True
            else:
                return False

        async def deposit(self, i: int) -> None:
            self.bal += i
