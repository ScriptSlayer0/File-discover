#!/bin/python3

import argparse,discover

# Create the parser
parser = argparse.ArgumentParser(description="Store all inputs in a single list.")

# Add a list argument
parser.add_argument("ext", nargs="*", help="The extenstions you want to search for, serperated by a space")

# Add a flag that appends a value to the list
parser.add_argument("-p", "--path", action="store_true", help="search all directories in path too?")

# Parse the arguments
args = parser.parse_args()

discover.discover(args.ext, args.path)