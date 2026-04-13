import random # for generating random bids in the demo
from auction import AuctionRound, bid_cost
from BST import BidBst
from strategies import DiceRoller, Cheapskate, Accountant, Historian, Human

def separator(title=""): #optional title
    print(f"\n── {title} ──" if title else "\n" + "─" * 40) # if no title, plain line of 40 dashes is printed
 
 
def press_enter():
    input("\n  [Press Enter to continue]") # waits for the user to press enter

# OPTION 1: Quick demo with random bids 
def demo_round():
    separator("Demo Auction Round") # prints a separating line with the title "Demo Auction Round"
    players = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"] # list of player names for the demo
    auction = AuctionRound(base_cost=1.0, alpha=10.0)  # creates a new auction round with specified base cost and alpha parameters for the cost function
 
    for player in players:  # loops through each player in the list of players
        price = random.randint(0, 15)  # generates a random bid price between 0 and 15
        auction.place_bid(player, price)  #calls place_bid from auction.py which inserts the bid into the BST
        print(f"  {player:<10} bids {price:>2}  (cost: {bid_cost(price, 1.0, 10.0):.2f})") #player:<10 alligns the player name to the left with a width of 10 charac, price:>2 allings price to the right with a width of 2 charac
 
    auction.resolve() # calls resolve from auction to find the winner based on the lowest unique bid
    auction.summary() # calls summary to print the results of the auction round 
    press_enter() # waits for enter to be pressed before returning to the main menu

#  OPTION 2: Show BST successor / predecessor 
def bst_demo():
    separator("BST Successor / Predecessor") # prints a separating line with the title "BST Successor / Predecessor"
    bst = BidBst() # creates a new empty BST
    for price, player in [(1,"A"),(5,"B"),(3,"C"),(8,"D"),(2,"E"),(7,"F"),(10,"G")]: # list of (price, player) pairs to insert into the BST
        bst.insert(price, player) # inserts each price and player pair into the bst using insert defined in BST
 
    bst.display() # calls display from BST to print the prices using inorder traversal
    print("\n  Successor   = next higher price in the BST.")
    print("  Predecessor = next lower price in the BST.")
    print("  Useful: if the lowest bid is not unique, jump to its successor.")
 
    while True:  # continuously running loop
        raw = input("\n  Enter a price to query (or 'q' to quit): ").strip() # strip removes any extra spaces after user inputs
        if raw.lower() == "q": # lower converts capital letters to lowercase
            break # if q is entered then the loop breaks and we return to the main menu
        try: #attempts to run the next 3 lines of code
            p = int(raw) # turns the input into an integer
            print(f"    Successor   of {p}: {bst.successor(p)}") #successor defined in BST finds the next higher price in the BST and returns a tuple of (price, player) or None
            print(f"    Predecessor of {p}: {bst.predecessor(p)}") #predecessor defined in BST finds the next lower price in the BST and returns a tuple of (price, player) or None
        except ValueError: # if the input cannotbe converted, the except element raises the value error and prints the message
            print("  Please type a whole number.")
 
    press_enter() #waits for the enter button to be pressed 

#  OPTION 3: Automated simulation
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

#  OPTION 4: Human vs bots 
def human_vs_bots():
    separator("Human vs Bots")
    name  = input("  Your name: ").strip() or "Player"
    human = Human(name)
    bots  = [("Bot_Dice",  DiceRoller()), ("Bot_Cheap", Cheapskate()),
             ("Bot_Acc",   Accountant()), ]
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

#  MAIN MENU 
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
 