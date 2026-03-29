CREATE OR REPLACE VIEW bi.dim_tiempo AS
SELECT
    tiempo_sk,
    anio_mes,
    anio,
    mes,
    fecha_mes
FROM dw.dim_tiempo;