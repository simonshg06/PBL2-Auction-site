from auction import AuctionRound, bid_cost
from BST import BidBst
from strategies import Human, DiceRoller, Cheapskate, Accountant, Historian
import random


def assign_strategies(player_names): # takes a list of player names
    available = [DiceRoller, Cheapskate, Accountant, Historian] # list of strategy classes
    return [(name, random.choice(available)()) for name in player_names] #random.choice picks a random strategy from the available list for each player

def separator(title=""): #optional title
    print(f"\n── {title} ──" if title else "\n" + "─" * 40) # if no title, plain line of 40 dashes is printed
 
 
def press_enter():
    input("\n  [Press Enter to continue]") # waits for the user to press enter

# OPTION 1: Quick demo with random bids 
def demo_round():
    separator("Demo Auction Round") # prints a separating line with the title "Demo Auction Round"
    filepath = "lowbid_manche_demo.csv" # the filepath/location of the csv file that will be loaded
    auction = AuctionRound(base_cost=1.0, alpha=10.0) # creates a new auction round

    try: # attempts t run the next 4 lines of code
        auction.load_from_csv(filepath) # loads the bids from the csv file into the auction file (load from cvs define in auction)
        for player, price in auction.bids: # for each player and price in the list of bids
            print(f"  {player:<10} bids {price:>2}  (cost: {bid_cost(price, 1.0, 10.0):.2f})") # prints the player 10 characters to the left, price 2 characters to the right and the bid cost to 2 decimals
        auction.resolve() # finds the winner of the auction round (resolve defined in auction)
        auction.summary() # prints the summary of the auction round, including the winner and the revenue (summary defined in auction)
    except FileNotFoundError: # if try fails then this code is run
        print(f"  ✗ File '{filepath}' not found.") # prints an error message if the file is not found at the specified location

    press_enter()

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
    filepath = "lowbid_manche_demo.csv"

    try:
        probe = AuctionRound(base_cost=1.0, alpha=10.0)
        probe.load_from_csv(filepath)
    except FileNotFoundError:
        print(f"  ✗ File '{filepath}' not found.")
        press_enter()
        return

    player_names = [player for player, _ in probe.bids]
    bots = assign_strategies(player_names)  # each player gets a strategy

    print("\n  Player strategy assignments:")
    for name, strat in bots:
        print(f"    {name:<14} → {strat.name}")

    try:
        n = int(input("  How many rounds? [500]: ").strip() or "500")
    except ValueError:
        n = 500

    base_cost, alpha = 1.0, 10.0
    wins         = {name: 0   for name in player_names}
    total_spent  = {name: 0.0 for name in player_names}
    total_profit = {name: 0.0 for name in player_names}
    no_winner    = 0
    total_rev    = 0.0
    history      = []

    print(f"\n  Running {n} rounds...", end=" ")

    for r in range(n):
        auction = AuctionRound(base_cost, alpha)
        for name, strat in bots:
            auction.place_bid(name, strat.bid(r, history, base_cost, alpha, max_price=20))
        winner = auction.resolve()
        total_rev += auction.seller_revenue
        if winner is None:
            no_winner += 1
        for name in player_names:
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
    strat_map = {name: strat.name for name, strat in bots}
    print(f"\n  {'Player':<14} {'Strat':<12} {'Wins':>5} {'Win%':>6} {'Avg Spent':>10} {'Total Profit':>13}")
    print("  " + "─" * 78) 
    for name in sorted(player_names, key=lambda x: wins[x], reverse=True):
        s_name = strat_map.get(name, "Unknown")
        print(f"  {name:<14} {s_name:<12} {wins[name]:>5} {100*wins[name]/n:>5.1f}%"
              f"  {total_spent[name]/n:>9.3f}  {total_profit[name]:>13.2f}")

    press_enter()

#  OPTION 4: Human vs bots 
def human_vs_bots():
    separator("Human vs Bots")
    filepath = "lowbid_manche_demo.csv"

    try:
        probe = AuctionRound(base_cost=1.0, alpha=10.0)
        probe.load_from_csv(filepath)
    except FileNotFoundError:
        print(f"  ✗ File '{filepath}' not found.")
        press_enter()
        return

    csv_players = assign_strategies([player for player, _ in probe.bids])

    your_name = input("  Your name: ").strip() or "Player"
    human = Human(your_name)
    base_cost, alpha, max_price, n_rounds = 1.0, 10.0, 20, 5

    all_players = [(your_name, human)] + csv_players
    wins = {p: 0 for p, _ in all_players}
    total_profit = {p: 0.0 for p, _ in all_players}
    history = []

    
    opponent_names = [name for name, strat in csv_players]
    print(f"\n  {n_rounds} rounds. Lowest UNIQUE bid wins.")
    print(f"  Opponents loaded: {', '.join(opponent_names)}") 
    print(f"  Cost = {base_cost} + {alpha} / (price + 1)\n")

    for r in range(n_rounds):
        separator(f"Round {r+1}/{n_rounds}")
        auction = AuctionRound(base_cost, alpha)
        
        
        auction.place_bid(your_name, human.bid(r, history, base_cost, alpha, max_price))
        
        
        for bname, strat in csv_players:
            auction.place_bid(bname, strat.bid(r, history, base_cost, alpha, max_price=20))
        
        winner = auction.resolve()
        auction.summary()
        
        for pname, _ in all_players:
            cost = auction.costs.get(pname, 0.0)
            if winner and winner[1] == pname:
                wins[pname] += 1
                total_profit[pname] += winner[0] - cost
            else:
                total_profit[pname] -= cost
        
        history.append(auction.analysis())
        if r < n_rounds - 1:
            press_enter()

    separator("Final Scoreboard")
    print(f"  {'Player':<16} {'Wins':>5} {'Total Profit':>13}")
    print("  " + "─" * 36)
    
    
    sorted_players = sorted(all_players, key=lambda x: wins[x[0]], reverse=True)
    
    for i, (pname, _) in enumerate(sorted_players, 1):
        is_you = " ← YOU" if pname == your_name else ""
        print(f"  {i}. {pname:<14} {wins[pname]:>5}  {total_profit[pname]:>13.2f}{is_you}")
    
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
 