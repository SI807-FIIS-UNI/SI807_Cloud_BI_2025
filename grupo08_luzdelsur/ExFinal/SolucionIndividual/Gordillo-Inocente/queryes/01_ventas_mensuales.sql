-- Query 1: Analisis de ventas mensuales por sucursal
-- Objetivo: Identificar tendencias temporales y performance por branch

SELECT 
    t.ano,
    t.mes,
    t.nombre_mes,
    s.branch,
    s.city,
    COUNT(f.venta_id) as total_transacciones,
    SUM(f.sales) as ventas_totales,
    SUM(f.gross_income) as margen_bruto,
    AVG(f.sales) as ticket_promedio,
    ROUND(SUM(f.gross_income) / SUM(f.sales) * 100, 2) as margen_porcentaje
FROM 
    fact_ventas f
    INNER JOIN dim_tiempo t ON f.tiempo_key = t.tiempo_key
    INNER JOIN dim_sucursal s ON f.sucursal_key = s.sucursal_key
GROUP BY 
    t.ano, t.mes, t.nombre_mes, s.branch, s.city
ORDER BY 
    t.ano, t.mes, ventas_totales DESC;
