-- 02. DIM_UBICACION: Validación de buckets geográficos
SELECT
  COUNT(*) AS total_buckets,
  COUNT(DISTINCT CONCAT(CAST(lat_bucket AS STRING), '-', CAST(lng_bucket AS STRING))) AS buckets_distintos
FROM `us-accidents-481401.us_accidents_dw.dim_ubicacion`;
