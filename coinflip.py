from random import randint
from discord.ext import commands

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def flip(self):
        return randint(0,1)

    @commands.command()
    async def coinflip(self, ctx, amt: int):
        eco = self.bot.get_cog('Eco')
        if eco and await eco.spend(ctx, amt):
            if self.flip():
                await ctx.channel.send("You Won!")
                await eco.earn(ctx, 2 * amt)
            else:
                await ctx.channel.send("You Lost $" + str(amt))

