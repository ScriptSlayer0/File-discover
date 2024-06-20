import os, platform

def find_home()->str:
    if "Windows" in platform.platform():
        return "HOMEPATH"
    return "HOME"

def discover(extensions):
    for entry in os.scandir(os.environ[find_home()]):
        if entry.is_dir() and not entry.name.startswith('.'):
            for rutabs, _, files in os.walk(entry.path):
                # Comprobar la extensión del archivo en lugar de si el archivo termina con la extensión
                for file in files:
                    if os.path.splitext(file)[1] in extensions:
                        print(os.path.join(rutabs, file)+'\n')

def main():
    # Solicitar al usuario que introduzca las extensiones de archivo que desea buscar
    user_extensions = input("Por favor, introduce las extensiones de archivo que deseas buscar, separadas por comas: ")
    # Convertir la cadena de entrada del usuario en un conjunto de extensiones
    extensions = set(extension.strip() for extension in user_extensions.split(','))
    discover(extensions)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupción del teclado recibida, saliendo...")
        exit()
