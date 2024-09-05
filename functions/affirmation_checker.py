def check_affirm(affirmation) -> bool:
    """Check if the user's input is an affirmation."""
    affirmations = {"y", "yes"}
    return affirmation.strip().lower() in affirmations