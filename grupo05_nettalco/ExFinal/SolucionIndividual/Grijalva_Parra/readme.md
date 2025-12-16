# Proyecto: US Accidents — Pipeline ETL (Bronce / Plata / Oro)

## Resumen
Este repositorio contiene scripts y funciones para desplegar un pipeline ETL sobre Google Cloud (GCP). Incluye ingestión en la capa **bronce**, transformación y modelo dimensional en **plata**, y generación de KPIs en **oro**. Los scripts de despliegue y orquestación se encuentran en la carpeta `scripts`.

## 1) Selección de nube (Justificación técnica)
- Nube seleccionada: **Google Cloud Platform (GCP)**.
- Justificación: los artefactos y comandos presentes usan `gcloud`, `gsutil`, `bq` y `dataproc` — integrar con GCP es natural y ofrece servicios gestionados necesarios: Cloud Storage para el Data Lake, Dataproc para procesos distribuídos (Spark), Cloud Functions para orquestar ETL y BigQuery para almacenamiento analítico y consultas rápidas. GCP facilita escalado, facturación por uso y componentes nativos para cada etapa del pipeline.

## 2) Estructura requerida (BRONCE)
La estructura implementada dentro del bucket (y replicada localmente en `scripts/bronce`) cubre:

- /bronce/raw
- /bronce/processed
- /bronce/curated

Scripts relevantes para crear el bucket y carpetas (CLI):

- `scripts/create_storage.sh` ([scripts/create_storage.sh](scripts/create_storage.sh))
- `scripts/create_folders.sh` ([scripts/create_folders.sh](scripts/create_folders.sh))

Para cargar CSV vía CLI (ejemplo):

```bash
# Subir un CSV local al bucket bronce/raw
gsutil cp archivos/US_Accidents_March23.csv gs://us-accidents-bd/bronce/raw/
```

## 3) Ingestión y Estructuración – BRONCE (Evidencias entregables)
- Carga por CLI: uso de `gsutil cp` (ver `scripts/create_folders.sh`).
- EDA mínimo: el repositorio contiene `scripts/bronce/etl_bronce.py` que incluye pasos de parseo y limpieza básicos; ejecutar localmente con Python para obtener estadísticas.

Ejecutar EDA mínimo (local):

```bash
python scripts/bronce/etl_bronce.py --input archivos/US_Accidents_March23.csv --mode eda
```

Salida esperada (ejemplos): conteo de filas, columnas con nulos, tipos de datos y distribuciones simples por columnas clave.

## 4) Transformación y Modelo Dimensional – PLATA y ORO
### Modelo estrella (resumen y justificación)
- Diseño mínimo: una tabla de hechos `fact_accidents` y dimensiones `dim_date`, `dim_location`, `dim_vehicle` (según columnas del CSV). Justificación técnica: modelo estrella optimiza consultas analíticas en BigQuery para agregaciones y facilita cálculo de KPIs en ORO.

- Esquema propuesto (simplificado):

	- dim_date(date_id, date, year, month, day, weekday)
	- dim_location(location_id, state, city, latitude, longitude)
	- dim_vehicle(vehicle_id, vehicle_type, vehicle_count)
	- fact_accidents(event_id, date_id, location_id, vehicle_id, casualties, severity, distance)

Incluye un gráfico esquemático (puedes generar uno en la carpeta `docs` o con un notebook):

```
					 dim_date      dim_location    dim_vehicle
							 \           |               /
							  \          |              /
							   \         |             /
								fact_accidents (hechos)
```

### Scripts y evidencias
- Generación de tablas de dimensión y hechos en plata: `scripts/plata/etl_plata.py` ([scripts/plata/etl_plata.py](scripts/plata/etl_plata.py)).
- Procesamiento y KPIs en oro: `scripts/oro/etl_oro.py` ([scripts/oro/etl_oro.py](scripts/oro/etl_oro.py)).

Ejemplo de ejecución para transformar a PLATA y cargar a BigQuery:

```bash
python scripts/plata/etl_plata.py --input gs://us-accidents-bd/bronce/processed/ --output bigquery
```

Para generar KPIs en ORO:

```bash
python scripts/oro/etl_oro.py --source bigquery --output gs://us-accidents-bd/oro/aggregates/
```

## 5) Orquestación y despliegue
- Scripts de despliegue y orquestación ubicados en `scripts/`:

- `scripts/deploy_functions.sh` — despliega Cloud Functions para `bronce`, `plata`, `oro`.
- `scripts/create_scheduler.sh` — crea jobs de Cloud Scheduler para ejecutar las funciones periódicamente.
- `scripts/create_dataproc.sh` — crea cluster Dataproc usado por cargas/transformaciones pesadas.
- `scripts/autoscaling.sh` — asigna política autoscaling al cluster.

