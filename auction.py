import csv
from BST import BidBST


def bid_cost(price, base_cost=1.0, alpha=10.0):
    return base_cost + alpha / (price + 1)


class AuctionRound:

    def __init__(self, base_cost=1.0, alpha=10.0):
        self.base_cost, self.alpha = base_cost, alpha
        self.bst, self.bids, self.costs = BidBST(), [], {}
        self.winner, self.seller_revenue = None, 0.0

    def place_bid(self, player, price):
        if not isinstance(price, int) or price < 0: raise ValueError("Invalid price") #detect error#
        self.bst.insert(price, player)
        self.bids.append((player, price))
        cost = bid_cost(price, self.base_cost, self.alpha)     #define cost#
        self.costs[player] = self.costs.get(player, 0) + cost
        self.seller_revenue += cost

    def load_from_list(self, bid_list):
        for player, price in bid_list:
            self.place_bid(player, price)

    def load_from_csv(self, filepath):
        with open(filepath) as f:
            for player, price in csv.reader(f):
                self.place_bid(player.strip(), int(price))


    def resolve(self):
        res = self.bst.find_lowest_unique()
        self.winner = res if res[0] is not None else None
        return self.winner

    def summary(self):
        print(f"\n{' SUMMARY ':═^30}")
        self.bst.display()
        print(f"Revenue: {self.seller_revenue:.2f} | Bids: {self.bst.total_bids}")
        if self.winner:
            price, player = self.winner
            print(f" {player} won at {price} (Profit: {price - self.costs[player]:.2f})")
        else:
            print(" No winner")
