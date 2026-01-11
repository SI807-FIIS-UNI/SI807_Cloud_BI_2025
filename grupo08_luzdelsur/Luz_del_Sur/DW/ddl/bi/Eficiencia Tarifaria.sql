CREATE OR REPLACE VIEW dev.bi.vw_dash5_tarifa_kpi AS
SELECT
    f.suministro_sk,
    f.tarifa_sk,
    f.cliente_sk,
    f.ubicacion_sk,
    f.tiempo_sk,

    t.codigo_tarifa,
    t.tipo_cliente,
    t.cargo_fijo,
    t.cargo_energia,

    f.anio,
    f.mes,
    f.anio_mes,

    f.energia_total,
    f.monto_facturado AS monto_real,

    -- Monto teórico
    (t.cargo_fijo + t.cargo_energia * f.energia_total) AS monto_teorico,

    -- Eficiencia tarifaria (%)
    CASE
        WHEN (t.cargo_fijo + t.cargo_energia * f.energia_total) = 0 THEN NULL
        ELSE f.monto_facturado
             / (t.cargo_fijo + t.cargo_energia * f.energia_total) * 100
    END AS eficiencia_tarifaria_pct,

    -- Brecha (%)
    CASE
        WHEN (t.cargo_fijo + t.cargo_energia * f.energia_total) = 0 THEN NULL
        ELSE (f.monto_facturado - (t.cargo_fijo + t.cargo_energia * f.energia_total))
             / (t.cargo_fijo + t.cargo_energia * f.energia_total) * 100
    END AS pct_brecha_tarifaria,

    -- Consumo promedio por tarifa
    AVG(f.energia_total) OVER (PARTITION BY f.tarifa_sk)
        AS consumo_promedio_tarifa

FROM dev.dw.fact_facturacion_mensual f
LEFT JOIN dev.dw.dim_tarifa t ON f.tarifa_sk = t.tarifa_sk;