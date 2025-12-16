CREATE VIEW vw_kpi_climatico AS
SELECT 
    c.Weather_Condition AS Condicion_Clima,
    c.Visibility_Mi AS Visibilidad_Promedio,
    COUNT(f.fact_id) AS Total_Accidentes,
    AVG(CAST(f.severity AS FLOAT)) AS Severidad_Promedio,
    -- KPI extra: % de accidentes graves (Severidad 3 o 4)
    (SUM(CASE WHEN f.severity >= 3 THEN 1 ELSE 0 END) * 100.0 / COUNT(f.fact_id)) AS Porcentaje_Accidentes_Graves
FROM 
    fact_accidentes f
INNER JOIN 
    dim_clima c ON f.fk_clima = c.clima_key
GROUP BY 
    c.Weather_Condition,
    c.Visibility_Mi;
GO