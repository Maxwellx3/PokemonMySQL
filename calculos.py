import os
import json
from db import conectar_db
import resnet50 as rn
from busqueda_faiss import construir_indice, buscar_similares, calcular_distancia_faiss
import numpy as np

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
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
    vector1 = json.loads(row1[0])
    vector2 = json.loads(row2[0])
    return calcular_distancia_faiss(vector1, vector2)

def obtener_top_10_similares(nombre, cursor):
    """
    Devuelve una lista con los 10 animales más similares al dado (por nombre)
    usando FAISS.
    """
    # Obtener vector base
    cursor.execute("SELECT vector_caracteristico FROM elementos WHERE nombre = %s", (nombre,))
    row = cursor.fetchone()
    if not row:
        raise ValueError("El animal no se encontró en la base de datos.")
    vector_base = json.loads(row[0])
    # Obtener todos los demás vectores
    cursor.execute("SELECT nombre, vector_caracteristico FROM elementos WHERE nombre <> %s", (nombre,))
    resultados = cursor.fetchall()
    nombres = []
    vectores = []
    for nombre_otro, vector_str in resultados:
        try:
            vector_otro = json.loads(vector_str)
            nombres.append(nombre_otro)
            vectores.append(vector_otro)
        except Exception as e:
            print(f"Error cargando vector para {nombre_otro}: {e}")
    # Construir índice FAISS y buscar similares
    index = construir_indice(vectores)
    indices, distancias = buscar_similares(index, vector_base)
    # Retornar nombres con sus distancias
    similares = [(nombres[i], float(distancias[j])) for j, i in enumerate(indices)]
    return similares

def calcular_max_distancia_faiss(vectores):
    """
    Calcula la distancia máxima entre todos los vectores usando FAISS.
    Recibe una lista de vectores (cada uno debe ser lista o array de floats).
    """
    if not vectores:
        return 100
    # Construir el índice FAISS
    index = construir_indice(vectores)
    # Convertimos a matriz numpy tipo float32
    datos = np.array(vectores, dtype='float32')
    # Buscamos la distancia de cada vector contra todos los vectores
    # (incluyendo a sí mismo con distancia 0)
    distancias, _ = index.search(datos, len(vectores))
    max_dist = distancias.max()
    return max_dist if max_dist else 100

def calcular_max_distancia():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT vector_caracteristico FROM elementos;")
    filas = cursor.fetchall()
    conn.close()
    vectores = [json.loads(fila[0]) for fila in filas if fila[0]]
    max_dist = calcular_max_distancia_faiss(vectores)
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
    
MAX_DISTANCIA = cargar_max_distancia()
conn = conectar_db()
cursor = conn.cursor()
# Insertar las imágenes
#insertar_imagenes(CARPETA_IMAGENES, cursor, conn)

#INSERTAR IMAGENES DE PRUEBA
#insertar_imagenes(CARPETA_TEST, cursor, conn)
cursor.close()
conn.close()

