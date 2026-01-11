CREATE TABLE lds_silver.silver_medidor
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/silver/medidor/'
) AS
SELECT
    m.id_medidor,
    m.id_suministro,
    m.marca_medidor,
    m.tecnologia_medidor            AS tecnologia_medidor,
    m.numero_serie,
    m.fecha_instalacion,
    CASE 
        WHEN m.fecha_retiro IS NOT NULL 
             AND m.fecha_retiro < m.fecha_instalacion 
        THEN NULL
        ELSE m.fecha_retiro
    END                            AS fecha_retiro,
    UPPER(m.estado_medidor)        AS estado_medidor,
    (m.fecha_retiro IS NULL)       AS medidor_activo
FROM lds_bronze.bronze_medidor m;
