-- ============================================
-- A) Validar conteo de registros por tabla
-- ============================================
SELECT
  table_id,
  row_count,
  size_bytes,
  TIMESTAMP_MILLIS(creation_time) AS creation_time,
  TIMESTAMP_MILLIS(last_modified_time) AS last_modified
FROM `ventas_nettalco.__TABLES__`
ORDER BY row_count DESC;

-- ============================================
-- B) Revisar esquema
-- ============================================
SELECT 
  table_name,
  column_name,
  data_type
FROM `ventas_nettalco.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name;

-- ============================================
-- C) Mostrar primeras filas
-- ============================================
SELECT *
FROM `ventas_nettalco.total_prendas_por_talla`
LIMIT 10;

-- ============================================
-- 4.5 Validaciones específicas por tabla
-- ============================================

-- 1️⃣ Total de prendas
SELECT SUM(TOTAL_PRENDAS) AS total_prendas_suma
FROM `ventas_nettalco.total_prendas_por_talla`;

-- 2️⃣ Top clientes por volumen
SELECT 
  TCODICLIE,
  TOTAL_PRENDAS
FROM `ventas_nettalco.volumen_ventas_por_cliente`
ORDER BY TOTAL_PRENDAS DESC
LIMIT 10;

-- 3️⃣ Validación por franja horaria
SELECT 
  FRANJA_HORARIA,
  COUNT(*) AS registros,
  SUM(TOTAL_PRENDAS) AS total
FROM `ventas_nettalco.tendencias_ventas_por_franja_horaria`
GROUP BY FRANJA_HORARIA;

-- 4️⃣ Productos más vendidos
SELECT 
  ESTILO,
  TOTAL_PRENDAS
FROM `ventas_nettalco.productos_mas_vendidos`
ORDER BY TOTAL_PRENDAS DESC
LIMIT 15;

-- 5️⃣ Eficiencia operativa
SELECT 
  MIN(EFICIENCIA_PORCENTUAL) AS min_ef,
  MAX(EFICIENCIA_PORCENTUAL) AS max_ef
FROM `ventas_nettalco.eficiencia_operativa`;

-- 6️⃣ Tendencias con promedio móvil
SELECT 
  DATE(FECHA_TERMINO_TS) AS FECHA_TERMINO,
  ESTILO,
  TOTAL_PRENDAS,
  PROMEDIO_MOVIL
FROM `ventas_nettalco.prediccion_ventas`
ORDER BY FECHA_TERMINO DESC
LIMIT 20;

-- 7️⃣ Comportamiento del cliente
SELECT
  TCODICLIE,
  FRECUENCIA_COMPRA,
  PROMEDIO_PRENDAS
FROM `ventas_nettalco.comportamiento_clientes`
ORDER BY FRECUENCIA_COMPRA DESC;
