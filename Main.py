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
    filepath = "lowbid_manche_demo.csv" # the filepath/location of the csv file that will be loaded to get the player names for the simulation, the actual bids from the csv are not used in this simulation, only the player names are used to assign strategies to each player

    try:
        probe = AuctionRound(base_cost=1.0, alpha=10.0) # creates a new auction round to be used as a probe to load the player names from the csv file, the base cost and alpha parameters are not important for this probe since we are only using it to load the player names
        probe.load_from_csv(filepath) # loads the bids from the csv file into the probe auction round, this is done to get the player names from the csv file so that we can assign strategies to each player in the simulation
    except FileNotFoundError:
        print(f"  ✗ File '{filepath}' not found.") # if the file is not found at the specified location, an error message is printed and the function returns to the main menu
        press_enter()
        return 

    player_names = [player for player, _ in probe.bids] # creates a list of player names by iterating through the list of bids in the probe auction round, we only take the player name and ignore the price (hence the underscore) since we only need the player names to assign strategies for the simulation
    bots = assign_strategies(player_names)  # each player gets a strategy

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

    for r in range(n):
        auction = AuctionRound(base_cost, alpha) # creates a new auction round for each round of the simulation with the specified base cost and alpha parameters
        for name, strat in bots: # for each player name and strategy in the list of bots
            auction.place_bid(name, strat.bid(r, history, base_cost, alpha, max_price=20)) # each bot places a bid using their strategy's bid method
        winner = auction.resolve() # finds the winner of the auction round using the resolve method defined in auction, which returns a tuple of (price, player) for the winning bid or None if there is no winner
        total_rev += auction.seller_revenue # adds the revenue from this round to the total revenue counter, seller_revenue is updated in the place_bid method defined in auction each time a bid is placed, so by the end of the round it contains the total revenue for that round
        if winner is None: # if there is no winner for this round, we increment the no_winner counter by 1
            no_winner += 1 # we increment the no_winner counter by 1
        for name in player_names: # for each player name in the list of player names
            cost = auction.costs.get(name, 0.0) # we get the total cost for this player from the auction round's costs dictionary, if the player did not place any bids then we default to 0.0  
            total_spent[name] += cost # we add the cost for this round to the total amount spent for this player
            if winner and winner[1] == name: # if there is a winner and the winner's name matches this player name, then we increment the wins counter for this player by 1 and add the profit from this round to their total profit. The profit is calculated as the winning price (winner[0]) minus the total cost for this player.
                wins[name]         += 1  # increment the wins counter for this player by 1
                total_profit[name] += winner[0] - cost # add the profit from this round to the total profit for this player, profit is calculated as the winning price (winner[0]) minus the total cost for this player (cost)
            else:
                total_profit[name] -= cost # if this player is not the winner, we subtract the cost of this round from their total profit 
        history.append(auction.analysis()) # adds the analysis of this round to the history list, analysis defined in auction returns a dictionary with stats about the round
    print("done!\n") # this is printed at the end of the simulation to show that it is finished

    print(f"  No winner:     {no_winner} rounds ({100*no_winner/n:.1f}%)") # prints the number of rounds with no winner and the percentage of rounds with no winner out of the total rounds
    print(f"  Total revenue: {total_rev:.2f}  (avg {total_rev/n:.2f}/round)") # prints the total revenue for the seller across all rounds and the average revenue per round, both to 2 decimal places
    strat_map = {name: strat.name for name, strat in bots} # creates a dictionary mapping each player name to their strategy name for easy lookup when printing the final results
    print(f"\n  {'Player':<14} {'Strat':<12} {'Wins':>5} {'Win%':>6} {'Avg Spent':>10} {'Total Profit':>13}") # prints the header for the final results table, with columns for Player, Strategy, Wins, Win Percentage, Average Spent, and Total Profit. 
    print("  " + "─" * 78)  # prints a separating line under the header, 78 characters long to match the width of the table
    for name in sorted(player_names, key=lambda x: wins[x], reverse=True): # sorts the player names based on the number of wins in descending order
        s_name = strat_map.get(name, "Unknown") # looks up the strategy name for this player from the strat_map dictionary, defaults to "Unknown" if the player name is not found
        print(f"  {name:<14} {s_name:<12} {wins[name]:>5} {100*wins[name]/n:>5.1f}%" # prints the player name, strategy, number of wins, win percentage
              f"  {total_spent[name]/n:>9.3f}  {total_profit[name]:>13.2f}")  # prints the average amount spent per round for this player (total spent divided by number of rounds) to 3 decimal places, and the total profit for this player to 2 decimal places

    press_enter()

