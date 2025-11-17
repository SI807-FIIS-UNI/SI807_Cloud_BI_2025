CREATE TABLE silver_db.silver_consumo_mensual (
  id_suministro       BIGINT,
  id_medidor          BIGINT,
  anio_mes            VARCHAR,
  energia_total_kwh   DOUBLE,
  demanda_max_kw      DOUBLE,
  n_registros         BIGINT,
  n_registros_error   BIGINT,
  pct_registros_error DOUBLE
);
