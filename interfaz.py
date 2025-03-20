import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import os
import json
from new_proyecto import obtener_top_10_similares, comparar_pokemones  # Importa las funciones definidas


seleccion_actual_1 = None
seleccion_actual_2 = None

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "303336",
    "database": "gaperros"
}

CARPETA_IMAGENES = "./gaperros"  # Carpeta donde están las imágenes

# Función para obtener las fotos desde MySQL
def obtener_fotos():
    conexion = mysql.connector.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM elementos")  # Ajusta el nombre de la tabla y columna
    fotos = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return fotos

# Función para mostrar la pantalla de búsqueda de imágenes similares
def buscar_similares():
    pantalla_inicio.pack_forget()
    pantalla_busqueda.pack(fill=tk.BOTH, expand=True)
    lista_fotos.delete(0, tk.END)
    for foto in obtener_fotos():
        lista_fotos.insert(tk.END, foto)

def comparar_imagenes():
    pantalla_inicio.pack_forget()
    pantalla_comparacion.pack(fill=tk.BOTH, expand=True)
    lista_fotos_1.delete(0, tk.END)
    lista_fotos_2.delete(0, tk.END)
    for foto in obtener_fotos():
        lista_fotos_1.insert(tk.END, foto)
        lista_fotos_2.insert(tk.END, foto)

# Función para mostrar la imagen seleccionada y sus 10 similares
def mostrar_imagen(event):
    seleccion = lista_fotos.curselection()
    if seleccion:
        id_foto = lista_fotos.get(seleccion[0])
        ruta_imagen = os.path.join(CARPETA_IMAGENES, id_foto)
        
        if os.path.exists(ruta_imagen):
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((300, 300), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(imagen)
            label_imagen.config(image=img_tk)
            label_imagen.image = img_tk
            
            # Obtener las 10 imágenes más similares
            conexion = mysql.connector.connect(**DB_CONFIG)
            cursor = conexion.cursor()
            similares = obtener_top_10_similares(id_foto, cursor)
            conexion.close()
            
            # Mostrar miniaturas de las imágenes similares
            for widget in frame_similares.winfo_children():
                widget.destroy()
            
            for i, (nombre_similar, _) in enumerate(similares):
                ruta_similar = os.path.join(CARPETA_IMAGENES, nombre_similar)
                if os.path.exists(ruta_similar):
                    img_similar = Image.open(ruta_similar)
                    img_similar = img_similar.resize((100, 100), Image.Resampling.LANCZOS)
                    img_similar_tk = ImageTk.PhotoImage(img_similar)
                    lbl = tk.Label(frame_similares, image=img_similar_tk)
                    lbl.image = img_similar_tk
                    lbl.grid(row=0, column=i, padx=5, pady=5)
        else:
            label_imagen.config(image=None, text="Imagen no encontrada")

# Función para mostrar la previsualización de la imagen seleccionada en la comparación
def mostrar_previsualizacion(event, lista, label, seleccion_global):
    global seleccion_actual_1, seleccion_actual_2
    
    seleccion = lista.curselection()
    if seleccion:
        id_foto = lista.get(seleccion[0])
        ruta_imagen = os.path.join(CARPETA_IMAGENES, id_foto)
        
        if os.path.exists(ruta_imagen):
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(imagen)
            label.config(image=img_tk)
            label.image = img_tk
            
            # Guardar la selección actual en la variable global correcta
            if seleccion_global == "1":
                seleccion_actual_1 = id_foto
            elif seleccion_global == "2":
                seleccion_actual_2 = id_foto


# Función para comparar dos imágenes
def calcular_distancia():
    global seleccion_actual_1, seleccion_actual_2
    
    if seleccion_actual_1 and seleccion_actual_2:
        conexion = mysql.connector.connect(**DB_CONFIG)
        cursor = conexion.cursor()
        distancia = comparar_pokemones(seleccion_actual_1, seleccion_actual_2, cursor)
        conexion.close()
        
        label_resultado.config(text=f"Distancia: {distancia:.4f}")
    else:
        label_resultado.config(text="Seleccione dos imágenes")


# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Buscador de Fotos")

# Pantalla de inicio
pantalla_inicio = tk.Frame(root)
tk.Label(pantalla_inicio, text="Seleccione una opción", font=("Arial", 16)).pack(pady=10)
tk.Button(pantalla_inicio, text="Buscar imágenes similares", command=buscar_similares).pack(pady=5)
tk.Button(pantalla_inicio, text="Comparar dos imágenes", command=comparar_imagenes).pack(pady=5)
pantalla_inicio.pack(fill=tk.BOTH, expand=True)

# Pantalla de búsqueda de imágenes 10 similares
pantalla_busqueda = tk.Frame(root)
entry_busqueda = tk.Entry(pantalla_busqueda)
entry_busqueda.pack(fill=tk.X, padx=10, pady=5)
frame_lista = tk.Frame(pantalla_busqueda)
frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
scrollbar = tk.Scrollbar(frame_lista)
lista_fotos = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
scrollbar.config(command=lista_fotos.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
lista_fotos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
label_imagen = tk.Label(pantalla_busqueda, text="Selecciona una foto", bg="gray")
label_imagen.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
frame_similares = tk.Frame(pantalla_busqueda)
frame_similares.pack(fill=tk.X, padx=10, pady=5)
lista_fotos.bind("<<ListboxSelect>>", mostrar_imagen)

# Pantalla de comparación de imágenes
pantalla_comparacion = tk.Frame(root)
tk.Label(pantalla_comparacion, text="Seleccione dos imágenes para comparar", font=("Arial", 14)).pack(pady=5)
frame_comparacion = tk.Frame(pantalla_comparacion)
frame_comparacion.pack()
lista_fotos_1 = tk.Listbox(frame_comparacion, height=10)
lista_fotos_1.pack(side=tk.LEFT, padx=5)
label_previsualizacion_1 = tk.Label(frame_comparacion)
label_previsualizacion_1.pack(side=tk.LEFT, padx=5)
lista_fotos_2 = tk.Listbox(frame_comparacion, height=10)
lista_fotos_2.pack(side=tk.RIGHT, padx=5)
label_previsualizacion_2 = tk.Label(frame_comparacion)
label_previsualizacion_2.pack(side=tk.RIGHT, padx=5)
tk.Button(pantalla_comparacion, text="Calcular Distancia", command=calcular_distancia).pack(pady=5)
label_resultado = tk.Label(pantalla_comparacion, text="Distancia: ", font=("Arial", 12))
label_resultado.pack()

lista_fotos_1.bind("<<ListboxSelect>>", lambda event: mostrar_previsualizacion(event, lista_fotos_1, label_previsualizacion_1, "1"))
lista_fotos_2.bind("<<ListboxSelect>>", lambda event: mostrar_previsualizacion(event, lista_fotos_2, label_previsualizacion_2, "2"))

root.mainloop()