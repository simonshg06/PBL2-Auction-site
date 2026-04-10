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
        self._inorder(self.root, result)  # recursive function implementing the root and the list 
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.price, list(node.players))) #creates a list that murges the names of the players that have the same bid and their bid 
            self._inorder(node.right, result)

    def display(self):
        print("\n── Auction state ──")
        entries = self.inorder()
        if not entries: #if the tree is empty , then 
            print("  (no bids)")
            return
            
        for price, players in entries: # we go through all the bids in the list result 
            tag = " UNIQUE" if len(players) == 1 else "" # within the list players, so if the price has only one bid then it is tagges with UNIQUE 
            print(f"  Price {price:>4} | {len(players)} bid(s) | {players}{tag}") # writes the price and leaves four spaces and indents it to the right, then the name of the people for that proce and wether or not their bid is unique 
        print(f"  Total bids: {self.total_bids}") # total amount of bids 

    def find_lowest_unique(self):
        return self._find_lowest_unique(self.root) #recusrive function , finds the lowest unique bid, starts at root 
    
    def _find_lowest_unique(self, node):
        if node is None:
            return (None, None) # has reached the end of the tree 
        result = self._find_lowest_unique(node.left)
        if result[0] is not None:
            return result # if on the keft of the tree we find a bid that has only one player bidding that price, then it is sent straught away and the search stops 
        if len(node.players) == 1: # if on the left there is nothing, then they check each node and id the len of players is 1 then that bid is unique and wins 
            return (node.price, node.players[0])
        return self._find_lowest_unique(node.right)# if the node has multiple bidders then it continues to analyse the tree to the right until it has only one bidder for a certain price 


    def successor(self, price): # the following functions are meant to find the bid just below and juste above 
        node, succ = self.root, None # succ = none in case no giher price exists 
        while node:
            if price < node.price: # if we have that the price of the node is bigge rthan the price we give then it could perhaps be the successor thus we place it as successor for now 
                succ, node = node, node.left
            elif price > node.price: # price is bigger so we have to go right to find bigger 
                node = node.right
            else: # occurs when price =node.rice
                if node.right: # if the node.price has a right node then it is the successor 
                    succ = self._min_node(node.right)
                break # stops the while loop 
        return (succ.price, list(succ.players)) if succ else None #returns the succ and returns none if no sucessor was found 
    
    
    def predecessor(self, price):# same thing but inversed , tryng ti find the biggets value just below the price i give 
        node, pred = self.root, None
        while node:
            if price > node.price:
                pred, node = node, node.right
            elif price < node.price:
                node = node.left
            else:
                if node.left:
                    pred = self._max_node(node.left)
                break
        return (pred.price, list(pred.players)) if pred else None
    
    
    def _min_node(self, node): # lowest bid 
        while node.left:
            node = node.left
        return node
    
    def _max_node(self, node):# biggest bid 
        while node.right:
            node = node.right
        return node
    
    
    def delete_player_bid(self, price, player):
        self.root = self._delete_player(self.root, price, player)# if you delete the root of the tree then the root changes 
    
    def _delete_player(self, node, price, player): # we go across the tree searching for the correct bid and the correct bidder 
        if node is None:
            return None # if the price doesnt exist, return none 
        if price < node.price:
            node.left = self._delete_player(node.left, price, player)# if the price is smaller than the one of the node, keep going left, to try find the exact price 
        elif price > node.price:
            node.right = self._delete_player(node.right, price, player)#the price is bigger than the one of the node, we go right trying to find exact price
        else: # if price = node.price 
            if player in node.players:# checks to see if that player actually placed a bid
                node.players.remove(player)# removes said player from the list
                self.total_bids -= 1# updates the amount of total bids 
            if not node.players: # if there was only one bid at that price, then remove the node completely 
                node = self._remove_node(node)
        return node
    
    def _remove_node(self, node): #updtaes the tree once we remove a node
        if node.left is None:# if there is no node to the left then the new node is the one that was to the right 
            return node.right
        if node.right is None: # if there was no node to the right then the nez node is the left one 
            return node.left
        succ = self._min_node(node.right) # if the node has txo children the we say that the nodes sucessor is the one to teh right 
        node.price, node.players = succ.price, succ.players # instead of deleting the node, we just replace tits values 
        node.right = self._delete_node_by_price(node.right, succ.price)# delete the orignal sucessor node 
        return node
    
    def _delete_node_by_price(self, node, price):
        if node is None: # if we dont find the price in the tree return none 
            return None
        if price < node.price:
            node.left = self._delete_node_by_price(node.left, price)
        elif price > node.price:
            node.right = self._delete_node_by_price(node.right, price)
        else: # when you find price == node.price
            if node.left is None: # if the is not left node then the right one replaces the node we just deleted
                return node.right
            if node.right is None:# if no right node then the left one becomes the new node 
                return node.left
            succ = self._min_node(node.right) # the new successor to the node is now the right node 
            node.price, node.players = succ.price, succ.players # we dont delete the node we replace it with the values of the new successor 
            node.right = self._delete_node_by_price(node.right, succ.price) # delete the node that was the sucessor 
        return node


    def price_distribution(self):
        return {price: len(players) for price, players in self.inorder()} ### for each price we know how many people placed that bid, this allows us to analyse the bid strategies 
    def unique_prices(self):
        return [price for price, players in self.inorder() if len(players) == 1] #gives a list of all the prices that have 1 bid 
    def height(self):
        return self._height(self.root)# the larger the height the longer it will take to find the winning bid 
    def _height(self, node):
        return 0 if node is None else 1 + max(self._height(node.left), self._height(node.right)) # checks the length of the right side and the left side and the biggest one defnies the size 



