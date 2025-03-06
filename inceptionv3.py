import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

def cargar_modelo(nombre_modelo):
    """
    Carga un modelo preentrenado según el nombre especificado.
    :param nombre_modelo: Nombre del modelo ('inceptionv3', 'vgg16', etc.)
    :return: Modelo cargado en modo evaluación
    """
    if nombre_modelo == 'inceptionv3':
        modelo = models.inception_v3(pretrained=True)
    elif nombre_modelo == 'vgg16':
        modelo = models.vgg16(pretrained=True)
    else:
        raise ValueError(f"Modelo '{nombre_modelo}' no soportado")
    
    modelo.eval()
    return modelo

def obtener_vector_caracteristico(imagen_path, nombre_modelo='inceptionv3'):
    """
    Obtiene el vector característico de una imagen usando el modelo especificado.
    :param imagen_path: Ruta de la imagen
    :param nombre_modelo: Nombre del modelo ('inceptionv3', 'vgg16', etc.)
    :return: Vector característico como numpy array
    """
    modelo = cargar_modelo(nombre_modelo)

    # Transformaciones para preprocesar la imagen
    if nombre_modelo == 'inceptionv3':
        transformacion = transforms.Compose([
            transforms.Resize(299),
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
    else:
        transformacion = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    # Abrir la imagen y aplicar transformaciones
    imagen = Image.open(imagen_path)
    imagen = transformacion(imagen).unsqueeze(0)

    # Obtener el vector característico
    with torch.no_grad():
        vector_caracteristico = modelo(imagen)

    return vector_caracteristico.squeeze().numpy()
