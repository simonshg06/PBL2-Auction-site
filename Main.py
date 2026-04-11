import random
from auction import AuctionRound, bid_cost
from BST import BidBst
from strategies import DiceRoller, Cheapskate, Accountant, Historian, Hipster, Human

def separator(title=""):
    print(f"\n── {title} ──" if title else "\n" + "─" * 40)
 
 
def press_enter():
    input("\n  [Press Enter to continue]")

# ── OPTION 1: Quick demo with random bids ────────────────
def demo_round():
    separator("Demo Auction Round")
    players = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
    auction = AuctionRound(base_cost=1.0, alpha=10.0)
 
    for player in players:
        price = random.randint(0, 15)
        auction.place_bid(player, price)
        print(f"  {player:<10} bids {price:>2}  (cost: {bid_cost(price, 1.0, 10.0):.2f})")
 
    auction.resolve()
    auction.summary()
    press_enter()