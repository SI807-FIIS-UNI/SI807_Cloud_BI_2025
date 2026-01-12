-- ============================
-- 02 - JOIN COMPLETO DEL MODELO ESTRELLA
-- ============================

SELECT 
  h.id_siniestro,
  p.tipo_persona,
  p.sexo,
  p.edad,
  p.gravedad,
  v.vehiculo,
  v.estado_soat,
  v.posee_citv,
  t.fecha,
  t.anio,
  t.mes,
  t.dia_semana,
  t.trimestre,
  tv.tipo_de_via_normalizado,
  h.latitud,
  h.longitud
FROM `sutran.hechos_siniestros` h
LEFT JOIN `sutran.dim_persona`   p ON h.id_persona  = p.id_persona
LEFT JOIN `sutran.dim_vehiculo`  v ON h.id_vehiculo = v.id_vehiculo
LEFT JOIN `sutran.dim_tiempo`    t ON h.id_tiempo   = t.id_tiempo
LEFT JOIN `sutran.dim_tipo_via`  tv ON h.id_tipo_via = tv.id_tipo_via
LIMIT 200;
