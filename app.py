import random
import streamlit as st
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from logic_utils import check_guess, parse_guess  # Import refactored functions

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def update_score(current_score: int, outcome: str, attempt_number: int):
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

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1  # FIXME: Ensure attempts and score start at 0

if "score" not in st.session_state:
    st.session_state.score = 0  # FIXME: Ensure attempts and score start at 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0  # Reset score
    st.session_state.status = "playing"  # Reset game status
    st.session_state.secret = random.randint(1, 100)
    st.success("New game started.")
    st.rerun()  # Reload the app to reset the state

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    # Parse the guess input
    success, guess_int, error_message = parse_guess(raw_guess)
    if not success:
        st.error(error_message)
        st.stop()

    # Ensure secret remains an integer
    secret = st.session_state.secret

    # Use refactored check_guess
    outcome, message = check_guess(guess_int, secret)

    st.session_state.score = update_score(
        current_score=st.session_state.score,
        outcome=outcome,
        attempt_number=st.session_state.attempts,
    )

    if outcome == "Win":
        st.balloons()
        st.session_state.status = "won"
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    else:
        if st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
        elif outcome in ["Too High", "Too Low"] and show_hint:
            st.warning(message)  # Show hint message if the checkbox is checked

# FIXME: Logic breaks here for incorrect hint messages
# FIX: Refactored hint logic into logic_utils.py using Copilot Agent mode

# FIXME: Score mismatch issue
# FIX: Updated score calculation logic to ensure consistency

# FIXME: Submit Guess button not working after New Game
# FIX: Reset session state variables properly when starting a new game

# FIXME: Attempts and score not counted properly
# FIX: Ensured session state updates correctly after each guess

# FIXME: Score/Attempts not starting at 0
# FIX: Initialized session state variables to start at 0

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
