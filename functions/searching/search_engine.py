from pathlib import Path
from typing import Union, List, Set
from functions.searching.safe_path_checker import is_safe_path
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# =========================
# Logging en vivo
# =========================
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Cambia a DEBUG si quieres más detalles

# =========================
# Helper functions
# =========================

def find_home() -> Path:
    """Return the home directory as a Path object."""
    return Path.home()


def _scan_block(directories: List[Path], extensions_set: Set[str]) -> tuple[list[str], list[Path]]:
    """
    Scan a list of directories (non-recursive) and return matching files and subdirectories.

    Returns:
        files_found (list[str]): List of file paths found.
        subdirs (list[Path]): List of subdirectories to scan next.
    """
    files_found = []
    subdirs = []

    for directory in directories:
        try:
            for entry in os.scandir(directory):
                if entry.is_file() and entry.name.endswith(tuple(extensions_set)):
                    files_found.append(entry.path)
                elif entry.is_dir():
                    subdirs.append(Path(entry.path))
        except PermissionError:
            logger.warning(f"Permission denied: {directory}")
        except OSError as e:
            logger.warning(f"Error accessing {directory}: {e}")

    return files_found, subdirs

# =========================
# Core search functions
# =========================

def search_files_parallel(
    directory: Path,
    extensions: Union[Set[str], List[str]],
    max_workers: int = 8
) -> List[Path]:
    """
    Search for files with specified extensions using parallel scanning,
    mostrando los archivos encontrados en tiempo real con logging.
    """
    extensions_set = set(extensions)
    files_found: List[Path] = []
    dirs_to_scan = [directory]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while dirs_to_scan:
            # Enviar un bloque de directorios a un hilo
            futures = {executor.submit(_scan_block, dirs_to_scan[:50], extensions_set): 1}
            dirs_to_scan = []

            for future in as_completed(futures):
                block_files, block_subdirs = future.result()
                for f in block_files:
                    files_found.append(Path(f))
                    logger.info(f"Archivo encontrado: {f}")  # Mostrar en vivo
                dirs_to_scan.extend(block_subdirs)

    return files_found


def search_directory(
    directory: Union[str, Path],
    extensions: Union[List[str], Set[str]],
    force_search: bool = False,
    user_authorized: bool = False,
    max_workers: int = 8
) -> List[Path]:
    """
    Search for files safely using parallel scanning, mostrando los archivos en vivo.

    Args:
        directory (str | Path): Directorio donde buscar.
        extensions (List[str] | Set[str]): Extensiones de archivo a buscar.
        force_search (bool): Ignorar la verificación de seguridad si True.
        user_authorized (bool): Ignorar la advertencia de seguridad si True.
        max_workers (int): Número de hilos para la búsqueda paralela.

    Returns:
        List[Path]: Lista de archivos encontrados.
    """
    directory_path = Path(directory).resolve(strict=False)

    if not directory_path.exists() or not directory_path.is_dir():
        logger.error(f"Directory {directory_path} does not exist or is not valid.")
        return []

    home_directory = find_home()
    if not is_safe_path(home_directory, directory_path) and not force_search and not user_authorized:
        logger.warning(
            f"Directory {directory_path} is outside home ({home_directory}). "
            f"Set user_authorized=True or force_search=True to proceed."
        )
        return []

    return search_files_parallel(directory_path, extensions, max_workers=max_workers)