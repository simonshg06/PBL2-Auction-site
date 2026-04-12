import random  # For random numbers 
import math    


class Strategy:  # Base class for all bidder types 
    name: str 
    registry: dict = {}  # Tracks all strategy types

    def __init_subclass__(cls):  # Auto-registers new strategies
        if hasattr(cls, "name"):
            Strategy._registry[cls.name.lower()] = cls

    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        raise NotImplementedError  # To be defined by child classes
    

class DiceRoller(Strategy):  # Pure random bidding 
    name = "DiceRoller"
    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        return random.randint(0, max_price)
    

class Cheapskate(Strategy):  # Bias toward lowest possible prices 
    name = "Cheapskate"
    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        prices = range(max_price + 1)
        weights = [math.exp(-0.5 * k) for k in prices]
        return random.choices(prices, weights=weights)[0]
    

class Accountant(Strategy):  # Maximizes (Price - Bid Cost) 
    name = "Accountant"
    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        def score(p):  # Economic rationalization logic 
            return p - (base_cost + alpha / (p + 1)) + random.gauss(0, 0.5)
        return max(range(max_price + 1), key=score)
    

class Historian(Strategy):  # Bids near previous winning prices 
    name = "Historian"
    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        if not history: return random.randint(1, max_price // 2)
        win_freq = {}
        for r in history[-50:]:  # Analyzes recent winners
            if r["winner"]:
                wp = r["winner"][0]
                win_freq[wp] = win_freq.get(wp, 0) + 1
        if not win_freq: return random.randint(0, max_price)
        base = random.choices(list(win_freq), weights=win_freq.values())[0]
        return max(0, min(max_price, base + random.randint(-2, 2)))
    

class Hipster(Strategy):  # Avoids popular prices to stay unique 
    name = "Hipster"
    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        if not history: return random.randint(0, max_price)
        price_freq = {}
        for r in history[-20:]:  # Analyzes price distribution 
            for price, count in r.get("price_distribution", {}).items():
                price_freq[price] = price_freq.get(price, 0) + count
        all_prices = sorted(range(max_price + 1), key=lambda p: price_freq.get(p, 0))
        cutoff = max(1, (max_price + 1) // 3)
        return random.choice(all_prices[:cutoff])  # Picks from least used prices
    

class Human(Strategy):  # Manual input for human players 
    name = "Human"
    def __init__(self, player_name="Human"):
        self.player_name = player_name
    def bid(self, round_number, history, base_cost, alpha, max_price=20):
        from auction import bid_cost
        print(f"\n── Your turn, {self.player_name} ──")
        for p in [0, 1, 2, 5, 10, max_price]:  # Shows cost reference 
            print(f"    price={p:>3} → cost={bid_cost(p, base_cost, alpha):.2f}")
        while True:
            try:
                price = int(input(f"  Enter bid (0–{max_price}): "))
                if 0 <= price <= max_price: return price
            except ValueError: pass
            

STRATEGIES = Strategy._registry  # Registry of all usable strategies 