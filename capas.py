import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np

# Modelo completo
resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
resnet.eval()

# Accedé al bloque que querés (por ejemplo, layer4[1])
bloque = resnet.layer4[1]

# Submodelo hasta conv3
modelo_conv3 = torch.nn.Sequential(
    resnet.conv1,
    resnet.bn1,
    resnet.relu,
    resnet.maxpool,
    resnet.layer1,
    resnet.layer2,
    resnet.layer3,
    resnet.layer4[0],
    torch.nn.Sequential(  # replicar el bloque [1] hasta conv3
        bloque.conv1,
        bloque.bn1,
        bloque.relu,
        bloque.conv2,
        bloque.bn2,
        bloque.relu,
        bloque.conv3  # aquí cortamos
    )
)

# Submodelo hasta bn3
modelo_bn3 = torch.nn.Sequential(
    *modelo_conv3,
    bloque.bn3
)

# Submodelo hasta relu final
modelo_relu = torch.nn.Sequential(
    *modelo_bn3,
    bloque.relu
)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

def obtener_vector_caracteristico(imagen_path, modelo_deseado):
    img = Image.open(imagen_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)  # [1, 3, 224, 224]
    with torch.no_grad():
        features = modelo_deseado(tensor)
        if len(features.shape) > 2:
            features = torch.flatten(features, start_dim=1)  # [1, N]
        features = features / features.norm(dim=1, keepdim=True)  # Normalizar
        vector = features.squeeze().numpy()
    return np.round(vector, 4)
