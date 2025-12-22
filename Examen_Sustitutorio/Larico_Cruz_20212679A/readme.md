# 🏛️ Examen Sustitutorio

Alumno: Diego César Larico Cruz - 20212679A

Este repositorio contiene la infraestructura y el código necesario para desplegar una solución de **Inteligencia de Negocios (BI)** basada en la nube. El proyecto migra datos históricos de admisión desde archivos planos (CSV) hacia un Data Warehouse moderno en **BigQuery**, utilizando una arquitectura **ETL Serverless**.

---

## 🚀 Guía de Despliegue (Paso a Paso)

Sigue estos bloques de código en tu **Google Cloud Shell** para implementar la solución completa.

### 🛠️ Paso 1: Configuración del Entorno

Define las variables globales del proyecto y habilita las APIs necesarias para que los servicios (Storage, Dataproc, BigQuery) puedan interactuar.

```bash
###############################################################################
# 1. VARIABLES Y APIS
# Define el ID del proyecto, región y nombres de recursos.
# Habilita los servicios de Dataproc, Storage y BigQuery.
###############################################################################

export PROJECT_ID="si807-g9"
export REGION="us-central1"
export BUCKET_NAME="ex_susti_bucket"
export DATASET_NAME="cepreuni_bi"
export TABLE_NAME="cepre_uni"
export CSV_FILE="Datos_abiertos_cepre_2024_1_2025_1.csv"

gcloud config set project $PROJECT_ID

gcloud services enable \
    storage-component.googleapis.com \
    dataproc.googleapis.com \
    bigquery.googleapis.com
```

---

### 📦 Paso 2: Infraestructura Data Lake

Crea el Bucket de almacenamiento y organiza las carpetas para separar los datos crudos (raw) de los códigos (scripts). Finalmente, carga el archivo fuente.

```bash
###############################################################################
# 2. DATA LAKE & INGESTA
# Crea el bucket, define la estructura de carpetas y sube el CSV.
###############################################################################

# Crear Bucket
gsutil mb -l $REGION gs://$BUCKET_NAME/

# Crear estructura de carpetas
touch .keep
gsutil cp .keep gs://$BUCKET_NAME/raw/.keep
gsutil cp .keep gs://$BUCKET_NAME/scripts/.keep
rm .keep

# Subir datos (Asumiendo que el CSV ya está en tu Cloud Shell)
gsutil cp $CSV_FILE gs://$BUCKET_NAME/raw/$CSV_FILE
```

---

### 🐍 Paso 3: Generación del Script ETL (PySpark)

Este bloque genera dinámicamente el archivo `etl_cepre_spark.py`. Este script lee el CSV, normaliza los nombres de columnas, aplica limpieza básica (trim/upper) y carga el resultado en una tabla plana de BigQuery.

```bash
###############################################################################
# 3. SCRIPT ETL (PYTHON/SPARK)
# Genera el archivo .py que ejecutará Dataproc.
# Realiza la lectura del CSV, limpieza y carga a BigQuery.
###############################################################################

cat <<EOF > etl_cepre_spark.py
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim

# Configuración
BUCKET_NAME = "$BUCKET_NAME"
DATASET_NAME = "$DATASET_NAME"
TABLE_NAME = "$TABLE_NAME"
CSV_PATH = f"gs://{BUCKET_NAME}/raw/$CSV_FILE"

spark = SparkSession.builder.appName("ETL-CepreUni").getOrCreate()

# 1. EXTRACT
df_raw = spark.read.option("header", True).option("inferSchema", True).csv(CSV_PATH)

# 2. TRANSFORM (Limpieza Básica)
df_curated = df_raw \\
    .withColumnRenamed("IDHASH", "id_hash") \\
    .withColumn("COLEGIO", upper(trim(col("COLEGIO")))) \\
    .withColumn("ESPECIALIDAD", upper(trim(col("ESPECIALIDAD")))) \\
    .withColumn("INGRESO", upper(trim(col("INGRESO"))))

# 3. LOAD (Escritura en BigQuery)
df_curated.write \\
    .format("bigquery") \\
    .option("table", f"{DATASET_NAME}.{TABLE_NAME}") \\
    .option("temporaryGcsBucket", BUCKET_NAME) \\
    .mode("overwrite") \\
    .save()
EOF

# Subir el script al bucket
gsutil cp etl_cepre_spark.py gs://$BUCKET_NAME/scripts/etl_cepre_spark.py

# Crea el dataset previo a ejecutar el job para evitar errores
bq mk --location=$REGION --dataset $PROJECT_ID:$DATASET_NAME || true

```

