import csv
from bst import BidBST


def bid_cost(price, base_cost=1.0, alpha=10.0):
    return base_cost + alpha / (price + 1)


class AuctionRound:
    
    def __init__(self, base_cost=1.0, alpha=10.0):
        self.base_cost, self.alpha = base_cost, alpha
        self.bst, self.bids, self.costs = BidBST(), [], {}
        self.winner, self.seller_revenue = None, 0.0

