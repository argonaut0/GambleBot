import discord
from discord.ext import commands

class Eco(commands.Cog):
    NO_BAL_STR = ", You don't have enough money!"
    INIT_WALLET_BAL = 1000


    def __init__(self, bot):
        self.bot = bot

        # wallets is dict(str, Wallet)
        self.wallets = {}
        # bank is dict(str, Account)
        self.bank = {}

    @commands.command()
    async def bal(self, ctx):
        await self.print_bal(ctx)

    async def print_bal(self, ctx):
        # type: (Context) -> None
        await self._check_wallet(ctx.author.id)
        wal = self.wallets[ctx.author.id].bal
        # TODO bank
        bal = 0 #self.bank[ctx.author.id].bal
        await ctx.channel.send(str(ctx.author) + " you have: \n   Wallet: $" + str(wal) + "\n   Bank: $" + str(bal))

    @commands.command()
    async def pay(self, ctx, usr: discord.Member, amt: int):
        # type: (Context, User, amt) -> bool
        await self._check_wallet(ctx.author.id)
        await self._check_wallet(usr.id)
        if await self.spend(ctx, amt):
            await self.wallets[usr.id].add(amt)
            await ctx.channel.send(str(ctx.author) + " gave " + str(usr) + " $" + str(amt))


    async def spend(self, ctx, amt):
        # type: (Context, int) -> bool
        await self._check_wallet(ctx.author.id)
        if not await self.wallets[ctx.author.id].use(amt):
            await ctx.channel.send(str(ctx.author) + Eco.NO_BAL_STR)
            return False
        return True


    async def earn(self, ctx, amt):
        await self._check_wallet(ctx.author.id)
        await self.wallets[ctx.author.id].add(amt)
        await self.print_bal(ctx)


    async def _check_wallet(self, uid):
        # type: (str) -> None
        if uid not in self.wallets:
            await self._add_wallet(uid)


    async def _add_wallet(self, uid):
        # type: (str) -> None
        self.wallets[uid] = Eco.Wallet(Eco.INIT_WALLET_BAL)


    class Wallet:
        def __init__(self, bal):
            # type: (int) -> None
            self.bal = bal

        async def use(self, i):
            # type: (int) -> bool
            if self.bal >= i:
                self.bal -= i
                return True
            else:
                return False

        async def add(self, i):
            # type: (int) -> None
            self.bal += i

    # TODO Unimplemented
    class Account:
        def __init__(self):
            self.bal = 0

        def __init__(self, bal):
            self.bal = bal

        async def withdraw(self, i):
            if self.bal >= i:
                self.bal -= i
                return True
            else:
                return False

        async def deposit(self, i):
            self.bal += i
