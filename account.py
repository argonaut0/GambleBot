# deprecated


# Represents a bank account for a player
class Account:
    def __init__(self):
        self.cash = 1000

    def use(self, i):
        if self.valid(i):
            self.cash -= i
            return i
        else:
            return None

    def add(self, i):
        self.cash += i

    def valid(self, i):
        return self.cash >= i
