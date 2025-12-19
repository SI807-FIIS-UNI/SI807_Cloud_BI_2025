-- Query 2: Top lineas de producto por ventas y margen
-- Objetivo: Identificar productos mas rentables para estrategia comercial

SELECT 
    p.product_line,
    COUNT(f.venta_id) as total_transacciones,
    SUM(f.quantity) as unidades_vendidas,
    SUM(f.sales) as ventas_totales,
    SUM(f.gross_income) as margen_bruto,
    AVG(f.rating) as rating_promedio,
    ROUND(SUM(f.gross_income) / SUM(f.sales) * 100, 2) as margen_porcentaje,
    ROUND(AVG(f.sales), 2) as ticket_promedio
FROM 
    fact_ventas f
    INNER JOIN dim_producto p ON f.producto_key = p.producto_key
GROUP BY 
    p.product_line
ORDER BY 
    ventas_totales DESC;
