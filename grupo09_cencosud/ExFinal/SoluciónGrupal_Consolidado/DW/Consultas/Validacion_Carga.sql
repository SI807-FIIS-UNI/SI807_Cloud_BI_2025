-- Contar registros en cada tabla RAW
SELECT 'dim_cliente_raw' AS tabla, COUNT(*) AS registros 
FROM `dataset_si807_g9.dim_cliente_raw`
UNION ALL
SELECT 'dim_periodo_raw', COUNT(*) 
FROM `dataset_si807_g9.dim_periodo_raw`
UNION ALL
SELECT 'dim_producto_raw', COUNT(*) 
FROM `dataset_si807_g9.dim_producto_raw`
UNION ALL
SELECT 'dim_promocion_raw', COUNT(*) 
FROM `dataset_si807_g9.dim_promocion_precio_raw`
UNION ALL
SELECT 'dim_tienda_raw', COUNT(*) 
FROM `dataset_si807_g9.dim_tienda_canal_raw`
UNION ALL
SELECT 'fact_venta_raw', COUNT(*) 
FROM `dataset_si807_g9.fact_hecho_venta_raw`;
