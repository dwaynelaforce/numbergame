from random import randint
import os, sys, time
import colorama

DEBUG = colorama.Fore.MAGENTA + "*** DEBUG ***"

class NumberGame():
    def __init__(self):
        self.gameover = False
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
        colorama.init(autoreset=True)
        
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
    
        print(DEBUG, self.range, self.number)

        self.player_guess()

    def get_user_input(self, prompt):
        user_input = input(prompt) if prompt else input("> ")
        user_input = user_input.casefold()
        if user_input in ("exit", "quit"):
            time.sleep(0.25)
            print("...goodbye...")
            time.sleep(1)
            sys.exit()
        return user_input

    def select_difficulty(self):
        valid = False
        while not valid:
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
                valid = True
                self.difficulty = difficulty
                print(f"\nDifficulty set to {self.difficulties[difficulty]['printed']}\n")
            else:
                print(colorama.Fore.RED + "\nInvalid input. Try again.\n")

    def player_guess(self):
        valid = False
        error_msg = (colorama.Fore.RED + "Invalid input.  Please enter a whole "
                    f"number /integer in range {self.range[0]} - {self.range[1]}.")
        while not valid:
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
            valid = True
        
        if not guess == self.number:
            if self.number < guess:
                print("Nope!  My number is", colorama.Fore.CYAN + "lower", "than", 
                      colorama.Fore.YELLOW + str(guess))
            elif self.number > guess:
                print("Nope!  My number is", colorama.Fore.CYAN + "higher", "than",
                colorama.Fore.YELLOW + str(guess))
            self.player_guess()
        else:
            # the game is over
            print("you win!")
            pass
        

if __name__ == "__main__":
    NumberGame().play()    

sys.exit()

def game():
    min, max = (1, 10)
    num = randint(min, max)
    gameover = False
    guess_count = 0
    
    print("Let's play a game.")
    print(f"I'm thinking of a whole number between {min} and {max}.")

    while not gameover:
        guess_is_valid = False
        while not guess_is_valid:
            print("Your guess:")
            guess = input()
            try:
                guess = int(guess)
                guess_is_valid = True
                guess_count += 1
            except:
                print("Please enter a whole number.")
        if guess == num:
            gameover = True
            print(f"Correct!  The number I was thinking of was {num}.  It took you {guess_count} guesses to get the right answer.")
            print("Care to play again? (y/n)")
            answer = None
            while not answer:
                answer = input().casefold()
                if answer == "y":
                    game()
                elif answer == "n":
                    print("Thanks for playing!  Goodbye.")
                else:
                    answer = None
                    print("Please enter 'y' or 'n'")
        elif guess < num:
            print("Go higher.")
        else:
            print("Go lower.")

if __name__ == "__main__":
    game()