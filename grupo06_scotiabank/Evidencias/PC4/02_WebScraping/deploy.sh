#!/bin/bash

# Script de despliegue para Cloud Function de SBS Downloader
# Proyecto: grupo6-scotiabank
# Incluye seguridad con Service Account desde el inicio

set -e  # Salir si hay algún error

PROJECT_ID="grupo6-scotiabank"
REGION="southamerica-east1"  # São Paulo (más cerca de Perú)
FUNCTION_NAME="sbs-downloader"
BUCKET_NAME="grupo6_scotiabank_bucket"
SA_NAME="sbs-downloader-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
SCHEDULER_SA_NAME="sbs-scheduler-sa"
SCHEDULER_SA_EMAIL="${SCHEDULER_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "======================================"
echo "Desplegando SBS Downloader a GCP"
echo "======================================"
echo "Proyecto: $PROJECT_ID"
echo "Región: $REGION (São Paulo)"
echo "Función: $FUNCTION_NAME"
echo "Seguridad: Service Account privado"
echo ""

# 1. Configurar proyecto
echo "📋 Configurando proyecto..."
gcloud config set project $PROJECT_ID

# 2. Habilitar APIs necesarias
echo "🔧 Habilitando APIs de GCP..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable run.googleapis.com

# 3. Crear bucket si no existe
echo "🪣 Verificando bucket..."
if ! gsutil ls gs://$BUCKET_NAME > /dev/null 2>&1; then
    echo "Creando bucket $BUCKET_NAME..."
    gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME
    echo "✓ Bucket creado"
else
    echo "✓ Bucket ya existe: $BUCKET_NAME"
fi

# Nota: Las carpetas en GCS se crean automáticamente cuando subes el primer archivo
# No es necesario crear carpetas manualmente

# 4. Crear Service Account para la Cloud Function
echo "🔐 Configurando Service Account para la función..."
if ! gcloud iam service-accounts describe $SA_EMAIL > /dev/null 2>&1; then
    echo "Creando Service Account: $SA_NAME..."
    gcloud iam service-accounts create $SA_NAME \
        --display-name="SBS Downloader Function Service Account" \
        --description="Service Account para ejecutar la Cloud Function de descarga SBS"
    echo "✓ Service Account creado"
else
    echo "✓ Service Account ya existe: $SA_NAME"
fi

# 5. Otorgar permisos al Service Account de la función
echo "🔑 Otorgando permisos al Service Account de la función..."

# Permiso para escribir en Cloud Storage
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/storage.objectAdmin" \
    --condition=None \
    --quiet

echo "✓ Permisos otorgados (Storage Object Admin)"

# 6. Desplegar Cloud Function (2nd gen) con Service Account
echo "🚀 Desplegando Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --region=$REGION \
    --runtime=python311 \
    --source=. \
    --entry-point=sbs_downloader_http \
    --trigger-http \
    --no-allow-unauthenticated \
    --service-account=$SA_EMAIL \
    --timeout=540s \
    --memory=512MB \
    --max-instances=1 \
    --set-env-vars=BUCKET_NAME=$BUCKET_NAME

echo "✓ Cloud Function desplegada"

# 7. Obtener URL de la función
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --gen2 --format='value(serviceConfig.uri)')
echo "URL de la función: $FUNCTION_URL"

# 8. Crear Service Account para Cloud Scheduler
echo "🔐 Configurando Service Account para el Scheduler..."
if ! gcloud iam service-accounts describe $SCHEDULER_SA_EMAIL > /dev/null 2>&1; then
    echo "Creando Service Account: $SCHEDULER_SA_NAME..."
    gcloud iam service-accounts create $SCHEDULER_SA_NAME \
        --display-name="SBS Scheduler Service Account" \
        --description="Service Account para invocar la Cloud Function desde Cloud Scheduler"
    echo "✓ Service Account creado"
else
    echo "✓ Service Account ya existe: $SCHEDULER_SA_NAME"
fi

