import time
from funtions.affirmation_checker import check_affirm
from funtions.disk_detection import detect_disks
from funtions.searching_directories import find_home, search_directory
from utils.screan_cleaner import cleaner

def discover(extensions, force_search, show_time, scan_disks):
    """Search for files with the specified extensions in the home directory and optionally in other disks."""
    home_directory = find_home()
    user_authorized = check_affirm("", context="force_search") if force_search else False

    start_time = time.time()  # Start the timer
    
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
