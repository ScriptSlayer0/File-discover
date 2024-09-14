import argparse

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Store all inputs in a single list.")
    parser.add_argument("-ext", "--extension", nargs="*", help="The extensions you want to search for, separated by a space")
    parser.add_argument("-f", "--forced", action="store_true", help="Force search")
    parser.add_argument("-p", "--path", action="store_true", help="Search all directories in path too?")
    parser.add_argument("-t", "--time", action="store_true", help="Show the time taken to scan all directories")
    parser.add_argument("-d", "--disk", action="store_true", help="Scan all hard disks")
    return parser.parse_args()
