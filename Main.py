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

# ── OPTION 2: Show BST successor / predecessor ───────────
def bst_demo():
    separator("BST Successor / Predecessor")
    bst = BidBst()
    for price, player in [(1,"A"),(5,"B"),(3,"C"),(8,"D"),(2,"E"),(7,"F"),(10,"G")]:
        bst.insert(price, player)
 
    bst.display()
    print("\n  Successor   = next higher price in the BST.")
    print("  Predecessor = next lower price in the BST.")
    print("  Useful: if the lowest bid is not unique, jump to its successor.")
 
    while True:
        raw = input("\n  Enter a price to query (or 'q' to quit): ").strip()
        if raw.lower() == "q":
            break
        try:
            p = int(raw)
            print(f"    Successor   of {p}: {bst.successor(p)}")
            print(f"    Predecessor of {p}: {bst.predecessor(p)}")
        except ValueError:
            print("  Please type a whole number.")
 
    press_enter()