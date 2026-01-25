import random
import time
import os
from game_log import log_game, show_leaderboard  # Logging functions for storing results
# -------------------
# Customer class
# -------------------
class Customer:
    def __init__(self, party_size=1, patience=3):
        # Each customer has a party size and patience level
        self.party_size = party_size
        self.patience = patience
        self.anger = 0       # Increases if patience runs out
        self.eat_time = party_size * 2  # Turns needed to finish eating
        self.symbol = self.generate_symbol ()

    def wait(self):
        #Decrease patience as time passes
        self.patience -= 1
        if self.patience <= 0:
            self.anger += 1  # Customer becomes angry if patience runs out

    def is_angry(self):
        #Return True if customer is angry and will leave.
        return self.anger > 2

    def eat_turn(self):
        #One turn of eating. Returns True if finished eating
        self.eat_time -= 1
        return self.eat_time <= 0

    def generate_symbol(self):
        #Randomly pick a symbol to represent this customer in the queue or at a table
        if self.party_size == 1:
            return random.choice(["👤","🗣"])
        elif self.party_size == 2:
            return random.choice(["👭", "👬", "👫"])
        elif self.party_size == 3:
            return "👤👥"
        elif self.party_size == 4:
            return "👭👬"

    def __repr__(self):
        #String representation of the customer for printing
        return f"{self.symbol}{'❤️'*self.patience}{'💢'*self.anger }"

# -------------------
# Table class
# -------------------
class Table:
    def __init__(self, capacity):
        self.capacity = capacity   # Maximum number of people at the table
        self.is_free = True        # Table starts free
        self.current_party = None  # No party seated initially

    def seat_party(self, customer):
        #Seat a customer if table is free and has enough capacity
        if self.is_free and customer.party_size <= self.capacity:
            self.is_free = False
            self.current_party = customer
            return True
        return False

    def serve(self):
        #Serve food to the current party. Returns earned money if finished
        if not self.is_free and self.current_party:
            finished = self.current_party.eat_turn()
            if finished:
                money = self.current_party.party_size * 5
                print(f"✅ Party of {self.current_party.party_size} finished, earned {money} 💰")
                self.clear_table()
                return money
        return 0

    def clear_table(self):
        #Free up the table after the party leaves
        self.is_free = True
        self.current_party = None

    def display(self):
        #Return a string representing table status for printing
        if self.is_free:
            return "🟩"*self.capacity
        else:
            eaten = self.current_party.party_size * 2 - self.current_party.eat_time
            total = self.current_party.party_size * 2
            return f"{'🟥'*self.capacity} {self.current_party.symbol} {eaten}/{total}"  # Red symbol + progress
    
# -------------------
# Queue class
# -------------------
class Queue:
    def __init__(self):
        self.customers = []  # List of waiting customers

    def add_customer(self, customer):
        #Add customer to the queue
        self.customers.append(customer)

    def remove_customer(self, customer):
        #Remove customer from the queue
        self.customers.remove(customer)

    def peek_next(self):
        #Return the next customer in the queue without removing them
        if self.customers:
            return self.customers[0]
        return None

    def display(self):
        #Return string representing all customers in the queue
        return " ".join(str(c) for c in self.customers)

# -------------------
# Restaurant class
# -------------------
class Restaurant:
    def __init__(self, player_name, total_time=20):
        self.money = 0
        self.time_left = total_time      # Game duration in turns
        self.queue = Queue()             # Queue of waiting customers
        self.tables = [Table(1), Table(2), Table(3), Table(4)]  # Tables of different sizes
        self.player_name = player_name

    def new_customer(self):
        #Randomly add a new customer with 70% chance each turn
        if random.random() < 0.7:
            party_size = random.randint(1, 4)
            customer = Customer(party_size=party_size, patience=3)
            self.queue.add_customer(customer)

    def seat_next_customer(self):
        #Manually seat the next customer in the queue if possible
        client = self.queue.peek_next()
        if not client:
            print("❌ No customers in queue")
            return
        #sort table by capacity before for choosing the optimal size
        for table in sorted(self.tables, key=lambda t: t.capacity):
            if table.seat_party(client):
                self.queue.remove_customer(client)
                print(f"🪑 Seated party of {client.party_size} at table ({table.capacity})")
                return
            
        print("❌ No free table available")

    def serve_table(self):
        #Serve all tables and add money if parties finish eating
        for table in self.tables:
            earned = table.serve()
            self.money += earned

    def wait_customers(self):
        #Decrease patience of all waiting customers and remove angry ones
        to_remove = []
        for c in self.queue.customers:
            c.wait()
            if c.is_angry():
                penalty = c.party_size * 2
                print(f"💢 Party of {c.party_size} left angrily! Lost {penalty} 💸")
                self.money -= penalty
                to_remove.append(c)
        for c in to_remove:
            self.queue.remove_customer(c)

    def update_time(self):
        #Decrease remaining time
        self.time_left -= 1

    def game_over(self):
        #Return True if the game time is over
        return self.time_left <= 0

    # -------------------
    # DRAW FUNCTION
    # -------------------
    def draw(self):
        #Clear screen and print current game state
        os.system("clear")  
        print(f"\n⏰ Time: {self.time_left}  💰 Money: {self.money}")
        print("Queue:", self.queue.display())
        print("Tables:", " ".join(table.display() for table in self.tables))
        print("\nMenu:")
        print("1️⃣ Seat next party")
        print("2️⃣ Serve food to tables")
        print("3️⃣ Wait")
        print("4️⃣ Save and exit")
        print("5️⃣ Exit without saving")
        

# -------------------
# GAME LOOP
# -------------------
os.system("clear") 
player_name = input("Enter your name: ")
game = Restaurant(player_name, total_time=50)
start_time = time.time()

while not game.game_over():
    game.new_customer()        # Add new customer randomly
    game.wait_customers()      # Update patience and remove angry customers
    game.draw()                # Redraw screen each turn

    choice = input("> ")       # Player chooses an action
    if choice == "1":
        game.seat_next_customer()
    elif choice == "2":
        game.serve_table()
    elif choice =="3":
        game.wait_customers()
    elif choice == "4":
            end_time = time.time()
            time_played = int(end_time - start_time) #seconds // 60  # minutes
            log_game(player_name, game.money, time_played) # insert to the log
            show_leaderboard() #show_leaderboard
            game.time_left=0

    elif choice == "5": # exit without saving
            game.time_left=0
    else:
        print("⏳ Waiting...")

    game.update_time()         # Reduce remaining game time
    time.sleep(0.5)            # Small delay for readability

# Game over
end_time = time.time()
time_played = int(end_time - start_time) #seconds     #minutes // 60

print(f"\n🏁 Game over! Money earned: {game.money}")
log_game(player_name, game.money, time_played)
show_leaderboard()
