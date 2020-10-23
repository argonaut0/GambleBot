from random import randrange
from abc import ABC, abstractmethod



"""
Abstract Game class

required functions listed below

all async methods return one of {True, False}

True: keep the game going
False: finish and remove the game from the list
"""
class Game(ABC):
  
  
  def __init__(self, player):
    pass
  
  
  async def play(self, message):
    pass
