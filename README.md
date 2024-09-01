# File-Discover

## Overview
**File-Discover** is a Python-based utility designed to locate and list files within a specified directory. This tool is ideal for users who need a quick and simple way to discover files in their system, whether for organizational purposes or system management.

## Features
- **Simple File Discovery**: Traverse directories to locate files based on specific criteria.
- **File Output**: Easily generate a list of discovered files.
- **Cross-Platform**: Works across different operating systems, including Linux, macOS, and Windows.

## Installation

### Clone the Repository
To start using **File-Discover**, clone the repository:
```bash
git clone https://github.com/ScriptSlayer0/File-discover.git
```

### Requirements
- Python 3.x
- psutil 6.0.0 (see requierements.txt)

### Setup
Navigate to the project directory:
```bash
cd File-discover
```

## Usage
To run the tool, execute the `discover.py` script:
```bash
python disc.py
```
Some more usage info:
```
usage: disc.py [-h] [-p] [ext ...]

Store all inputs in a single list.

positional arguments:
  ext         The extenstions you want to search for, serperated by a space

options:
  -h, --help  show this help message and exit
  -p, --path  search all directories in path too?
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or encounter any issues, feel free to open an issue on GitHub.

---
Happy discovering!
