CREATE TABLE lds_silver.silver_suministro
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/silver/suministro/'
) AS
SELECT
    s.id_suministro,
    s.id_cliente,
    s.id_ubicacion,
    s.direccion_suministro,
    UPPER(s.nivel_tension)                  AS nivel_tension,
    s.id_sist_electrico                     AS id_sist_electrico,
    s.fecha_alta_suministro,
    UPPER(s.estado_suministro)              AS estado_suministro,
    (s.fecha_alta_suministro >= DATE '2023-01-01') AS es_suministro_nuevo
FROM lds_bronze.bronze_suministro s;

