from traceback import print_tb
from img2vec_pytorch import Img2Vec
from PIL import Image
import numpy as np
import os
import psycopg2
import json

# Inicializar el modelo (seleccionar el tipo de modelo)
# Puedes usar 'resnet-18', 'resnet-50', 'resnet-101', 'resnet-152', 'vgg-16' o 'vgg-19'
img2vec = Img2Vec(model='resnet50')

def preprocess_image(image_path):
    # Cargar la imagen
    img = Image.open(image_path)
    
    # Convertir la imagen a formato RGB si es RGBA
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # Redimensionar la imagen a las dimensiones aceptadas por el modelo (si es necesario)
    img = img.resize((224, 224))  # Las dimensiones pueden variar según el modelo
    
    return img

# Función para calcular el histograma de colores de una imagen
def calcular_histograma_de_colores(imagen_path):
    imagen = Image.open(imagen_path)
    imagen_np = np.array(imagen)
    hist_red, _ = np.histogram(imagen_np[:,:,0].ravel(), bins=256, range=(0, 256))
    hist_green, _ = np.histogram(imagen_np[:,:,1].ravel(), bins=256, range=(0, 256))
    hist_blue, _ = np.histogram(imagen_np[:,:,2].ravel(), bins=256, range=(0, 256))
    histograma = np.concatenate((hist_red, hist_green, hist_blue))
    return histograma

ruta_carpeta1 = './pokemon_images_shiny'

# Conexión a la base de datos
conn = psycopg2.connect(
        dbname='Proyecto2',
        user='postgres',
        password='1',
        host='localhost',
    )
# Abrir un cursor para realizar operaciones con la base de datos
cur = conn.cursor()


for filename in os.listdir(ruta_carpeta1):        
    vec = img2vec.get_vec(preprocess_image(os.path.join(ruta_carpeta1, filename)))
    # Calcular el histograma de colores
    hist = calcular_histograma_de_colores(os.path.join(ruta_carpeta1, filename))
    # Insertar los datos en la tabla de la base de datos # Convertir los vectores de NumPy a listas de Python
    # Convertir los vectores a formato JSON
    vec_json = json.dumps(vec.tolist())  # Convierte el ndarray a una lista y luego a JSON
    hist_json = json.dumps(hist.tolist())  # Convierte el ndarray a una lista y luego a JSON
    print(hist)
    # Insertar los datos en la tabla de la base de datos
    cur.execute("INSERT INTO elementos (texto, vector_caracteristico, histograma) VALUES (%s, %s, %s)", (str(filename), vec_json, hist_json))
# Cerrar la conexión a la base de datos
# Hacer commit para guardar los cambios
conn.commit()
cur.close()
conn.close()


