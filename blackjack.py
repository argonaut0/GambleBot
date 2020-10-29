import discord
import copy
from random import randrange
from discord.ext import commands
from gtypes import Card, CardHand


class Blackjack(commands.Cog):
    DECK: CardHand = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def blackjack(self, ctx, bet: int):
        # type: (self, context, int) -> None
        eco = self.bot.get_cog('Eco')
        games = self.bot.get_cog('Games')
        if eco and games:
            if not games.active(ctx) and await eco.spend(ctx, bet):
                games.add(ctx, Blackjack._Game(ctx.author, bet, self))
                await games.get(ctx).start(ctx.message)


    class _Game:
        def __init__(self, player, bet, handle):
            # type: (_Game, User, int, Blackjack) -> None
            self.bot = handle.bot
            self.player = player
            self.bet = bet
            self.pool: CardHand = copy.deepcopy(Blackjack.DECK)
            self.hand: CardHand = []
            self.hidden: Card = None
            # Dealer Hand
            self.dealer_hand: CardHand = []


        ##
        # PUBLIC API
        ##

        # Does the initial deal
        # return: True if the game is still going
        async def start(self, m):
            # type: (Message) -> bool
            self.hidden = self.draw()
            self.dealer_hand.append("X")
            self.dealer_hand.append(self.draw())
            return await self._hit(m)

        # Makes a play
        # return: True if the game is still going
        async def play(self, m):
            # type: (Message) -> bool
            if m.content == 'hit':
                return await self._hit(m)
            if m.content == 'stand':
                await self._stand(m)
                return False
            return True

        ##
        # PRIVATE GAME FUNCTIONS
        ##

        # Makes a hit
        # return: True if the game is still going
        async def _hit(self, m):
            # type: (Message) -> bool
            self.hand.append(self.draw())

            await m.channel.send(str(self.player) + "\n" + self.print_hands())

            return await self._eval_game(m)

        # Makes the stand and ends the game if no one busts or blackjacks
        async def _stand(self, m):
            # type: (Message) -> bool
            self.dealer_hand[0] = self.hidden
            while self._sum(self.dealer_hand) < 17:
                self.dealer_hand.append(self.draw())

            await m.channel.send(str(self.player) + "\n" + self.print_hands())

            if await self._eval_game(m):
                if self._sum(self.dealer_hand) > self._sum(self.hand):
                    await self.lose(m)
                else:
                    await self.win(m)

        # Checks for busts or blackjacks
        # return: True if the game is still going
        async def _eval_game(self, m):
            # type: (Message) -> bool
            if self._sum(self.hand) == 21:
                await m.channel.send("Blackjack!")
                await self.blackjack(m)
                return False
            elif self._sum(self.hand) > 21:
                await m.channel.send("Bust!")
                await self.lose(m)
                return False
            elif self._sum(self.dealer_hand) == 21:
                await m.channel.send("Dealer Blackjack!")
                await self.lose(m)
                return False
            elif self._sum(self.dealer_hand) > 21:
                await m.channel.send("Dealer bust!")
                await self.win(m)
                return False
            return True

        ##
        # PRIVATE HELPER FUNCTIONS
        ##

        # return: pretty str representation of the 2 hands
        def print_hands(self) -> str:
            return "Dealer hand: " + str(self.dealer_hand) + "\n" + "Your hand is " + str(self.hand)

        # return: popped random card from the deck
        def draw(self) -> Card:
            return self.pool.pop(randrange(len(self.pool)))

        # process player blackjack
        async def blackjack(self, m) -> None:
            await m.channel.send("Blackjack! You won $" + str(self.bet * 2))
            await self.payout(m, 2.5 * self.bet)

        # process player win
        async def win(self, m) -> None:
            await m.channel.send("You Won $" + str(self.bet * 2))
            await self.payout(m, 2 * self.bet)

        # process player loss
        async def lose(self, m) -> None:
            await m.channel.send("You Lost $" + str(self.bet))

        # dispense winnings
        async def payout(self, m, amt):
            eco = self.bot.get_cog('Eco')
            if eco:
                await eco.earn(m, amt)

        # return: the sum of the hand
        def _sum(self, cds: CardHand) -> int:
            s: int = 0

            def a(c):
                nonlocal s
                if c == "A":
                    return
                elif c in ("J", "Q", "K"):
                    s += 10
                else:
                    s += c

            for c in cds:
                if c == "X":
                    a(self.hidden)
                else:
                    a(c)
            for c in cds:
                if c == "A" or (c == "X" and self.hidden == "A"):
                    if s + 11 > 21:
                        s += 1
                    else:
                        s += 11
            return s

