import subprocess
import shlex
import platform
import json
import os

# Archivo para almacenar los alias
ALIAS_FILE = "alias.json"

def cargar_alias():
    """Carga los alias desde el archivo JSON"""
    try:
        if os.path.exists(ALIAS_FILE):
            with open(ALIAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except json.JSONDecodeError:
        print(f"Error al leer el archivo de alias. Creando uno nuevo.")
        return {}

def guardar_alias(alias_dict):
    """Guarda los alias en el archivo JSON"""
    with open(ALIAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(alias_dict, f, indent=4)

def ejecutar_comando(comando, alias_dict):
    """Ejecuta un comando del sistema, manejando posibles errores"""
    try:
        # Verificar si el comando es un alias
        partes = comando.split()
        if partes[0] in alias_dict:
            comando_real = alias_dict[partes[0]]
            # Reemplazar el alias por el comando real y mantener los argumentos
            if len(partes) > 1:
                comando = comando_real + " " + " ".join(partes[1:])
            else:
                comando = comando_real
        
        # Detectar el sistema operativo
        if platform.system() == 'Windows':
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        else:
            args = shlex.split(comando)
            resultado = subprocess.run(args, capture_output=True, text=True)
        
        # Mostrar la salida
        print(resultado.stdout)
        
        # Mostrar errores si los hay
        if resultado.stderr:
            print("Error:", resultado.stderr)
    
    except FileNotFoundError:
        print(f"Comando no encontrado: {comando}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def procesar_comando_interno(comando, alias_dict):
    """Procesa comandos internos del emulador"""
    partes = comando.split()
    
    # Comandos para manejar alias
    if partes[0] == "alias":
        if len(partes) == 1:
            # Mostrar todos los alias
            if not alias_dict:
                print("No hay alias definidos.")
            else:
                print("Alias definidos:")
                for alias, cmd in alias_dict.items():
                    print(f"{alias} = '{cmd}'")
        elif len(partes) >= 3 and partes[1] not in ["remove", "rm"]:
            # Crear un nuevo alias: alias nombre comando
            nombre_alias = partes[1]
            comando_alias = " ".join(partes[2:])
            alias_dict[nombre_alias] = comando_alias
            guardar_alias(alias_dict)
            print(f"Alias '{nombre_alias}' creado para el comando '{comando_alias}'")
        elif len(partes) == 3 and (partes[1] == "remove" or partes[1] == "rm"):
            # Eliminar un alias
            nombre_alias = partes[2]
            if nombre_alias in alias_dict:
                del alias_dict[nombre_alias]
                guardar_alias(alias_dict)
                print(f"Alias '{nombre_alias}' eliminado.")
            else:
                print(f"El alias '{nombre_alias}' no existe.")
        else:
            print("Uso de alias:\n  alias               - Mostrar todos los alias\n  alias nombre comando - Crear un alias\n  alias remove nombre - Eliminar un alias")
        return True
        
    # Comando para mostrar ayuda
    elif partes[0] == "help":
        print("Comandos disponibles:")
        print("  exit              - Salir del emulador")
        print("  alias             - Gestionar alias")
        print("  help              - Mostrar esta ayuda")
        print("  [comando sistema] - Ejecutar un comando del sistema")
        return True
        
    return False

def main():
    # Cargar alias existentes
    alias_dict = cargar_alias()
    
    print("Bienvenido al emulador de terminal con soporte para alias.")
    print("Escribe 'exit' para salir, 'help' para ver la ayuda.")
    
    while True:
        # Solicitar al usuario que ingrese un comando
        comando = input("$ ")
        
        # Salir del bucle si el usuario escribe 'exit'
        if comando.lower() == 'exit':
            break
        
        # Ignorar líneas vacías
        if not comando.strip():
            continue
            
        # Procesar comandos internos
        if not procesar_comando_interno(comando, alias_dict):
            # Si no es un comando interno, ejecutarlo como comando del sistema
            ejecutar_comando(comando, alias_dict)
    
    print("Gracias por usar el emulador de terminal. ¡Hasta luego!")

if __name__ == "__main__":
    main()