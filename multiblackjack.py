import discord
import copy
from discord.ext import commands
from gtypes import Card, CardHand


class mBlackjack(commands.Cog):
    DECK: CardHand = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

    class Player:
        def __init__(self):
            return

    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.players: mBlackjack.Player = []
        self.pool: CardHand = copy.deepcopy(mBlackjack.DECK)
        self.dealer = mBlackjack.Player()

    @commands.command()
    async def gblackjack(self, ctx, *args: discord.Member):
        for m in args:
            await ctx.send('Hello {0.name}'.format(m)) 
