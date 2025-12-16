-- ============================
-- 01 - VALIDACIÓN GENERAL 
-- ============================

-- Conteo de registros por tabla
SELECT 'fact_flights_delay' AS tabla, COUNT(*) AS total FROM `FinalOrtiz.fact_flights_delay`
UNION ALL SELECT 'dim_date',     COUNT(*) FROM `FinalOrtiz.dim_date`
UNION ALL SELECT 'dim_carrier',  COUNT(*) FROM `FinalOrtiz.dim_carrier`
UNION ALL SELECT 'dim_airport',  COUNT(*) FROM `FinalOrtiz.dim_airport`
UNION ALL SELECT 'dim_aircraft', COUNT(*) FROM `FinalOrtiz.dim_aircraft`;
-- si tienes dim_route, descomenta:
-- UNION ALL SELECT 'dim_route', COUNT(*) FROM `examen-final-481401.FinalOrtiz.dim_route`;

-- ============================
-- Duplicados en claves primarias 
-- ============================

-- dim_date 
SELECT Date, COUNT(*) AS rep
FROM `examen-final-481401.FinalOrtiz.dim_date`
GROUP BY date
HAVING COUNT(*) > 1;

-- dim_carrier 
SELECT uniquecarrier, COUNT(*) AS rep
FROM `examen-final-481401.FinalOrtiz.dim_carrier`
GROUP BY uniquecarrier
HAVING COUNT(*) > 1;

-- dim_airport 
SELECT airport_code, COUNT(*) AS rep
FROM `examen-final-481401.FinalOrtiz.dim_airport`
GROUP BY airport_code
HAVING COUNT(*) > 1;

-- dim_aircraft 
SELECT TailNum, COUNT(*) AS rep
FROM `examen-final-481401.FinalOrtiz.dim_aircraft`
GROUP BY TailNum
HAVING COUNT(*) > 1;
