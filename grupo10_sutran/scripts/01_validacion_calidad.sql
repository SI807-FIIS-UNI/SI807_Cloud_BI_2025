-- ============================
-- 01 - VALIDACIÓN GENERAL
-- ============================

-- Conteo de registros por tabla
SELECT 'hechos_siniestros' AS tabla, COUNT(*) AS total FROM `sutran.hechos_siniestros`
UNION ALL SELECT 'dim_persona',  COUNT(*) FROM `sutran.dim_persona`
UNION ALL SELECT 'dim_vehiculo', COUNT(*) FROM `sutran.dim_vehiculo`
UNION ALL SELECT 'dim_tiempo',   COUNT(*) FROM `sutran.dim_tiempo`
UNION ALL SELECT 'dim_tipo_via', COUNT(*) FROM `sutran.dim_tipo_via`;

-- Duplicados en claves primarias
SELECT id_persona, COUNT(*) AS rep
FROM `sutran.dim_persona`
GROUP BY id_persona
HAVING COUNT(*) > 1;

SELECT id_vehiculo, COUNT(*) AS rep
FROM `sutran.dim_vehiculo`
GROUP BY id_vehiculo
HAVING COUNT(*) > 1;

SELECT id_tiempo, COUNT(*) AS rep
FROM `sutran.dim_tiempo`
GROUP BY id_tiempo
HAVING COUNT(*) > 1;

SELECT id_tipo_via, COUNT(*) AS rep
FROM `sutran.dim_tipo_via`
GROUP BY id_tipo_via
HAVING COUNT(*) > 1;

-- Validación de claves foráneas nulas en hechos
SELECT
  COUNT(*) AS total_registros,
  COUNTIF(id_persona IS NULL)   AS nulos_persona,
  COUNTIF(id_vehiculo IS NULL)  AS nulos_vehiculo,
  COUNTIF(id_tiempo IS NULL)    AS nulos_tiempo,
  COUNTIF(id_tipo_via IS NULL)  AS nulos_tipo_via
FROM `sutran.hechos_siniestros`;

-- Validación de coordenadas inválidas
SELECT *
FROM `sutran.hechos_siniestros`
WHERE latitud IS NULL 
   OR longitud IS NULL
   OR latitud NOT BETWEEN -90 AND 90
   OR longitud NOT BETWEEN -180 AND 180;

