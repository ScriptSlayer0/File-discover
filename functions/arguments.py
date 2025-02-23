import argparse
from typing import List

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Search for files with specified extensions in directories.")
    
    # Argumento para las extensiones de los archivos
    parser.add_argument(
        "-ext", "--extension", 
        nargs="*", 
        default=[], 
        help="The file extensions to search for (e.g., '.txt', '.py'). Separate by space."
    )
    
    # Argumento para forzar la búsqueda sin restricciones
    parser.add_argument(
        "-f", "--forced", 
        action="store_true", 
        help="Force search even in unsafe locations."
    )
    
    # Argumento para permitir la búsqueda en todos los directorios del PATH
    parser.add_argument(
        "-p", "--path", 
        action="store_true", 
        help="Search directories listed in the PATH environment variable."
    )
    
    # Argumento para mostrar el tiempo que tomó realizar la búsqueda
    parser.add_argument(
        "-t", "--time", 
        action="store_true", 
        help="Display the time taken to scan the directories."
    )
    
    # Argumento para buscar en todos los discos duros
    parser.add_argument(
        "-d", "--disk", 
        action="store_true", 
        help="Scan all available hard disks on the system."
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validaciones para las extensiones
    if args.extension:
        # Asegurarse de que las extensiones tengan un formato válido (incluyendo el punto)
        args.extension = {ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in args.extension}
    
    return args
