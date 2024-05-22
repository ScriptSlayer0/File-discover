import os

def discover(extensiones):
    # Usar os.scandir en lugar de os.listdir para un mejor rendimiento
    with open('file_list', 'w+') as file_list:
        for entrada in os.scandir(os.environ['HOME']):
            if entrada.is_dir() and not entrada.name.startswith('.'):
                for rutabs, _, archivos in os.walk(entrada.path):
                    # Comprobar la extensión del archivo en lugar de si el archivo termina con la extensión
                    for archivo in archivos:
                        if os.path.splitext(archivo)[1] in extensiones:
                            file_list.write(os.path.join(rutabs, archivo)+'\n')

def main():
    # Solicitar al usuario que introduzca las extensiones de archivo que desea buscar
    extensiones_usuario = input("Por favor, introduce las extensiones de archivo que deseas buscar, separadas por comas: ")
    # Convertir la cadena de entrada del usuario en un conjunto de extensiones
    extensiones = set(extension.strip() for extension in extensiones_usuario.split(','))
    discover(extensiones)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupción del teclado recibida, saliendo...")
        exit()
