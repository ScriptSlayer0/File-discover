import os
import platform

def cleaner():
    """Clear the screen based on the operating system."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
