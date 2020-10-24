import discord
import os
from blackjack import Blackjack
from account import Account
import keepalive

token = os.environ.get("DISCORD_BOT_SECRET")
client = discord.Client()

# games is a dict {discord.Member : ABC game.Game}, contains all the games currently running
games = {}
# accounts is a dict {discord.Member.id : account.Account}
accounts = {}


# Runs on Login
@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))


# Runs on send message
@client.event
async def on_message(message):
    # Check so that the bot does not respond to itself
    if message.author == client.user:
        return

    # Check for active games
    if message.author in games:
        if not await games[message.author].play(message):
            del games[message.author]

    # Check for commands
    if message.content.startswith("."):
        # Create a new account if not existing
        if message.author.id not in accounts:
            accounts[message.author.id] = Account()
        c = message.content[1:].split(" ")
        if c[0] == "blackjack":
            try:
                if accounts[message.author.id].valid(int(c[1])):
                    games[message.author] = Blackjack(message.author, accounts[message.author.id], int(c[1]))
                    await games[message.author].start(message)
            except ValueError:
                return
        if c[0] == "bal":
            await message.channel.send(str(message.author) + " you have $" + str(accounts[message.author.id].cash))


# keepalive.keep_alive()
client.run(token)
