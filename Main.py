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

# ── OPTION 3: Automated simulation ───────────────────────
def run_simulation():
    separator("Multi-Round Simulation")
    try:
        n = int(input("  How many rounds? [500]: ").strip() or "500")
    except ValueError:
        n = 500
 
    bots = [
        ("DiceRoller", DiceRoller()),
        ("Cheapskate", Cheapskate()),
        ("Accountant", Accountant()),
        ("Historian",  Historian()),
        ("Hipster",    Hipster()),
    ]
    base_cost, alpha, max_price = 1.0, 10.0, 20
    wins         = {name: 0   for name, _ in bots}
    total_spent  = {name: 0.0 for name, _ in bots}
    total_profit = {name: 0.0 for name, _ in bots}
    no_winner    = 0
    total_rev    = 0.0
    history      = []
 
    print(f"\n  Running {n} rounds...", end=" ")

    for r in range(n):
        auction = AuctionRound(base_cost, alpha)
        for name, strat in bots:
            auction.place_bid(name, strat.bid(r, history, base_cost, alpha, max_price))
        winner = auction.resolve()
        total_rev += auction.seller_revenue
        if winner is None:
            no_winner += 1
        for name, _ in bots:
            cost = auction.costs.get(name, 0.0)
            total_spent[name] += cost
            if winner and winner[1] == name:
                wins[name]         += 1
                total_profit[name] += winner[0] - cost
            else:
                total_profit[name] -= cost
        history.append(auction.analysis())
    print("done!\n")
 
    print(f"  No winner:     {no_winner} rounds ({100*no_winner/n:.1f}%)")
    print(f"  Total revenue: {total_rev:.2f}  (avg {total_rev/n:.2f}/round)")
    print(f"\n  {'Player':<14} {'Wins':>5} {'Win%':>6} {'Avg Spent':>10} {'Total Profit':>13}")
    print("  " + "─" * 52)
    for name, _ in sorted(bots, key=lambda x: wins[x[0]], reverse=True):
        print(f"  {name:<14} {wins[name]:>5} {100*wins[name]/n:>5.1f}%"
              f"  {total_spent[name]/n:>9.3f}  {total_profit[name]:>13.2f}")
    press_enter()

# ── OPTION 4: Human vs bots ──────────────────────────────
def human_vs_bots():
    separator("Human vs Bots")
    name  = input("  Your name: ").strip() or "Player"
    human = Human(name)
    bots  = [("Bot_Dice",  DiceRoller()), ("Bot_Cheap", Cheapskate()),
             ("Bot_Acc",   Accountant()), ("Bot_Hip",   Hipster())]
    all_players = [(name, human)] + bots
    base_cost, alpha, max_price, n_rounds = 1.0, 10.0, 20, 5
 
    wins         = {p: 0   for p, _ in all_players}
    total_profit = {p: 0.0 for p, _ in all_players}
    history      = []
 
    print(f"\n  {n_rounds} rounds. Lowest UNIQUE bid wins.")
    print(f"  Cost = {base_cost} + {alpha} / (price + 1)\n")
 
    for r in range(n_rounds):
        separator(f"Round {r+1}/{n_rounds}")
        auction = AuctionRound(base_cost, alpha)
        auction.place_bid(name, human.bid(r, history, base_cost, alpha, max_price))
        for bname, strat in bots:
            auction.place_bid(bname, strat.bid(r, history, base_cost, alpha, max_price))
        winner = auction.resolve()
        auction.summary()
        for pname, _ in all_players:
            cost = auction.costs.get(pname, 0.0)
            if winner and winner[1] == pname:
                wins[pname]         += 1
                total_profit[pname] += winner[0] - cost
            else:
                total_profit[pname] -= cost
        history.append(auction.analysis())
        if r < n_rounds - 1:
            press_enter()
 
    separator("Final Scoreboard")
    print(f"  {'Player':<16} {'Wins':>5} {'Total Profit':>13}")
    print("  " + "─" * 36)
    for i, (pname, _) in enumerate(sorted(all_players, key=lambda x: wins[x[0]], reverse=True), 1):
        you = " ← YOU" if pname == name else ""
        print(f"  {i}. {pname:<14} {wins[pname]:>5}  {total_profit[pname]:>13.2f}{you}")
    press_enter()

# ── MAIN MENU ────────────────────────────────────────────
MENU = [
    ("Demo auction round (random bids)",     demo_round),
    ("BST successor / predecessor explorer", bst_demo),
    ("Run simulation (bots only)",           run_simulation),
    ("Play against the bots",                human_vs_bots),
    ("Exit",                                 None),
]
 
def main():
    print("\n" + "═" * 45)
    print("   LowBid — Lowest Unique Bid Wins")
    print("═" * 45)
    print("  Winner = lowest bid chosen by exactly 1 person.")
    print("  Cost   = base_cost + alpha / (price + 1)")
    print("═" * 45)
 
    while True:
        print("\n  MAIN MENU")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"  {i}. {label}")
        choice = input("\n  Choose (1-5): ").strip()
        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(MENU)):
                raise ValueError
        except ValueError:
            print("  Please enter a number between 1 and 5.")
            continue
        label, action = MENU[idx]
        if action is None:
            print("\n  Goodbye!\n")
            break
        action()
 
 
if __name__ == "__main__":
    main()
 