Referencias: [scripts/deploy_functions.sh](scripts/deploy_functions.sh), [scripts/create_scheduler.sh](scripts/create_scheduler.sh), [scripts/create_dataproc.sh](scripts/create_dataproc.sh), [scripts/autoscaling.sh](scripts/autoscaling.sh).

## 6) Logs y evidencias en `docs`
- Las evidencias de ETL y logs en vivo deben guardarse en la carpeta `docs` dentro del repositorio y también en `gs://us-accidents-bd/docs/` (ya creada por los scripts). Añade salidas de ejecución, capturas o `etl_logs` exportadas desde BigQuery.

Recomendación para guardar logs localmente a `docs/`:

```bash
mkdir -p docs
python scripts/bronce/etl_bronce.py --input archivos/US_Accidents_March23.csv --mode eda --save-logs docs/eda_brOnce.log
gsutil cp docs/eda_brOnce.log gs://us-accidents-bd/docs/
```

## 7) Cómo probar rápido (resumen de comandos)

```bash
# 1. Crear storage y carpetas
bash scripts/create_storage.sh
bash scripts/create_folders.sh

# 2. Subir CSV de ejemplo
gsutil cp archivos/US_Accidents_March23.csv gs://us-accidents-bd/bronce/raw/

# 3. Ejecutar ETL bronce local (EDA + procesado)
python scripts/bronce/etl_bronce.py --input archivos/US_Accidents_March23.csv --mode eda

# 4. Transformar a PLATA y cargar a BigQuery
python scripts/plata/etl_plata.py --input gs://us-accidents-bd/bronce/processed/ --output bigquery

# 5. Generar KPIs en ORO
python scripts/oro/etl_oro.py --source bigquery --output gs://us-accidents-bd/oro/aggregates/

# 6. Desplegar funciones y scheduler (opcional)
bash scripts/deploy_functions.sh
bash scripts/create_scheduler.sh
```

## 8) Validación de consultas SQL

- Propósito: asegurar que las consultas a BigQuery son correctas, eficientes y con coste controlado antes de su despliegue en producción.
- Pasos recomendados de validación:
	- Usar `bq` y la consola de BigQuery para ejecutar una revisión previa (`dry-run`/explain) y revisar el plan de ejecución.
	- Probar consultas sobre subconjuntos de datos (muestras) y comparar resultados con ejecuciones locales/ETL de referencia.
	- Añadir pruebas unitarias simples que verifiquen salidas esperadas para consultas clave contra datasets de prueba.
	- Revisar estimaciones de bytes leídos y añadir filtros/particionamiento/clustering para reducir costes.

Ejemplo de comprobación rápida (dry-run con `bq` API o consola):

```sql
-- ================================
-- VALIDACIONES MODELO ESTRELLA
-- Proyecto: US Accidents
-- ================================

-- 1. DIM_TIEMPO: Cobertura temporal
SELECT
	MIN(fecha) AS fecha_min,
	MAX(fecha) AS fecha_max,
	COUNT(DISTINCT hora) AS horas_distintas
FROM `us-accidents-481401.us_accidents_dw.dim_tiempo`;

-- 2. DIM_UBICACION: Validación de buckets geográficos
SELECT
	COUNT(*) AS total_buckets,
	COUNT(DISTINCT CONCAT(CAST(lat_bucket AS STRING), '-', CAST(lng_bucket AS STRING))) AS buckets_distintos
FROM `us-accidents-481401.us_accidents_dw.dim_ubicacion`;

-- 3. DIM_CLIMA: Distribución por clima
SELECT
	Source,
	COUNT(*) AS registros
FROM `us-accidents-481401.us_accidents_dw.dim_clima`
GROUP BY Source
ORDER BY registros DESC;

-- 4. FACT_ACCIDENTES: Métricas generales
SELECT
	MIN(Severity) AS severidad_min,
	MAX(Severity) AS severidad_max,
	AVG(Duration_minutes) AS duracion_promedio,
	COUNT(*) AS total_accidentes
FROM `us-accidents-481401.us_accidents_dw.fact_accidentes`;

-- 5. KPI_ACCIDENTES_CLIMA
SELECT
	Source,
	total_accidentes
FROM `us-accidents-481401.us_accidents_dw.kpi_accidentes_clima`
ORDER BY total_accidentes DESC;

-- 6. KPI_ACCIDENTES_UBICACION (Top 10 hotspots)
SELECT
	lat_bucket,
	lng_bucket,
	total_accidentes
FROM `us-accidents-481401.us_accidents_dw.kpi_accidentes_ubicacion`
ORDER BY total_accidentes DESC
LIMIT 10;

-- 7. KPI_HORAS_CRITICAS
SELECT
	hora,
	total_accidentes
FROM `us-accidents-481401.us_accidents_dw.kpi_horas_criticas`
ORDER BY total_accidentes DESC;

-- 8. KPI_SEVERIDAD_PROMEDIO
SELECT
	severidad_promedio
FROM `us-accidents-481401.us_accidents_dw.kpi_severidad_promedio`;

-- 9. QUERY ESTRELLA (JOIN COMPLETO PARA ANALISIS)
SELECT
	t.hora,
	u.lat_bucket,
	u.lng_bucket,
	AVG(f.Severity) AS severidad_promedio,
	COUNT(*) AS accidentes
FROM `us-accidents-481401.us_accidents_dw.fact_accidentes` f
JOIN `us-accidents-481401.us_accidents_dw.dim_tiempo` t
	ON f.Start_Time_ts = t.fecha
JOIN `us-accidents-481401.us_accidents_dw.dim_ubicacion` u
	ON f.lat_bucket = u.lat_bucket
 AND f.lng_bucket = u.lng_bucket
GROUP BY t.hora, u.lat_bucket, u.lng_bucket
ORDER BY accidentes DESC
LIMIT 10;
```

