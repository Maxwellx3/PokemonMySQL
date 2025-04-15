import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from db import obtener_fotos, obtener_cursor
from calculos import obtener_top_10_similares, comparar_animales, comparar_con_imagen_externa, obtener_top_10_similares_externa, MAX_DISTANCIA

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
CARPETA_IMAGENES = "./gaperros"
ruta_imagen_externa = None

seleccion_actual_1 = None
seleccion_actual_2 = None

root = tk.Tk()
root.title("Buscador de Fotos")

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

def ir_a_comparacion_con_externa():
    pantalla_inicio.pack_forget()
    pantalla_busqueda.pack_forget()
    pantalla_comparacion.pack_forget()
    lista_fotos_base.delete(0, tk.END)
    for foto in obtener_fotos():
        lista_fotos_base.insert(tk.END, foto)
    # Muestra la pantalla de comparación externa
    pantalla_externa.pack(fill=tk.BOTH, expand=True)

def calcular_similitudes_externa(ruta_externa):
    conn, cursor = obtener_cursor()
    try:
        # Usar la nueva función optimizada
        similares = obtener_top_10_similares_externa(ruta_externa, cursor)
        mostrar_resultados_similares_externa(similares)
    finally:
        conn.close()

def buscar_similares_externa():
    pantalla_inicio.pack_forget()
    pantalla_busqueda_externa.pack(fill=tk.BOTH, expand=True)
    
    # Limpiar resultados previos
    label_imagen_externa.config(image=None, text="Selecciona una imagen externa")
    for widget in frame_similares_externa.winfo_children():
        widget.destroy()

def seleccionar_imagen_externa_top10():
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png")])
    if ruta:
        mostrar_imagen_externa(ruta)
        calcular_similitudes_externa(ruta)

