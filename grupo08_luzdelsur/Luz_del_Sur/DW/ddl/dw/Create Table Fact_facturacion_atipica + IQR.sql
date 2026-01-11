CREATE TABLE dw.fact_facturacion_atipica AS
WITH iqr AS (
    SELECT
        cliente_sk,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY energia_total) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY energia_total) AS q3
    FROM dw.fact_facturacion_mensual
    GROUP BY cliente_sk
),
bounds AS (
    SELECT
        cliente_sk,
        q1,
        q3,
        (q3 - q1) AS iqr,
        q1 - 1.5 * (q3 - q1) AS lower_bound,
        q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM iqr
),
variacion AS (
    SELECT
        cliente_sk,
        tiempo_sk,
        energia_total,
        LAG(energia_total) OVER (PARTITION BY cliente_sk ORDER BY tiempo_sk) AS energia_prev
    FROM dw.fact_facturacion_mensual
)
SELECT
    -- 1. FKs (surrogates)
    f.cliente_sk,
    f.suministro_sk,
    f.medidor_sk,
    f.tarifa_sk,
    f.ubicacion_sk,
    f.tiempo_sk,

    -- 2. Métricas
    f.energia_total,
    f.monto_facturado,

    -- 3. Límites IQR
    b.q1,
    b.q3,
    b.iqr,
    b.lower_bound,
    b.upper_bound,

    -- 4. Atípico por IQR
    CASE 
        WHEN f.energia_total < b.lower_bound 
          OR f.energia_total > b.upper_bound
        THEN TRUE ELSE FALSE
    END AS es_atipico_iqr,

    -- 5. Variación intermensual (>50%)
    CASE 
        WHEN v.energia_prev IS NOT NULL
         AND ABS(f.energia_total - v.energia_prev) / NULLIF(v.energia_prev,0) > 0.5
        THEN TRUE ELSE FALSE
    END AS es_atipico_variacion,

    -- 6. Flags de calidad del sistema
    f.es_energia_cero,
    f.es_energia_negativa,
    f.es_monto_negativo,
    f.es_nulo_energia,
    f.es_nulo_monto,

    -- 7. Bandera final: cualquier regla encendida
    CASE WHEN
        (f.energia_total < b.lower_bound OR f.energia_total > b.upper_bound)
        OR (v.energia_prev IS NOT NULL
            AND ABS(f.energia_total - v.energia_prev) / NULLIF(v.energia_prev,0) > 0.5)
        OR f.es_energia_cero
        OR f.es_energia_negativa
        OR f.es_monto_negativo
    THEN TRUE ELSE FALSE END AS es_atipico
FROM dw.fact_facturacion_mensual f
LEFT JOIN bounds    b USING (cliente_sk)
LEFT JOIN variacion v USING (cliente_sk, tiempo_sk);