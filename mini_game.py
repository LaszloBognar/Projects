import random

def number_guessing_game():
    secret_number = random.randint(1, 10)
    print("I am thinking of a number between 1 and 10.")

    guess = int(input("Take a guess: "))

    if guess == secret_number:
        print("Correct! You guessed it!")
    else:
        print(f"Nope! The number was {secret_number}. Try again!")
        
number_guessing_game() #Call function. Without this the code won't run as intended because I must call the function.  