# 📘 PC4 — Arquitectura Completa de Procesamiento de Datos en Google Cloud (Grupo 02 – EsSalud)

Procesamiento Bronce → Plata con Dataproc
Procesamiento Plata → Oro con Dataflow
Orquestación con Cloud Composer
Visualización en Looker Studio

Este documento describe la arquitectura completa del flujo de datos del proyecto EsSalud para el PC4, abarcando todo el ciclo de vida del dato, desde la ingestión de los archivos CSV originales hasta la visualización analítica en Looker Studio.
Se implementa un proceso robusto que incluye:

✔ Capa Bronce (ingesta)
✔ Capa Plata (limpieza y normalización)
✔ Capa Oro (modelamiento para BI)
✔ Orquestación automática
✔ Seguridad basada en roles IAM

## 🏗 1. Arquitectura General del Proyecto

La solución se implementa completamente en Google Cloud Platform (GCP), siguiendo un enfoque modular y escalable de procesamiento de datos.

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Graficos/Nueva_Arquitectura.png)

🔹 Flujo General

1. Fuentes (CSV originales de EsSalud):

- Obesidad.csv
- Hipertension.csv
- Diabetes.csv
- Ubigeo.csv

2. Ingesta → Capa Bronce
Los archivos son almacenados sin modificaciones en Cloud Storage, y también se cargan en BigQuery (dataset: essalud_bronce).

3. Transformación → Capa Plata
Procesamiento con Dataproc (Spark):
- Limpieza (nulos, duplicados)
- Normalización
- Creación de tablas dimension y hechos

4. Carga → BigQuery Plata
Las tablas finales Silver se almacenan en:
✔ GCS en formato CSV
✔ BigQuery en el dataset essalud_plata

5. Capa Oro (Modelamiento BI)
BigQuery sirve como fuente de dashboards en Looker Studio.

6. Orquestación y Seguridad

- Cloud Composer automatiza el pipeline
- IAM y Admin definen permisos por rol

## 🗂 2. Capa Bronce — Ingesta y Almacenamiento

Los archivos CSV originales se almacenan en:

gs://grupo2-essalud-datalake/bronce/

Y se cargan directamente en BigQuery:

grupo2-essalud.essalud_bronce.Diabetes
grupo2-essalud.essalud_bronce.Obesidad
grupo2-essalud.essalud_bronce.Hipertension
grupo2-essalud.essalud_bronce.Ubigeo

## ⚙️ 3. Capa Plata — Procesamiento con Dataproc (Spark)

La transformación Bronce → Plata se realiza con Apache Spark en Dataproc, donde se ejecuta el procesamiento ETL:

✔ Proceso ejecutado en Dataproc:

- Lectura de tablas Bronce desde BigQuery

- Limpieza:
    - Eliminar nulos
    - Eliminar duplicados
    - Normalizar strings

- Creación de tablas dimensión y hechos

- Generación de ID secuenciales (por ejemplo: Cod_Diagnostico)

- Escritura en:

    - Cloud Storage (CSV)
    - BigQuery (dataset plata)

✔ Dataset Plata

grupo2-essalud.essalud_plata

✔ Tablas generadas (Silver):
| **Tabla**	| **Tipo**	|**Descripción**|
|---------------------------|----------|---------------------------------------------|
|**paciente**               |Dimensión |Información del paciente|
|**medico**                 |Dimensión |Información del médico|
|**cie10**	                |Dimensión |Catálogo de enfermedades|
|**procedimiento**          |Dimensión |Catálogo de procedimientos|
|**ubigeo**                 |Dimensión |Ubicación geográfica|
|**diagnostico**            |Hechos	   |Registro de diagnósticos (con PK incremental)|
|**resultado_procedimiento**|Hechos    |Resultados de laboratorio|
|**metricas_calidad**       |Auditoría |Métricas de limpieza|

Para mayor entendimiento del proceso Bronce - Plata
- [Procesamiento Bronce Plata Datproc](./Partes/Procesamiento_Bronce_Plata_Datproc.md)


## 🧱 4. Capa Oro — Procesamiento con Dataflow (Apache Beam)|

Una vez generada la capa Plata, se procesa Plata → Oro utilizando Google Cloud Dataflow (Apache Beam).

✔ Funciones de Dataflow en la capa Oro:

- Lectura directa desde BigQuery (Silver)

- Unión de dimensiones y hechos

- Cálculo de métricas analíticas:

    - Tendencias de enfermedades
    - Mapa por Ubigeo
    - Promedios de laboratorio
    - Segmentación por edad y sexo

- Modelamiento dimensional (star schema para BI)

- Generación de tablas finales para análisis

✔ Dataset Oro
grupo2-essalud.essalud_oro

✔ Tablas finales (Gold Layer):

|**Tabla Oro**	| **Descripción**|
|-----------------|------------------------------|
|**fact_diagnostico** | Métricas por diagnóstico|
|**fact_resultados**  |Métricas de laboratorio|
|**dim_paciente**     |	 Lista final optimizada|
|**dim_cie10**        |	Catálogo final|
|**dim_medico**	      |Información de médicos|
|**dim_tiempo**       |	Desglose por fechas|

## 📊 5. Visualización — Looker Studio

La capa Oro es conectada a Looker Studio mediante BigQuery.

Dashboards generados:

- Distribución de enfermedades por región
- Tendencias temporales (líneas)
- Mapa interactivo por Ubigeo
- Promedios de laboratorio por diagnóstico
- Segmentación por categoría demográfica

## 🎛 6. Orquestación — Cloud Composer

Para automatizar el proceso ETL completo, se usa Cloud Composer (Airflow).

DAG principal:

|**Tarea**|Servicio	|Descripción|
|------|-------------------------|-----------------------------------|
|**T1**|GCS → Bronce	         |Cargar CSV iniciales|
|**T2**|DataprocSubmitJobOperator|	Ejecutar script Spark para Silver|
|**T3**|DataflowOperator	     |Ejecutar pipeline para Oro|
|**T4**|BigQueryOperator	     |Validación de calidad|
|**T5**|EmailOperator          	 |Notificación|

## 🔐 7. Seguridad — IAM & Admin

Principios implementados:

✔ Principio de privilegio mínimo

Cada rol solo tiene acceso a lo que necesita.

✔ Service Accounts dedicadas

- `dataproc-sa` → ejecuta jobs Spark

- `dataflow-sa` → ejecuta pipelines Beam

- `composer-sa` → orquesta el workflow

- `bigquery-loader-sa` → carga datos

✔ Roles asignados
|Servicio	|Rol|
|----------|--------------------------------|
|**GCS**	|Storage Object Viewer / Creator|
|**BigQuery**	|Data Editor / Viewer|
|**Dataproc**	|Dataproc Editor|
|**Dataflow**	|Dataflow Worker|
|**Composer**	|Composer Worker|

✔ Auditoría

- Cloud Audit Logs habilitado
- Monitoreo de consultas en BigQuery
- Historial de cambios IAM

Para mayor entendimiento de Seguridad — IAM & Admin
- [Procesamiento Bronce Plata Datproc](./Partes/Seguridad.md)

## 📝 8. Conclusiones Finales

- Se implementó un pipeline completo de arquitectura moderna en GCP.

- Dataproc procesa la capa Bronce → Plata aplicando limpieza y normalización.

- Dataflow genera la Capa Oro, optimizada para analítica.

- BigQuery sirve como almacenamiento centralizado para BI.

- Looker Studio provee dashboards interactivos listos para presentación.

- Cloud Composer automatiza y programa todo el proceso.

- IAM garantiza seguridad, auditoría y control de accesos.