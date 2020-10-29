from discord.ext import commands


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # games is dict(str, Game)
        self.games = {}

        @self.bot.event
        async def on_message(m):
            if m.author == self.bot.user:
                return
            if m.author.id in self.games:
                if not await self.games[m.author.id].play(m):
                    del self.games[m.author.id]
            else:
                ctx = await self.bot.get_context(m)
                if ctx.valid:
                    await self.bot.invoke(ctx)

    def add(self, ctx, game):
        self.games[ctx.author.id] = game

    def rm(self, ctx):
        del self.games[ctx.author.id]

    def active(self, ctx):
        return ctx.author.id in self.games

    def get(self, ctx):
        return self.games[ctx.author.id]
