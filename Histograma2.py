from img2vec_pytorch import Img2Vec
from PIL import Image
import numpy as np

# Función para obtener el vector característico de una imagen usando Img2Vec (ResNet-18)
def obtener_vector_caracteristico(imagen_path):
    img2vec = Img2Vec(model='vgg-16')
    img = Image.open(imagen_path)
    # Convertir la imagen a formato RGB si es RGBA
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    # Redimensionar la imagen a las dimensiones aceptadas por el modelo (224x224)
    img = img.resize((224, 224))
    # Obtener el vector característico de la imagen
    vector_caracteristico = img2vec.get_vec(img)
    # Truncar los valores del vector a 4 decimales
    vector_caracteristico_truncado = np.round(vector_caracteristico, 4)
    return vector_caracteristico_truncado

# Establecer opciones de impresión para mostrar los valores en notación decimal
np.set_printoptions(suppress=True)

# Función para calcular el histograma de colores de una imagen
def calcular_histograma_de_colores(imagen_path):
    imagen = Image.open(imagen_path)
    imagen_np = np.array(imagen)
    hist_red, _ = np.histogram(imagen_np[:,:,0].ravel(), bins=256, range=(0, 256))
    hist_green, _ = np.histogram(imagen_np[:,:,1].ravel(), bins=256, range=(0, 256))
    hist_blue, _ = np.histogram(imagen_np[:,:,2].ravel(), bins=256, range=(0, 256))
    histograma = np.concatenate((hist_red, hist_green, hist_blue))
    return histograma

# Ruta de la imagen
ruta_imagen = 'abra.jpg'

# Obtener el vector característico de la imagen
vector_caracteristico = obtener_vector_caracteristico(ruta_imagen)
print("Vector Característico:")
print(vector_caracteristico)

# Obtener el histograma de colores de la imagen
histograma = calcular_histograma_de_colores(ruta_imagen)
print("\nHistograma de Colores (vector):")
print(histograma)
