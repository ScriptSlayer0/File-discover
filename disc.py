#!/bin/python3
import argparse, discover

try:
    # Create the parser
    parser = argparse.ArgumentParser(description="Store all inputs in a single list.")

    # Add a list argument
    parser.add_argument("-ext", "--extension", nargs="*", help="The extensions you want to search for, separated by a space")

    # Add a flag that appends a value to the list
    parser.add_argument("-p", "--path", action="store_true", help="Search all directories in path too?")
    parser.add_argument("-t", "--time", action="store_true", help="Show the time taken to scan all directories")
    parser.add_argument("-d", "--disk", action="store_true", help="Scan all hard disks")

    # Parse the arguments
    args = parser.parse_args()

    discover.discover(args.extension, args.path, args.time, args.disk)
except KeyboardInterrupt:
    print("KeyboardInterrupt detected")
