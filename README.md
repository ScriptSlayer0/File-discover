# File-Discover
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ScriptSlayer0_File-discover&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ScriptSlayer0_File-discover)
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
- psutil
- See for more details [requierements.txt](https://github.com/ScriptSlayer0/File-discover/blob/main/requirements.txt)

### Setup
Navigate to the project directory:
```bash
cd File-discover
```

## Usage
To run the tool, execute the `discover.py` script:
```bash
python discover.py
```
Some more usage info:
```
usage: discover.py [-h] [-p] [-ext]

Store all inputs in a single list.

options:
-h, --help            Show this help message and exit
-ext, --extension      The extensions you want to search for, separated by a space
-f, --forced           Force search
-p, --path             Search all directories in path too?
-t, --time             Show the time taken to scan all directories
-d, --disk             Scan all hard disks
 -s, --structure       Show only the partition structure of hard disks
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or encounter any issues, feel free to open an issue on GitHub.

---
Happy discovering!
