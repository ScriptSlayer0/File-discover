import os
from funtions.is_save_path import is_safe_path

def find_home() -> str:
    """Return the home directory based on the operating system."""
    return os.path.expanduser("~")

def search_directory(directory, extensions, force_search=False, user_authorized=False):
    """Search for files with the specified extensions in the directory."""
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist or is not a valid directory!")
        return
    
    home_directory = find_home()
    
    if not is_safe_path(home_directory, directory) and not force_search and not user_authorized:
        print(f"Some paths of {directory} are outside of {home_directory} folder and might be unsafe!")
        return
    
    try:
        with os.scandir(directory) as it:
            for entry in it:
                try:
                    if entry.is_file() and os.path.splitext(entry.name)[1] in extensions and is_safe_path(directory, entry.path):
                        print(entry.path)
                    elif entry.is_dir():
                        search_directory(entry.path, extensions, force_search, user_authorized)
                except PermissionError:
                    print(f"Permission denied: {entry.path}")
    except PermissionError:
        print(f"Permission denied: {directory}")
    except Exception as e:
        print(f"An error occurred: {e}")