---

### 🔥 Paso 4: Ejecución del Job (Dataproc Serverless)

Envía el trabajo al clúster de Spark sin servidor. Esto procesa los datos y crea la tabla base `cepre_uni` en BigQuery.

```bash
###############################################################################
# 4. EJECUCIÓN DEL PIPELINE
# Envía el job a Dataproc Serverless.
# Usa el conector de BigQuery (spark-bigquery-latest).
###############################################################################

gcloud dataproc batches submit pyspark \
    gs://$BUCKET_NAME/scripts/etl_cepre_spark.py \
    --region=$REGION \
    --deps-bucket=gs://$BUCKET_NAME \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    --version=2.1 \
    --subnet=default
```

---

### 🏛️ Paso 5: Modelado Dimensional (SQL)

Una vez que la tabla base existe,
```bash

# Dimensión Tiempo
bq query --use_legacy_sql=false --project_id=$PROJECT_ID \
"CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_tiempo\` AS
SELECT DISTINCT 
    ABS(FARM_FINGERPRINT(CONCAT(ANIO_POSTULA, '-', CICLO_POSTULA))) as id_tiempo,
    CONCAT(ANIO_POSTULA, '-', CICLO_POSTULA) as periodo,
    CAST(ANIO_POSTULA AS INT64) as anio,
    CAST(CICLO_POSTULA AS INT64) as ciclo
FROM \`$PROJECT_ID.$DATASET_NAME.$TABLE_NAME\`
WHERE ANIO_POSTULA IS NOT NULL;"

# Dimensión Ubicación
bq query --use_legacy_sql=false --project_id=$PROJECT_ID \
"CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_ubicacion\` AS
SELECT DISTINCT 
    ABS(FARM_FINGERPRINT(CONCAT(DOMICILIO_DEPA, DOMICILIO_PROV, DOMICILIO_DIST))) as id_ubicacion,
    DOMICILIO_DEPA as departamento,
    DOMICILIO_PROV as provincia,
    DOMICILIO_DIST as distrito,
    CASE 
        WHEN DOMICILIO_DEPA IN ('LIMA', 'CALLAO') THEN 'LIMA METROPOLITANA'
        ELSE 'PROVINCIA' 
    END as macro_zona
FROM \`$PROJECT_ID.$DATASET_NAME.$TABLE_NAME\`
WHERE DOMICILIO_DIST IS NOT NULL;"

# Dimensión Especialidad
bq query --use_legacy_sql=false --project_id=$PROJECT_ID \
"CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_especialidad\` AS
SELECT DISTINCT 
    ABS(FARM_FINGERPRINT(ESPECIALIDAD)) as id_especialidad,
    ESPECIALIDAD as carrera
FROM \`$PROJECT_ID.$DATASET_NAME.$TABLE_NAME\`
WHERE ESPECIALIDAD IS NOT NULL;"


###################################################

bq query --use_legacy_sql=false --project_id=$PROJECT_ID \
"CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.fact_postulaciones\` AS
SELECT
    -- Llaves Foráneas (FK)
    ABS(FARM_FINGERPRINT(CONCAT(ANIO_POSTULA, '-', CICLO_POSTULA))) as id_tiempo,
    ABS(FARM_FINGERPRINT(CONCAT(DOMICILIO_DEPA, DOMICILIO_PROV, DOMICILIO_DIST))) as id_ubicacion,
    ABS(FARM_FINGERPRINT(ESPECIALIDAD)) as id_especialidad,
    
    -- Identificador Único (Degenerado)
    id_hash as id_postulante_hash,

    -- Métricas
    CAST(COALESCE(CALIF_FINAL, 0) AS FLOAT64) as puntaje_final,
    (CAST(ANIO_POSTULA AS INT64) - CAST(ANIO_NACIMIENTO AS INT64)) as edad,
    
    -- KPIs (Banderas)
    CASE WHEN INGRESO = 'SI' THEN 1 ELSE 0 END as es_ingresante,
    1 as cantidad_postulacion, -- Para contar filas fácilmente
    
    -- Atributos de contexto
    MODO_INGRESO as modalidad

FROM \`$PROJECT_ID.$DATASET_NAME.$TABLE_NAME\`
WHERE ANIO_POSTULA IS NOT NULL;"

```


