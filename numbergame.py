# TODO
# implement leaderboard in some kind of permanent file in logs

from random import randint
import os, sys, time
import colorama

DEBUG = False

colorama.init(autoreset=True)

class NumberGame():
    def __init__(self):
        self.count_guesses = 0
        self.range = None
        self.number = None
        self.difficulty = None
        self.difficulties = {
            'easy' : {
                'multiplier' : 1,
                'range' : (1, 10),
                'printed' : colorama.Fore.GREEN + "Easy"
            },
            'medium' : {
                'multiplier' : 2,
                'range' : (1, 100),
                'printed' : colorama.Fore.YELLOW + "Medium"
            },
            'hard' : {
                'multiplier' : 3,
                'range' : (1, 500),
                'printed' : colorama.Fore.RED + "Hard"
            }
        }
    
    def play(self):
        
        print(colorama.Fore.CYAN + "\nLet's play a numbers game!\n")
        time.sleep(0.25)
        print('Enter "exit" or "quit" at any time end the game.\n')
        self.select_difficulty()
        self.range = self.difficulties[self.difficulty]['range']
        time.sleep(0.5)
        self.number = randint(*self.range)
        print("Alright... let's get started!\n")
        time.sleep(0.5)
        print(colorama.Fore.CYAN + "I'm thinking of a number", "between",
              colorama.Fore.YELLOW + str(self.range[0]), "and",
              colorama.Fore.YELLOW + str(self.range[1]), "(inclusive).\n")
    
        if DEBUG: print(colorama.Fore.MAGENTA + "*** DEBUG ***", "number is:", self.number)

        self.player_guess()

        print(colorama.Fore.GREEN + "You got it!", colorama.Fore.CYAN + str(self.number), "was my number.")
        time.sleep(0.25)
        score = (11 - self.count_guesses) * self.difficulties[self.difficulty]['multiplier'] * 100
        if score < 0: 
            score = 0
        print("Your score:", colorama.Fore.MAGENTA + str(score))
        time.sleep(0.25)
        
        self.process_leaderboard(score)
        
        valid = False
        while not valid:
            print("\n")
            play_again = self.get_user_input("Play again? y/n ")
            if not play_again in ['y','n']:
                print("Incorrect input.")
                continue
            valid = True
            if play_again == 'y':
                self.reset()
                self.play()
            else:
                print("Thanks for playing, goodbye!")

    def reset(self):
        self.count_guesses = 0
        self.range = None
        self.number = None
        self.difficulty = None

    def get_user_input(self, prompt="> "):
        user_input = input(prompt)
        user_input = user_input.casefold()
        if user_input in ("exit", "quit"):
            time.sleep(0.25)
            print("...goodbye...")
            time.sleep(1)
            sys.exit()
        return user_input

    def select_difficulty(self):
        while True:
            print("Game settings:")
            time.sleep(0.25)
            for key in self.difficulties:
                printed = self.difficulties[key]['printed']
                _range = f"{self.difficulties[key]['range'][0]} - {self.difficulties[key]['range'][1]}"
                print(f" * {printed}:", _range)
                time.sleep(0.1)
            print("")
            difficulty = self.get_user_input(prompt="Select a difficulty: ")
            time.sleep(0.25)
            if difficulty in self.difficulties.keys():
                self.difficulty = difficulty
                print(f"\nDifficulty set to {self.difficulties[difficulty]['printed']}\n")
                return
            else:
                print(colorama.Fore.RED + "\nInvalid input. Try again.\n")

    def player_guess(self):
        error_msg = (colorama.Fore.RED + "Invalid input.  Please enter a whole "
                    f"number / integer in range {self.range[0]} - {self.range[1]}.")
        while True:
            guess = self.get_user_input("Your guess: ")
            try:
                guess = int(guess)
            except:
                print(error_msg)
                continue
            if not self.range[0] <= guess <= self.range[1]:
                print(error_msg)
                continue
            self.count_guesses += 1
            break
        
        if not guess == self.number:
            if self.number < guess:
                print(colorama.Fore.RED + "Nope!", "My number is", 
                      colorama.Fore.CYAN + "lower", "than", colorama.Fore.YELLOW + str(guess))
            elif self.number > guess:
                print(colorama.Fore.RED + "Nope!", "My number is", 
                      colorama.Fore.CYAN + "higher", "than", colorama.Fore.YELLOW + str(guess))
            self.player_guess()

    def process_leaderboard(self, score):
        # print leaderboard
        current_leaders = []
        if os.path.exists("leaderboard.txt"):
            with open("leaderboard.txt", "r") as file:
                for line in file:
                    leader = line.split(",")
                    current_leaders.append((int(leader[0]), leader[1].replace("\n","")))
        current_leaders.sort()
        current_leaders.reverse()
        time.sleep(0.25)
        print("\n" ,colorama.Fore.MAGENTA + "* * * LEADERBOARD * * *")
        for leader in current_leaders:
            points, name = leader[0], leader[1]
            time.sleep(0.1)
            print(name.upper(), points)

        # evaluate whether or not the player's score qualifies for the leaderboard
        add_player_to_leaderboard = False
        if len(current_leaders) < 10:
            add_player_to_leaderboard = True
        else:
            for leader in current_leaders:
                leader_score = leader[0]
                if score > leader_score:
                    add_player_to_leaderboard = True
                    break

        if not add_player_to_leaderboard: return

        # offer player to record name on leaderboard
        while True:
            time.sleep(0.25)
            print("\n") 
            print(colorama.Fore.GREEN + "You made it into the top ten!")
            time.sleep(0.5)
            print("Enter your initials for the leaderboard? Max 3 characters. "
                    "Leave blank if you don't want to be on the leaderboard.")
            name = self.get_user_input()
            if not 0 <= len(name) <= 3:
                print(colorama.Fore.RED + "Invalid input.")
                continue
            break
        if not name: return

        # add player to leaderboard and overwrite file
        if len(name) < 3:
            name = name + (" " * (3-len(name))) #add whitespace in case name is too short
        current_leaders.append((score, name))
        current_leaders.sort()
        current_leaders.reverse()
        if len(current_leaders) > 10:
            current_leaders = current_leaders[:10]
        leaderboard_str = ""
        for leader in current_leaders:
            leader_score = leader[0]
            leader_name = leader[1]
            leaderboard_str += f"{str(leader_score)},{leader_name}\n"
        with open("leaderboard.txt", "w") as file:
            file.write(leaderboard_str)

        # print leaderboard again with player line highlighted
        print("\n" ,colorama.Fore.MAGENTA + "* * * LEADERBOARD * * *")
        for leader in current_leaders:
            points, leader_name = leader[0], leader[1]
            printline = ""
            if all([leader_name == name, points == score]):
                printline = colorama.Fore.CYAN
            printline += f"   {leader_name.upper()} {str(points)}"
            time.sleep(0.1)
            print(printline)

        

if __name__ == "__main__":
    NumberGame().play()