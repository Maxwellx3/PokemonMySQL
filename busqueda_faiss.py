import faiss
import numpy as np

def construir_indice(vectores):
    """
    Construye el índice FAISS a partir de una lista de vectores.
    Cada vector debe ser una lista de floats.
    """
    dimension = len(vectores[0])
    index = faiss.IndexFlatL2(dimension)
    datos = np.array(vectores, dtype='float32')
    index.add(datos)
    return index

def buscar_similares(index, vector_consulta, top_k=10):
    """
    Devuelve los índices y distancias de los top_k vectores más similares.
    """
    consulta = np.array([vector_consulta], dtype='float32')
    distancias, indices = index.search(consulta, top_k)
    return indices[0], distancias[0]

def calcular_distancia_faiss(vector1, vector2):
    """
    Calcula la distancia euclidiana usando FAISS entre dos vectores.
    """
    v1 = np.array([vector1], dtype='float32')
    v2 = np.array(vector2, dtype='float32')
    index = faiss.IndexFlatL2(len(vector1))
    index.add(v2.reshape(1, -1))
    distancias, _ = index.search(v1, 1)
    return distancias[0][0]