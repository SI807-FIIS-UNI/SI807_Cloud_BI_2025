CREATE TABLE bronze_db.bronze_medidor (
  id_medidor        BIGINT,
  nro_medidor       VARCHAR,
  id_suministro     BIGINT,
  tipo_medidor      VARCHAR,
  tecnologia        VARCHAR,
  modelo            VARCHAR,
  marca             VARCHAR,
  constante         DOUBLE,
  tension_nominal   VARCHAR,
  fecha_instalacion DATE,
  fecha_retiro      DATE,
  estado_medidor    VARCHAR,
  es_principal      VARCHAR
);
