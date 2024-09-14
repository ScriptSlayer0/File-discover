from funtions.affirmation_checker import check_affirm

def get_user_authorization(force_search):
    """Determine if the user is authorized to perform the search."""
    if force_search:
        return True
    return check_affirm("", context="force_search")