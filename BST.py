class BSTNode:     # here our BSTNode will act as a bag that contains all the bets of the same price 
    def __init__(self, price, player):
        self.price = price  #it places the prices in order, it tells the tree where to place the node(price), lower prices on the right, higher on the left)
        self.players = [player] #list of all the players that placed a bet of the same amount, if there is only one person in this list, they have the opportunity to win 
        self.left = self.right = None # on left is lower bids and on right is higher bids 
class BidBst:
    def __init__(self): #this is the top of the tree, when we try to find the winner, we start here and go left as much as we can 
        self.root = None # initialize hem at zero or none in this case and we will ad d them to the variable 
        self.total_bids = 0

    def insert(self, price, player): # if the bid doesnt exist yet, this function will create a new node for that bid 
        self.root = self._insert(self.root, price, player)
        self.total_bids += 1  # if the bid doesnt exist it updated the amount of different bids 
    
    def _insert(self, node, price, player):
        if node is None:
            return BSTNode(price, player)
        if price == node.price: # if the bid already exists then they will add that player to the list o fplayers that have already placed that same bid
            node.players.append(player)
        elif price < node.price:
            node.left = self._insert(node.left, price, player) #if the node (the bid) is cheaper then it goes left otherwise it goes right 
        else:
            node.right = self._insert(node.right, price, player)
        return node
    
    def inorder(self):# reading the tree in order, starts on the left with the lower values, then goes to the right to the bigger values 
        result = []
        self._inorder(self.root, result)  # 
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.price, list(node.players))) #creates a list that murges the names of the players that have the same bid and their bid 
            self._inorder(node.right, result)

    def display(self):
        print("\n── Auction state ──")
        entries = self.inorder()
        if not entries:
            print("  (no bids)")
            return
            
        for price, players in entries:
            tag = " ✓ UNIQUE" if len(players) == 1 else ""
            print(f"  Price {price:>4} | {len(players)} bid(s) | {players}{tag}")
        print(f"  Total bids: {self.total_bids}")

