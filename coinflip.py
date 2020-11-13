from random import randint
from discord.ext import commands


##
# Single Player CoinFlip Cog
#
# Requires Eco and Games Cogs
##
class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def flip(self):
        return randint(0, 1)

    ##
    # CoinFlip command
    #
    #   Flips a coin and deducts or pays out a bet accordingly
    @commands.command()
    async def coinflip(self, ctx, amt: int):
        eco = self.bot.get_cog('Eco')
        if eco and await eco.spend(ctx, amt):
            if self.flip():
                await ctx.channel.send("You Won!")
                await eco.earn(ctx, 2 * amt)
            else:
                await ctx.channel.send("You Lost $" + str(amt))
