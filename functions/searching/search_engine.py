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
        try:
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    if entry.is_file() and any(entry.name.endswith(ext) for ext in extensions):
                        file_path = current_dir / entry.name
                        matching_files.append(file_path)
                        print(file_path)
                    elif entry.is_dir():
                        scan_directory(current_dir / entry.name)
        except PermissionError:
            print(f"Permission denied: {current_dir}")
        except Exception as e:
            print(f"An error occurred while searching {current_dir}: {e}")

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
        print(f"The directory {directory_path} does not exist or is not a valid directory!")
        return []
    
    home_directory = find_home()
    
    if not is_safe_path(home_directory, directory_path) and not force_search and not user_authorized:
        print(f"Warning: Some paths of {directory_path} are outside of {home_directory} folder and might be unsafe!")
        user_input = input("Do you want to proceed with the search? (y/n): ").lower()
        if user_input != 'y':
            print("Search aborted.")
            return []
    
    return search_files(directory_path, set(extensions))
