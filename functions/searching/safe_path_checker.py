# CWE-23 patch
from pathlib import Path
from typing import Union

def is_safe_path(basedir: Union[str, Path], path: Union[str, Path], follow_symlinks: bool = True) -> bool:
    """
    Check if the given path is within the base directory.

    Args:
        basedir (Union[str, Path]): The base directory path.
        path (Union[str, Path]): The path to check.
        follow_symlinks (bool): Whether to follow symlinks. Defaults to True.

    Returns:
        bool: True if the path is safe (within the base directory), False otherwise.
    """
    try:
        # Convert to Path objects and resolve
        basedir_path = Path(basedir).resolve(strict=True)
        check_path = Path(path).resolve(strict=True) if follow_symlinks else Path(path).absolute()

        # Check if the path to check is within the base directory
        return check_path == basedir_path or basedir_path in check_path.parents
    except (ValueError, OSError, RuntimeError) as e:
        print(f"Error checking path safety: {e}")
        return False
