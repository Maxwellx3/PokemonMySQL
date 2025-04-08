-- Tabla 'elementos': Almacena información sobre las imágenes

CREATE TABLE elementos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT,
    vector_caracteristico LONGTEXT,
    UNIQUE KEY (nombre(255))
);
