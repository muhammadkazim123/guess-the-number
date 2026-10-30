import random

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 7


def generate_secret_number():
    return random.randint(MIN_NUMBER, MAX_NUMBER)


def check_guess(guess, secret_number):
    if guess < secret_number:
        return "low"
    elif guess > secret_number:
        return "high"
    else:
        return "correct"