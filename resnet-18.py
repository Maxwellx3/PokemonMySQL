from img2vec_pytorch import Img2Vec
from PIL import Image
import numpy as np
import os

# Inicializar el modelo (seleccionar el tipo de modelo)
# Puedes usar 'resnet-18', 'resnet-50', 'resnet-101', 'resnet-152', 'vgg-16' o 'vgg-19'
img2vec = Img2Vec(model='resnet-18')

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

# Rutas de las imágenes
ruta_imagen1 = 'abra.jpg'
ruta_carpeta = './poke'
# Preprocesar las imágenes
img1 = preprocess_image(ruta_imagen1)
# Obtener los vectores de características de las dos imágenes
vec1 = img2vec.get_vec(img1)
his1 = calcular_histograma_de_colores(ruta_imagen1)

for filename in os.listdir(ruta_carpeta):
    img2 = preprocess_image(os.path.join(ruta_carpeta, filename))
    vec2 = img2vec.get_vec(img2)
    distance = np.linalg.norm(vec1 - vec2)
    print(distance)

print('Histograma')
for filename in os.listdir(ruta_carpeta):
    img2 = calcular_histograma_de_colores(os.path.join(ruta_carpeta, filename))
    distance = np.linalg.norm(his1 - img2)
    print(distance)

