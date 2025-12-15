CREATE OR REPLACE VIEW bi.dim_cliente AS
SELECT
    cliente_sk,
    id_cliente,
    tipo_cliente,
    fecha_alta,
    estado_cliente,
    antiguedad_anios,
    tiene_email,
    tiene_celular,
    id_ubicacion
FROM dw.dim_cliente;