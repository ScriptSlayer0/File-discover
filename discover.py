import os

def discover():
    home = os.environ['HOME']
    carpetas = [x for x in os.listdir(home) if not x.startswith('.')]
    extensiones = ['.mp3', '.mp4', '.rar', '.avi', '.png', '.jpeg', '.zip', '.dat', '.txt', '.pdf', '.exe', '.msi',
                    'iv', '.pem', '.tar']
    
    with open('file_list', 'w+') as file_list:
        for carpeta in carpetas:
            ruta = os.path.join(home, carpeta)
            for extension in extensiones:
                for rutabs, directorio, archivo in os.walk(ruta):
                    for file in archivo:
                        if file.endswith(extension):
                            file_list.write(os.path.join(rutabs, file)+'\n')

def main():
    discover()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()