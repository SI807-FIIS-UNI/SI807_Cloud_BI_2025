#!/bin/bash
set -e

# =====================================
# CONFIGURACIÓN GENERAL
# =====================================
PROJECT_ID="final-espinal-aguilar"
REGION="southamerica-west1"
BUCKET_NAME="final-bucket-espinal-aguilar"

echo "Proyecto: $PROJECT_ID"
echo "Región: $REGION"
echo "Bucket: $BUCKET_NAME"

gcloud config set project $PROJECT_ID

# =====================================
# OBTENER PROJECT NUMBER
# =====================================
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
  --format="value(projectNumber)")

EVENTARC_SA="service-${PROJECT_NUMBER}@gcp-sa-eventarc.iam.gserviceaccount.com"

echo "Eventarc Service Account: $EVENTARC_SA"

# =====================================
# 1. HABILITAR APIS
# =====================================
echo "Habilitando APIs necesarias..."

gcloud services enable \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  pubsub.googleapis.com \
  eventarc.googleapis.com \
  dataproc.googleapis.com \
  dataproc-control.googleapis.com \
  storage.googleapis.com \
  bigquery.googleapis.com \
  bigquerystorage.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com

# =====================================
# 2. CREAR BUCKET (SI NO EXISTE)
# =====================================
echo "Creando bucket $BUCKET_NAME..."

gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME || echo "Bucket ya existe"

# Crear carpetas lógicas
gsutil mkdir gs://$BUCKET_NAME/resources || true
gsutil mkdir gs://$BUCKET_NAME/raw || true

# =====================================
# 3. SUBIR SCRIPTS SPARK
# =====================================
echo "Subiendo SparkJobs..."

gsutil cp SparkJobs/*.py gs://$BUCKET_NAME/resources/

# =====================================
# 4. PERMISOS EVENTARC SOBRE BUCKET
# =====================================
echo "Asignando permisos Eventarc sobre el bucket..."

gsutil iam ch \
  serviceAccount:$EVENTARC_SA:roles/storage.objectViewer \
  gs://$BUCKET_NAME || true

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$EVENTARC_SA" \
  --role="roles/storage.legacyBucketReader" || true


# =====================================
# 5. PERMISOS CLOUD STORAGE → PUBSUB
# =====================================
echo "Asignando permisos Cloud Storage Service Agent..."

STORAGE_SA="service-${PROJECT_NUMBER}@gs-project-accounts.iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$STORAGE_SA" \
  --role="roles/pubsub.publisher" || true

# =====================================
# 6. LIMPIAR NOTIFICACIONES GCS
# =====================================
echo "Limpiando notificaciones GCS..."

for n in $(gsutil notification list gs://$BUCKET_NAME 2>/dev/null); do
  gsutil notification delete $n || true
done



# =====================================
# 7. DESPLEGAR CLOUD FUNCTION
# =====================================
echo "Desplegando Cloud Function final-dispatcher..."

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/CloudFunction"

gcloud functions deploy final-dispatcher \
  --gen2 \
  --runtime python310 \
  --region $REGION \
  --source . \
  --entry-point final_dispatcher \
  --trigger-bucket $BUCKET_NAME \
  --memory 512MB

echo "--- Despliegue completo exitoso"
