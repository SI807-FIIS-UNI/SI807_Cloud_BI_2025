CREATE VIEW vw_kpi_horas_criticas AS
SELECT 
    t.hora AS Hora_Dia,
    CASE 
        WHEN t.hora BETWEEN 6 AND 9 THEN 'Mañana (Hora Pico)'
        WHEN t.hora BETWEEN 16 AND 19 THEN 'Tarde (Hora Pico)'
        ELSE 'Horario Normal'
    END AS Franja_Horaria,
    COUNT(f.fact_id) AS Total_Accidentes,
    AVG(CAST(f.severity AS FLOAT)) AS Severidad_Promedio
FROM 
    fact_accidentes f
INNER JOIN 
    dim_tiempo t ON f.fk_tiempo_inicio = t.tiempo_key
GROUP BY 
    t.hora
-- Nota: En SQL Server las vistas no suelen llevar ORDER BY, 
-- el ordenamiento se hace al consultar la vista.
GO