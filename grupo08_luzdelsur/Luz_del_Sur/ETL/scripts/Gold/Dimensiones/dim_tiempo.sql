CREATE TABLE lds_gold.dim_tiempo
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/dim_tiempo/'
) AS
SELECT DISTINCT
    c.anio_mes,
    CAST(c.anio AS INTEGER) AS anio,
    CAST(c.mes AS INTEGER)  AS mes,
    -- construir YYYY-MM-01 y castear a DATE
    CAST(
        CONCAT(
            c.anio, '-',
            LPAD(c.mes, 2, '0'),
            '-01'
        ) AS DATE
    ) AS fecha_mes
FROM lds_silver.silver_consolidado_mensual c;

