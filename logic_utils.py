def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"  # Corrected message
    else:
        return "Too Low", "📈 Go HIGHER!"  # Corrected message


def parse_guess(guess_input):
    """
    Parse the user input into an integer guess.
    Returns a tuple (success, value, error_message).
    """
    try:
        guess = int(guess_input)
        return True, guess, None
    except ValueError:
        return False, None, "Invalid input. Please enter a number."

# FIXME: Incorrect hint messages
# FIX: Refactored hint logic into logic_utils.py using Copilot Agent mode
