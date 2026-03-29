CREATE OR REPLACE VIEW bi.dim_suministro AS
SELECT
    suministro_sk,
    id_suministro,
    id_cliente,
    id_ubicacion,
    direccion_suministro,
    nivel_tension,
    id_sist_electrico,
    fecha_alta_suministro,
    estado_suministro,
    es_suministro_nuevo
FROM dw.dim_suministro;