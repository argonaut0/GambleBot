from game import Game
from random import randrange
from discord import Member
from discord import Message
from account import Account
from gtypes import Card, CardHand

class Blackjack(Game):
  DECK: CardHand = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

  ## Init vars
  def __init__(self, player: Member, account: Account, bet: int):
    self.account: Account = account
    self.bet: int = bet
    self.pool: CardHand = Blackjack.DECK
    self.player: Member = player
    self.hand: CardHand = []
    self.hidden: Card = None
    # Dealer Hand
    self.dealerhand = []
    self.account.use(bet)


  ##
  ## PUBLIC API
  ##

  ## Does the initial deal
  # return: True if the game is still going
  async def start(self, m: Message) -> bool:
    self.hidden = self.draw()
    self.dealerhand.append("X")
    self.dealerhand.append(self.draw())
    return await self._hit(m)


  ## Makes a play
  # return: True if the game is still going
  async def play(self, m: Message) -> bool:
    if m.content == 'hit':
      return await self._hit(m)
    if m.content == 'stand':
      await self._stand(m)
      return False
    return True


  ##
  ## PRIVATE GAME FUNCTIONS
  ##

  ## Makes a hit
  # return: True if the game is still going
  async def _hit(self, m: Message) -> bool:
    self.hand.append(self.draw())

    await m.channel.send(str(self.player) +"\n"+ self.prnthands())

    return await self._eval_game(m)


  ## Makes the stand and ends the game if no one busts or blackjacks
  async def _stand(self, m: Message) -> None:
    self.dealerhand[0] = self.hidden
    while self._sum(self.dealerhand) < 17:
      self.dealerhand.append(self.draw())

    await m.channel.send(str(self.player) +"\n"+ self.prnthands())

    if await self._eval_game(m):
      if self._sum(self.dealerhand) > self._sum(self.hand):
        await self.lose(m)
      else:
        await self.win(m)


  ## Checks for busts or blackjacks
  # return: True if the game is still going
  async def _eval_game(self, m: Message) -> bool:
    if self._sum(self.hand) == 21:
      await m.channel.send("Blackjack!")
      await self.blackjack(m)
      return False
    elif self._sum(self.hand) > 21:
      await m.channel.send("Bust!")
      await self.lose(m)
      return False
    elif self._sum(self.dealerhand) == 21:
      await m.channel.send("Dealer Blackjack!")
      await self.lose(m)
      return False
    elif self._sum(self.dealerhand) > 21:
      await m.channel.send("Dealer bust!")
      await self.win(m)
      return False
    return True


  ##
  ## PRIVATE HELPER FUNCTIONS
  ##

  ## return: the sum of the hand
  def _sum(self, cds):
    s = 0
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
  

  ## return: pretty str representation of the 2 hands
  def prnthands(self) -> str:
    return "Dealer hand: " + str(self.dealerhand) + "\n" + "Your hand is " + str(self.hand)


  ## return: popped random card from the deck
  def draw(self) -> Card:
    return self.pool.pop(randrange(len(Blackjack.DECK)))


  ## process player blackjack
  async def blackjack(self, message) -> None:
    await message.channel.send("Blackjack! You won $" + str(self.bet * 2))
    self.account.add(2.5 * self.bet)


  ## process player win
  async def win(self, message) -> None:
    await message.channel.send("You Won $" + str(self.bet * 2))
    self.account.add(2 * self.bet)


  ## process player loss
  async def lose(self, message) -> None:
    await message.channel.send("You Lost $" + str(self.bet))
