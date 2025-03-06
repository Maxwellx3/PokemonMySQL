from math import dist
from traceback import print_tb
from img2vec_pytorch import Img2Vec
from PIL import Image
import numpy as np

# Inicializar el modelo (seleccionar el tipo de modelo)
# Puedes usar 'resnet-18', 'resnet-50', 'resnet-101', 'resnet-152', 'vgg-16' o 'vgg-19'
img2vec = Img2Vec(model='resnet50')  # Inicializar una sola vez fuera de la función

def obtener_vector_caracteristico(imagen_path):
    img = Image.open(imagen_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize((224, 224))
    vector = img2vec.get_vec(img)
    return np.round(vector, 4)

# Función para calcular el histograma de colores de una imagen
def calcular_histograma_de_colores(imagen_path):
    try:
        imagen = Image.open(imagen_path)
        imagen_np = np.array(imagen)
        hist_red, _ = np.histogram(imagen_np[:,:,0].ravel(), bins=256, range=(0, 256))
        hist_green, _ = np.histogram(imagen_np[:,:,1].ravel(), bins=256, range=(0, 256))
        hist_blue, _ = np.histogram(imagen_np[:,:,2].ravel(), bins=256, range=(0, 256))
        histograma = np.concatenate((hist_red, hist_green, hist_blue))
        return histograma
    except Exception as e:
        print(f"Error procesando {imagen_path}: {str(e)}")
        return np.zeros(768)  # Vector cero como fallback

def normalize_to_100(vector):
    min_val = np.min(vector)
    max_val = np.max(vector)
    
    normalized_vector = 100 * ((vector - min_val) / (max_val - min_val))
    
    return normalized_vector
