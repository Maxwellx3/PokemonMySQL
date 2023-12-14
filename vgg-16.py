import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

def obtener_vector_caracteristico_VGG16(imagen_path):
    # Cargar el modelo VGG-16 pre-entrenado
    modelo = models.vgg16(pretrained=True)
    # Colocar el modelo en modo de evaluación (no entrenamiento)
    modelo.eval()
    
    # Transformar la imagen para que coincida con los requisitos del modelo VGG-16
    transformacion = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    imagen = Image.open(imagen_path)
    imagen = transformacion(imagen).unsqueeze(0)  # Agregar una dimensión adicional para batch
    
    # Obtener el vector característico de la imagen con VGG-16
    with torch.no_grad():
        vector_caracteristico = modelo(imagen)
    
    return vector_caracteristico.squeeze().numpy()  # Convertir a numpy array y quitar la dimensión de batch

# Ejemplo de uso
ruta_imagen = 'abra.jpg'  # Reemplaza con la ruta de tu imagen
vector_caracteristico_vgg16 = obtener_vector_caracteristico_VGG16(ruta_imagen)
print("Vector Característico con VGG-16:")
print(vector_caracteristico_vgg16)
