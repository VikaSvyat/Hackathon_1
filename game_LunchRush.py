import random
import os
import time

def clear():
    os.system("clear")  # macOS / Linux

def draw(queue, money, time_left):
    print("=" * 35)
    print("  SNOWY LUNCH RUSH 🍔")
    print("=" * 35)
    print(f"👥 Queue: {'🙂 ' * queue}")
    print(f"💰 Money: {money}")
    print(f"⏰ Time left: {time_left}")
    print("=" * 35)
    print("1️⃣ Serve client")
    print("2️⃣ Skip client")
    print("3️⃣ Do nothing")
    print("4 - save and exit")
    print("5 - exit without saving")
    print("=" * 35)

def game():
    queue = 0
    money = 0
    time_left = 20

    while time_left > 0:
        clear()

        # new client appears (70% chance)
        if random.random() < 0.7:
            queue += 1

        draw(queue, money, time_left)

        choice = input("Choose action (1/2/3): ")

        if choice == "1":
            if queue > 0:
                print("🍔 Serving client...")
                time.sleep(1)
                queue -= 1
                money += 5
            else:
                print("❌ No clients!")
                time.sleep(1)

        elif choice == "2":
            if queue > 0:
                print("😡 Client left!")
                time.sleep(1)
                queue -= 1
            else:
                print("❌ No clients!")
                time.sleep(1)

        elif choice == "3":
            print("⏳ Waiting...")
            time.sleep(1)

        elif choice == "4":
            print("place for saving")
            time_left = -1
        elif choice == "5": # exit without saving
            time_left = -1

        else:
            print("❌ Invalid choice")
            time.sleep(1)

        time_left -= 1

    clear()
    print("🏁 GAME OVER")
    print(f"💰 Total money earned: {money}")

game()
