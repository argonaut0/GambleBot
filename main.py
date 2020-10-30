import os
import logging

from discord.ext import commands

from eco import Eco
from games import Games
from blackjack import Blackjack
from coinflip import CoinFlip


COMMAND_PREFIX = "."
TOKEN = os.environ.get("DISCORD_BOT_SECRET")

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.add_cog(Eco(bot))
bot.add_cog(Games(bot))
bot.add_cog(Blackjack(bot))
bot.add_cog(CoinFlip(bot))


@bot.event
async def on_ready():
    print("logged in as {0.user}".format(bot))


bot.run(TOKEN)
