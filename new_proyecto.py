import psycopg2
import os
import resnet50 as rn
import json


# Establecer la conexión con la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='proyecto',
    user='postgres',
    password='1',
    host='localhost'
)
cursor = conn.cursor()

# Ruta de la carpeta que contiene las imágenes
carpeta_imagenes = './poke'

# Recorrer la carpeta y leer cada imagen
for filename in os.listdir(carpeta_imagenes):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        with open(os.path.join(carpeta_imagenes, filename), 'rb') as file:
                vec = rn.preprocess_image(os.path.join(carpeta_imagenes, filename))
                # Calcular el histograma de colores
                hist = rn.calcular_histograma_de_colores(os.path.join(carpeta_imagenes, filename))
                # Insertar los datos en la tabla de la base de datos # Convertir los vectores de NumPy a listas de Python
                # Convertir los vectores a formato JSON
                vec_json = json.dumps(vec.tolist())  # Convierte el ndarray a una lista y luego a JSON
                hist_json = json.dumps(hist.tolist())  # Convierte el ndarray a una lista y luego a JSON
                # Ejecutar la consulta para insertar la imagen en la base de datos
                cursor.execute("INSERT INTO elementos (nombre, vector_caracteristico,histograma) VALUES (%s, %s, %s)", (filename,vec.tolist() ,hist.tolist() ))
                conn.commit()

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()
