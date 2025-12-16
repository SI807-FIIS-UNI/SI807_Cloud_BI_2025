-- Query 3: Segmentacion de clientes por tipo y ciudad
-- Objetivo: Analizar comportamiento de compra por perfil de cliente

SELECT 
    c.customer_type,
    c.gender,
    s.city,
    COUNT(f.venta_id) as total_transacciones,
    SUM(f.sales) as ventas_totales,
    SUM(f.gross_income) as margen_bruto,
    ROUND(AVG(f.sales), 2) as ticket_promedio,
    ROUND(AVG(f.quantity), 2) as cantidad_promedio,
    ROUND(AVG(f.rating), 2) as rating_promedio
FROM 
    fact_ventas f
    INNER JOIN dim_cliente c ON f.cliente_key = c.cliente_key
    INNER JOIN dim_sucursal s ON f.sucursal_key = s.sucursal_key
GROUP BY 
    c.customer_type, c.gender, s.city
ORDER BY 
    ventas_totales DESC;
