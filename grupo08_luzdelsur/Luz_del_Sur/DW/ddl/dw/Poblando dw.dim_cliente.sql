INSERT INTO dw.dim_cliente
(
    id_cliente,
    tipo_cliente,
    fecha_alta,
    estado_cliente,
    antiguedad_anios,
    tiene_email,
    tiene_celular,
    id_ubicacion
)
SELECT DISTINCT   -- por si acaso, para evitar duplicados de clientes
    id_cliente,
    tipo_cliente,
    fecha_alta,
    estado_cliente,
    antiguedad_anios,
    tiene_email,
    tiene_celular,
    id_ubicacion
FROM staging.dim_cliente;