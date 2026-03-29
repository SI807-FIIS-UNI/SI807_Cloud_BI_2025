CREATE OR REPLACE VIEW bi.facturacion_atipica AS
SELECT
    -- Fact (claves)
    f.cliente_sk,
    f.suministro_sk,
    f.medidor_sk,
    f.tarifa_sk,
    f.ubicacion_sk,
    f.tiempo_sk,

    -- Métricas
    f.energia_total,
    f.monto_facturado,

    -- Estadísticos IQR
    f.q1,
    f.q3,
    f.iqr,
    f.lower_bound,
    f.upper_bound,

    -- Flags de atipicidad
    f.es_atipico_iqr,
    f.es_atipico_variacion,
    f.es_energia_cero,
    f.es_energia_negativa,
    f.es_monto_negativo,
    f.es_nulo_energia,
    f.es_nulo_monto,
    f.es_atipico,

    -- Dim Cliente
    c.tipo_cliente,
    c.estado_cliente,
    c.antiguedad_anios,
    c.tiene_email,
    c.tiene_celular,

    -- Dim Ubicación (ajustado a tus columnas)
    u.distrito,
    u.zona,
    u.ubigeo,

    -- Dim Tarifa
    t.descripcion       AS tarifa_desc,
    t.codigo_tarifa     AS tarifa_codigo,
    t.nivel_tension     AS tarifa_tension,
    t.segmento_objetivo AS tarifa_segmento,

    -- Dim Tiempo
    tm.anio      AS anio_dim,
    tm.mes       AS mes_dim,
    tm.anio_mes  AS periodo_dim,
    tm.fecha_mes AS fecha_dim

FROM dw.fact_facturacion_atipica f
LEFT JOIN dw.dim_cliente    c  ON f.cliente_sk   = c.cliente_sk
LEFT JOIN dw.dim_ubicacion  u  ON f.ubicacion_sk = u.ubicacion_sk
LEFT JOIN dw.dim_tarifa     t  ON f.tarifa_sk    = t.tarifa_sk
LEFT JOIN dw.dim_tiempo     tm ON f.tiempo_sk    = tm.tiempo_sk;