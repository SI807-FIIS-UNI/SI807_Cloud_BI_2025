CREATE TABLE lds_gold.dim_medidor
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/dim_medidor/'
) AS
SELECT
    m.id_medidor,
    m.id_suministro,
    m.marca_medidor,
    m.tecnologia_medidor,
    m.numero_serie,
    m.fecha_instalacion,
    m.fecha_retiro,
    m.estado_medidor,
    m.medidor_activo
FROM lds_silver.silver_medidor m;
