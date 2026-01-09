-- ============================================================================
-- VALIDACIÓN COMPLETA: CUBO OLAP VS FACT TABLE
-- Proyecto: grupo09_retail_analytics
-- Dataset: dataset_si807_g9
-- Autor: Grupo 9
-- Fecha: 2025
-- ============================================================================

-- VALIDACIÓN 1: Comparación de Totales Generales (MÁS IMPORTANTE)
-- ============================================================================
WITH totales_generales AS (
    -- Totales del Cubo OLAP
    SELECT 
        'CUBO OLAP' AS origen,
        COUNT(*) AS num_registros,
        ROUND(SUM(total_ventas_netas), 2) AS total_ventas,
        SUM(total_unidades) AS total_unidades,
        SUM(total_tickets) AS total_tickets
    FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`
    
    UNION ALL
    
    -- Totales de la Fact Table
    SELECT 
        'FACT TABLE' AS origen,
        COUNT(*) AS num_registros,
        ROUND(SUM(monto_venta_neta), 2) AS total_ventas,
        SUM(num_secuencia) AS total_unidades,
        COUNT(DISTINCT cod_ticket) AS total_tickets
    FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated`
)
SELECT 
    origen,
    num_registros,
    total_ventas,
    total_unidades,
    total_tickets,
    -- Calcular diferencias
    total_ventas - LAG(total_ventas) OVER (ORDER BY origen DESC) AS diff_ventas,
    total_unidades - LAG(total_unidades) OVER (ORDER BY origen DESC) AS diff_unidades,
    total_tickets - LAG(total_tickets) OVER (ORDER BY origen DESC) AS diff_tickets,
    -- Calcular porcentaje de error
    ROUND(ABS(total_ventas - LAG(total_ventas) OVER (ORDER BY origen DESC)) / 
          NULLIF(LAG(total_ventas) OVER (ORDER BY origen DESC), 0) * 100, 4) AS error_ventas_pct,
    -- Status del resultado
    CASE 
        WHEN ABS(total_ventas - LAG(total_ventas) OVER (ORDER BY origen DESC)) < 0.01 
        THEN '✅ CORRECTO'
        WHEN ABS(total_ventas - LAG(total_ventas) OVER (ORDER BY origen DESC)) < 
             LAG(total_ventas) OVER (ORDER BY origen DESC) * 0.001 
        THEN '⚠️ TOLERANCIA ACEPTABLE'
        WHEN ABS(total_ventas - LAG(total_ventas) OVER (ORDER BY origen DESC)) < 
             LAG(total_ventas) OVER (ORDER BY origen DESC) * 0.05 
        THEN '🔴 DIFERENCIA GRAVE'
        ELSE '🔴🔴 DIFERENCIA CRÍTICA'
    END AS status
FROM totales_generales
ORDER BY origen DESC;


-- VALIDACIÓN 2: Comparación por Año
-- ============================================================================
WITH ventas_por_anio AS (
    SELECT 
        'CUBO OLAP' AS origen,
        anio,
        ROUND(SUM(total_ventas_netas), 2) AS total_ventas,
        SUM(total_unidades) AS total_unidades
    FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`
    GROUP BY anio
    
    UNION ALL
    
    SELECT 
        'FACT TABLE' AS origen,
        p.anio,
        ROUND(SUM(f.monto_venta_neta), 2) AS total_ventas,
        SUM(f.num_secuencia) AS total_unidades
    FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
    JOIN `etl-retail-analytics.dataset_si807_g9.dim_periodo_curated` p 
        ON f.sk_periodo = p.sk_periodo
    GROUP BY p.anio
)
SELECT 
    anio,
    MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) AS cubo_ventas,
    MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END) AS fact_ventas,
    ROUND(ABS(MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) - 
              MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END)), 2) AS diferencia,
    ROUND(ABS(MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) - 
              MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END)) / 
          NULLIF(MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END), 0) * 100, 4) AS error_pct,
    CASE 
        WHEN ABS(MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) - 
                 MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END)) < 0.01 
        THEN '✅ OK'
        ELSE '❌ ERROR'
    END AS status
FROM ventas_por_anio
GROUP BY anio
ORDER BY anio;


-- VALIDACIÓN 3: Comparación por Ciudad
-- ============================================================================
WITH ventas_por_ciudad AS (
    SELECT 
        'CUBO OLAP' AS origen,
        ciudad,
        ROUND(SUM(total_ventas_netas), 2) AS total_ventas
    FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`
    GROUP BY ciudad
    
    UNION ALL
    
    SELECT 
        'FACT TABLE' AS origen,
        t.ciudad,
        ROUND(SUM(f.monto_venta_neta), 2) AS total_ventas
    FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
    JOIN `etl-retail-analytics.dataset_si807_g9.dim_tienda_canal_curated` t 
        ON f.sk_tienda = t.sk_tienda
    GROUP BY t.ciudad
)
SELECT 
    ciudad,
    MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) AS cubo_ventas,
    MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END) AS fact_ventas,
    ROUND(ABS(MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) - 
              MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END)), 2) AS diferencia,
    CASE 
        WHEN ABS(MAX(CASE WHEN origen = 'CUBO OLAP' THEN total_ventas END) - 
                 MAX(CASE WHEN origen = 'FACT TABLE' THEN total_ventas END)) < 0.01 
        THEN '✅' ELSE '❌'
    END AS status
