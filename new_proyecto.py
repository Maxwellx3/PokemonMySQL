import psycopg2
import os

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
            img_data = file.read()
            # Ejecutar la consulta para insertar la imagen en la base de datos
            cursor.execute("INSERT INTO tabla_imagenes (nombre, imagen) VALUES (%s, %s)", (filename, psycopg2.Binary(img_data)))
            conn.commit()

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()
