import time
from functions.arguments import parse_arguments
from functions.disk_detection import detect_disks
from functions.disk_structure.disk_partitions import print_partition_structure
from functions.scanning_time import format_elapsed_time
from functions.user_authoritation_checker import get_user_authorization
from functions.searching.search_engine_old import find_home, search_directory
from functions.utils.screan_cleaner import cleaner

def perform_search(home_directory, extensions, force_search, user_authorized, scan_disks):
    """Perform the search operation on the home directory and optionally on other disks."""
    search_directory(home_directory, extensions, force_search, user_authorized)
    
    if scan_disks:
        disks = detect_disks()
        for disk in disks:
            if disk != home_directory:
                if force_search or user_authorized:
                    search_directory(disk, extensions, force_search, user_authorized)
                else:
                    print(f"Cannot perform a complete scan of disk {disk} without proper authorization. Skipping.")

def discover(extensions, force_search, show_time, scan_disks):
    """Search for files with the specified extensions in the home directory and optionally in other disks."""
    home_directory = find_home()
    user_authorized = get_user_authorization(force_search)

    start_time = time.time()  # Start the timer
    
    perform_search(home_directory, extensions, force_search, user_authorized, scan_disks)
    
    if show_time:
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time
        formatted_time = format_elapsed_time(elapsed_time)
        print(f"Total time taken for scanning: {formatted_time}")

def main():
    """Main function to run the file discovery program."""
    cleaner()
    print("Welcome to the File Discovery Tool!")

    args = parse_arguments()
    
    #When user inputs -s or --structure
    if args.structure:
        print_partition_structure()
        return

    if not args.extension:
        print("No file extensions provided. Exiting...")
        return

    extensions = set(extension.strip() for extension in args.extension if extension.strip())
    
    if not extensions:
        print("No valid file extensions provided. Exiting...")
        return

    discover(extensions, args.forced, args.time, args.disk)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interruption received, exiting...")
