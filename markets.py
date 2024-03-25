class Bid:
    def __init__(self, owner, price, quantity):
        self.owner = owner
        self.price = price
        self.quantity = quantity

class Ask:
    def __init__(self, owner, price, quantity):
        self.owner = owner
        self.price = price
        self.quantity = quantity

class Market:
    def __init__(self, true_value = 0, num_people = 12):
        self.true_value = true_value
        self.num_people = num_people
        ## position is a dict to represent each person's position
        self.position = {}
        ## balance is a dict to represent each person's balance
        self.balance = {}
        ## Point system to rank people
        self.points = {}
        ## Initialize all entries with 0. Person are denoted as 1, 2, 3 ...
        for i in range(1, num_people + 1):
            self.position[i] = 0
            self.balance[i] = 0
            self.points[i] = 0
        self.bids = [] # List of Bid objects
        self.asks = [] # List of Ask objects
        self.bid_dict = {}
        self.ask_dict = {}
        self.orderbook_spreads = {}
    
    def set_true_value(self, true_value):
        self.true_value = true_value
    
    def set_num_people(self, num_people):
        self.num_people = num_people
        self.position = {}
        self.balance = {}
        for i in range(1, num_people + 1):
            self.position[i] = 0
            self.balance[i] = 0
    
    def add_bid(self, owner, price, quantity):
        if owner in self.bid_dict:
            return
        self.bid_dict[owner] = (price, quantity)
        self.bids.append(Bid(owner, price, quantity))
    
    def add_ask(self, owner, price, quantity):
        if owner in self.ask_dict:
            return
        self.ask_dict[owner] = (price, quantity)
        self.asks.append(Ask(owner, price, quantity))
    
    def sort_bids(self):
        # Sort by price in descending order, with ties broken by larger qty\
        self.bids.sort(key=lambda x: (-x.price, -x.quantity))
        
    def sort_asks(self):
        # Sort by price in ascending order, with ties broken by larger qty
        self.asks.sort(key=lambda x: (x.price, -x.quantity))
    
    def clear_overlapping_orders(self):
        ## Function to clear overlapping orders
        ## by matching bids and asks and adding
        ## the resulting transactions to the position
        ## dictionary, using mid-price as the transaction
        flag = False
        for bid in self.bids:
            for ask in self.asks:
                if bid.price >= ask.price: # If there is a match
                    flag = True
                    if bid.quantity > ask.quantity:
                        settle_qty = ask.quantity
                        bid.quantity -= settle_qty
                        self.asks.remove(ask)
                    else:
                        settle_qty = bid.quantity
                        ask.quantity -= settle_qty
                        self.bids.remove(bid)
                    self.position[bid.owner] = self.position.get(bid.owner, 0) + settle_qty
                    self.position[ask.owner] = self.position.get(ask.owner, 0) - settle_qty
                    self.balance[bid.owner] = self.balance.get(bid.owner, 0) - settle_qty * (bid.price + ask.price) / 2
                    self.balance[ask.owner] = self.balance.get(ask.owner, 0) + settle_qty * (bid.price + ask.price) / 2
                    break
        if flag:
            self.clear_overlapping_orders()
        else:
            self.bids = [bid for bid in self.bids if bid.quantity > 0]
            self.asks = [ask for ask in self.asks if ask.quantity > 0]
            return
        
    def take_bid(self, taker, quantity): # Taker sells quantity
        ## Function to take a bid
        bid_idx = 0
        while quantity > 0 and bid_idx < len(self.bids):
            curr_bid = self.bids[bid_idx]
            if curr_bid.quantity <= quantity: # Priority bid has less quantity than taker
                exec_qty = curr_bid.quantity
                bid_idx += 1
            else:
                exec_qty = quantity
            quantity -= exec_qty
            curr_bid.quantity -= exec_qty
            self.position[taker] -= exec_qty
            self.position[curr_bid.owner] += exec_qty
            self.balance[taker] += exec_qty * curr_bid.price
            self.balance[curr_bid.owner] -= exec_qty * curr_bid.price
        self.bids = [bid for bid in self.bids if bid.quantity > 0]
        self.sort_bids()
        
    def take_ask(self, taker, quantity):
        ## Function to take an ask
        ask_idx = 0
        while quantity > 0 and ask_idx < len(self.asks):
            curr_ask = self.asks[ask_idx]
            if curr_ask.quantity <= quantity:
                exec_qty = curr_ask.quantity
                ask_idx += 1
            else:
                exec_qty = quantity
            quantity -= exec_qty
            curr_ask.quantity -= exec_qty
            self.position[taker] += exec_qty
            self.position[curr_ask.owner] -= exec_qty
            self.balance[taker] -= exec_qty * curr_ask.price
            self.balance[curr_ask.owner] += exec_qty * curr_ask.price
        self.asks = [ask for ask in self.asks if ask.quantity > 0]
        self.sort_asks()

    def print_position(self):
        print("Position:")
        for key in self.position:
            print("Person", key, ":", self.position[key])
    
    def print_balance(self):
        print("Balance:")
        for key in self.balance:
            print("Person", key, ":", self.balance[key])
            
    def view_orderbook(self):
        print("Bids:")
        for bid in self.bids:
            print(bid.owner, bid.price, bid.quantity)
        print("Asks:")
        for ask in self.asks:
            print(ask.owner, ask.price, ask.quantity)
    
    def start_game(self):
        self.sort_bids()
        self.sort_asks()
        self.orderbook_spreads = {}
        # Calculate difference between bid and ask for each person
        for key in self.position:
            self.orderbook_spreads[key] = self.ask_dict.get(key, 99999999)[0] - self.bid_dict.get(key, 0)[0]
        # Give points to people with the smallest spreads
        # Person with smallest spread gets 3, second smallest gets 2, third smallest gets 1
        spread_list: tuple[int, float] = sorted(self.orderbook_spreads.items(), key=lambda x: x[1])
        for i in range(3):
            self.points[spread_list[i][0]] = 3 - i
        self.clear_overlapping_orders()
        self.print_position()
        self.print_balance()
        self.view_orderbook()
    
    def rank(self):
        # Rank people by balance, tie broken by smaller orderbook spreads
        self.ranking = sorted(self.balance, key=lambda x: (self.balance[x], self.orderbook_spreads[x]))
        # First 4 gets 20, 19, 18, 17 points, next 4 gets 15, 13, 11, 9 points
        # Next 4 gets 6, 3, 0, -3 points, last 4 gets -7, -11, -15, -19 points
        increment = 1
        point = 20
        for i, person in enumerate(self.ranking):
            self.points[person] += point
            if i % 4 == 3:
                increment += 1
            point -= increment
    def settle(self):
        # Convert position to balance, using true value.
        for key in self.position:
            self.balance[key] += self.position[key] * self.true_value
            self.position[key] = 0