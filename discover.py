import os, platform, psutil

def screen_cleaner():
    # Clear the screen based on the operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def find_home() -> str:
    # Return the home directory based on the operating system
    return os.environ["USERPROFILE"] if "Windows" in platform.system() else os.environ["HOME"]

def detect_disks() -> list:
    # Detect and return a list of disk partitions, excluding system partitions
    return [partition.mountpoint for partition in psutil.disk_partitions() if not partition.mountpoint.startswith('/sys')]

def is_safe_path(basedir, path, follow_symlinks=True):
    # Check if the path is within the base directory
    real_path = os.path.realpath(path) if follow_symlinks else os.path.abspath(path)
    return real_path.startswith(basedir)

def search_directory(directory, extensions):
    # Validate the directory before using it
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist or is not a valid directory!")
        return
    
    # Check if the directory is within the user's home directory
    if not is_safe_path(find_home(), directory):
        print(f"The directory {directory} is outside your user folder and might be unsafe!")
        return
    
    # Walk through the directory and print files with the specified extensions
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file)[1] in extensions and is_safe_path(directory, file_path):
                print(file_path)

def discover(extensions, search_path):
    # Search for files with the specified extensions in the home directory and optionally in other disks
    home_directory = find_home()
    search_directory(home_directory, extensions)
    
    if search_path:
        for disk in detect_disks():
            if disk != home_directory:
                search_directory(disk, extensions)

def check_affirm(affirmation):
    # Check if the user's input is an affirmation
    return affirmation.lower() in ["y", "yes"]

def main():
    # Main function to run the file discovery program
    screen_cleaner()
    print("Welcome to file discover")
    user_extensions = input("Please enter the file extensions you want to search for, separated by commas: ")
    search_path = check_affirm(input("Would you like to search path too [y/n]: "))
    extensions = set(extension.strip() for extension in user_extensions.split(','))
    discover(extensions, search_path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interruption received, exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
