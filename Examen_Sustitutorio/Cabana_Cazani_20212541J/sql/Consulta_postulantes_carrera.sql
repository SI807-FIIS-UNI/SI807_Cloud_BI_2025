SELECT 
    t.anio,
    c.nombre_carrera,
    COUNT(*) as total_postulantes,
    SUM(f.ingreso_flag) as total_ingresantes,
    ROUND((SUM(f.ingreso_flag) / COUNT(*)) * 100, 2) as tasa_ingreso_pct
FROM db_cepreuni1.fact_admision f
JOIN db_cepreuni1.dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN db_cepreuni1.dim_carrera c ON f.id_carrera = c.id_carrera
GROUP BY t.anio, c.nombre_carrera
ORDER BY total_postulantes DESC
LIMIT 20