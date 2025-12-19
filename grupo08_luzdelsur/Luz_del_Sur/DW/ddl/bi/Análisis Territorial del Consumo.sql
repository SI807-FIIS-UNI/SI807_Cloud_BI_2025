CREATE OR REPLACE VIEW dev.bi.vw_dash4_geo_territorial AS
SELECT
    u.zona,
    u.distrito,

    -- Consumo y facturación
    AVG(f.energia_total)              AS consumo_promedio_distrito,
    AVG(f.monto_facturado)            AS ticket_promedio_distrito,

    -- Riesgo operativo
    AVG(CASE WHEN fa.es_atipico THEN 1 ELSE 0 END) * 100
                                      AS pct_registros_atipicos,

    -- Umbral alto de consumo
    PERCENTILE_CONT(0.9)
        WITHIN GROUP (ORDER BY f.energia_total)
                                      AS p90_consumo_distrito,

    -- Soporte de filtros
    f.anio,
    f.mes,
    f.anio_mes

FROM dev.dw.fact_facturacion_mensual f
JOIN dev.dw.dim_ubicacion u
  ON f.ubicacion_sk = u.ubicacion_sk
LEFT JOIN dev.dw.fact_facturacion_atipica fa
  ON fa.suministro_sk = f.suministro_sk
 AND fa.tiempo_sk     = f.tiempo_sk

GROUP BY
    u.zona,
    u.distrito,
    f.anio,
    f.mes,
    f.anio_mes;