from pathlib import Path
from typing import List, Union, Set
from functions.searching.safe_path_checker import is_safe_path
import os

def find_home() -> Path:
    """Return the home directory as a Path object."""
    return Path.home()

def search_files(directory: Path, extensions: Set[str]) -> List[Path]:
    """
    Search for files with specified extensions in a directory and its subdirectories.

    Args:
        directory (Path): The directory to search in.
        extensions (Set[str]): Set of file extensions to search for.

    Returns:
        List[Path]: List of file paths matching the extensions.
    """
    matching_files = []

    def scan_directory(current_dir: Path):
        """Recursively scan a directory for files with the given extensions."""
        try:
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    if entry.is_file() and any(entry.name.endswith(ext) for ext in extensions):
                        file_path = current_dir / entry.name
                        matching_files.append(file_path)
                        print(f"Found file: {file_path}")
                    elif entry.is_dir():
                        scan_directory(current_dir / entry.name)
        except FileNotFoundError:
            print(f"Directory {current_dir} not found.")
        except PermissionError:
            print(f"Permission denied for {current_dir}.")
        except Exception as e:
            print(f"Error scanning {current_dir}: {e}")

    
    scan_directory(directory)
    return matching_files

def search_directory(directory: Union[str, Path], extensions: List[str], force_search: bool = False, user_authorized: bool = False) -> List[Path]:
    """
    Search for files with the specified extensions in the directory.

    Args:
        directory (Union[str, Path]): The directory to search in.
        extensions (List[str]): List of file extensions to search for.
        force_search (bool): Whether to force the search in unsafe paths.
        user_authorized (bool): Whether the user has authorized the search.

    Returns:
        List[Path]: List of file paths matching the extensions.
    """
    directory_path = Path(directory).resolve()
    if not directory_path.is_dir():
        # Check if the directory exists and is valid
        print(f"The directory {directory_path} does not exist or is not a valid directory!")
        print("Please ensure the path is correct and accessible.")
        return []

    home_directory = find_home()
    
    if not is_safe_path(home_directory, directory_path) and not force_search and not user_authorized:
        # Check if the path is unsafe and prompt the user
        print(f"Warning: Some paths of {directory_path} are outside of {home_directory} folder and might be unsafe!")
        print("Do you want to proceed with the search? (y/n)")
        user_input = input().lower()
        if user_input != 'y':
            print("Search aborted.")
            return []
    
    return search_files(directory_path, set(extensions))
