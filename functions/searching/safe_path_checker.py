from pathlib import Path
from typing import Union

def is_safe_path(
    basedir: Union[str, Path], 
    path: Union[str, Path], 
    follow_symlinks: bool = True
) -> bool:
    try:
        basedir_path = Path(basedir).resolve(strict=True)
        check_path = Path(path).resolve(strict=True) if follow_symlinks else Path(path).absolute()
        return check_path == basedir_path or basedir_path in check_path.parents
    except (ValueError, OSError, RuntimeError):
        return False