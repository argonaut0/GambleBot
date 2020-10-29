# deprecated
from abc import ABC, abstractmethod
from discord import Member, Message
from account import Account

"""
Abstract Game class

all async methods return one of {True, False}

True: keep the game going
False: finish and remove the game from the list
"""


class Game(ABC):

    # Init vars
    def __init__(self, player: Member, account: Account, bet: int):
        self.player: Member = player
        self.account: Account = account
        self.bet: int = bet

    # return: True if the game is still running
    async def start(self, m: Message) -> bool:
        pass

    # return: True if the game is still running
    @abstractmethod
    async def play(self, m: Message) -> bool:
        pass
