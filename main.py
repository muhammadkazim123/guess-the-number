
import random

MIN_NUMBER = 1
MAX_NUMBER = 100
MAX_ATTEMPTS = 5


def generate_secret_number():
    return random.randint(MIN_NUMBER, MAX_NUMBER)


def check_guess(guess, secret_number):
    if guess < secret_number:
        return "low"
    elif guess > secret_number:
        return "high"
    return "correct"


def is_prime(number):
    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def generate_riddle(number):
    special_riddles = {
        28: [
            ("range", {"min": 20, "max": 30},
             "I am between 20 and 30, inclusive."),
            ("divisible", {"divisor": 7},
             "I am divisible by 7."),
            ("greater_than", {"value": 25},
             "I am greater than 25.")
        ],

        45: [
            ("two_digit", {},
             "I am a two-digit number."),
            ("digit_sum", {"value": 9},
             "My digits add up to 9."),
            ("divisible", {"divisor": 5},
             "I am divisible by 5."),
            ("less_than", {"value": 50},
             "I am less than 50.")
        ],

        47: [
            ("prime", {},
             "I am a prime number."),
            ("range", {"min": 40, "max": 50},
             "I am between 40 and 50, inclusive."),
            ("greater_than", {"value": 45},
             "I am greater than 45.")
        ],

        13: [
            ("square_equals", {"value": 169},
             "My square is 169.")
        ],

        6: [
            ("even", {},
             "I am an even number."),
            ("cube_equals", {"value": 216},
             "My cube is 216.")
        ]
    }

    if number in special_riddles:
        clues = special_riddles[number]

    else:
        lower = ((number - 1) // 10) * 10 + 1
        upper = min(lower + 9, 100)

        parity = "even" if number % 2 == 0 else "odd"
        remainder = number % 7
        digit_sum = sum(int(digit) for digit in str(number))

        range_texts = [
            f"I am greater than {lower - 1} and less than {upper + 1}.",
            f"My value lies between {lower} and {upper}, inclusive.",
            f"You can find me in the number range {lower} to {upper}.",
            f"I am at least {lower} and no greater than {upper}."
        ]

        parity_texts = {
            "even": [
                "I am an even number.",
                "I can be divided by 2 without a remainder."
            ],
            "odd": [
                "I am an odd number.",
                "I cannot be divided by 2 without a remainder."
            ]
        }

        clues = [
            (
                "range",
                {"min": lower, "max": upper},
                range_texts[number % len(range_texts)]
            ),
            (
                parity,
                {},
                parity_texts[parity][number % 2]
            ),
            (
                "modulo",
                {"divisor": 7, "remainder": remainder},
                f"When divided by 7, my remainder is {remainder}."
            ),
            (
                "digit_sum",
                {"value": digit_sum},
                f"The sum of my digits is {digit_sum}."
            )
        ]

    return {
        "clues": [
            {
                "type": clue_type,
                "data": data,
                "text": description
            }
            for clue_type, data, description in clues
        ]
    }


def check_riddle_guess(guess, clues):
    results = []

    for clue in clues:
        clue_type = clue["type"]
        data = clue["data"]

        matches = False
        hint = ""

        if clue_type == "range":
            matches = data["min"] <= guess <= data["max"]

            if guess < data["min"]:
                hint = "Your guess is below the required range."
            elif guess > data["max"]:
                hint = "Your guess is above the required range."
            else:
                hint = "Your guess fits the required range."

        elif clue_type == "divisible":
            divisor = data["divisor"]
            matches = guess % divisor == 0

            hint = (
                f"Your guess is divisible by {divisor}."
                if matches
                else f"Your guess is not divisible by {divisor}."
            )

        elif clue_type == "greater_than":
            matches = guess > data["value"]

            hint = (
                "Your guess is greater than the required value."
                if matches
                else "Your guess needs to be greater."
            )

        elif clue_type == "less_than":
            matches = guess < data["value"]

            hint = (
                "Your guess is below the required limit."
                if matches
                else "Your guess needs to be smaller."
            )

        elif clue_type == "two_digit":
            matches = 10 <= guess <= 99

            hint = (
                "Your guess has two digits."
                if matches
                else "Think of a two-digit number."
            )

        elif clue_type == "digit_sum":
            actual_sum = sum(int(digit) for digit in str(guess))
            matches = actual_sum == data["value"]

            hint = (
                "Your digit sum is correct."
                if matches
                else f"Your digits add up to {actual_sum}, not {data['value']}."
            )

        elif clue_type == "prime":
            matches = is_prime(guess)

            hint = (
                "Your guess is a prime number."
                if matches
                else "Your guess is not a prime number."
            )

        elif clue_type == "square_equals":
            matches = guess ** 2 == data["value"]

            hint = (
                "Your guess has the correct square."
                if matches
                else f"The square of your guess is {guess ** 2}."
            )

        elif clue_type == "cube_equals":
            matches = guess ** 3 == data["value"]

            hint = (
                "Your guess has the correct cube."
                if matches
                else f"The cube of your guess is {guess ** 3}."
            )

        elif clue_type == "even":
            matches = guess % 2 == 0

            hint = (
                "Your guess is even."
                if matches
                else "Try an even number."
            )

        elif clue_type == "odd":
            matches = guess % 2 != 0

            hint = (
                "Your guess is odd."
                if matches
                else "Try an odd number."
            )

        elif clue_type == "modulo":
            divisor = data["divisor"]
            actual_remainder = guess % divisor

            matches = actual_remainder == data["remainder"]

            hint = (
                f"Your remainder is {actual_remainder}, which matches."
                if matches
                else (
                    f"Your remainder is {actual_remainder}. "
                    "Think about the required remainder."
                )
            )

        results.append({
            "text": clue["text"],
            "matches": matches,
            "hint": hint
        })

    return results


# Compatibility functions used by app.py

def build_riddle(number):
    return generate_riddle(number)["clues"]


def analyse_riddle_guess(guess, riddle):
    results = check_riddle_guess(guess, riddle)

    feedback = [
        {
            "text": item["text"],
            "matched": item["matches"],
            "message": item["hint"]
        }
        for item in results
    ]

    matched = sum(item["matched"] for item in feedback)
    total = len(feedback)

    return matched, total, feedback
