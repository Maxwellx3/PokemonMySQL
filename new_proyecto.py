import mysql.connector
import os
import resnet50 as rn
import json
import math

def calcular_distancia(p1, p2):
    # Verificar que ambos vectores tengan la misma longitud
    if len(p1) != len(p2):
        raise ValueError("Los vectores deben tener la misma longitud")
    
    # Calcular la distancia euclidiana
    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    return distance

# Establecer la conexión con la base de datos PostgreSQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',        # Usuario de MySQL
    password='303336',
    database='pokemon'
)
cursor = conn.cursor()

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = './pokemones'

# Recorrer la carpeta y leer cada imagen
for filename in os.listdir(carpeta_imagenes):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Obtener el vector característico y el histograma
        vec = rn.obtener_vector_caracteristico(os.path.join(carpeta_imagenes, filename))
        hist = rn.calcular_histograma_de_colores(os.path.join(carpeta_imagenes, filename))
        
        # Convertir los vectores a formato JSON
        vec_json = json.dumps(vec.tolist())  # Convierte el ndarray a una lista y luego a JSON
        hist_json = json.dumps(hist.tolist())  # Convierte el ndarray a una lista y luego a JSON
        
        # Insertar los datos en la tabla de la base de datos
        cursor.execute("INSERT INTO elementos (nombre, vector_caracteristico, histograma) VALUES (%s, %s, %s)", 
                       (filename, vec_json, hist_json))
        conn.commit()

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()
