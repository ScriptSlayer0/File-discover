from pathlib import Path
import time
from typing import List, Set
from functions.arguments import parse_arguments
from functions.disk_structure.disk_detection import detect_disks
from functions.disk_structure.disk_partitions import print_partition_structure
from functions.scanning_time import format_elapsed_time
from functions.searching.search_engine import search_directory
from functions.user_authoritation_checker import get_user_authorization
from functions.utils.screan_cleaner import cleaner

def perform_search(directory: Path, extensions: Set[str], force_search: bool, user_authorized: bool) -> List[Path]:
    """
    Perform the search operation on a given directory.

    Args:
        directory (Path): The directory to search in.
        extensions (Set[str]): Set of file extensions to search for.
        force_search (bool): Whether to force the search.
        user_authorized (bool): Whether the user has authorized the search.

    Returns:
        List[Path]: List of found file paths.
    """
    return search_directory(directory, extensions, force_search, user_authorized)

def discover(extensions: Set[str], force_search: bool, show_time: bool, scan_disks: bool) -> None:
    """
    Search for files with the specified extensions in the home directory and optionally in other disks.

    Args:
        extensions (Set[str]): Set of file extensions to search for.
        force_search (bool): Whether to force the search.
        show_time (bool): Whether to display the time taken for scanning.
        scan_disks (bool): Whether to scan other disks.
    """
    home_directory = Path.home()
    user_authorized = get_user_authorization(force_search)

    start_time = time.time()

    all_found_files = perform_search(home_directory, extensions, force_search, user_authorized)
    
    if scan_disks:
        disks = detect_disks()
        for disk in disks:
            if disk != home_directory:
                if force_search or user_authorized:
                    all_found_files.extend(perform_search(disk, extensions, force_search, user_authorized))
                else:
                    print(f"Cannot perform a complete scan of disk {disk} without proper authorization. Skipping.")

    print(f"\nTotal files found: {len(all_found_files)}")

    if show_time:
        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_time = format_elapsed_time(elapsed_time)
        print(f"Total time taken for scanning: {formatted_time}")

def main() -> None:
    """Main function to run the file discovery program."""
    cleaner()
    print("Welcome to the File Discovery Tool!")

    args = parse_arguments()
    
    if args.structure:
        print_partition_structure()
        return

    if not args.extension:
        print("No file extensions provided. Exiting...")
        return

    extensions = set(ext.strip().lower() for ext in args.extension if ext.strip())
    
    if not extensions:
        print("No valid file extensions provided. Exiting...")
        return

    discover(extensions, args.forced, args.time, args.disk)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nKeyboard interruption received, exiting...")
