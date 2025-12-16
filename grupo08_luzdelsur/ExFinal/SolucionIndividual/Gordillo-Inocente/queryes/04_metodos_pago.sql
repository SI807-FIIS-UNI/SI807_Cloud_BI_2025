-- Query 4: Analisis de metodos de pago por sucursal
-- Objetivo: Identificar preferencias de pago para optimizar operaciones

SELECT 
    s.city,
    s.branch,
    pg.payment_method,
    COUNT(f.venta_id) as total_transacciones,
    SUM(f.sales) as ventas_totales,
    ROUND(AVG(f.sales), 2) as ticket_promedio,
    ROUND(COUNT(f.venta_id) * 100.0 / SUM(COUNT(f.venta_id)) OVER (PARTITION BY s.city), 2) as porcentaje_ciudad
FROM 
    fact_ventas f
    INNER JOIN dim_sucursal s ON f.sucursal_key = s.sucursal_key
    INNER JOIN dim_pago pg ON f.pago_key = pg.pago_key
GROUP BY 
    s.city, s.branch, pg.payment_method
ORDER BY 
    s.city, total_transacciones DESC;