O puede ejecutar este bloque ejecuta consultas SQL en BigQuery para transformar esa tabla plana en un Modelo Estrella (Hechos y Dimensiones), aplicando reglas de negocio avanzadas.

```sql
###############################################################################
# 5. MODELADO STAR SCHEMA (SQL)
# Ejecutar en BigQuery Console.
# Crea Dimensiones y Tabla de Hechos con lógica de negocio.
###############################################################################

-- A. CREAR DATASET (Si no existe)
CREATE SCHEMA IF NOT EXISTS `si807-g9.cepreuni_bi`;

-- B. DIMENSIONES
CREATE OR REPLACE TABLE `cepreuni_bi.dim_tiempo` AS
SELECT DISTINCT 
    ABS(FARM_FINGERPRINT(CONCAT(CAST(ANIO_POSTULA AS STRING), '-', CAST(CICLO_POSTULA AS STRING)))) as id_tiempo,
    CONCAT(ANIO_POSTULA, '-', CICLO_POSTULA) as periodo,
    CAST(ANIO_POSTULA AS INT64) as anio,
    CAST(CICLO_POSTULA AS INT64) as ciclo
FROM `cepreuni_bi.cepre_uni` WHERE ANIO_POSTULA IS NOT NULL;

CREATE OR REPLACE TABLE `cepreuni_bi.dim_ubicacion` AS
SELECT DISTINCT 
    ABS(FARM_FINGERPRINT(CONCAT(DOMICILIO_DEPA, DOMICILIO_PROV, DOMICILIO_DIST))) as id_ubicacion,
    DOMICILIO_DEPA as departamento,
    DOMICILIO_PROV as provincia,
    CASE WHEN DOMICILIO_DEPA LIKE '%LIMA%' THEN 'LIMA METROPOLITANA' ELSE 'PROVINCIA' END as macro_zona
FROM `cepreuni_bi.cepre_uni` WHERE DOMICILIO_DIST IS NOT NULL;

CREATE OR REPLACE TABLE `cepreuni_bi.dim_especialidad` AS
SELECT DISTINCT 
    ABS(FARM_FINGERPRINT(ESPECIALIDAD)) as id_especialidad,
    ESPECIALIDAD as carrera
FROM `cepreuni_bi.cepre_uni` WHERE ESPECIALIDAD IS NOT NULL;

-- C. TABLA DE HECHOS (FACT TABLE)
CREATE OR REPLACE TABLE `cepreuni_bi.fact_postulaciones` AS
SELECT
    ABS(FARM_FINGERPRINT(CONCAT(CAST(ANIO_POSTULA AS STRING), '-', CAST(CICLO_POSTULA AS STRING)))) as id_tiempo,
    ABS(FARM_FINGERPRINT(CONCAT(DOMICILIO_DEPA, DOMICILIO_PROV, DOMICILIO_DIST))) as id_ubicacion,
    ABS(FARM_FINGERPRINT(ESPECIALIDAD)) as id_especialidad,
    IDHASH as id_postulante_hash,
    CAST(COALESCE(CALIF_FINAL, 0) AS FLOAT64) as puntaje_final,
    (CAST(ANIO_POSTULA AS INT64) - CAST(ANIO_NACIMIENTO AS INT64)) as edad,
    CASE WHEN INGRESO = 'SI' THEN 1 ELSE 0 END as es_ingresante,
    1 as cantidad_postulacion
FROM `cepreuni_bi.cepre_uni`
WHERE ANIO_POSTULA IS NOT NULL;
```

---

## 📊 Visualización

Conectar **Looker Studio** a la tabla `cepreuni_bi.fact_postulaciones` y realizar **Left Joins** con las dimensiones para visualizar el Dashboard.

### Pasos para conectar:

1. Accede a [Looker Studio](https://lookerstudio.google.com/)
2. Crear nuevo informe
3. Seleccionar BigQuery como fuente de datos
4. Configurar las uniones (joins) entre `fact_postulaciones` y las tablas de dimensiones
5. Diseñar gráficos y métricas según los KPIs del negocio

---

## 📂 Estructura del Proyecto

```
.
├── data/
├── etl/
├── sql/
├── dashboard/
├── docs/
└── readme.md
```

---

## 🛠️ Tecnologías Utilizadas

- **Google Cloud Storage** 
- **Dataproc Serverless** - Procesamiento distribuido con PySpark
- **BigQuery** - Data Warehouse
- **Looker Studio** - Visualización de datos

---
