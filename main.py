import tkinter as tk
from tkinter import simpledialog, messagebox, Label, Entry, Button
from markets import Market

class MarketApp:
    def __init__(self, master, market):
        self.master = master
        self.market = market
        self.entries = []  # To keep track of all entry widgets for bids and asks
        tk.Button(root, text="View Positions", command=self.view_positions).grid(row = 0, column=0)
        tk.Button(root, text="View Balances", command=self.view_balances).grid(row = 0, column=1)
        tk.Button(root, text="Take Bid", command=self.submit_bid_take).grid(row = 0, column=2)
        tk.Button(root, text="Take Ask", command=self.submit_ask_take).grid(row = 0, column=3)
        tk.Button(root, text="Start Game", command=self.start_game).grid(row = 0, column=4)
        tk.Button(root, text="Create Order Form", command=self.create_order_form).grid(row = 0, column=5)
        tk.Button(root, text="Submit Order Form", command=self.submit_orders).grid(row = 0, column=6)
        tk.Button(root, text="View Orderbook", command=self.view_orderbook).grid(row = 0, column=7)
    def create_order_form(self):
        self.entries = []  # Clear the entries list
        for i in range(1, self.market.num_people + 1):
            Label(self.master, text=f"Player {i} Bid Price:").grid(row=i, column=0)
            Label(self.master, text=f"Player {i} Bid Quantity:").grid(row=i, column=2)
            Label(self.master, text=f"Player {i} Ask Price:").grid(row=i, column=4)
            Label(self.master, text=f"Player {i} Ask Quantity:").grid(row=i, column=6)
            
            # Bid Price
            bid_price_entry = Entry(self.master)
            bid_price_entry.grid(row=i, column=1)
            # Bid Quantity
            bid_quantity_entry = Entry(self.master)
            bid_quantity_entry.grid(row=i, column=3)
            # Ask Price
            ask_price_entry = Entry(self.master)
            ask_price_entry.grid(row=i, column=5)
            # Ask Quantity
            ask_quantity_entry = Entry(self.master)
            ask_quantity_entry.grid(row=i, column=7)
            
            self.entries.append((bid_price_entry, bid_quantity_entry, ask_price_entry, ask_quantity_entry))
        
        # Submit Button
        Button(self.master, text="Submit Orders", command=self.submit_orders).grid(row=self.market.num_people + 2, column=0, columnspan=4)
    
    def submit_orders(self):
        for i, (bid_price, bid_quantity, ask_price, ask_quantity) in enumerate(self.entries, start=1):
            try:
                bid_price_val = float(bid_price.get())
                bid_quantity_val = int(bid_quantity.get())
                ask_price_val = float(ask_price.get())
                ask_quantity_val = int(ask_quantity.get())
                
                if bid_price_val and bid_quantity_val:
                    self.market.add_bid(i, bid_price_val, bid_quantity_val)
                if ask_price_val and ask_quantity_val:
                    self.market.add_ask(i, ask_price_val, ask_quantity_val)
            except ValueError:
                messagebox.showwarning("Warning", "Invalid input. Please enter numeric values.")
                return
        
        messagebox.showinfo("Success", "Orders submitted successfully.")
        for entry in self.entries:  # Clear the fields after submission
            for field in entry:
                field.delete(0, tk.END)

    def submit_bid(self):
        owner = simpledialog.askinteger("Input", "Owner ID:")
        price = simpledialog.askfloat("Input", "Price:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        market.add_bid(owner, price, quantity)
        messagebox.showinfo("Info", "Bid submitted!")

    def submit_ask(self):
        owner = simpledialog.askinteger("Input", "Owner ID:")
        price = simpledialog.askfloat("Input", "Price:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        market.add_ask(owner, price, quantity)
        messagebox.showinfo("Info", "Ask submitted!")
        
    def submit_bid_take(self):
        owner = simpledialog.askinteger("Input", "Owner ID:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        market.take_bid(owner, quantity)
        messagebox.showinfo("Info", "Bid taken!")


    def submit_ask_take(self):
        owner = simpledialog.askinteger("Input", "Owner ID:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        market.take_ask(owner, quantity)
        messagebox.showinfo("Info", "Ask taken!")

    def view_positions(self):
        positions = "\n".join([f"Person {k}: {v}" for k, v in market.position.items()])
        messagebox.showinfo("Positions", positions)

    def view_balances(self):
        balances = "\n".join([f"Person {k}: {v}" for k, v in market.balance.items()])
        messagebox.showinfo("Balances", balances)
        
    def view_orderbook(self):
        orderbook = "Bids:\n" + "\n".join([f"{bid.owner} {bid.price} {bid.quantity}" for bid in market.bids]) + "\nAsks:\n" + "\n".join([f"{ask.owner} {ask.price} {ask.quantity}" for ask in market.asks])
        messagebox.showinfo("Orderbook", orderbook)

    def start_game(self):
        market.start_game()
        messagebox.showinfo("Info", "Game started!")
    
    def settle(self):
        market.settle()
        messagebox.showinfo("Info", "Settlement done!")

# read true value from true_value.txt
with open("true_value.txt", "r") as f:
    true_value = float(f.read().strip())

market = Market(true_value=true_value, num_people=11)
root = tk.Tk()
app = MarketApp(root, market)
# market = Market(true_value=100, num_people=5)

# root = tk.Tk()
# root.title("Market Making Game")


root.mainloop()