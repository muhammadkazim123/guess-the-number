from flask import Flask, render_template, request, redirect, url_for, session

from main import (
    generate_secret_number,
    check_guess,
    MAX_ATTEMPTS,
    MIN_NUMBER,
    MAX_NUMBER
)

app = Flask(__name__)

import os

app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")


def start_new_round():
    """Start a fresh game."""

    session["secret_number"] = generate_secret_number()
    session["attempts_left"] = MAX_ATTEMPTS
    session["guesses_used"] = 0
    session["status"] = "playing"
    session["message"] = "SYSTEM READY. ENTER YOUR FIRST GUESS."
    session["message_type"] = "neutral"


@app.route("/", methods=["GET", "POST"])
def home():

    if "secret_number" not in session:
        start_new_round()

    if request.method == "POST":

        action = request.form.get("action", "guess")

        if action == "restart":
            start_new_round()

        elif session["status"] != "playing":
            session["message"] = "ROUND COMPLETE. START A NEW ROUND."
            session["message_type"] = "warning"

        else:
            raw_guess = request.form.get("guess", "").strip()

            try:
                guess = int(raw_guess)

                if not MIN_NUMBER <= guess <= MAX_NUMBER:
                    raise ValueError

                session["guesses_used"] += 1

                result = check_guess(
                    guess,
                    session["secret_number"]
                )

                if result == "correct":

                    session["status"] = "won"
                    session["message"] = "JACKPOT! YOU FOUND THE NUMBER."
                    session["message_type"] = "good"

                else:

                    session["attempts_left"] -= 1

                    if session["attempts_left"] == 0:

                        session["status"] = "lost"
                        session["message"] = (
                            "GAME OVER. THE NUMBER WAS "
                            + str(session["secret_number"])
                        )
                        session["message_type"] = "bad"

                    elif result == "low":

                        session["message"] = "TOO LOW. AIM HIGHER."
                        session["message_type"] = "neutral"

                    else:

                        session["message"] = "TOO HIGH. AIM LOWER."
                        session["message_type"] = "neutral"

            except ValueError:

                session["message"] = "INVALID INPUT. ENTER 1 TO 100."
                session["message_type"] = "bad"

        # Return the browser directly to the game panel
        return redirect(url_for("home") + "#game")

    display_number = (
        session["secret_number"]
        if session["status"] != "playing"
        else "??"
    )

    return render_template(
        "index.html",
        status=session["status"],
        attempts_left=session["attempts_left"],
        guesses_used=session["guesses_used"],
        max_attempts=MAX_ATTEMPTS,
        display_number=display_number,
        message=session["message"],
        message_type=session["message_type"]
    )


if __name__ == "__main__":
   app.run(debug=False)