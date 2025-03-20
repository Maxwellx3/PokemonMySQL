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

def insertar_imagenes(carpeta_imagenes, cursor, conn):
    for filename in os.listdir(carpeta_imagenes):
        if filename.lower().endswith(('.jpg', '.png')):
            ruta_imagen = os.path.join(carpeta_imagenes, filename)
            # Obtener vector característico y histograma
            vec = rn.obtener_vector_caracteristico(ruta_imagen)
            hist = rn.calcular_histograma_de_colores(ruta_imagen)
            
            # Convertir a formato JSON
            vec_json = json.dumps(vec.tolist())
            hist_json = json.dumps(hist.tolist())
            
            # Insertar en la base de datos (usando INSERT IGNORE para evitar duplicados)
            cursor.execute("INSERT IGNORE INTO elementos (nombre, vector_caracteristico, histograma) VALUES (%s, %s, %s)",
                           (filename, vec_json, hist_json))
    conn.commit()

def comparar_pokemones(nombre1, nombre2, cursor):
    # Recuperar los vectores de los dos Pokémon
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre1,))
    row1 = cursor.fetchone()
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre2,))
    row2 = cursor.fetchone()
    
    if row1 is None or row2 is None:
        raise ValueError("Uno de los Pokémon no se encontró en la base de datos.")
    
    # Convertir JSON a listas
    vector1 = json.loads(row1[0])
    vector2 = json.loads(row2[0])
    
    # Calcular la distancia euclidiana
    distancia = calcular_distancia(vector1, vector2)
    return distancia

def obtener_top_10_similares(nombre, cursor):
    """
    Dado el nombre de un Pokémon, obtiene su vector característico y calcula la distancia euclidiana
    con los demás Pokémon almacenados en la base de datos. Retorna una lista con los 10 Pokémon más
    similares (los que tengan menor distancia).
    """
    # Obtener el vector del Pokémon base
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError("El Pokémon base no se encontró en la base de datos.")
    
    base_vector = json.loads(row[0])
    
    # Obtener todos los demás registros (excluyendo el Pokémon base)
    cursor.execute("SELECT nombre, vector_caracteristico FROM elementos WHERE nombre <> %s", (nombre,))
    registros = cursor.fetchall()
    
    similitudes = []
    for registro in registros:
        nombre_otro = registro[0]
        vector_otro = json.loads(registro[1])
        dist = calcular_distancia(base_vector, vector_otro)
        similitudes.append((nombre_otro, dist))
    
    # Ordenar por distancia ascendente y tomar los primeros 10
    similitudes.sort(key=lambda x: x[1])
    return similitudes[:10]

# Establecer la conexión con la base de datos PostgreSQL
conn = mysql.connector.connect(
    host='localhost',
    user='root', 
    password='303336',
    database='gaperros'
)
cursor = conn.cursor()

# Insertar las imágenes
# insertar_imagenes('./gaperros', cursor, conn)

# Comparar dos Pokémon
"""
try:
    dist = comparar_pokemones("electrode.jpg", "empoleon.jpg", cursor)
    print("La distancia euclidiana entre los Pokémon es:", dist)
except ValueError as e:
    print(e)

# Obtener los 10 Pokémon más similares
"""

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()
