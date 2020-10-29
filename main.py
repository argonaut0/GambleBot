import os
from discord.ext import commands
from blackjack import Blackjack
from account import Account

COMMAND_PREFIX = "."

token = os.environ.get("DISCORD_BOT_SECRET")
# games is a dict {discord.Member.id : ABC game.Game}, contains all the games currently running
games = {}
# accounts is a dict {discord.Member.id : account.Account}
accounts = {}
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


async def no_game_active(ctx):
    return ctx.message.author.id not in games


async def has_account(ctx):
    return ctx.message.author.id in accounts


async def not_has_account(ctx):
    return ctx.message.author.id not in accounts


@bot.event
async def on_ready():
    print("logged in as {0.user}".format(bot))


@bot.command()
@commands.check(no_game_active)
@commands.check(has_account)
async def blackjack(ctx, bet: int):
    if accounts[ctx.author.id].valid(bet):
        games[ctx.author] = Blackjack(ctx.author, accounts[ctx.author.id], bet)
        await games[ctx.author].start(ctx)


@bot.command()
@commands.check(has_account)
async def bal(ctx):
    print("Checked a bal")
    m = ctx.message
    await m.channel.send(str(m.author) + " you have $" + str(accounts[m.author.id].cash))


@bot.command()
@commands.check(not_has_account)
async def acc(ctx):
    print("Created a new account")
    m = ctx.message
    accounts[m.author.id] = Account()
    await m.channel.send(str(m.author) + " you have $" + str(accounts[m.author.id].cash))


# keepalive.keep_alive()
bot.run(token)
