import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

# Cargar ResNet50 con los pesos actualizados
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()  # Modo evaluación
model = torch.nn.Sequential(*list(model.children())[:-1])  # Quitar la capa de clasificación

# Transformaciones para la imagen
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def obtener_vector_caracteristico(imagen_path):
    img = Image.open(imagen_path).convert("RGB")
    img = transform(img).unsqueeze(0)  # Agregar dimensión de batch
    with torch.no_grad():
        vector = model(img).squeeze().numpy()  # Obtener el vector característico
    return np.round(vector, 4)

def calcular_histograma_de_colores(imagen_path):
    """
    Calcula y normaliza el histograma de colores de una imagen.
    
    Retorna:
        np.ndarray: Histograma normalizado (concatenado para los canales R, G y B).
    """
    try:
        imagen = Image.open(imagen_path)
        imagen_np = np.array(imagen)
        # Calcular histogramas para cada canal
        hist_red, _ = np.histogram(imagen_np[:, :, 0].ravel(), bins=256, range=(0, 256))
        hist_green, _ = np.histogram(imagen_np[:, :, 1].ravel(), bins=256, range=(0, 256))
        hist_blue, _ = np.histogram(imagen_np[:, :, 2].ravel(), bins=256, range=(0, 256))
        # Concatenar histogramas
        histograma = np.concatenate((hist_red, hist_green, hist_blue))
        # Normalizar dividiendo por la suma total (o número de píxeles)
        total = np.sum(histograma)
        if total > 0:
            histograma_normalizado = histograma / total
        else:
            histograma_normalizado = histograma
        return histograma_normalizado
    except Exception as e:
        print(f"Error procesando {imagen_path}: {str(e)}")
        return np.zeros(768)  # Vector cero como fallback

def normalize_to_100(vector):
    min_val = np.min(vector)
    max_val = np.max(vector)
    if max_val == min_val:
        return np.zeros_like(vector)
    normalized_vector = 100 * ((vector - min_val) / (max_val - min_val))
    
    return normalized_vector
