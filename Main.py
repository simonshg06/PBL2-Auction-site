import random
from auction import AuctionRound, bid_cost
from BST import BidBst
from strategies import DiceRoller, Cheapskate, Accountant, Historian, Hipster, Human

def separator(title=""):
    print(f"\n── {title} ──" if title else "\n" + "─" * 40)
 
 
def press_enter():
    input("\n  [Press Enter to continue]")

