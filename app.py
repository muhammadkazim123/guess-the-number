
import os

from flask import Flask, render_template, request, redirect, url_for, session

from main import (
    MIN_NUMBER,
    MAX_NUMBER,
    MAX_ATTEMPTS,
    generate_secret_number,
    build_riddle,
    analyse_riddle_guess,
    check_guess,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")


def start_new_round():
    secret_number = generate_secret_number()

    session["secret_number"] = secret_number
    session["riddle"] = build_riddle(secret_number)
    session["attempts_left"] = MAX_ATTEMPTS
    session["guesses_used"] = 0
    session["status"] = "playing"
    session["message"] = "SYSTEM READY. STUDY THE CLUES AND FIND THE NUMBER."
    session["message_type"] = "neutral"
    session["clue_feedback"] = []
    session["last_guess"] = None


@app.route("/", methods=["GET", "POST"])
def home():

    if "secret_number" not in session or "riddle" not in session:
        start_new_round()

    anchor = "game"

    if request.method == "POST":

        action = request.form.get("action", "guess")

        if action == "restart":
            start_new_round()
            anchor = "game"

        elif session["status"] != "playing":
            session["message"] = "ROUND COMPLETE. START A NEW ROUND."
            session["message_type"] = "warning"

        else:
            anchor = "guess-form"

            raw_guess = request.form.get("guess", "").strip()

            try:
                guess = int(raw_guess)

                if not MIN_NUMBER <= guess <= MAX_NUMBER:
                    raise ValueError

                session["guesses_used"] += 1
                session["last_guess"] = guess

                matched, total, feedback = analyse_riddle_guess(
                    guess,
                    session["riddle"]
                )

                session["clue_feedback"] = feedback

                result = check_guess(
                    guess,
                    session["secret_number"]
                )

                if result == "correct":

                    session["status"] = "won"

                    session["message"] = (
                        f"JACKPOT! YOU FOUND {guess}. "
                        f"YOU MATCHED ALL {total} CLUES."
                    )

                    session["message_type"] = "good"

                else:

                    session["attempts_left"] -= 1

                    clue_summary = (
                        f"Your guess matches {matched} of {total} clues."
                    )

                    if session["attempts_left"] == 0:

                        session["status"] = "lost"

                        session["message"] = (
                            f"GAME OVER. THE NUMBER WAS "
                            f"{session['secret_number']}. {clue_summary}"
                        )

                        session["message_type"] = "bad"

                    elif result == "low":

                        session["message"] = (
                            f"TOO LOW. AIM HIGHER. {clue_summary}"
                        )

                        session["message_type"] = "neutral"

                    else:

                        session["message"] = (
                            f"TOO HIGH. AIM LOWER. {clue_summary}"
                        )

                        session["message_type"] = "neutral"

            except ValueError:

                session["message"] = (
                    "INVALID INPUT. ENTER A WHOLE NUMBER FROM 1 TO 100."
                )

                session["message_type"] = "bad"

        return redirect(url_for("home") + f"#{anchor}")

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
        message_type=session["message_type"],
        riddle=session["riddle"],
        clue_feedback=session.get("clue_feedback", []),
        last_guess=session.get("last_guess"),
    )


if __name__ == "__main__":
    app.run(debug=False)
