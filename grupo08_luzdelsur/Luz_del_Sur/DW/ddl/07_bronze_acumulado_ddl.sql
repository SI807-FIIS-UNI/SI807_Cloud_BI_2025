CREATE TABLE bronze_db.bronze_acumulado (
  id_suministro      BIGINT,
  id_medidor         BIGINT,
  anio_mes           VARCHAR,
  energia_total_kwh  DOUBLE,
  demanda_max_kw     DOUBLE,
  n_registros        BIGINT,
  n_registros_error  BIGINT
);
