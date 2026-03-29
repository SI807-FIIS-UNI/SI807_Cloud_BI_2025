CREATE TABLE lds_gold.dim_suministro
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/dim_suministro/'
) AS
SELECT
    s.id_suministro,
    s.id_cliente,
    s.id_ubicacion,
    s.direccion_suministro,
    s.nivel_tension,
    s.id_sist_electrico,
    s.fecha_alta_suministro,
    s.estado_suministro,
    s.es_suministro_nuevo
FROM lds_silver.silver_suministro s;
