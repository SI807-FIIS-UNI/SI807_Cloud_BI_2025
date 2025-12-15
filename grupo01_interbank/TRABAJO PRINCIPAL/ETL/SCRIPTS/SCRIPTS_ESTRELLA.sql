-- DIM_CANAL
CREATE OR REPLACE TABLE `project-sin-477115.ESTRELLA.DIM_CANAL` AS
SELECT
  ROW_NUMBER() OVER (ORDER BY canal) AS id_canal,
  canal AS nombre_canal
FROM (
  SELECT DISTINCT canal FROM `project-sin-477115.refined_data.tlv_ranking`
  UNION ALL
  SELECT DISTINCT canal FROM `project-sin-477115.refined_data.virtual_ranking`
  UNION ALL
  SELECT DISTINCT canal FROM `project-sin-477115.refined_data.tiendas_ranking`
);

-- DIM_EJECUTIVO
CREATE OR REPLACE TABLE `project-sin-477115.ESTRELLA.DIM_EJECUTIVO` AS
SELECT
  ROW_NUMBER() OVER (ORDER BY ejecutivo, jefe) AS id_ejecutivo,
  ejecutivo AS nombre_ejecutivo,
  jefe AS nombre_jefe
FROM (
  SELECT DISTINCT ejecutivo, jefe FROM `project-sin-477115.refined_data.tlv_ranking`
  UNION DISTINCT
  SELECT DISTINCT ejecutivo, jefe FROM `project-sin-477115.refined_data.virtual_ranking`
  UNION DISTINCT
  SELECT DISTINCT ejecutivo, jefe FROM `project-sin-477115.refined_data.tiendas_ranking`
);

-- DIM_FECHA
CREATE OR REPLACE TABLE `project-sin-477115.ESTRELLA.DIM_FECHA` AS
SELECT
  CAST(REPLACE(fecha_raw, '-', '') AS INT64) AS id_fecha,
  DATE(fecha_raw) AS fecha,
  CAST(SUBSTR(REPLACE(fecha_raw, '-', ''), 1, 6) AS INT64) AS periodo,
  1 AS dia_util_flag,
  0 AS dia_final_util,
  CAST(SUBSTR(REPLACE(fecha_raw, '-', ''), 1, 4) AS INT64) AS anio,
  CAST(SUBSTR(REPLACE(fecha_raw, '-', ''), 5, 2) AS INT64) AS mes_num,
  'DESCONOCIDO' AS nombre_dia_semana
FROM (
  SELECT DISTINCT dia AS fecha_raw
  FROM `project-sin-477115.refined_data.registro_comunicaciones`
  UNION DISTINCT
  SELECT DISTINCT SUBSTR(fecha, 1, 10) AS fecha_raw
  FROM `project-sin-477115.refined_data.cli_cambios`
);


-- DIM_CLIENTE
CREATE OR REPLACE TABLE `project-sin-477115.ESTRELLA.DIM_CLIENTE` AS
WITH temp_cambios_clientes_reciente AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY `Codigo Unico`
      ORDER BY fecha DESC
    ) AS rn
  FROM `project-sin-477115.refined_data.cli_cambios`
)
SELECT
  ROW_NUMBER() OVER (ORDER BY u.`Codigo Unico`) AS id_cliente,
  u.`Codigo Unico`,
  COALESCE(s.ruc, c.ruc) AS ruc,
  c.nombre AS nombre_cliente,
  s.`Segmento FX`,
  s.`Tipo Cuenta`,
  s.logeo,
  s.`Num Logeos`,
  s.`Flg Dig`,
  CASE 
    WHEN c.utilidad < 500 AND c.`Codigo Unico` IS NOT NULL THEN 1
    ELSE 0
  END AS flag_fuga
FROM (
  -- Clientes desde SEGMENTOS (ya normalizado)
  SELECT DISTINCT
    `Codigo Unico`,
    ruc
  FROM `project-sin-477115.refined_data.segmentos`

  UNION DISTINCT

  -- Clientes desde cli_cambios (renombrando correctamente)
  SELECT DISTINCT
    `Codigo Unico` AS codigo_unico,
    ruc
  FROM `project-sin-477115.refined_data.cli_cambios`
) u
LEFT JOIN `project-sin-477115.refined_data.segmentos` s
  ON u.`Codigo Unico` = s.`Codigo Unico`
LEFT JOIN temp_cambios_clientes_reciente c
  ON u.`Codigo Unico` = c.`Codigo Unico`
 AND c.rn = 1;

-- DIM_COMUNICACION
CREATE OR REPLACE TABLE `project-sin-477115.ESTRELLA.DIM_COMUNICACION` AS
SELECT
  ROW_NUMBER() OVER (
    ORDER BY `Tipo Cliente`, especificacion, estado, card
  ) AS id_comunicacion,
  `Tipo Cliente`,
  especificacion,
  estado,
  card,
  CASE 
    WHEN especificacion = 'SMS' AND cantidad > 10000 THEN 1
    ELSE 0
  END AS flag_presupuesto
FROM (
  SELECT DISTINCT
    `Tipo Cliente`,
    Especificacion,
    estado,
    card,
    cantidad
  FROM `project-sin-477115.refined_data.registro_comunicaciones`
);

-- UTILIDAD TRADING
CREATE OR REPLACE VIEW `project-sin-477115.ESTRELLA.VW_UTILIDAD_TRADING_BI` AS
SELECT
  /* =========================
     CLAVES
     ========================= */
  f.id_hecho,
  f.id_fecha,
  f.id_cliente,
  f.id_ejecutivo,
  f.id_canal,
  f.id_comunicacion,

  /* =========================
     DIM_FECHA
     ========================= */
  df.fecha,
  df.anio,
  df.mes_num,
  df.periodo,
  df.nombre_dia_semana,
  df.dia_util_flag,

  /* =========================
     DIM_CLIENTE
     ========================= */
  dc.`Codigo Unico`,
  dc.ruc,
  dc.nombre_cliente,
  dc.`Segmento FX` as segmento_fx,
  dc.`Tipo Cuenta`,
  dc.logeo,
  dc.`Num Logeos`,
  dc.`Flg Dig`,
  dc.flag_fuga,

  /* =========================
     DIM_EJECUTIVO
     ========================= */
  de.nombre_ejecutivo,
  de.nombre_jefe,

  /* =========================
     DIM_CANAL
     ========================= */
  dca.nombre_canal,

  /* =========================
     DIM_COMUNICACION
     ========================= */
  dco.`Tipo Cliente`,
  dco.especificacion,
  dco.estado,
  dco.card,
  dco.flag_presupuesto,

  /* =========================
     MÉTRICAS
     ========================= */
  f.monto,
  f.desembolsado,
  f.volumen_cambiado,
  f.utilidad

FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f

/* =========================
   JOINS DIMENSIONES
   ========================= */
LEFT JOIN `project-sin-477115.ESTRELLA.DIM_FECHA` df
  ON f.id_fecha = df.id_fecha

LEFT JOIN `project-sin-477115.ESTRELLA.DIM_CLIENTE` dc
  ON f.id_cliente = dc.id_cliente

LEFT JOIN `project-sin-477115.ESTRELLA.DIM_EJECUTIVO` de
  ON f.id_ejecutivo = de.id_ejecutivo

LEFT JOIN `project-sin-477115.ESTRELLA.DIM_CANAL` dca
  ON f.id_canal = dca.id_canal

LEFT JOIN `project-sin-477115.ESTRELLA.DIM_COMUNICACION` dco
  ON f.id_comunicacion = dco.id_comu
