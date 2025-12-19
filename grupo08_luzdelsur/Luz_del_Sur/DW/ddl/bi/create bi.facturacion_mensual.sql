CREATE OR REPLACE VIEW bi.facturacion_mensual AS
SELECT
    f.*,
    c.tipo_cliente,
    u.distrito,
    u.zona,
    u.ubigeo,
    t.descripcion AS tarifa_desc,
    tm.anio      AS anio_dim,
    tm.mes       AS mes_dim,
    tm.anio_mes  AS periodo_dim,
    tm.fecha_mes AS fecha_dim
FROM dw.fact_facturacion_mensual f
LEFT JOIN dw.dim_cliente    c  ON f.cliente_sk   = c.cliente_sk
LEFT JOIN dw.dim_ubicacion  u  ON f.ubicacion_sk = u.ubicacion_sk
LEFT JOIN dw.dim_tarifa     t  ON f.tarifa_sk    = t.tarifa_sk
LEFT JOIN dw.dim_tiempo     tm ON f.tiempo_sk    = tm.tiempo_sk;