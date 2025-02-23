import argparse

def parse_arguments():
    #Customisation is now possible
    parser = argparse.ArgumentParser(
        prog='discover.py',
        usage='%(prog)s [-h] [-ext [EXTENSION ...]] [-f] [-p] [-t] [-d] [-s]',
        description="File discovery tool that stores all inputs in a single list."
    )
    
    parser.add_argument("-ext", "--extension", nargs="*", help="The extensions you want to search for, separated by a space")
    parser.add_argument("-f", "--forced", action="store_true", help="Force search")
    parser.add_argument("-p", "--path", action="store_true", help="Search all directories in path too?")
    parser.add_argument("-t", "--time", action="store_true", help="Show the time taken to scan all directories")
    parser.add_argument("-d", "--disk", action="store_true", help="Scan all hard disks")
    parser.add_argument("-s", "--structure", action="store_true", help="Show only the partition structure of hard disks")

    return parser.parse_args()
