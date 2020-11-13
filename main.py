# Standard Libraries
import os
import logging

# Libraries
from discord.ext import commands

# Custom Cogs
from eco import Eco
from games import Games
from blackjack import Blackjack
from coinflip import CoinFlip


# Load Settings
COMMAND_PREFIX = "."
TOKEN = os.environ.get("DISCORD_BOT_SECRET")

# Enable Logging
logging.basicConfig(level=logging.INFO)

# Load Cogs
bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.add_cog(Eco(bot))
bot.add_cog(Games(bot))
bot.add_cog(Blackjack(bot))
bot.add_cog(CoinFlip(bot))


# Runs on bot ready, overrides default listener
@bot.event
async def on_ready():
    print("logged in as {0.user}".format(bot))


bot.run(TOKEN)
