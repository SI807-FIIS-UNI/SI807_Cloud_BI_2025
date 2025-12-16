#!/bin/bash

# Configuración
export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-central1"
export BUCKET_NAME="${PROJECT_ID}-datalake"
export CLUSTER_NAME="cluster-etl-sot"

echo "--- 1. Preparando Infraestructura ---"
gsutil mb -l $REGION gs://$BUCKET_NAME/ 2>/dev/null || echo "Bucket ya existe"
bq mk --location=$REGION --dataset $PROJECT_ID:sot_analytics 2>/dev/null || echo "Dataset ya existe"

echo "--- 2. Subiendo Archivos (Data y Scripts) ---"
# Subimos los JSON que tengas en tu carpeta local data/raw
gsutil cp data/raw/*.json gs://$BUCKET_NAME/bronze/
# Subimos el script de python
gsutil cp scripts/etl_spark.py gs://$BUCKET_NAME/scripts/

echo "--- 3. Procesando con Dataproc (Spark) ---"
gcloud dataproc clusters create $CLUSTER_NAME \
    --region=$REGION --single-node --master-machine-type=e2-standard-2 --quiet

gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/etl_spark.py \
    --cluster=$CLUSTER_NAME --region=$REGION \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    -- $BUCKET_NAME

gcloud dataproc clusters delete $CLUSTER_NAME --region=$REGION --quiet

echo "--- 4. Modelando en BigQuery ---"
# Lee el archivo SQL local y lo ejecuta en la nube
bq query --use_legacy_sql=false --project_id=$PROJECT_ID "$(cat scripts/modeling.sql)"

echo "--- FIN DEL PROCESO ---"