import os, platform, psutil

def screen_cleaner():
    os.system('cls' if os.name == 'nt' else 'clear')

def find_home() -> str:
    return os.environ["USERPROFILE"] if "Windows" in platform.platform() else os.environ["HOME"]

def detect_disks() -> list:
    return [partition.mountpoint for partition in psutil.disk_partitions() if not partition.mountpoint.startswith('/sys')]

def search_directory(directory, extensions):
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] in extensions:
                print(os.path.join(root, file))

def discover(extensions, search_path):
    home_directory = find_home()
    search_directory(home_directory, extensions)
    
    if search_path:
        for disk in detect_disks():
            if disk != home_directory:
                search_directory(disk, extensions)

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
    except Exception as e:
        print(f"An error occurred: {e}")
