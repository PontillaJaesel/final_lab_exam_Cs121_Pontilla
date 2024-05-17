from utils.user import User
from utils.dice_game import DiceRollGame
import time
import os

def main():
    keep_running = True
    while keep_running:
        os.system('cls' if os.name == 'nt' else 'clear')
        current_user = User("", "")
        print("Welcome to the Dice Roll Game!")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        user_choice = input("Select an option (1, 2, or 3): ")
        
        if user_choice == "1":
            current_user.register()
        elif user_choice == "2":
            if current_user.login():
                game_session = DiceRollGame(current_user.username)
                game_session.show_menu()
        elif user_choice == "3":
            print("Exiting the game...")
            time.sleep(0.5)
            print("Goodbye!")
            keep_running = False
        else:
            print("Invalid selection. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()
