SELECT 
    t.anio,
    
    -- KPI GESTIÓN 1: Demanda (Volumen)
    COUNT(*) as total_postulantes,
    
    -- KPI GESTIÓN 2: Competitividad (Postulantes por cada vacante)
    ROUND(COUNT(*) / SUM(f.ingreso_flag), 1) as postulantes_por_vacante,
    
    -- KPI ACADÉMICO 1: Promedio de Notas (Nivel académico)
    ROUND(AVG(f.puntaje_final), 2) as promedio_nota_general,
    
    -- KPI ACADÉMICO 2: Tasa de Ingreso (% de éxito)
    ROUND((SUM(f.ingreso_flag) / COUNT(*)) * 100, 2) as tasa_ingreso_pct

FROM db_cepreuni1.fact_admision f
JOIN db_cepreuni1.dim_tiempo t ON f.id_tiempo = t.id_tiempo
GROUP BY t.anio
ORDER BY t.anio DESC