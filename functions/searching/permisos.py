import os

modo = os.stat(r"C:\Users\Unai\SendTo").st_mode

def get_rwx(mode):
    # Owner permissions (r, w, x)
    r = (mode & 4) != 0  # SUID (4)  // Lectura
    w = (mode & 2) != 0  # SGID (2)  // Escritura
    x = (mode & 1) != 0  # sticky (1) // Ejecución

    # Group permissions (r, w, x)
    gr_r = (mode & 8) != 0  # Group r
    gr_w = (mode & 16) != 0  # Group w
    gr_x = (mode & 32) != 0  # Group x

    # Others permissions (r, w, x)
    oth_r = (mode & 128) != 0  # Others r
    oth_w = (mode & 256) != 0  # Others w
    oth_x = (mode & 512) != 0  # Others x

    # Construir la cadena rwx con hyphens
    rwx = []
    if r:
        rwx.append("r")
    else:
        rwx.append("-")
    if w:
        rwx.append("w")
    else:
        rwx.append("-")
    if x:
        rwx.append("x")
    else:
        rwx.append("-")

    if gr_r:
        rwx.append("r")
    else:
        rwx.append("-")
    if gr_w:
        rwx.append("w")
    else:
        rwx.append("-")
    if gr_x:
        rwx.append("x")
    else:
        rwx.append("-")

    if oth_r:
        rwx.append("r")
    else:
        rwx.append("-")
    if oth_w:
        rwx.append("w")
    else:
        rwx.append("-")
    if oth_x:
        rwx.append("x")
    else:
        rwx.append("-")

    return "".join(rwx)


print(f"Permisos: {get_rwx(modo)}")


