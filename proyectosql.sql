-- Tabla 'elementos': Almacena información sobre las imágenes

CREATE TABLE elementos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT,
    vector_caracteristico TEXT,
    histograma TEXT,
    UNIQUE KEY (nombre(255))
);

CREATE TABLE pivotes (
    id_pivote INT AUTO_INCREMENT PRIMARY KEY,
    pivote TEXT,
    vector_caracteristico TEXT,
    histograma TEXT
);

CREATE TABLE nodos (
    id_nodo INT AUTO_INCREMENT PRIMARY KEY,
    distancia_vc REAL,
    distancia_his REAL, 
    id_pivote INT,
    nodo_padre INT,
    FOREIGN KEY (id_pivote) REFERENCES pivotes(id_pivote),
    FOREIGN KEY (nodo_padre) REFERENCES nodos(id_nodo)
);

CREATE TABLE nodos_hoja (
    id_nodo_hoja INT,
    id_elemento INT,
    PRIMARY KEY (id_nodo_hoja, id_elemento),
    FOREIGN KEY (id_nodo_hoja) REFERENCES nodos(id_nodo),
    FOREIGN KEY (id_elemento) REFERENCES elementos(id)
);

CREATE TABLE log (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    cadena TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into nodos (distancia_vc, distancia_his, id_pivote, nodo_padre) values ( null,null,null, null);
