CREATE OR REPLACE VIEW dev.bi.vw_dash2_facturacion_irregular_v2 AS
WITH base AS (
    SELECT
        f.*,
        LAG(f.monto_facturado) OVER (
            PARTITION BY f.suministro_sk
            ORDER BY f.anio, f.mes
        ) AS monto_prev
    FROM dev.dw.fact_facturacion_mensual f
),
stats AS (
    SELECT
        b.*,

        -- Variación en soles
        (b.monto_facturado - b.monto_prev) AS dif_monto,

        -- Variación porcentual
        CASE
            WHEN b.monto_prev IS NULL OR b.monto_prev = 0 THEN NULL
            ELSE (b.monto_facturado - b.monto_prev) / b.monto_prev * 100
        END AS variacion_monto_pct,

        -- Costo efectivo por kWh
        CASE WHEN b.energia_total > 0
             THEN b.monto_facturado / b.energia_total
        END AS costo_kwh,

        -- Estadísticas globales por suministro (para boxplots)
        AVG(b.monto_facturado) OVER (PARTITION BY b.suministro_sk)
            AS promedio_suministro,

        STDDEV(b.monto_facturado) OVER (PARTITION BY b.suministro_sk)
            AS stddev_suministro,

        percentile_cont(0.9) WITHIN GROUP (ORDER BY b.monto_facturado)
            OVER (PARTITION BY b.suministro_sk) AS p90_suministro

    FROM base b
)
SELECT
    s.suministro_sk,
    s.cliente_sk,
    s.tarifa_sk,
    s.ubicacion_sk,
    s.tiempo_sk,

    c.tipo_cliente,
    c.estado_cliente,

    u.distrito,
    u.zona,

    t.codigo_tarifa,
    t.segmento_objetivo,

    s.anio,
    s.mes,
    s.anio_mes,

    s.energia_total,
    s.monto_facturado,

    -- KPI importantes
    s.dif_monto,
    s.variacion_monto_pct,
    s.costo_kwh,

    -- Estadísticas
    s.promedio_suministro,
    s.stddev_suministro,
    s.p90_suministro,

    -- Flags del sistema
    s.es_energia_cero,
    s.es_energia_negativa,
    s.es_monto_negativo,
    s.es_nulo_energia,
    s.es_nulo_monto,

    -- Flags de atípicos (ya calculados en DW)
    fa.es_atipico_iqr,
    fa.es_atipico_variacion,
    fa.es_atipico

FROM stats s
LEFT JOIN dev.dw.dim_cliente   c ON s.cliente_sk   = c.cliente_sk
LEFT JOIN dev.dw.dim_tarifa    t ON s.tarifa_sk    = t.tarifa_sk
LEFT JOIN dev.dw.dim_ubicacion u ON s.ubicacion_sk = u.ubicacion_sk
LEFT JOIN dev.dw.fact_facturacion_atipica fa
       ON fa.suministro_sk = s.suministro_sk
      AND fa.tiempo_sk     = s.tiempo_sk;