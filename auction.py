import csv
from bst import BidBST

def bid_cost(price, base_cost=1.0, alpha=10.0):
    return base_cost + alpha / (price + 1)
