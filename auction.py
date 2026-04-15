import csv
from BST import BidBst


def bid_cost(price, base_cost=1.0, alpha=10.0):  # cost increases as price decreases, formula given in the app doc
    return base_cost + alpha / (price + 1) # higher price = lower cost penalty


class AuctionRound:

    def __init__(self, base_cost=1.0, alpha=10.0):  
        self.base_cost, self.alpha = base_cost, alpha  # parameters for the cost function
        self.bst, self.bids, self.costs = BidBst(), [], {} # BST to store bids (imported), list to track order of bids, dict to track total cost per player
        self.winner, self.seller_revenue = None, 0.0 # initialize winner and seller revenue

    def place_bid(self, player, price):
        if not isinstance(price, int) or price < 0: raise ValueError("Invalid price") #isinstance imported, check price is a non-negative integer, raie valueRrror just displays an error message
        self.bst.insert(price, player) # ìnsert defined at BST, it finds where the price belongs in the tree
        self.bids.append((player, price)) # adds the player and their price to the list of bids
        cost = bid_cost(price, self.base_cost, self.alpha)     # calculate this bid's cost
        self.costs[player] = self.costs.get(player, 0) + cost # .get() adds to player to the dic rather than returning an error
        self.seller_revenue += cost # running total amount of money the seller has made

    def load_from_list(self, bid_list): #  load from a Python list
        for player, price in bid_list: #loops through each pair of player and price in the list of tuples (player, price)
            self.place_bid(player, price) #inserts each pair into the search tree

    def load_from_csv(self, filepath, round_number=None):
        with open(filepath, newline='') as f: # opens the CSV file for reading, newline='' is used to ensure that newlines are handled correctly across different platforms
            reader = csv.reader(f) # creates a CSV reader object that will iterate over lines in the given file
            next(reader)  # skip header, this is used to skip the first line of the CSV file
            for row in reader: # loops through each row in the CSV file
                if round_number is None: # if no round number is specified, we assume the old format and load all bids
                    player, price = row # in the old CSV format, there are only 2 columns: player and price, so we unpack the row into these two variables
                    self.place_bid(player.strip(), int(price)) # we use strip() to remove any leading or trailing whitespace from the player's name, and convert the price to an integer before placing the bid
                else:
                    manche, joueur, prix = row # in the new CSV format, there are 3 columns: manche (round), joueur (player), and prix (price)
                    if int(manche) == round_number: # we check if the manche (round) matches the specified round number
                        self.place_bid(joueur, int(prix)) # if it matches, we place the bid for that player and price

    def resolve(self): 
        res = self.bst.find_lowest_unique() # find lowest price with one bidder (defined in bst), returns a tuple of (price, player)
        self.winner = res if res[0] is not None else None #res[0] is the price
        return self.winner # returns the winning bid as a tuple of (price, player) or None if there is no winner

    def summary(self):
        print(f"\n{' SUMMARY ':═^30}") #\n creates a new line, ' SUMMARY ' is the text to be centered, and ═^30 means to center the text within a width of 30 characters, using the character '═' for padding on both sides.
        self.bst.display() # display() defined in BST, prints the prices using inorder traversal
        print(f"Revenue: {self.seller_revenue:.2f} | Bids: {self.bst.total_bids}") # the :.2f gives the revunue to 2 decimal places, .total bids gives the total number of bids placed defined in BST
        if self.winner: # if there is a winner
            price, player = self.winner # unpacks the tupple into 2 variables
            print(f" {player} won at {price} (Profit: {price - self.costs[player]:.2f})") # calculates the profit by subtracting the prize money by the amount they spent on bids (also to 2 decimal places)
        else: # if the winner is None
            print(" No winner") # self explanotory, this note is decoration


    def analysis(self):
        unique_players = len({player for player, _ in self.bids}) # the underscore ignores the price, a set doesnt allow duplicates so we get the number of unique players
        return {
            "total_bids": self.bst.total_bids, # total number of bids placed, defined in BST
            "revenue": round(self.seller_revenue, 2), # total revenue rounded to 2 decimal places
            "avg_cost": round(self.seller_revenue / unique_players, 2) if unique_players else 0, # average cost per unique player rounded to 2 decimal places
            "winner": self.winner, # winner defined as the winners tuple of (price, player) or None
    }