def mostrar_imagen_externa(ruta):
    try:
        imagen = Image.open(ruta).resize((300, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(imagen)
        label_imagen_externa.config(image=img_tk, text="")
        label_imagen_externa.image = img_tk
    except Exception as e:
        label_imagen_externa.config(text="Error al cargar imagen externa")

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
            conn, cursor = obtener_cursor()
            similares = obtener_top_10_similares(id_foto, cursor)
            conn.close()
            for widget in frame_similares.winfo_children():
                widget.destroy()
            for i, (nombre_similar, distancia) in enumerate(similares):
                ruta_similar = os.path.join(CARPETA_IMAGENES, nombre_similar)
                if os.path.exists(ruta_similar):
                    img_similar = Image.open(ruta_similar).resize((100, 100), Image.Resampling.LANCZOS)
                    img_similar_tk = ImageTk.PhotoImage(img_similar)
                    similitud = max(0, 100 * (1 - ((distancia) / (MAX_DISTANCIA))))
                    frame_item = tk.Frame(frame_similares)
                    frame_item.grid(row=0, column=i, padx=5, pady=5)
                    lbl_img = tk.Label(frame_item, image=img_similar_tk)
                    lbl_img.image = img_similar_tk
                    lbl_img.pack()
                    tk.Label(frame_item, text=f"Distancia: {distancia:.4f}\nSimilitud: {similitud:.2f}%", font=("Arial", 10)).pack() #text=f"{similitud:.2f}%", font=("Arial", 10) #text=f"Distancia: {distancia:.4f}\nSimilitud: {similitud:.2f}%"
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
            imagen = Image.open(ruta_imagen).resize((200, 200), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(imagen)
            label.config(image=img_tk)
            label.image = img_tk
            if seleccion_global == "1":
                seleccion_actual_1 = id_foto
            elif seleccion_global == "2":
                seleccion_actual_2 = id_foto

def mostrar_previsualizacion_externa(ruta, label):
    if os.path.exists(ruta):
        try:
            imagen = Image.open(ruta).resize((200, 200), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(imagen)
            label.config(image=img_tk)
            label.image = img_tk  # Mantener referencia
            label.config(text="")  # Eliminar texto "Sin imagen cargada"
        except Exception as e:
            label.config(text="Error al cargar imagen externa")

def mostrar_resultados_similares_externa(resultados):
    # Limpiar frame anterior
    for widget in frame_similares_externa.winfo_children():
        widget.destroy()
    
    # Mostrar cada resultado
    for i, (nombre_img, distancia) in enumerate(resultados):
        ruta_img = os.path.join(CARPETA_IMAGENES, nombre_img)
        if os.path.exists(ruta_img):
            frame = tk.Frame(frame_similares_externa)
            frame.grid(row=0, column=i, padx=5, pady=5)
            
            # Miniatura
            img = Image.open(ruta_img).resize((100, 100), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            lbl_img = tk.Label(frame, image=img_tk)
            lbl_img.image = img_tk
            lbl_img.pack()
            
            # Texto
            similitud = max(0, 100 * (1 - (distancia / MAX_DISTANCIA)))
            tk.Label(frame, text=f"Distancia: {distancia:.4f}\nSimilitud: {similitud:.2f}%", 
                    font=("Arial", 8)).pack()

def seleccionar_imagen_externa():
    global ruta_imagen_externa
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png")])
    if ruta:
        ruta_imagen_externa = ruta
        mostrar_previsualizacion_externa(ruta, label_previsualizacion_externa)  # reutilizamos label de la derecha

        if seleccion_actual_1:
            conn, cursor = obtener_cursor()
            try:
                distancia = comparar_con_imagen_externa(seleccion_actual_1, ruta, cursor)
                conn.close()
                if distancia != 0:
                    similitud = max(0, 100 * (1 - ((distancia) / (MAX_DISTANCIA))))
                else:
                    similitud = 100
                label_resultado_externa.config(text=f"Distancia: {distancia:.4f}\nSimilitud: {similitud:.2f}%")
            except Exception as e:
                label_resultado_externa.config(text=str(e))
        else:
            label_resultado_externa.config(text="Seleccione primero una imagen de la base de datos")

# Función para comparar dos imágenes
def calcular_distancia():
    global seleccion_actual_1, seleccion_actual_2
    
    if seleccion_actual_1 and seleccion_actual_2:
        conn, cursor = obtener_cursor()
        try:
            distancia = comparar_animales(seleccion_actual_1, seleccion_actual_2, cursor)
        except ValueError as e:
            distancia = None
            label_resultado.config(text=str(e))
        conn.close()
        if distancia is not None:
            if distancia != 0:
                similitud = max(0, 100 * (1 - ((distancia) / (MAX_DISTANCIA))))
            else: similitud = 100
            label_resultado.config(text=f"Distancia: {distancia:.4f}\nSimilitud: {similitud:.2f}%")
    else:
        label_resultado.config(text="Seleccione dos imágenes")

# Función para volver al inicio
def volver_inicio():
    pantalla_busqueda.pack_forget()
    pantalla_comparacion.pack_forget()
    pantalla_externa.pack_forget()
    pantalla_busqueda_externa.pack_forget()
    pantalla_inicio.pack(fill=tk.BOTH, expand=True)



pantalla_actual = None
# Pantalla de inicio
pantalla_inicio = tk.Frame(root)
tk.Label(pantalla_inicio, text="Seleccione una opción", font=("Arial", 16)).pack(pady=10)
tk.Button(pantalla_inicio, text="Buscar imágenes similares", command=buscar_similares).pack(pady=5)
tk.Button(pantalla_inicio, text="Comparar dos imágenes", command=comparar_imagenes).pack(pady=5)
tk.Button(pantalla_inicio, text="Comparar con imagen externa", command=ir_a_comparacion_con_externa).pack(pady=5)
tk.Button(pantalla_inicio, text="Buscar similares para imagen externa", 
         command=buscar_similares_externa).pack(pady=5)


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
tk.Button(pantalla_busqueda, text="Volver al inicio", command=volver_inicio).pack(pady=5)

pantalla_externa = tk.Frame(root)
tk.Label(pantalla_externa, text="Seleccione una imagen de la base y cargue una externa", font=("Arial", 14)).pack(pady=5)
frame_externa = tk.Frame(pantalla_externa)
frame_externa.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
# Lista de la base de datos (izquierda)
frame_izquierdo = tk.Frame(frame_externa)
frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_lista_base = tk.Frame(frame_izquierdo)
frame_lista_base.pack(padx=5, fill=tk.BOTH, expand=True)
scrollbar_base = tk.Scrollbar(frame_lista_base, orient=tk.VERTICAL)
lista_fotos_base = tk.Listbox(frame_lista_base, height=10, yscrollcommand=scrollbar_base.set)
scrollbar_base.config(command=lista_fotos_base.yview)
scrollbar_base.pack(side=tk.RIGHT, fill=tk.Y)
lista_fotos_base.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
label_previsualizacion_base = tk.Label(frame_izquierdo, text="Sin imagen cargada")
label_previsualizacion_base.pack(pady=10)
# Imagen externa (derecha)
frame_externa_derecha = tk.Frame(frame_externa)
frame_externa_derecha.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH, expand=True)
label_previsualizacion_externa = tk.Label(frame_externa_derecha, text="Sin imagen cargada")
label_previsualizacion_externa.pack(pady=10)
tk.Button(frame_externa_derecha, text="Cargar Imagen Externa", command=seleccionar_imagen_externa).pack(pady=5)
# Resultado y volver
label_resultado_externa = tk.Label(pantalla_externa, text="Distancia: ", font=("Arial", 12))
label_resultado_externa.pack()
tk.Button(pantalla_externa, text="Volver al inicio", command=volver_inicio).pack(pady=5)
# Bind de selección en la lista de la base
# Cambiar el binding original por:
lista_fotos_base.bind("<<ListboxSelect>>", 
    lambda e: mostrar_previsualizacion(e, lista_fotos_base, label_previsualizacion_base, "1"))


# Pantalla de comparación de imágenes
pantalla_comparacion = tk.Frame(root)
tk.Label(pantalla_comparacion, text="Seleccione dos imágenes para comparar", font=("Arial", 14)).pack(pady=5)
frame_comparacion = tk.Frame(pantalla_comparacion)
frame_comparacion.pack()

frame_lista1 = tk.Frame(frame_comparacion)
frame_lista1.pack(side=tk.LEFT, padx=5)
scrollbar1 = tk.Scrollbar(frame_lista1, orient=tk.VERTICAL)
lista_fotos_1 = tk.Listbox(frame_lista1, height=10, yscrollcommand=scrollbar1.set)
scrollbar1.config(command=lista_fotos_1.yview)
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
lista_fotos_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
label_previsualizacion_1 = tk.Label(frame_comparacion)
label_previsualizacion_1.pack(side=tk.LEFT, padx=5)

frame_lista2 = tk.Frame(frame_comparacion)
frame_lista2.pack(side=tk.RIGHT, padx=5)
scrollbar2 = tk.Scrollbar(frame_lista2, orient=tk.VERTICAL)
lista_fotos_2 = tk.Listbox(frame_lista2, height=10, yscrollcommand=scrollbar2.set)
scrollbar2.config(command=lista_fotos_2.yview)
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
lista_fotos_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
label_previsualizacion_2 = tk.Label(frame_comparacion)
label_previsualizacion_2.pack(side=tk.RIGHT, padx=5)

tk.Button(pantalla_comparacion, text="Calcular Distancia", command=calcular_distancia).pack(pady=5)
label_resultado = tk.Label(pantalla_comparacion, text="Distancia: ", font=("Arial", 12))
label_resultado.pack()
tk.Button(pantalla_comparacion, text="Volver al inicio", command=volver_inicio).pack(pady=5)

lista_fotos_1.bind("<<ListboxSelect>>", lambda event: mostrar_previsualizacion(event, lista_fotos_1, label_previsualizacion_1, "1"))
lista_fotos_2.bind("<<ListboxSelect>>", lambda event: mostrar_previsualizacion(event, lista_fotos_2, label_previsualizacion_2, "2"))

pantalla_busqueda_externa = tk.Frame(root)
# Cabecera
tk.Label(pantalla_busqueda_externa, text="Buscar similares para imagen externa", 
        font=("Arial", 14)).pack(pady=10)
# Botón de carga
tk.Button(pantalla_busqueda_externa, text="Cargar Imagen Externa", 
        command=seleccionar_imagen_externa_top10).pack(pady=5)
# Preview imagen externa
label_imagen_externa = tk.Label(pantalla_busqueda_externa, bg="gray", 
                               text="Selecciona una imagen externa")
label_imagen_externa.pack(fill=tk.X, padx=10, pady=5)
# Frame para resultados
frame_similares_externa = tk.Frame(pantalla_busqueda_externa)
frame_similares_externa.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
tk.Button(pantalla_busqueda_externa, text="Volver al inicio", 
        command=volver_inicio).pack(pady=10)

root.mainloop()