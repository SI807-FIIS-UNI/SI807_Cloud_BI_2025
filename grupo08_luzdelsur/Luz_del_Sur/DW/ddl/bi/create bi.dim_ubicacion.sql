CREATE OR REPLACE VIEW bi.dim_ubicacion AS
SELECT
    ubicacion_sk,
    id_ubicacion,
    distrito,
    zona,
    ubigeo
FROM dw.dim_ubicacion;