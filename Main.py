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
    separator("Multi-Round Simulation") # prints a separating line with the title "Multi-Round Simulation"
    filepath = "lowbid_manche_demo.csv" # the filepath/location of the csv file that will be loaded, this is used to get the player names and assign them strategies

    try:
        probe = AuctionRound(base_cost=1.0, alpha=10.0) # creates a new auction round
        probe.load_from_csv(filepath) # loads the bids from the csv file into the auction file (prob.bids) (load from cvs define in auction)
    except FileNotFoundError: # if try fails then this code is run
        print(f"  ✗ File '{filepath}' not found.") # prints an error message if the file is not found at the specified location
        press_enter()
        return 

    player_names = [player for player, _ in probe.bids] # goes through the list probe.bids and creates a list just for player names
    bots = assign_strategies(player_names)  # creates a list of tuples of (player name, strategy instance) by assigning a random strategy to each player

    print("\n  Player strategy assignments:") # prints the header for the player strategy assignments
    for name, strat in bots: # for each player name and strategy in the list of bots
        print(f"    {name:<14} → {strat.name}") # prints the player name 14 characters to the left. strat.name gives the name of the strategy (defined in each strategy class)

    try:
        n = int(input("  How many rounds? [500]: ").strip() or "500") # user inputs the number of rounds they want, entering nothing defaults to 500
    except ValueError: 
        n = 500 # in case the user mistypes, the number of rounds defaults to 500

    base_cost, alpha = 1.0, 10.0
    wins         = {name: 0   for name in player_names} # dictionary to track the number of wins for each player, initialized to 0
    total_spent  = {name: 0.0 for name in player_names} # dictionary to track the total amount spent on bids for each player, initialized to 0.0
    total_profit = {name: 0.0 for name in player_names} # dictionary to track the total profit for each player, initialized to 0.0
    no_winner    = 0 # counter to track the number of rounds with no winner, initialized to 0
    total_rev    = 0.0 # counter to track the total revenue for the seller across all rounds, initialized to 0.0
    history      = [] # list to track the history of each round's analysis, initialized to an empty list

    print(f"\n  Running {n} rounds...", end=" ") # prints the amount of rounds being run, end=" " keeps what we just printed on the same line as the "done!" that is printed at the end of the simulation

    for r in range(n): # loop that runs for the number of rounds specified by the user
        auction = AuctionRound(base_cost, alpha) # creates a new auction round for each round of the simulation
        print(f"\n  Running {n} rounds...", end=" ") # this is printed at the start of each round to show the progress of the simulation
        for name, strat in bots: # for each player name and strategy in the list of bots
            auction.place_bid(name, strat.bid(r, history, base_cost, alpha, max_price=20)) # places a bid for each player using their strategy's bid method defined in each strategy class
        winner = auction.resolve() # finds the winner of the auction round (resolve defined in auction)
        total_rev += auction.seller_revenue # adds the revenue from this round to the total revenue counter
        if winner is None: # if there is no winner for this round, the winner variable is None and we add 1 to the no_winner counter
            no_winner += 1 # no winner counter is increased by 1
        for name in player_names: # for each player name in the list of player names
            cost = auction.costs.get(name, 0.0) # gets the cost for this player from the auction costs dictionary, if the player did not place a bid then the cost defaults to 0.0
            total_spent[name] += cost # adds the cost of this round to the total spent for this player
            if winner and winner[1] == name: #checks if we have a winner and if the winner's name matches this player name
                wins[name]         += 1 # if this player is the winner, we add 1 to their win count
                total_profit[name] += winner[0] - cost # if this player is the winner, we add the profit from this round (winning price - cost) to their total profit
            else:
                total_profit[name] -= cost # if this player is not the winner, we subtract the cost of this round from their total profit 
        history.append(auction.analysis()) # adds the analysis of this round to the history list, analysis defined in auction returns a dictionary with stats about the round
    print("done!\n") # this is printed at the end of the simulation to show that it is finished

    print(f"  No winner:     {no_winner} rounds ({100*no_winner/n:.1f}%)") # prints how many rounds had no winner and the percentage of rounds with no winner to 1 decimal place
    print(f"  Total revenue: {total_rev:.2f}  (avg {total_rev/n:.2f}/round)") # prints the total seller revenue and the average per round, both to 2 decimal places
    strat_map = {name: strat.name for name, strat in bots} # creates a dictionary showing each player's assigned strategy
    print(f"\n  {'Player':<14} {'Strat':<12} {'Wins':>5} {'Win%':>6} {'Avg Spent':>10} {'Total Profit':>13}") # prints the header for the player results, with formatting for each column
    print("  " + "─" * 78)  # prints a separating line of 78 dashes with 2 spaces before it
    for name in sorted(player_names, key=lambda x: wins[x], reverse=True): # sorts the player names by their number of wins in descending order
        s_name = strat_map.get(name, "Unknown") # gets the strategy name for this player from the strat_map dictionary, defaults to "Unknown" if not found
        print(f"  {name:<14} {s_name:<12} {wins[name]:>5} {100*wins[name]/n:>5.1f}%" # prints the player name, strategy name, number of wins, win percentage, average amount spent per round and total profit for each player
              f"  {total_spent[name]/n:>9.3f}  {total_profit[name]:>13.2f}") # total spent per round is printed to 3 decimal places, total profit is printed to 2 decimal places

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
 