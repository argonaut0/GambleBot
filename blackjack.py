from game import Game
from random import randrange

class Blackjack(Game):
  cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

  def __init__(self, player, account, bet):
    self.account = account
    self.bet = bet
    self.pool = Blackjack.cards
    self.player = player
    self.cards = []
    self.hidden = None
    self.aicard = []

    self.account.use(bet)

  
  async def start(self, message):
    self.hidden = self.draw()
    self.aicard.append("X")
    self.aicard.append(self.draw())

    return await self.hit(message)

  async def play(self, message):
    
    if message.content == 'hit':
      return await self.hit(message)
    if message.content == 'stand':
      return await self.stand(message)
    return True


  async def hit(self, message):
    self.cards.append(self.draw())

    await message.channel.send(str(self.player) +"\n"+ self.prnthands())

    return await self.eval_game(message)


  async def stand(self, message):
    self.aicard[0] = self.hidden
    while self.sum(self.aicard) < 17:
      self.aicard.append(self.draw())

    await message.channel.send(str(self.player) +"\n"+ self.prnthands())

    return await self.end_game(message)


  async def end_game(self, message):
    if await self.eval_game(message):
      if self.sum(self.aicard) > self.sum(self.cards):
        await self.lose(message)
      else:
        await self.win(message)
    return False


  async def eval_game(self, message):
    if self.sum(self.cards) == 21:
      await message.channel.send("Blackjack!")
      await self.win(message)
      return False
    elif self.sum(self.cards) > 21:
      await message.channel.send("Bust!")
      await self.lose(message)
      return False
    elif self.sum(self.aicard) == 21:
      await message.channel.send("Dealer Blackjack!")
      await self.lose(message)
      return False
    elif self.sum(self.aicard) > 21:
      await message.channel.send("Dealer bust!")
      await self.win(message)
      return False
    return True


  def prnthands(self):
    return "Dealer hand: " + str(self.aicard) + "\n" + "Your hand is " + str(self.cards)

  
  def draw(self):
    return self.pool.pop(randrange(len(Blackjack.cards)))

  async def win(self, message):
    await message.channel.send("You Won! $" + str(self.bet * 2))
    self.account.add(2 * self.bet)

  async def lose(self, message):
    await message.channel.send("You Lost $" + str(self.bet))


  def sum(self, cds):
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
