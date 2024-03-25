import tkinter as tk
from tkinter import simpledialog, messagebox, Label, Entry, Button, ttk
from markets import Market

class MarketApp:
    def __init__(self, master, market):
        self.master = master
        self.market = market
        self.entries = []  # To keep track of all entry widgets for bids and asks
        tk.Button(root, text="Create Order Form", command=self.create_order_form).grid(row = 0, column=0)
        tk.Button(root, text="Start Game", command=self.start_game).grid(row = 0, column=1)
        tk.Button(root, text="Submit Order Form", command=self.submit_orders).grid(row = 0, column=2)
        tk.Button(root, text="Take Bid", command=self.submit_bid_take).grid(row = 1, column=0)
        tk.Button(root, text="Take Ask", command=self.submit_ask_take).grid(row = 1, column=1)
        tk.Button(root, text="View Orderbook", command=self.view_orderbook).grid(row = 1, column=2)
        tk.Button(root, text="View Balance and Positions", command=self.view_balance_and_positions).grid(row = 1, column=3)
        tk.Button(root, text="Update Orderbook and Status", command=self.update_orderbook_and_status).grid(row = 1, column = 4)
        tk.Button(root, text="True Value", command=self.set_true_value).grid(row = 2, column=0)
        tk.Button(root, text="Settle", command=self.settle).grid(row = 3, column=0)
        tk.Button(root, text="Rank", command=self.rank_pnl).grid(row = 3, column = 1)
        tk.Button(root, text="Rank Point", command=self.rank_point).grid(row = 3, column = 2)

    def create_order_form(self):
        self.entries = []  # Clear the entries list
        for i in range(1, self.market.num_people + 1):
            Label(self.master, text=f"Player {i} Bid Price:").grid(row=i + 4, column=0)
            Label(self.master, text=f"Player {i} Bid Quantity:").grid(row=i + 4, column=2)
            Label(self.master, text=f"Player {i} Ask Price:").grid(row=i + 4, column=4)
            Label(self.master, text=f"Player {i} Ask Quantity:").grid(row=i + 4, column=6)
            
            # Bid Price
            bid_price_entry = Entry(self.master)
            bid_price_entry.grid(row=i + 4, column=1)
            # Bid Quantity
            bid_quantity_entry = Entry(self.master)
            bid_quantity_entry.grid(row=i + 4, column=3)
            # Ask Price
            ask_price_entry = Entry(self.master)
            ask_price_entry.grid(row=i + 4, column=5)
            # Ask Quantity
            ask_quantity_entry = Entry(self.master)
            ask_quantity_entry.grid(row=i + 4, column=7)
            
            self.entries.append((bid_price_entry, bid_quantity_entry, ask_price_entry, ask_quantity_entry))
        
        # Submit Button
        Button(self.master, text="Submit Orders", command=self.submit_orders).grid(row=self.market.num_people + 6, column=0, columnspan=4)
    
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
        self.update_orderbook_and_status()
        messagebox.showinfo("Info", "Bid taken!")


    def submit_ask_take(self):
        owner = simpledialog.askinteger("Input", "Owner ID:")
        quantity = simpledialog.askinteger("Input", "Quantity:")
        market.take_ask(owner, quantity)
        self.update_orderbook_and_status()
        messagebox.showinfo("Info", "Ask taken!")

    def view_positions(self):
        positions = "\n".join([f"Person {k}: {v}" for k, v in market.position.items()])
        messagebox.showinfo("Positions", positions)

    def view_balances(self):
        balances = "\n".join([f"Person {k}: {v}" for k, v in market.balance.items()])
        messagebox.showinfo("Balances", balances)
        
    def view_balance_and_positions(self):
        status_window = tk.Toplevel(self.master)
        status_window.title("Status")
        self.balance_position_tree = ttk.Treeview(status_window, columns=('Owner', 'Position', 'Balance'), show='headings')
        tree = self.balance_position_tree
        tree.heading('Owner', text='Owner')
        tree.heading('Position', text='Position')
        tree.heading('Balance', text='Balance')
        tree.pack(expand=True, fill='both')
        
        for key in market.position:
            tree.insert('', 'end', values=(key, market.position[key], market.balance[key]))
        
        
    def view_orderbook(self):
        # Create a new window to display the order book
        style = ttk.Style()

        style.configure("Treeview", font=("Helvetica", 20))
        style.configure("Treeview", rowheight = 30)
        orderbook_window = tk.Toplevel(self.master)
        orderbook_window.title("Orderbook")

        # Create a Treeview widget within the new window
        self.orderbook_tree = ttk.Treeview(orderbook_window, columns=('Owner', 'Price', 'Quantity'), show='headings')
        tree = self.orderbook_tree
        tree.heading('Owner', text='Owner')
        tree.heading('Price', text='Price')
        tree.heading('Quantity', text='Quantity')
        tree.pack(expand=True, fill='both')

        # Insert asks into the Treeview, in reverse order
        for ask in market.asks[::-1]:
            tree.insert('', 'end', values=(ask.owner, ask.price, ask.quantity), tags=('ask',))
        # Insert bids into the Treeview
        for bid in market.bids:
            tree.insert('', 'end', values=(bid.owner, bid.price, bid.quantity), tags=('bid',))
        

        # Optionally, configure the tags to style bids and asks differently
        tree.tag_configure('bid', background='lightgreen')
        tree.tag_configure('ask', background='lightcoral')

    def start_game(self):
        market.start_game()
        messagebox.showinfo("Info", "Game started!")
    
    def set_true_value(self):
        true_value = simpledialog.askfloat("Input", "True Value:")
        market.set_true_value(true_value)
        messagebox.showinfo("Info", "True value set!")
    
    def settle(self):
        market.settle()
        messagebox.showinfo("Info", "Settlement done!")
    
    def rank_pnl(self):
        market.rank()
        rank_window = tk.Toplevel(self.master)
        rank_window.title("Ranking")
        tree = ttk.Treeview(rank_window, columns=('Owner', 'Balance', 'Spread'), show='headings')
        tree.heading('Owner', text='Owner')
        tree.heading('Balance', text='Balance')
        tree.heading('Spread', text='Spread')
        tree.pack(expand=True, fill='both')
        for key in market.ranking:
            tree.insert('', 'end', values=(key, market.balance[key], market.orderbook_spreads[key]))

    def rank_point(self):
        market.rank_points()
        rank_point_window = tk.Toplevel(self.master)
        rank_point_window.title("Ranking")
        tree = ttk.Treeview(rank_point_window, columns=('Owner', 'Points'), show='headings')
        tree.heading('Owner', text='Owner')
        tree.heading('Points', text='Points')
        tree.pack(expand=True, fill='both')
        for key, value in enumerate(market.point_ranking):
            tree.insert('', 'end', values=(value, market.points[value]))

    def update_orderbook_and_status(self):
        for i in self.orderbook_tree.get_children():
            self.orderbook_tree.delete(i)
        for i in self.balance_position_tree.get_children():
            self.balance_position_tree.delete(i)
        for key in market.position:
            self.balance_position_tree.insert('', 'end', values=(key, market.position[key], market.balance[key]))
        # Insert asks into the Treeview, in reverse order
        for ask in market.asks[::-1]:
            self.orderbook_tree.insert('', 'end', values=(ask.owner, ask.price, ask.quantity), tags=('ask',))
        # Insert bids into the Treeview
        for bid in market.bids:
            self.orderbook_tree.insert('', 'end', values=(bid.owner, bid.price, bid.quantity), tags=('bid',))


# read true value from true_value.txt
with open("true_value_1.txt", "r") as f:
    true_value = float(f.read().strip())

market = Market(true_value=true_value, num_people=3)
root = tk.Tk()
app = MarketApp(root, market)
# market = Market(true_value=100, num_people=5)

# root = tk.Tk()
# root.title("Market Making Game")


root.mainloop()