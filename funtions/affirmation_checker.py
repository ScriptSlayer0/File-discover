def check_affirm(affirmation, context="") -> bool:
    """Check if the user's input is an affirmation."""
    affirmations = {"y", "yes"}
    if context == "force_search":
        print("Warning: Searching in other disks might be unsafe and could take a long time.")
        user_choice = input("Do you want to proceed with a full search in all disks? [y/n]: ")
        return user_choice.strip().lower() in affirmations
    return affirmation.strip().lower() in affirmations
