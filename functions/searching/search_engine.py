import os
from typing import List, Set, Generator, Union
from pathlib import Path
from functools import lru_cache
from functions.searching.safe_path_checker import is_safe_path

class DirectorySearcher:
    """A class to handle file searching operations with safety checks."""
    
    def __init__(self, extensions: Set[str], force_search: bool = False, user_authorized: bool = False):
        """
        Initialize the DirectorySearcher.
        
        Args:
            extensions: Set of file extensions to search for (including the dot)
            force_search: Override safety checks if True
            user_authorized: Consider the user as authorized to search anywhere if True
        """
        self.extensions = {f".{ext.lstrip('.').lower()}" for ext in extensions}
        self.force_search = force_search
        self.user_authorized = user_authorized
        self.home_directory = self._get_home_directory()
    
    @staticmethod
    @lru_cache(maxsize=1)
    def _get_home_directory() -> Path:
        """Return the cached home directory path."""
        return Path.home()
    
    def _is_safe_location(self, directory: Path) -> bool:
        """
        Check if the directory is safe to search.
        
        Args:
            directory: Path to check
            
        Returns:
            bool: True if the directory is safe to search
        """
        return (self.force_search or 
                self.user_authorized or 
                is_safe_path(str(self.home_directory), str(directory)))
    
    def _should_process_file(self, file_path: Path) -> bool:
        """
        Check if the file should be processed based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            bool: True if the file should be processed
        """
        return file_path.suffix.lower() in self.extensions
    
    def search_files(self, directory: Path) -> Generator[Path, None, None]:
        """
        Search for files with specified extensions in the directory.
        
        Args:
            directory: Directory to search in
            
        Yields:
            Path: Paths of matching files
        """
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    if entry.is_file() and self._should_process_file(path):
                        yield path
                    elif entry.is_dir():
                        yield from self.search_files(path)
        except (PermissionError, OSError) as e:
            print(f"Access error: {directory} - {e}")
    
    def search_directory(self, directory: Union[str, Path]) -> List[Path]:
        """
        Main method to search for files in a directory with safety checks.
        
        Args:
            directory: Directory path to search in
            
        Returns:
            List of paths to matching files
        """
        directory_path = Path(directory).resolve()
        
        if not directory_path.is_dir():
            raise ValueError(f"The path {directory_path} does not exist or is not a directory")
            
        if not self._is_safe_location(directory_path):
            print(f"Warning: Some paths of {directory_path} are outside of {self.home_directory} "
                  "folder and might be unsafe!")
            
        return list(self.search_files(directory_path))

def search_files_in_directory(
    directory: str,
    extensions: Set[str],
    force_search: bool = False,
    user_authorized: bool = False
) -> List[Path]:
    """
    Convenience function to search files without instantiating the class directly.
    
    Args:
        directory: Directory to search in
        extensions: File extensions to look for
        force_search: Override safety checks if True
        user_authorized: Consider the user as authorized to search anywhere if True
        
    Returns:
        List of paths to matching files
    """
    searcher = DirectorySearcher(extensions, force_search, user_authorized)
    return searcher.search_directory(directory)
