CREATE VIEW vw_kpi_geografico AS
SELECT 
    u.State AS Estado,
    u.City AS Ciudad,
    COUNT(f.fact_id) AS Total_Accidentes,
    -- Casteamos a FLOAT para obtener decimales en el promedio
    AVG(CAST(f.severity AS FLOAT)) AS Severidad_Promedio, 
    SUM(f.distance_mi) AS Distancia_Afectada_Total
FROM 
    fact_accidentes f
INNER JOIN 
    dim_ubicacion u ON f.fk_ubicacion = u.ubicacion_key
GROUP BY 
    u.State, 
    u.City;
GO