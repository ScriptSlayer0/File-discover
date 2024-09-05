# CWE-23 patch
import os

def is_safe_path(basedir, path, follow_symlinks=True) -> bool:
    """Check if the path is within the base directory."""
    try:
        # Ensure the base directory is a canonical absolute path
        basedir = os.path.realpath(basedir)
        real_path = os.path.realpath(path) if follow_symlinks else os.path.abspath(path)
        
        # Check if the real path is within the base directory
        return os.path.commonpath([basedir, real_path]) == basedir
    except (ValueError, OSError) as e:
        #print(f"Error checking path safety: {e}")
        return False
