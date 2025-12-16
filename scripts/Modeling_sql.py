CREATE OR REPLACE TABLE `sot_analytics.dim_contrata` AS 
SELECT id_contrata, nombre, zona FROM `sot_analytics.stg_contratas`;

CREATE OR REPLACE TABLE `sot_analytics.fact_sot` 
PARTITION BY fecha_creacion AS 
SELECT 
    s.id_sot, s.id_contrata, s.fecha_creacion, s.fecha_planificada, s.fecha_cierre,
    s.estado_sot, s.tiempo_planificado_min, s.tiempo_real_min, s.tiempo_excedente,
    IF(s.estado_sot = 'INSTALADA', 1, 0) as es_instalada,
    IF(s.estado_sot = 'FRAUDE', 1, 0) as es_fraude
FROM `sot_analytics.stg_sots` s;