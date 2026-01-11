CREATE OR REPLACE VIEW bi.dim_medidor AS
SELECT
    medidor_sk,
    id_medidor,
    id_suministro,
    marca_medidor,
    tecnologia_medidor,
    numero_serie,
    fecha_instalacion,
    fecha_retiro,
    estado_medidor,
    medidor_activo
FROM dw.dim_medidor;