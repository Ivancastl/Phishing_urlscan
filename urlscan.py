import requests
import pyfiglet
import pandas as pd
import os

# URL de la API de búsqueda de urlscan.io
search_url = "https://urlscan.io/api/v1/search/"

# Ruta del archivo donde se almacenará la API
api_key_file = "api_key.txt"

# Función para mostrar la etiqueta con arte ASCII
def mostrar_etiqueta():
    # Generar arte ASCII para "API-Urlscan.io"
    texto_ascii = pyfiglet.figlet_format("API-Urlscan.io") 
    print(texto_ascii)
    
    # Agregar tu nombre de usuario de Twitter y el enlace de tu grupo de Telegram
    print("\nSígueme en Twitter: @ivancastl")
    print("Únete a mi grupo de Telegram: https://t.me/+_g4DIczsuI9hOWZh")

# Función para guardar la clave API en un archivo
def guardar_api_key(api_key):
    with open(api_key_file, "w") as file:
        file.write(api_key)

# Función para cargar la clave API desde el archivo
def cargar_api_key():
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as file:
            return file.read().strip()
    else:
        return None

# Función para buscar usando query
def search_by_query(query, api_key):
    headers = {"API-Key": api_key}
    response = requests.get(search_url, params={"q": query}, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Lista para almacenar los resultados
        results_list = []

        # Revisar todos los resultados para encontrar posibles coincidencias
        if "results" in data:
            for result in data["results"]:
                result_data = {
                    "URL": result["page"].get("url", "N/A"),
                    "ID": result.get("_id", "N/A"),
                    "Submitter": result.get("submitter", "N/A"),
                    "Task": result.get("task", "N/A"),
                    "Stats": result.get("stats", "N/A"),
                    "Page": result.get("page", "N/A"),
                    "Result": result.get("result", "N/A"),
                    "Screenshot": result.get("screenshot", "N/A"),
                }
                results_list.append(result_data)

        # Guardar los resultados en un archivo Excel
        df = pd.DataFrame(results_list)
        df.to_excel("report_clave.xlsx", index=False)

        print("El reporte ha sido generado como 'report_clave.xlsx'")

    else:
        print(f"Error en la solicitud con query: {response.status_code}")
        print(response.text)

# Función para buscar usando hash
def search_by_hash(hash_value, api_key):
    # Usar el formato correcto: hash:<hash_value>
    params = {"q": f"hash:{hash_value}"}
    headers = {"API-Key": api_key}
    response = requests.get(search_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        result_list = []
        for result in data.get('results', []):
            result_data = {
                "URL": result["page"].get("url", "N/A"),
                    "ID": result.get("_id", "N/A"),
                    "Submitter": result.get("submitter", "N/A"),
                    "Task": result.get("task", "N/A"),
                    "Stats": result.get("stats", "N/A"),
                    "Page": result.get("page", "N/A"),
                    "Result": result.get("result", "N/A"),
                    "Screenshot": result.get("screenshot", "N/A"),
            }
            result_list.append(result_data)
        
        # Crear el reporte en Excel
        df = pd.DataFrame(result_list)
        df.to_excel("report_hash.xlsx", index=False)
        print("El reporte ha sido generado como 'report_hash.xlsx'")

    else:
        print(f"Error en la solicitud con hash: {response.status_code}")
        print(response.text)

# Verificar si ya tenemos una clave API guardada
api_key = cargar_api_key()

# Si no se encuentra la clave API, pedir al usuario que la ingrese
if not api_key:
    api_key = input("Introduce tu clave API de urlscan.io: ").strip()
    guardar_api_key(api_key)  # Guardar la clave API para futuras ejecuciones

# Menú para que el usuario elija qué buscar
mostrar_etiqueta()  # Llamar la función para mostrar la etiqueta

print("Opciones de búsqueda:")
print("1. Buscar por palabra clave y dominio legítimo (query)")
print("2. Buscar por hash de una imagen u otro archivo")

# Solicitar al usuario elegir la opción
opcion = input("Elija una opción (1 o 2): ").strip()

if opcion == "1":
    # Solicitar al usuario el query (palabra clave y dominio legítimo)
    palabra_clave = input("Introduce la palabra clave para buscar (por ejemplo, 'gobmx'): ").strip()
    sitio_legitimo = input("Introduce el dominio legítimo para excluir (por ejemplo, 'gob.mx'): ").strip()
    
    # Construir el query interno
    query = f"*page.domain:{palabra_clave}* NOT page.domain:{sitio_legitimo}"
    print(f"Buscando con query: {query}")
    
    # Realizar la búsqueda con query
    search_by_query(query, api_key)

elif opcion == "2":
    # Solicitar al usuario el hash
    hash_value = input("Introduce el hash de la imagen o archivo (SHA-256): ").strip()
    
    # Realizar la búsqueda con hash
    search_by_hash(hash_value, api_key)

else:
    print("Opción inválida. Elija 1 o 2.")