# 9. Otorgar permiso al Scheduler SA para invocar la función
echo "🔑 Otorgando permisos de invocación..."
gcloud functions add-invoker-policy-binding $FUNCTION_NAME \
    --region=$REGION \
    --member="serviceAccount:$SCHEDULER_SA_EMAIL" \
    --gen2

echo "✓ Permisos de invocación otorgados"

# 10. Crear o actualizar Cloud Scheduler job
echo "⏰ Configurando Cloud Scheduler..."

if gcloud scheduler jobs describe sbs-downloader-monthly --location=$REGION > /dev/null 2>&1; then
    echo "Job de scheduler ya existe. Actualizando..."
    gcloud scheduler jobs update http sbs-downloader-monthly \
        --location=$REGION \
        --schedule="0 2 1 * *" \
        --uri=$FUNCTION_URL \
        --http-method=POST \
        --headers="Content-Type=application/json" \
        --message-body='{}' \
        --time-zone="America/Lima" \
        --oidc-service-account-email=$SCHEDULER_SA_EMAIL \
        --quiet
else
    echo "Creando nuevo job de scheduler..."
    gcloud scheduler jobs create http sbs-downloader-monthly \
        --location=$REGION \
        --schedule="0 2 1 * *" \
        --uri=$FUNCTION_URL \
        --http-method=POST \
        --headers="Content-Type=application/json" \
        --message-body='{}' \
        --time-zone="America/Lima" \
        --oidc-service-account-email=$SCHEDULER_SA_EMAIL \
        --description="Ejecuta descarga de reportes SBS el primer día de cada mes a las 2 AM"
fi

echo "✓ Scheduler configurado"

echo ""
echo "======================================"
echo "✅ DESPLIEGUE COMPLETADO"
echo "======================================"
echo ""
echo "📝 Información del despliegue:"
echo "  - Función: $FUNCTION_NAME"
echo "  - Región: $REGION (São Paulo)"
echo "  - URL: $FUNCTION_URL"
echo "  - Función SA: $SA_EMAIL"
echo "  - Scheduler SA: $SCHEDULER_SA_EMAIL"
echo "  - Schedule: Primer día de cada mes a las 2:00 AM (Lima)"
echo "  - Bucket: gs://$BUCKET_NAME/data/raw/SBS/"
echo "  - Seguridad: ✓ Privada (solo accesible vía Service Account)"
echo ""
echo "🧪 Para probar manualmente (requiere autenticación):"
echo ""
echo "  # Método 1: Usando gcloud (recomendado)"
echo "  gcloud functions call $FUNCTION_NAME \\"
echo "    --region=$REGION \\"
echo "    --gen2 \\"
echo "    --data='{}'"
echo ""
echo "  # Método 2: Usando curl con token de identidad"
echo "  TOKEN=\$(gcloud auth print-identity-token)"
echo "  curl -X POST $FUNCTION_URL \\"
echo "    -H \"Authorization: Bearer \$TOKEN\" \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{}'"
echo ""
echo "  # Para probar un solo reporte:"
echo "  gcloud functions call $FUNCTION_NAME \\"
echo "    --region=$REGION \\"
echo "    --gen2 \\"
echo "    --data='{\"formato\": \"B-2201\"}'"
echo ""
echo "📊 Para ver logs:"
echo "  gcloud functions logs read $FUNCTION_NAME --region=$REGION --gen2 --limit=50"
echo ""
echo "⏰ Para ejecutar el scheduler manualmente:"
echo "  gcloud scheduler jobs run sbs-downloader-monthly --location=$REGION"
echo ""
echo "📂 Para ver archivos descargados:"
echo "  gsutil ls -r gs://$BUCKET_NAME/data/raw/SBS/"
echo ""
echo "📋 Para ver el log CSV:"
echo "  gsutil cat gs://$BUCKET_NAME/logs/descargas_sbs.csv | head -20"
echo ""
echo "🗑️  Para destruir todos los recursos:"
echo "  ./destroy.sh"
echo ""