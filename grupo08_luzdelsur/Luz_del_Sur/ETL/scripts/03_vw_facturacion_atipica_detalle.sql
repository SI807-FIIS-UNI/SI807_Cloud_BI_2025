CREATE OR REPLACE VIEW gold_db.vw_facturacion_atipica_detalle AS
SELECT
  g.id_suministro,
  g.id_medidor,
  g.anio_mes,
  SUBSTR(g.anio_mes, 1, 4) AS anio,
  SUBSTR(g.anio_mes, 6, 2) AS mes,
  s.zona,
  g.distrito,
  g.tipo_cliente,
  g.nivel_tension,
  g.cod_tarifa,
  g.energia_total_kwh,
  g.demanda_max_kw,
  g.n_registros,
  g.n_registros_error,
  g.pct_registros_error,
  g.facturacion_teorica,
  g.n_segmento,
  g.q1,
  g.q3,
  g.iqr,
  g.umbral_superior,
  g.es_atipico
FROM gold_db.gold_facturacion_teorica_mes g
JOIN bronze_db.bronze_suministro s
  ON g.id_suministro = s.id_suministro;
