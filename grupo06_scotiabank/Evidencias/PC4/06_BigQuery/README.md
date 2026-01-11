# 🔎 VALIDACIONES Y KPIs DEL DATASET ORO — BIGQUERY SQL

- Tabla central: grupo6-scotiabank.oro.hecho_riesgo
- Dimensiones: banco, indicador, moneda, fecha

## 1️⃣ Validación de valores nulos críticos

🔍 Detecta registros incompletos que podrían generar inconsistencias en los cálculos.

```sql
SELECT *
FROM `grupo6-scotiabank.oro.hecho_riesgo`
WHERE id_banco IS NULL
   OR id_fecha IS NULL
   OR id_moneda IS NULL
   OR id_indicador IS NULL
   OR valor IS NULL
LIMIT 20;
```

## 2️⃣ Validación semántica contra límites definidos (zona verde/amarilla/roja)

📊 Clasifica valores del hecho en RIESGO, AMARILLO u ÓPTIMO, según límites definidos y el sentido del indicador (flag_limite).

```sql
SELECT
  hr.id_banco,
  b.nombre AS banco_nombre,
  i.nombre AS indicador,
  hr.valor,
  i.lim_amarillo_min,
  i.lim_amarillo_max,
  i.flag_limite,
  CASE 
    WHEN i.flag_limite = 1 AND hr.valor < i.lim_amarillo_min THEN 'RIESGO'
    WHEN i.flag_limite = 1 AND hr.valor BETWEEN i.lim_amarillo_min AND i.lim_amarillo_max THEN 'ZONA AMARILLA'
    WHEN i.flag_limite = 1 AND hr.valor > i.lim_amarillo_max THEN 'ÓPTIMO'
    
    WHEN i.flag_limite = 0 AND hr.valor < i.lim_amarillo_min THEN 'ÓPTIMO'
    WHEN i.flag_limite = 0 AND hr.valor BETWEEN i.lim_amarillo_min AND i.lim_amarillo_max THEN 'ZONA AMARILLA'
    WHEN i.flag_limite = 0 AND hr.valor > i.lim_amarillo_max THEN 'RIESGO'
  END AS clasificacion
FROM `grupo6-scotiabank.oro.hecho_riesgo` hr
JOIN `grupo6-scotiabank.oro.dim_indicador` i USING(id_indicador)
JOIN `grupo6-scotiabank.oro.dim_banco` b USING(id_banco)
LIMIT 20;
```

## 3️⃣ Validación de cobertura temporal del dataset
🕒 Verifica que cada indicador posea información continua y no tenga huecos temporales.
```sql
SELECT 
  hr.id_indicador,
  i.nombre AS indicador,
  COUNT(DISTINCT hr.id_fecha) AS meses_reportados
FROM `grupo6-scotiabank.oro.hecho_riesgo` hr
JOIN `grupo6-scotiabank.oro.dim_indicador` i USING(id_indicador)
GROUP BY hr.id_indicador, i.nombre
ORDER BY meses_reportados DESC
LIMIT 20;
```

# 🚀 KPIs Y MÉTRICAS — ANÁLISIS EVOLUTIVO

## 4️⃣ KPI — Promedio histórico del indicador por banco

📈 Mide el comportamiento agregado del indicador para cada banco a lo largo del tiempo.

```sql
SELECT
  hr.id_banco,
  b.nombre AS banco,
  hr.id_indicador,
  i.nombre AS indicador,
  AVG(hr.valor) AS promedio_valor
FROM `grupo6-scotiabank.oro.hecho_riesgo` hr
JOIN `grupo6-scotiabank.oro.dim_banco` b USING(id_banco)
JOIN `grupo6-scotiabank.oro.dim_indicador` i USING(id_indicador)
GROUP BY 1,2,3,4
ORDER BY promedio_valor DESC
LIMIT 20;
```

## 5️⃣ KPI — Tendencia mensual por banco e indicador (variación porcentual)
📉 Permite identificar si los valores mejoran o empeoran en el tiempo, mostrando la evolución del riesgo.

```sql
WITH serie AS (
  SELECT
    hr.id_banco,
    b.nombre AS banco,
    hr.id_indicador,
    i.nombre AS indicador,
    hr.id_fecha,
    hr.valor,
    LAG(hr.valor) OVER(PARTITION BY hr.id_banco, hr.id_indicador ORDER BY hr.id_fecha) AS valor_prev
  FROM `grupo6-scotiabank.oro.hecho_riesgo` hr
  JOIN `grupo6-scotiabank.oro.dim_banco` b USING(id_banco)
  JOIN `grupo6-scotiabank.oro.dim_indicador` i USING(id_indicador)
)
SELECT *,
       (valor - valor_prev) / NULLIF(valor_prev, 0) * 100 AS variacion_pct
FROM serie
LIMIT 20;
```

## 6️⃣ KPI — Salud financiera consolidada por banco
🏦 Resume cuántos indicadores están en estado óptimo, advertencia o riesgo para cada banco
```sql
SELECT
  b.nombre AS banco,
  COUNT(CASE WHEN valor > lim_amarillo_max AND flag_limite = 1 THEN 1 END) AS kpis_optimos,
  COUNT(CASE WHEN valor BETWEEN lim_amarillo_min AND lim_amarillo_max THEN 1 END) AS kpis_amarillo,
  COUNT(CASE WHEN valor < lim_amarillo_min AND flag_limite = 1 THEN 1 END) AS kpis_rojos
FROM `grupo6-scotiabank.oro.hecho_riesgo` hr
JOIN `grupo6-scotiabank.oro.dim_indicador` i USING(id_indicador)
JOIN `grupo6-scotiabank.oro.dim_banco` b USING(id_banco)
GROUP BY banco
ORDER BY kpis_rojos DESC
LIMIT 20;

```
# 🎥 Evidencia — Validaciones y KPIs en BigQuery

[![Validaciones BigQuery](https://img.youtube.com/vi/BbjPsJvi9TI/0.jpg)](https://youtu.be/BbjPsJvi9TI)

