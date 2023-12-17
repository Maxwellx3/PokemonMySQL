from math import dist
from traceback import print_tb
from img2vec_pytorch import Img2Vec
from PIL import Image
import numpy as np

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
    img = img2vec.get_vec(img)
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

def normalize_to_100(vector):
    min_val = np.min(vector)
    max_val = np.max(vector)
    
    normalized_vector = 100 * ((vector - min_val) / (max_val - min_val))
    
    return normalized_vector
'''
ruta1 = 'abra.jpg'
ruta2 = 'alakazam.jpg'

img1 = preprocess_image(ruta1)  

img2 =  preprocess_image(ruta2)

distance = np.linalg.norm(img1 - img2)

print(distance)

his1 = normalize_to_100(calcular_histograma_de_colores(ruta1))
his2 = normalize_to_100(calcular_histograma_de_colores(ruta2))


distance = np.linalg.norm(his1-his2)

print(distance)

concatenado1 = np.concatenate((img1,his1))
concatenado2 = np.concatenate((img2,his2))

print(np.linalg.norm(concatenado1-concatenado2))
ruta_carpeta1 = './pokemon_images_shiny'''


'''
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
    
    print(vec)
    # Insertar los datos en la tabla de la base de datos
    cur.execute("INSERT INTO elementos (texto, vector_caracteristico, histograma) VALUES (%s, %s, %s)", (str(filename), vec_json, hist_json))
# Cerrar la conexión a la base de datos
# Hacer commit para guardar los cambios
conn.commit()
cur.close()
conn.close()
'''