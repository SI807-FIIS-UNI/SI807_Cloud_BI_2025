CREATE TABLE bronze_db.bronze_suministro (
  id_suministro      BIGINT,
  id_cliente         BIGINT,
  id_sector          BIGINT,
  distrito           VARCHAR,
  zona               VARCHAR,
  nivel_tension      VARCHAR,
  tipo_suministro    VARCHAR,
  fecha_alta         DATE,
  estado_suministro  VARCHAR
);
