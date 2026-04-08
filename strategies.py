import random
import math

class Strategy:
    name: str
    _registry: dict = {}

    def __init_subclass__(cls):
        if hasattr(cls, "name"):
            Strategy._registry[cls.name.lower()] = cls

    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        raise NotImplementedError
    
class DiceRoller(Strategy):
    name = "DiceRoller"

    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        return random.randint(0, max_price)

