import os, platform

def find_home()->str:
    if "Windows" in platform.platform():
        return "HOMEPATH"
    return "HOME"

def discover(extensions, search_path):
    for entry in os.scandir(os.environ[find_home()]):
        if entry.is_dir() and not entry.name.startswith('.'):
            for rutabs, _, files in os.walk(entry.path):
                # Comprobar la extensión del archivo en lugar de si el archivo termina con la extensión
                for file in files:
                    if os.path.splitext(file)[1] in extensions:
                        print(os.path.join(rutabs, file))
    if search_path:
        for path in os.environ['PATH'].split(os.pathsep):
            try:
                for entry in os.scandir(path):
                    if entry.is_dir() and not entry.name.startswith('.'):
                        for rutabs, _, files in os.walk(entry.path):
                            # Comprobar la extensión del archivo en lugar de si el archivo termina con la extensión
                            for file in files:
                                if os.path.splitext(file)[1] in extensions:
                                    print(os.path.join(rutabs, file))
            except: pass


def check_affirm(affirmation):
    if affirmation.lower()=="y" or affirmation.lower()=="yes":
        return True
    else:
        return False
def main():
    # Solicitar al usuario que introduzca las extensiones de archivo que desea buscar
    user_extensions = input("Please enter the file extensions you want to search for, separated by commas: ")
    search_path = check_affirm(input("Would you like to search path too [y/n]: "))
    # Convertir la cadena de entrada del usuario en un conjunto de extensiones
    extensions = set(extension.strip() for extension in user_extensions.split(','))
    discover(extensions, search_path)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n Interrupción del teclado recibida, saliendo...")
        exit()
