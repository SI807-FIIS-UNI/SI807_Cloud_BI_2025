from google.cloud import bigquery

# =========================
# CONFIGURACIÓN
# =========================
PROJECT_ID = "double-basis-481318-h5"
DATASET_PLATA = "dw_plata"
DATASET_ORO = "dw_oro"

client = bigquery.Client(project=PROJECT_ID)

# =========================
# KPI 1: TASA GLOBAL NO-SHOW
# =========================
query_kpi_global = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ORO}.kpi_no_show_global` AS
SELECT
  COUNT(*) AS total_citas,
  SUM(no_show) AS total_no_show,
  ROUND(SUM(no_show) / COUNT(*) * 100, 2) AS tasa_no_show_pct
FROM `{PROJECT_ID}.{DATASET_PLATA}.fact_citas`;
"""

# =========================
# KPI 2: NO-SHOW POR EDAD Y GÉNERO
# =========================
query_kpi_edad_genero = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ORO}.kpi_no_show_edad_genero` AS
SELECT
  p.gender,
  CASE
    WHEN p.age < 18 THEN '0-17'
    WHEN p.age BETWEEN 18 AND 35 THEN '18-35'
    WHEN p.age BETWEEN 36 AND 60 THEN '36-60'
    ELSE '60+'
  END AS rango_edad,
  COUNT(*) AS total_citas,
  SUM(f.no_show) AS total_no_show,
  ROUND(SUM(f.no_show) / COUNT(*) * 100, 2) AS tasa_no_show_pct
FROM `{PROJECT_ID}.{DATASET_PLATA}.fact_citas` f
JOIN `{PROJECT_ID}.{DATASET_PLATA}.dim_paciente` p
  ON f.paciente_id = p.paciente_id
GROUP BY gender, rango_edad;
"""

# =========================
# KPI 3: NO-SHOW POR DÍA Y HORA
# =========================
query_kpi_tiempo = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ORO}.kpi_no_show_tiempo` AS
SELECT
  t.dia_semana,
  t.hora,
  COUNT(*) AS total_citas,
  SUM(f.no_show) AS total_no_show,
  ROUND(SUM(f.no_show) / COUNT(*) * 100, 2) AS tasa_no_show_pct
FROM `{PROJECT_ID}.{DATASET_PLATA}.fact_citas` f
JOIN `{PROJECT_ID}.{DATASET_PLATA}.dim_tiempo` t
  ON f.tiempo_id = t.tiempo_id
GROUP BY dia_semana, hora;
"""

# =========================
# KPI 4: NO-SHOW POR LEAD TIME
# =========================
query_kpi_lead_time = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ORO}.kpi_no_show_lead_time` AS
SELECT
  CASE
    WHEN lead_time = 0 THEN 'Mismo día'
    WHEN lead_time BETWEEN 1 AND 3 THEN '1-3 días'
    WHEN lead_time BETWEEN 4 AND 7 THEN '4-7 días'
    ELSE '8+ días'
  END AS rango_anticipacion,
  COUNT(*) AS total_citas,
  SUM(no_show) AS total_no_show,
  ROUND(SUM(no_show) / COUNT(*) * 100, 2) AS tasa_no_show_pct
FROM `{PROJECT_ID}.{DATASET_PLATA}.fact_citas`
GROUP BY rango_anticipacion;
"""


# =========================
# KPI 5: NO-SHOW VS CANAL (SMS)
# =========================
query_kpi_canal = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ORO}.kpi_no_show_canal` AS
SELECT
  c.descripcion_canal,
  COUNT(*) AS total_citas,
  SUM(f.no_show) AS total_no_show,
  ROUND(SUM(f.no_show) / COUNT(*) * 100, 2) AS tasa_no_show_pct
FROM `{PROJECT_ID}.{DATASET_PLATA}.fact_citas` f
JOIN `{PROJECT_ID}.{DATASET_PLATA}.dim_canal` c
  ON f.canal_id = c.canal_id
GROUP BY c.descripcion_canal
ORDER BY tasa_no_show_pct DESC;
"""


# =========================
# EJECUCIÓN
# =========================
queries = [
    query_kpi_global,
    query_kpi_edad_genero,
    query_kpi_tiempo,
    query_kpi_lead_time,
    query_kpi_canal
]

for q in queries:
    client.query(q).result()

print("✔ PLATA → ORO completado")
print("KPIs generados en dataset ORO:")
print("- kpi_no_show_global")
print("- kpi_no_show_edad_genero")
print("- kpi_no_show_tiempo")
print("- kpi_no_show_lead_time")
print("- kpi_no_show_canal")

