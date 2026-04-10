
from dataclasses import dataclass
from auction import AuctionRound

@dataclass
class PlayerStats:
    wins: int = 0
    total_spent: float = 0.0
    total_profit: float = 0.0

class Simulation:
    def __init__(self, players, base_cost=1.0, alpha=10.0, max_price=20):
        self.players = players
        self.base_cost = base_cost
        self.alpha = alpha
        self.max_price = max_price
        self._reset_stats()

    def _reset_stats(self): # create empty PlayerStats for each player
        
        self.stats = {name: PlayerStats() for name, _ in self.players}
        self.seller_revenues = []
        self.round_history = []
        self.rounds_played = 0
        self.no_winner_rounds = 0

    def run(self, n_rounds=500, verbose=False, verbose_every=100):
        for r in range(n_rounds):
            self._run_one_round(r, verbose and r % verbose_every == 0)
        self.rounds_played += n_rounds