#  OPTION 4: Human vs bots 
def human_vs_bots():
    separator("Human vs Bots") # prints a separating line with the title "Human vs Bots"
    filepath = "lowbid_manche_demo.csv" # the filepath/location of the csv file that will be loaded to get the player names for the bots

    try:
        probe = AuctionRound(base_cost=1.0, alpha=10.0) # creates a new auction round 
        probe.load_from_csv(filepath, 1)  # loads the bids from the csv file for round 1 into the probe auction round
    except FileNotFoundError:
        print(f"  ✗ File '{filepath}' not found.") # if the file is not found at the specified location, an error message is printed and the function returns to the main menu
        press_enter()
        return 

    csv_player_names = [player for player, _ in probe.bids] # creates a list of player names by iterating through the list of bids in the probe auction round

    your_name = input("  Your name: ").strip() or "Player" # prompts the user to enter their name, if they just press enter without typing a name, it defaults to "Player"
    human = Human(your_name) # creates a new Human strategy object for the user
    base_cost, alpha, max_price = 1.0, 10.0, 20 

    try:
        n_rounds = int(input("  How many rounds? [10]: ").strip() or "10") # prompts the user to enter the number of rounds they want to play
    except ValueError:
        n_rounds = 10 # if the user enters an invalid number, the number of rounds defaults to 10

    all_player_names = [your_name] + csv_player_names # creates a list of all player names including the human player and the players from the csv file
    wins = {p: 0 for p in all_player_names} # dictionary to track the number of wins for each player, initialized to 0
    total_profit = {p: 0.0 for p in all_player_names} # dictionary to track the total profit for each player, initialized to 0.0
    history = [] # list to track the history of each round's analysis, initialized to an empty list

    print(f"\n  {n_rounds} rounds. Lowest UNIQUE bid wins.") # prints the rules of the game and the number of rounds being played
    print(f"  You are playing against {len(csv_player_names)} players from the CSV.") # prints the number of players from the csv file that the user is playing against
    print(f"  Cost = {base_cost} + {alpha} / (price + 1)\n") # prints the cost function that is being used in the auction rounds, with the specified base cost and alpha parameters

    for r in range(1, n_rounds + 1):  # loop through each round of the game, starting from 1 up to and including n_rounds
        separator(f"Round {r}/{n_rounds}") # prints a separating line with the title "Round X/Y" where X is the current round number and Y is the total number of rounds
        auction = AuctionRound(base_cost, alpha) # creates a new auction round for this round of the game with the specified base cost and alpha parameters

        # load the real bids from the CSV for this round
        auction.load_from_csv(filepath, r) # loads the bids from the csv file for this round into the auction round

        # add the human's bid on top
        auction.place_bid(your_name, human.bid(r, history, base_cost, alpha, max_price)) # prompts the human player to place their bid for this round using the bid method defined in the Human strategy class

        winner = auction.resolve() # finds the winner of this round using the resolve method defined in auction
        auction.summary() # prints the summary of this round, including the winner and the revenue for the seller

        for pname in all_player_names: # for each player name in the list of all player names
            cost = auction.costs.get(pname, 0.0) # we get the total cost for this player from the auction round's costs dictionary, if the player did not place any bids then we default to 0.0
            if winner and winner[1] == pname: # if there is a winner and the winner's name matches this player name, then we increment the wins counter for this player by 1
                wins[pname] += 1 # increment the wins counter for this player by 1
                total_profit[pname] += winner[0] - cost # if this player is the winner, we add the profit from this round to their total profit
            else:
                total_profit[pname] -= cost # if this player is not the winner, we subtract the cost of this round from their total profit

        history.append(auction.analysis()) # adds the analysis of this round to the history list
        if r < n_rounds: # if this is not the last round, we prompt the user to press enter to continue to the next round
            press_enter()

    separator("Final Scoreboard") # prints a separating line with the title "Final Scoreboard"
    print(f"  {'Player':<16} {'Wins':>5} {'Total Profit':>13}") # prints the header for the final scoreboard, with columns for Player, Wins, and Total Profit
    print("  " + "─" * 36) # prints a 36 character separator line under the header

    sorted_players = sorted(all_player_names, key=lambda x: wins[x], reverse=True)[:20] # sorts the player names based on the number of wins in descending order and takes the top 20 players for display on the scoreboard

    for i, pname in enumerate(sorted_players, 1): # loops through the sorted list of player names, with i as the index starting from 1 and pname as the player name
        is_you = " ← YOU" if pname == your_name else "" # adds an arrow and "YOU" next to the player's name if it matches the human player's name for easy identification on the scoreboard
        print(f"  {i}. {pname:<14} {wins[pname]:>5}  {total_profit[pname]:>13.2f}{is_you}") # prints the player's rank (i), name, number of wins, total profit to 2 decimal places, and the "YOU" marker if this player is the human player

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
 