**### Proyecto Final: Sistema de Inteligencia de Negocios End-to-End en GCP**



\## Descripción

Este proyecto implementa una arquitectura de datos moderna en \*\*Google Cloud Platform (GCP)\*\* para el análisis de órdenes de servicio (SOTs) en una empresa de telecomunicaciones. Se procesa un volumen de \*\*1 Millón de registros\*\* simulados, orquestando un flujo ETL desde un Data Lake (GCS) hasta un Data Warehouse (BigQuery) utilizando Apache Spark (Dataproc).



\## Arquitectura

1\.  \*\*Ingesta (Bronze):\*\* Generación de data sintética (JSON) almacenada en Google Cloud Storage.

2\.  \*\*Procesamiento (Silver):\*\* Cluster efímero de \*\*Dataproc (Spark)\*\* para limpieza, transformación y carga a Staging.

3\.  \*\*Modelado (Gold):\*\* Esquema Estrella en \*\*BigQuery\*\* con tablas particionadas para optimización de costos y consultas.



\## Guía de Reproducción



\### 1. Prerrequisitos

\* Cuenta de Google Cloud Platform activa.

\* Cloud Shell activado.

\* APIs habilitadas: `dataproc`, `bigquery`, `storage`.



\### 2. Configuración del Entorno

Ejecutar en la terminal de Cloud Shell:



```bash

export PROJECT\_ID=$(gcloud config get-value project)

export REGION="us-central1"

export BUCKET\_NAME="${PROJECT\_ID}-datalake"

export CLUSTER\_NAME="cluster-etl-sot"



\# Crear Bucket para Data Lake

gsutil mb -l $REGION gs://$BUCKET\_NAME/



**###ETL**

cat <<EOF > etl\_spark.py

import sys

from pyspark.sql import SparkSession

from pyspark.sql.functions import col, to\_date, when



bucket = sys.argv\[1].replace('gs://', '').strip()

input\_path = f"gs://{bucket}/bronze"

temp\_bucket = f"{bucket}/tmp"



spark = SparkSession.builder.appName("ETL\_SOT").getOrCreate()



\# Carga Contratas

spark.read.json(f"{input\_path}/bronze\_contratas.json") \\

&nbsp;   .write.format("bigquery") \\

&nbsp;   .option("table", "sot\_analytics.stg\_contratas") \\

&nbsp;   .option("temporaryGcsBucket", temp\_bucket).mode("overwrite").save()



\# Carga y Transformación de SOTS

df = spark.read.json(f"{input\_path}/bronze\_sots.json")

df\_clean = df \\

&nbsp;   .withColumn("fecha\_creacion", to\_date(col("fecha\_creacion"))) \\

&nbsp;   .withColumn("fecha\_planificada", to\_date(col("fecha\_planificada"))) \\

&nbsp;   .withColumn("fecha\_cierre", to\_date(col("fecha\_cierre"))) \\

&nbsp;   .withColumn("tiempo\_excedente", col("tiempo\_real\_min") - col("tiempo\_planificado\_min")) \\

&nbsp;   .withColumn("tiempo\_excedente", when(col("tiempo\_excedente") < 0, 0).otherwise(col("tiempo\_excedente")))



df\_clean.write.format("bigquery") \\

&nbsp;   .option("table", "sot\_analytics.stg\_sots") \\

&nbsp;   .option("temporaryGcsBucket", temp\_bucket).mode("overwrite").save()

EOF



\# Subir script y ejecutar Job en Cluster Efímero

gsutil cp etl\_spark.py gs://$BUCKET\_NAME/scripts/

gcloud dataproc clusters create $CLUSTER\_NAME --region=$REGION --single-node --master-machine-type=e2-standard-2 --quiet

gcloud dataproc jobs submit pyspark gs://$BUCKET\_NAME/scripts/etl\_spark.py --cluster=$CLUSTER\_NAME --region=$REGION --jars=gs://spark-lib/bigquery/spark-bigquery-latest\_2.12.jar -- $BUCKET\_NAME

gcloud dataproc clusters delete $CLUSTER\_NAME --region=$REGION --quiet





**###BIG QUERY**



\# Crear Dimensiones y Tabla de Hechos Particionada

bq query --use\_legacy\_sql=false "

CREATE OR REPLACE TABLE \\`$PROJECT\_ID.sot\_analytics.dim\_contrata\\` AS 

SELECT id\_contrata, nombre, zona FROM \\`$PROJECT\_ID.sot\_analytics.stg\_contratas\\`;



CREATE OR REPLACE TABLE \\`$PROJECT\_ID.sot\_analytics.fact\_sot\\` 

PARTITION BY fecha\_creacion AS 

SELECT 

&nbsp;   s.id\_sot, s.id\_contrata, s.fecha\_creacion, s.fecha\_planificada, s.fecha\_cierre,

&nbsp;   s.estado\_sot, s.tiempo\_planificado\_min, s.tiempo\_real\_min, s.tiempo\_excedente,

&nbsp;   IF(s.estado\_sot = 'INSTALADA', 1, 0) as es\_instalada,

&nbsp;   IF(s.estado\_sot = 'FRAUDE', 1, 0) as es\_fraude

FROM \\`$PROJECT\_ID.sot\_analytics.stg\_sots\\` s;"

