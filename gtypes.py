from typing import Literal, List

##
# Defines custom types for use in games
#
##
Card = Literal["A", "J", "Q", "K", 2, 3, 4, 5, 6, 7, 8, 9, 10]
CardHand = List[Card]
