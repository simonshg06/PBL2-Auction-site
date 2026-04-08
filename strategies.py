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

class Cheapskate(Strategy):
    name = "Cheapskate"

    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        prices = range(max_price + 1)
        weights = [math.exp(-0.5 * k) for k in prices]
        return random.choices(prices, weights=weights)[0]
    
class Accountant(Strategy):
    name = "Accountant"

    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        def score(p):
            return p - (base_cost + alpha / (p + 1)) + random.gauss(0, 0.5)
        return max(range(max_price + 1), key=score)