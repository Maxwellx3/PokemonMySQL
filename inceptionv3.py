import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

def obtener_vector_caracteristico_InceptionV3(imagen_path):
    # Cargar el modelo pre-entrenado InceptionV3
    modelo = models.inception_v3(pretrained=True)
    # Colocar el modelo en modo de evaluación (no entrenamiento)
    modelo.eval()
    
    # Transformaciones para preprocesar la imagen
    transformacion = transforms.Compose([
        transforms.Resize(299),  # Redimensionar a tamaño 299x299 (InceptionV3)
        transforms.CenterCrop(299),  # Recortar al centro
        transforms.ToTensor(),  # Convertir a tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalizar
    ])
    
    # Abrir la imagen y aplicar transformaciones
    imagen = Image.open(imagen_path)
    imagen = transformacion(imagen).unsqueeze(0)  # Agregar una dimensión adicional para batch
    
    # Obtener el vector característico de la imagen con InceptionV3
    with torch.no_grad():
        vector_caracteristico = modelo(imagen)
    
    return vector_caracteristico.squeeze().numpy()  # Convertir a numpy array y quitar la dimensión de batch

# Ejemplo de uso
ruta_imagen = 'abra.jpg'  # Reemplaza con la ruta de tu imagen
vector_caracteristico_inceptionv3 = obtener_vector_caracteristico_InceptionV3(ruta_imagen)
print("Vector Característico con InceptionV3:")
print(vector_caracteristico_inceptionv3)
