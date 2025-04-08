import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Cargar ResNet50 con pesos actualizados
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()  # Modo evaluación
# Quitar la capa de clasificación (obteniendo la salida de la capa de pooling final)
model = torch.nn.Sequential(*list(model.children())[:-1])

# Definir las transformaciones
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                         std=[0.229, 0.224, 0.225])
])

def obtener_vector_caracteristico(imagen_path):
    img = Image.open(imagen_path).convert("RGB")
    img = transform(img).unsqueeze(0)  # Agregar dimensión de batch
    with torch.no_grad():
        features = model(img)  # Salida con forma (1, 2048, 1, 1)
        # Aplanar a (1, 2048)
        features = features.view(features.size(0), -1)
        # Normalizar el vector (L2 normalization)
        features = features / features.norm(dim=1, keepdim=True)
        vector = features.squeeze().numpy()
    return np.round(vector, 4)
