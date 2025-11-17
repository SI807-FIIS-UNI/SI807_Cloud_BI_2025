-- ============================================================================
-- POBLACIÓN DEL CUBO OLAP
-- Proyecto: grupo09_retail_analytics
-- Dataset: dataset_si807_g9
-- Autor: Grupo 9
-- Fecha: 2025
-- ============================================================================

-- PASO 1: Limpiar tabla antes de insertar (evita duplicados)
-- ============================================================================
TRUNCATE TABLE `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`;


-- PASO 2: Insertar datos agregados desde CURATED
-- ============================================================================
INSERT INTO `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`
SELECT
    -- Dimensiones del GROUP BY
    p.anio,
    p.nombre_mes,
    t.ciudad,
    t.nombre_tienda,
    pr.categoria,
    pr.marca,

    -- Métricas Calculadas
    ROUND(SUM(f.monto_venta_neta), 2) AS total_ventas_netas,
    SUM(f.num_secuencia) AS total_unidades,
    COUNT(DISTINCT f.cod_ticket) AS total_tickets

FROM
    `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` f
    
INNER JOIN
    `etl-retail-analytics.dataset_si807_g9.dim_periodo_curated` p 
    ON f.sk_periodo = p.sk_periodo
    
INNER JOIN
    `etl-retail-analytics.dataset_si807_g9.dim_tienda_canal_curated` t 
    ON f.sk_tienda = t.sk_tienda
    
INNER JOIN
    `etl-retail-analytics.dataset_si807_g9.dim_producto_curated` pr 
    ON f.sk_producto = pr.sk_producto

-- Agrupación por todas las dimensiones
GROUP BY
    p.anio,
    p.nombre_mes,
    t.ciudad,
    t.nombre_tienda,
    pr.categoria,
    pr.marca;


-- PASO 3: Verificar resultado
-- ============================================================================
SELECT 
    'Cubo OLAP poblado exitosamente' AS status,
    COUNT(*) AS total_combinaciones,
    ROUND(SUM(total_ventas_netas), 2) AS total_ventas,
    SUM(total_unidades) AS total_unidades,
    SUM(total_tickets) AS total_tickets
FROM `etl-retail-analytics.dataset_si807_g9.resumen_ventas_analytics`;
