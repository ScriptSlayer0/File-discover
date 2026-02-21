import os
import stat
import sys


def get_tipo_archivo(mode):
    if stat.S_ISDIR(mode):
        return "d"
    elif stat.S_ISLNK(mode):
        return "l"
    elif stat.S_ISCHR(mode):
        return "c"
    elif stat.S_ISBLK(mode):
        return "b"
    elif stat.S_ISSOCK(mode):
        return "s"
    elif stat.S_ISFIFO(mode):
        return "p"
    else:
        return "-"


def get_rwx(mode):
    permisos = []

    # Owner
    permisos.append("r" if mode & stat.S_IRUSR else "-")
    permisos.append("w" if mode & stat.S_IWUSR else "-")
    if mode & stat.S_ISUID:
        permisos.append("s" if mode & stat.S_IXUSR else "S")
    else:
        permisos.append("x" if mode & stat.S_IXUSR else "-")

    # Group
    permisos.append("r" if mode & stat.S_IRGRP else "-")
    permisos.append("w" if mode & stat.S_IWGRP else "-")
    if mode & stat.S_ISGID:
        permisos.append("s" if mode & stat.S_IXGRP else "S")
    else:
        permisos.append("x" if mode & stat.S_IXGRP else "-")

    # Others
    permisos.append("r" if mode & stat.S_IROTH else "-")
    permisos.append("w" if mode & stat.S_IWOTH else "-")
    if mode & stat.S_ISVTX:
        permisos.append("t" if mode & stat.S_IXOTH else "T")
    else:
        permisos.append("x" if mode & stat.S_IXOTH else "-")

    return "".join(permisos)


def permisos_especiales(mode):
    return {
        "SUID": bool(mode & stat.S_ISUID),
        "SGID": bool(mode & stat.S_ISGID),
        "Sticky": bool(mode & stat.S_ISVTX),
    }


def main(ruta="."):  # por defecto usa directorio actual
    try:
        st = os.stat(ruta)
        mode = st.st_mode

        tipo = get_tipo_archivo(mode)
        rwx = get_rwx(mode)
        especiales = permisos_especiales(mode)

        print(f"Archivo: {ruta}")
        print(f"Permisos estilo ls -l: {tipo}{rwx}")
        print(f"Octal: {oct(mode & 0o7777)}")

        # Mostrar permisos especiales
        any_especial = any(especiales.values())
        if any_especial:
            print("Permisos especiales activos:")
            for k, v in especiales.items():
                if v:
                    print(f"  {k}")
        else:
            print("No hay permisos especiales.")

    except FileNotFoundError:
        print("El archivo no existe.")


if __name__ == "__main__":
    # Si hay argumento lo usa, si no usa "."
    ruta = sys.argv[1] if len(sys.argv) > 1 else "."
    main(ruta)