import random

def guess_the_number():
    secret_number = random.randint(1, 10)
    guess = None

    while guess != secret_number:
        guess = int(input("Guess the secret number: "))
        if guess != secret_number:
            print("Wrong number. Try again.")
        else:
            print("You are right! You guessed the secret number!")

guess_the_number()