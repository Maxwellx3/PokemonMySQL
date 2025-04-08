import os
import json
import math
import numpy as np
from db import conectar_db
import resnet50 as rn
import capas as crn

ARCHIVO_DISTANCIA = "max_distancia.txt"
CARPETA_IMAGENES = "./gaperros"
CARPETA_TEST = "./test"

def insertar_imagenes(carpeta_imagenes, cursor, conn):
    for filename in os.listdir(carpeta_imagenes):
        if filename.lower().endswith(('.jpg', '.png')):
            ruta_imagen = os.path.join(carpeta_imagenes, filename)
            vec = rn.obtener_vector_caracteristico(ruta_imagen) #Aqui cambio las capas a usar
            print(filename)
            # Convertir a formato JSON
            vec_json = json.dumps(vec.tolist())
            
            # INSERT IGNORE para evitar duplicados
            cursor.execute("INSERT IGNORE INTO elementos (nombre, vector_caracteristico) VALUES (%s, %s)",
                           (filename, vec_json))
    conn.commit()

def calcular_distancia(p1, p2):
    if len(p1) != len(p2):
        raise ValueError("Los vectores deben tener la misma longitud")
    # Distancia euclidiana
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def obtener_datos_imagen(nombre, cursor):
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre,))
    fila = cursor.fetchone()
    if fila is None:
        raise ValueError("La imagen no se encontró en la base de datos.")
    vector = json.loads(fila[0])
    return vector

def comparar_animales(nombre1, nombre2, cursor):
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre1,))
    row1 = cursor.fetchone()
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre2,))
    row2 = cursor.fetchone()
    
    if row1 is None or row2 is None:
        raise ValueError("Uno de los animales no se encontró en la base de datos.")
    
    # Convertir JSON a listas
    vector1 = json.loads(row1[0])
    vector2 = json.loads(row2[0])
    
    # Distancia euclidiana
    return calcular_distancia(vector1, vector2)
    
def obtener_top_10_similares(nombre, cursor):
    """
    Dado el nombre de un animal, obtiene su vector característico y calcula la distancia euclidiana
    con los demás animales almacenados en la base de datos. Retorna una lista con los 10 animales más
    similares (los que tengan menor distancia).
    """
    # Obtener el vector del animal base
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError("El animal base no se encontró en la base de datos.")
    base_vector = json.loads(row[0])
    
    cursor.execute("SELECT nombre, vector_caracteristico FROM elementos WHERE nombre <> %s", (nombre,))    
    similitudes = []
    for registro in cursor.fetchall():
        nombre_otro = registro[0]
        vector_otro = json.loads(registro[1])
        dist = calcular_distancia(base_vector, vector_otro)
        similitudes.append((nombre_otro, dist))
    
    similitudes.sort(key=lambda x: x[1])
    return similitudes[:10]

def calcular_max_distancia():
    """
    Calcula la distancia máxima entre todos los vectores almacenados en la tabla 'elementos'.
    Esta función recorre todos los pares y guarda el resultado en un archivo para uso futuro.
    """
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT vector_caracteristico FROM elementos;")
    filas = cursor.fetchall()
    conn.close()

    vectores = [np.array(json.loads(fila[0])) for fila in filas if fila[0]]
    max_dist = 0
    if vectores:
        for i in range(len(vectores)):
            for j in range(i + 1, len(vectores)):
                dist = np.linalg.norm(vectores[i] - vectores[j])
                max_dist = max(max_dist, dist)
    max_dist = max_dist if max_dist else 100

    with open(ARCHIVO_DISTANCIA, "w") as f:
        f.write(str(max_dist))
    return max_dist

def cargar_max_distancia():
    """Carga la distancia máxima desde un archivo, o la calcula si el archivo no existe."""
    if os.path.exists(ARCHIVO_DISTANCIA):
        with open(ARCHIVO_DISTANCIA, "r") as f:
            return float(f.read().strip())
    else:
        return calcular_max_distancia()
        #return ValueError("No se encontro archivo de maxima distancia.")
    
MAX_DISTANCIA = cargar_max_distancia()
conn = conectar_db()
cursor = conn.cursor()
# Insertar las imágenes
#insertar_imagenes(CARPETA_IMAGENES, cursor, conn)

#INSERTAR IMAGENES DE PRUEBA
#insertar_imagenes(CARPETA_TEST, cursor, conn)
cursor.close()
conn.close()

