from random import randint

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