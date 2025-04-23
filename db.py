import mysql.connector

# Configuración de la conexión a MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "port": 3307,
    "database": "gaperros"
}

def conectar_db():
    """Establece y devuelve una conexión a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)

def obtener_cursor():
    """Devuelve una conexión y su cursor."""
    conn = conectar_db()
    return conn, conn.cursor()

def obtener_fotos():
    """Recupera la lista de nombres de imágenes almacenadas en la tabla 'elementos'."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM elementos")
    fotos = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return fotos
