CREATE OR REPLACE VIEW dev.bi.vw_dash3_consumo_cliente AS
WITH base AS (
    SELECT
        f.*,
        LAG(f.energia_total) OVER (
            PARTITION BY f.suministro_sk
            ORDER BY f.anio, f.mes
        ) AS energia_prev
    FROM dev.dw.fact_facturacion_mensual f
)
SELECT
    b.suministro_sk,
    b.cliente_sk,
    b.tarifa_sk,
    b.ubicacion_sk,
    b.tiempo_sk,

    c.tipo_cliente,
    c.estado_cliente,
    u.distrito,
    u.zona,

    b.anio,
    b.mes,
    b.anio_mes,
    b.energia_total,
    b.monto_facturado,

    -- Consumo promedio por cliente
    AVG(b.energia_total) OVER (PARTITION BY b.cliente_sk)
        AS consumo_promedio_cliente,

    -- Variación mensual
    (b.energia_total - b.energia_prev) AS dif_consumo,

    CASE
        WHEN b.energia_prev = 0 OR b.energia_prev IS NULL THEN NULL
        ELSE (b.energia_total - b.energia_prev) / b.energia_prev * 100
    END AS variacion_consumo_pct,

    -- Percentil 90 global
    percentile_cont(0.9) WITHIN GROUP (ORDER BY b.energia_total)
        OVER () AS p90_consumo,

    CASE
        WHEN b.energia_total >
             percentile_cont(0.9) WITHIN GROUP (ORDER BY b.energia_total) OVER ()
        THEN 1 ELSE 0
    END AS es_consumo_alto,

    AVG(b.monto_facturado) OVER (PARTITION BY b.cliente_sk)
        AS ticket_promedio_cliente

FROM base b
LEFT JOIN dev.dw.dim_cliente     c ON b.cliente_sk     = c.cliente_sk
LEFT JOIN dev.dw.dim_ubicacion   u ON b.ubicacion_sk   = u.ubicacion_sk;