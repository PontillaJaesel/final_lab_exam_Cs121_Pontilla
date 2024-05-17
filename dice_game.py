import os
import time 
import random
from utils.score import Score

class DiceRollGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.records_dir = "player_scores"
        self.records_file = os.path.join(self.records_dir, "leaderboard.txt")
        self.ensure_directory_exists()
        self.score = Score(self.player_name, "")

    def ensure_directory_exists(self):
        os.makedirs(self.records_dir, exist_ok = True)

    def retrieve_scores(self):
        score_list = []
        if os.path.exists(self.records_file):
            with open(self.records_file, "r") as file:
                for line in file:
                    user, points, stages, date = line.strip().split(",")
                    score_list.append((user, int(points), int(stages), date))
        return score_list
    
    def record_scores(self, score_list):
        with open(self.records_file, "w") as file:
            for record in score_list:
                file.write(f"{record[0]},{record[1]},{record[2]},{record[3]}\n")

    def ask_to_continue(self):
        while True:
            response = input("\nProceed to the next round? (1 for Yes, 0 for No): ")
            if response in ["1", "0"]:
                return response == "1"
            print("Invalid input. Please enter 1 for Yes or 0 for No.")
            input("Press Enter to continue...")

    def start_game(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Game starting for {self.player_name}...")

        cpu_points, player_points, rounds_won = 0, 0, 0

        while True:
            for _ in range(3):
                cpu_roll, player_roll = random.randint(1, 6), random.randint(1, 6)

                print(f"{self.player_name} rolled: {player_roll}")
                print(f"CPU rolled: {cpu_roll}")

                if player_roll > cpu_roll:
                    player_points += 1
                    print(f"You win this round, {self.player_name}!\n")
                elif cpu_roll > player_roll:
                    cpu_points += 1
                    print("CPU wins this round!\n")
                else:
                    print("It's a tie!\n")
                time.sleep(1)

            while cpu_points == player_points:
                cpu_roll, player_roll = random.randint(1, 6), random.randint(1, 6)

                print(f"{self.player_name} rolled: {player_roll}")
                print(f"CPU rolled: {cpu_roll}")

                if player_roll > cpu_roll:
                    player_points += 1
                    print(f"You win this tiebreaker, {self.player_name}!\n")
                elif cpu_roll > player_roll:
                    cpu_points += 1
                    print("CPU wins this tiebreaker!\n")
                else:
                    print("It's a tie!\n")
                time.sleep(1)

            if player_points > cpu_points:
                player_points += 3
                rounds_won += 1
                self.score.update_score(player_points, rounds_won)
                player_points, cpu_points = self.score.reset_score()
                print(f"\nYou won this round, {self.player_name}!\n")

                if not self.ask_to_continue():
                    leaderboard = self.retrieve_scores()
                    leaderboard.append(self.score.to_record())
                    leaderboard.sort(key=lambda x: x[1], reverse=True)
                    self.record_scores(leaderboard[:10])
                    self.score.reset_overall_score()
                    round_word = "round" if rounds_won == 1 else "rounds"
                    print(f"Game Over. You won {rounds_won} {round_word}.")
                    break
            else:
                if rounds_won == 0:
                    player_points, cpu_points = self.score.reset_score()
                    print(f"\nYou lost this round.\n")
                    print("Game Over. You didn't win any rounds.")
                    input("Press Enter to continue...")
                    break

                self.score.update_score(player_points, 0)
                player_points, cpu_points = self.score.reset_score()
                leaderboard = self.retrieve_scores()
                leaderboard.append(self.score.to_record())
                leaderboard.sort(key=lambda x: x[1], reverse=True)
                self.record_scores(leaderboard[:10])
                self.score.reset_overall_score()
                round_word = "round" if rounds_won == 1 else "rounds"
                print(f"Game Over. You won {rounds_won} {round_word}.")
                input("Press Enter to continue...")
                break

    def display_top_scores(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Top Scores:")
        scores = self.retrieve_scores()
        if not scores:
            print("No games played yet. Play a game to see top scores.")
        else:
            for idx, (user, points, stages, date) in enumerate(scores, start=1):
                print(f"{idx}. {user}: Points - {points}, Wins - {stages} (Achieved on: {date})")
        input("Press Enter to continue...")

    def logout(self):
        print(f"Goodbye, {self.player_name}")
        print("You have logged out successfully")
        time.sleep(1)
        return True
        
    def show_menu(self):
        os.system('cls')
        while True:
            print(f"Welcome, {self.player_name}")
            print("Menu:")
            print("1. Start Game\n2. Show Top Scores\n3. Log Out")
            user_choice = input("Enter the number of your choice: ")
            if user_choice == "1":
                self.start_game()
            elif user_choice == "2":
                self.display_top_scores()
            elif user_choice == "3":
                if self.logout():
                    break
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