FROM ventas_por_ciudad
GROUP BY ciudad
ORDER BY fact_ventas DESC;


-- VALIDACIÓN 4: Verificar Duplicados en el Cubo
-- ============================================================================
SELECT 
    'Duplicados en Cubo OLAP' AS validacion,
    COUNT(*) AS total_registros,
    COUNT(DISTINCT CONCAT(
        CAST(anio AS STRING), '-',
        nombre_mes, '-',
        ciudad, '-',
        nombre_tienda, '-',
        categoria, '-',
        marca
    )) AS combinaciones_unicas,
    COUNT(*) - COUNT(DISTINCT CONCAT(
        CAST(anio AS STRING), '-',
        nombre_mes, '-',
        ciudad, '-',
        nombre_tienda, '-',
        categoria, '-',
        marca
    )) AS registros_duplicados,
    CASE 
        WHEN COUNT(*) = COUNT(DISTINCT CONCAT(
            CAST(anio AS STRING), '-',
            nombre_mes, '-',
            ciudad, '-',
            nombre_tienda, '-',
            categoria, '-',
            marca
        )) THEN '✅ SIN DUPLICADOS'
        ELSE '❌ HAY DUPLICADOS'
    END AS status
FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`;


-- VALIDACIÓN 5: Verificar Integridad Referencial
-- ============================================================================
SELECT 
    'Productos sin match' AS problema,
    COUNT(*) AS registros_afectados,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated`), 2) AS porcentaje,
    CASE WHEN COUNT(*) = 0 THEN '✅ OK' ELSE '❌ PROBLEMA' END AS status
FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
LEFT JOIN `etl-retail-analytics.dataset_si807_g9.dim_producto_curated` pr 
    ON f.sk_producto = pr.sk_producto
WHERE pr.sk_producto IS NULL

UNION ALL

SELECT 
    'Tiendas sin match',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated`), 2),
    CASE WHEN COUNT(*) = 0 THEN '✅ OK' ELSE '❌ PROBLEMA' END
FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
LEFT JOIN `etl-retail-analytics.dataset_si807_g9.dim_tienda_canal_curated` t 
    ON f.sk_tienda = t.sk_tienda
WHERE t.sk_tienda IS NULL

UNION ALL

SELECT 
    'Periodos sin match',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated`), 2),
    CASE WHEN COUNT(*) = 0 THEN '✅ OK' ELSE '❌ PROBLEMA' END
FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
LEFT JOIN `etl-retail-analytics.dataset_si807_g9.dim_periodo_curated` p 
    ON f.sk_periodo = p.sk_periodo
WHERE p.sk_periodo IS NULL;


-- VALIDACIÓN 6: Resumen Ejecutivo de Todas las Validaciones
-- ============================================================================
WITH validacion_totales AS (
    SELECT 
        'Totales Generales' AS validacion,
        CASE 
            WHEN ABS(
                (SELECT SUM(total_ventas_netas) FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`) -
                (SELECT SUM(monto_venta_neta) FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated`)
            ) < 0.01 THEN '✅ PASS'
            ELSE '❌ FAIL'
        END AS resultado,
        ROUND(ABS(
            (SELECT SUM(total_ventas_netas) FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`) -
            (SELECT SUM(monto_venta_neta) FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated`)
        ), 2) AS diferencia
),
validacion_duplicados AS (
    SELECT 
        'Sin Duplicados' AS validacion,
        CASE 
            WHEN COUNT(*) = COUNT(DISTINCT CONCAT(
                CAST(anio AS STRING), nombre_mes, ciudad, nombre_tienda, categoria, marca
            )) THEN '✅ PASS'
            ELSE '❌ FAIL'
        END AS resultado,
        COUNT(*) - COUNT(DISTINCT CONCAT(
            CAST(anio AS STRING), nombre_mes, ciudad, nombre_tienda, categoria, marca
        )) AS diferencia
    FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`
),
validacion_integridad AS (
    SELECT 
        'Integridad Referencial' AS validacion,
        CASE 
            WHEN (
                SELECT COUNT(*) 
                FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
                LEFT JOIN `etl-retail-analytics.dataset_si807_g9.dim_producto_curated` pr ON f.sk_producto = pr.sk_producto
                WHERE pr.sk_producto IS NULL
            ) = 0 THEN '✅ PASS'
            ELSE '❌ FAIL'
        END AS resultado,
        (
            SELECT COUNT(*) 
            FROM `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
            LEFT JOIN `etl-retail-analytics.dataset_si807_g9.dim_producto_curated` pr ON f.sk_producto = pr.sk_producto
            WHERE pr.sk_producto IS NULL
        ) AS diferencia
)
SELECT * FROM validacion_totales
UNION ALL
SELECT * FROM validacion_duplicados
UNION ALL
SELECT * FROM validacion_integridad;
