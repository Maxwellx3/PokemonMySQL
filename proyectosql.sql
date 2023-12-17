create extension plpython3u;

CREATE TABLE elementos (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    vector_caracteristico FLOAT[],
	histograma FLOAT[]
);

CREATE TABLE pivotes (
    id_pivote serial PRIMARY KEY,
    pivote text,
	vector_caracteristico FLOAT[],
	histograma FLOAT[]
);

CREATE TABLE nodos (
    id_nodo serial PRIMARY KEY,
    distancia_vc REAL,
	distancia_his REAL, 
	id_pivote integer REFERENCES pivotes(id_pivote),
    nodo_padre integer REFERENCES nodos(id_nodo)
);

CREATE TABLE nodos_hoja (
	id_nodo_hoja integer REFERENCES nodos (id_nodo),
	id_elemento integer REFERENCES elementos (id),
    PRIMARY KEY (id_nodo_hoja, id_elemento)
);

CREATE TABLE log (
    id_log serial PRIMARY KEY,
    cadena text,
    fecha timestamp DEFAULT current_timestamp
);

insert into nodos (distancia_vc, distancia_his, id_pivote, nodo_padre) values ( null,null,null, null);


CREATE OR REPLACE FUNCTION distancia(p1 double precision[], p2 double precision[])
RETURNS double precision AS $$
    import math
    
    # Verificar que ambos vectores tengan la misma longitud
    if len(p1) != len(p2):
        raise ValueError("Los vectores deben tener la misma longitud")

    # Calcular la distancia euclidiana
    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    return distance
$$ LANGUAGE plpython3u;


-- Ejemplo de uso de la función
SELECT distancia(ARRAY[1.0, 2.0, 3.0], ARRAY[4.0, 5.0, 6.0]);

select distancia(e.vector_caracteristico,el.vector_caracteristico) from elementos e, elementos el
where e.id = 1 and el.id =2;