## 9) Autoscaling aplicado al cluster

- Implementación: se asignó la política de autoscaling `etl-autoscaling` al cluster Dataproc mediante `scripts/autoscaling.sh`.
- Efecto esperado: el cluster ajusta automáticamente el número de workers según la carga, permitiendo manejar picos de carga durante ETL y reducir costos en periodos de baja actividad.
- Comandos útiles:

```bash
# Ver estado del cluster
gcloud dataproc clusters describe us-accidents-cluster --region=us-central1

# Ver políticas de autoscaling
gcloud dataproc autoscaling-policies list --region=us-central1
```

Nota: ajustar los umbrales y límites de la política (`etl-autoscaling`) según pruebas de rendimiento y presupuesto.

## 11) Desarrollo de BI (Power BI)

- Herramienta elegida: **Power BI Desktop**. El desarrollo de dashboards se realizará conectando a la capa ORO / DW (BigQuery) o a archivos exportados desde BigQuery a CSV/Cloud Storage.

- Requisito: guardar los archivos del desarrollo en el repositorio para reproducibilidad:
	- Power BI files: `dashboard/BI Accidentes USA (2016-2023).pbix`
	- Consultas / scripts (Power Query M / DAX): `docs/powerbi/scripts/`
	- Capturas y evidencias: `evidencias`

- 3.3 Visualización de KPIs – Dashboards (requerimientos y reproducibilidad)
	- Crear al menos 2 dashboards conectados a la capa ORO o al DW.
	- Los `.pbix`, las consultas Power Query (M) y cualquier script de preparación deben guardarse en `docs/powerbi/`.
	- Para reproducibilidad se propone uno de estos flujos:
		1. Conexión directa desde Power BI a BigQuery (recomendado si hay permisos): crear fuente de datos con credenciales de servicio o cuenta de usuario.
		2. Exportar tablas ORO a CSV y guardarlas en `gs://us-accidents-bd/oro/aggregates/`, luego descargar y utilizar en Power BI Desktop.

	Más detalles en: [Ir al README del dashboard](dashboard/README.md)

- KPIs seleccionados y justificación
	- Distancia afecta por mes: permite medir la magnitud del impacto (longitud/área afectada) y su evolución temporal para detectar tendencias y estacionalidad.
	- Promedio de gravedad del accidente por clima: relaciona condiciones meteorológicas con severidad para priorizar alertas y recursos.
	- Distancia afecta por hora luego del accidente: analiza cómo varía la afectación temporalmente tras un evento (útil para responder y planear logística).
	- Total de accidentes por hora: indicador operativo para identificar horas punta y orientar campañas de prevención.

- Dashboards propuestos
	- Dashboard 1 — "KPIs Operativos": métricas agregadas (Total accidentes por hora, Distancia afecta por mes), filtros por región/estado y una línea temporal para tendencias.

	- Dashboard 2 — "Análisis de Severidad y Clima": heatmap o barras del Promedio de gravedad por clima, y un gráfico temporal de Distancia afecta por hora luego del accidente.

- Decisiones de diseño y visualización (sustento)
	- Tipo de gráficos: se eligen series temporales (líneas) para tendencias, barras para comparaciones por categoría, y mapas/heatmaps para análisis geoespacial (ubicación de hotspots).
	- Interactividad: filtros por fecha, estado/ciudad y clima para facilitar drill-down; usar slicers en Power BI para selección rápida.
	- Rendimiento: conectar por extracto (CSV) en caso de datasets muy grandes, o aplicar particionado/filtrado en la consulta para reducir datos transferidos.
	- Accesibilidad: usar paletas de color con contraste suficiente y texto claro en KPI cards para lectura rápida.

Desktop: [BI Accidentes USA (2016-2023)](dashboard/BI%20Accidentes%20USA%20(2016-2023).pbix)