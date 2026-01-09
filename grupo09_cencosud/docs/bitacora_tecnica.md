# 📜 BITÁCORA DEL PROYECTO ETL MIGRACIÓN A GCP

**Proyecto:** ETL de Ventas Retail (Hadoop/Hive a GCP/BigQuery)
**Fecha de Inicio:** 2025-11-15
[cite_start]**Equipo:** Grupo 9 (Cabana Cazani Gabriel, Larico Cruz Diego) [cite: 3, 4]
[cite_start]**Infraestructura Anterior:** Hortonworks HDP Sandbox (Hive, Spark, HDFS) [cite: 6]
**Infraestructura Nueva:** Google Cloud Platform (BigQuery, Dataproc Serverless, GCS)

---

## 1. FASE DE PREPARACIÓN E INGESTA (RAW)

Esta fase se centró en establecer el entorno Serverless en GCP y replicar la ingesta de datos CSV sucios.

### Decisiones Clave

* **Data Warehouse:** Se eligió **BigQuery (BQ)** como sustituto de Hive/HDFS para el catálogo y el almacenamiento final.
* **Dataset:** Se creó el dataset **`dataset_si807_g9`** para alojar todas las capas (RAW, CURATED, ANALYTICS).
* [cite_start]**Almacenamiento:** Se utilizó **Cloud Storage (GCS)** (`mi-etl-proyecto-2025`) para alojar los archivos CSV y Parquet, replicando la estructura lógica `/raw/`, `/curated/`, `/analytics/` que se usaba en HDFS[cite: 10, 11, 67, 68].

### Tareas y Problemas Resueltos

| Tarea | Estado | Observación / Solución |
| :--- | :--- | :--- |
| **Creación de Tablas RAW (DDL)** | ✔️ Completada | [cite_start]Se ejecutó `CREATE EXTERNAL TABLE` en BigQuery[cite: 162], apuntando a los CSV en GCS. [cite_start]Se usó `skip_leading_rows = 1` para replicar la propiedad `TBLPROPERTIES ("skip.header.line.count"="1")` de Hive[cite: 190]. |
| **Error de Ingesta (Lectura CSV)** | ✔️ Resuelto | **Problema:** Las tablas externas en BQ no mostraban datos (estaban vacías) al hacer `SELECT`. Se diagnosticó que BQ fallaba al intentar interpretar los tipos de datos (`INT`, `FLOAT`) del CSV sucio. <br> **Solución:** Se modificó el DDL de la Capa RAW para definir **todos los campos como `STRING`**. Esto forzó a BQ a leer los datos sin fallar y postergó el *casting* (conversión de tipos) a la capa Spark (Dataproc). |
| **Corrección de Tipos BQ** | ✔️ Resuelto | Se confirmó que el tipo `DOUBLE` de Hive no existe en BigQuery. Se ajustaron los DDLs de las capas CURATED y ANALYTICS para usar **`FLOAT64`** para todos los campos decimales (ej: `monto_venta_neta`). |

---

## 2. FASE DE TRANSFORMACIÓN (CURATED)

Esta fase se centró en migrar la lógica de limpieza PySpark a un entorno Serverless y cargar los resultados a la capa CURATED de BigQuery.

### Tareas y Problemas Resueltos

| Tarea | Estado | Observación / Solución |
| :--- | :--- | :--- |
| **Adaptación de Código Spark** | ✔️ Completada | Se consolidó la lógica de limpieza y transformación de las 6 tablas en un script autónomo (`etl_curated_job.py`). Se adaptaron las sentencias de Hive (`spark.table(default.tabla)`) a BigQuery (`spark.table(dataset_si807_g9.tabla)`). |
| **Creación de Tablas CURATED/ANALYTICS** | ✔️ Completada | [cite_start]Se ejecutó el DDL (`CREATE TABLE`) para crear las estructuras vacías en `dataset_si807_g9`, utilizando tipos de datos limpios (`DATE`, `INT64`, `FLOAT64`)[cite: 315]. |
| **Error de Conectividad de Red (Dataproc)** | ✔️ Resuelto | **Problema:** El envío del Lote PySpark falló con el error "No hay ninguna red local disponible". <br> **Solución:** Se verificó la red VPC y se configuró correctamente la subred, confirmando que la **Compute Engine Service Account** tuviera el rol **Usuario de red de Compute** (`roles/compute.networkUser`). |
| **Error de Sintaxis CLI (gcloud)** | ✔️ Resuelto | **Problema:** El comando `gcloud dataproc` no reconocía los flags `--executor-cores` o `--executor-memory`. <br> **Solución:** Se corrigió la sintaxis, pasando los recursos del ejecutor a través del flag **`--properties`** (Ej: `--properties=spark.executor.cores=4,spark.executor.memory=16g`). |
| **Ejecución y Carga** | ✔️ Completada | [cite_start]Se ejecutó el Job de Lote (Batch) Serverless, que transformó la data RAW y la cargó a la Capa CURATED en BigQuery, usando el método `df.write.format("bigquery")...`[cite: 358]. |

---

## 3. FASE DE ANALÍTICA Y VISUALIZACIÓN

Esta fase se enfoca en el uso del Data Warehouse para el consumo de BI.

### Tareas y Próximos Pasos

| Tarea | Estado | Observación / Solución |
| :--- | :--- | :--- |
| **Creación del Cubo OLAP (ANALYTICS)** | ✔️ Completada | [cite_start]Se ejecutó la consulta SQL de agregación (`INSERT INTO`) en BigQuery para llenar la tabla `resumen_ventas_analytics` [cite: 457-485]. |
| **Conexión a Looker Studio** | ✔️ Completada | Se conectó la tabla `resumen_ventas_analytics` como fuente principal. [cite_start]Se eliminó la necesidad de ODBC que se usaba para Power BI[cite: 538]. |
| **Desarrollo de KPIs** | 🏗️ En Progreso | El desarrollo de KPIs complejos (ej: "Ticket Promedio por Canal") requiere la **Combinación de Datos (Data Blending)** en Looker Studio, uniendo la tabla agregada (`resumen_ventas_analytics`) con tablas de dimensiones (`dim_tienda_canal_curated`). |
