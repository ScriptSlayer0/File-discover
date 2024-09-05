import os
import psutil
import time
from utils.screan_cleaner import cleaner

def find_home() -> str:
    """Return the home directory based on the operating system."""
    return os.path.expanduser("~")

def detect_disks() -> list:
    """Detect and return a list of disk partitions, excluding system partitions."""
    partitions = psutil.disk_partitions()
    print("Detected partitions:", partitions)
    return [partition.mountpoint for partition in partitions if not partition.mountpoint.startswith('/sys')]

# CWE-23 patch
def is_safe_path(basedir, path, follow_symlinks=True) -> bool:
    """Check if the path is within the base directory."""
    try:
        # Ensure the base directory is a canonical absolute path
        basedir = os.path.realpath(basedir)
        real_path = os.path.realpath(path) if follow_symlinks else os.path.abspath(path)
        
        # Check if the real path is within the base directory
        return os.path.commonpath([basedir]) == os.path.commonpath([basedir, real_path])
    except (ValueError, OSError) as e:
        # If the paths are on different drives or an error occurs, they are not safe
        print(f"Error checking path safety: {e}")
        return False

def check_affirm(affirmation) -> bool:
    """Check if the user's input is an affirmation."""
    affirmations = {"y", "yes"}
    return affirmation.strip().lower() in affirmations

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

def discover(extensions, force_search, show_time, scan_disks):
    """Search for files with the specified extensions in the home directory and optionally in other disks."""
    home_directory = find_home()
    user_authorized = False
    
    start_time = time.time()  # Start the timer
    
    if force_search:
        print("Warning: Searching in other disks might be unsafe and could take a long time.")
        user_choice = input("Do you want to proceed with a full search in all disks? [y/n]: ")
        user_authorized = check_affirm(user_choice)
    
    search_directory(home_directory, extensions, force_search, user_authorized)
    
    if scan_disks and user_authorized:
        for disk in detect_disks():
            if disk != home_directory:
                search_directory(disk, extensions, force_search, user_authorized)
    
    if show_time:
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time
        days, remainder = divmod(elapsed_time, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        time_parts = []
        if days > 0:
            time_parts.append(f"{int(days)} days")
        if hours > 0:
            time_parts.append(f"{int(hours)} hours")
        if minutes > 0:
            time_parts.append(f"{int(minutes)} minutes")
        time_parts.append(f"{seconds:.2f} seconds")
        
        print(f"Total time taken for scanning: {', '.join(time_parts)}")

def main():
    """Main function to run the file discovery program."""
    cleaner()
    print("Welcome to the File Discovery Tool!")
    user_extensions = input("Please enter the file extensions you want to search for, separated by commas (e.g., .exe, .pdf): ")
    
    if not user_extensions:
        print("No file extensions provided. Exiting...")
        return
    
    force_search = check_affirm(input("Would you like to force search in all directories, including potentially unsafe ones? [y/n]: "))
    
    extensions = set(extension.strip() for extension in user_extensions.split(',') if extension.strip())
    
    if not extensions:
        print("No valid file extensions provided. Exiting...")
        return
    
    discover(extensions, force_search, show_time=True, scan_disks=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interruption received, exiting...")
