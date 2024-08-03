import os, platform, psutil

def screen_cleaner():
    if os.name == 'nt': #windows
        os.system('cls')
    else:
        os.system('clear')

def find_home() -> str:
    if "Windows" in platform.platform():
        return os.environ["USERPROFILE"]
    return os.environ["HOME"]

def detect_disks() -> list:
    partitions = psutil.disk_partitions()
    disks = [partition.mountpoint for partition in partitions if not partition.mountpoint.startswith('/sys')]
    return disks

def discover(extensions, search_path):
    home_directory = find_home()
    
    # Search in the user's home directory
    for entry in os.scandir(home_directory):
        if entry.is_dir() and not entry.name.startswith('.'):
            for root, _, files in os.walk(entry.path):
                for file in files:
                    if os.path.splitext(file)[1] in extensions:
                        print(os.path.join(root, file))
    
    # Search in other disks
    if search_path:
        disks = detect_disks()
        for disk in disks:
            if disk != home_directory:  # Avoid searching in the user's home directory again
                for entry in os.scandir(disk):
                    if entry.is_dir() and not entry.name.startswith('.'):
                        for root, _, files in os.walk(entry.path):
                            for file in files:
                                if os.path.splitext(file)[1] in extensions:
                                    print(os.path.join(root, file))

def check_affirm(affirmation):
    return affirmation.lower() in ["y", "yes"]

def main():
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
        exit()
    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
