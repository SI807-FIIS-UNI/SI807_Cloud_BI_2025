#!/bin/bash

# Script de destrucción para Cloud Function de SBS Downloader
# Elimina TODOS los recursos creados y revoca permisos

set -e  # Salir si hay algún error

PROJECT_ID="grupo6-scotiabank"
REGION="southamerica-east1"
FUNCTION_NAME="sbs-downloader"
BUCKET_NAME="grupo6_scotiabank_bucket"
SA_NAME="sbs-downloader-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
SCHEDULER_SA_NAME="sbs-scheduler-sa"
SCHEDULER_SA_EMAIL="${SCHEDULER_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "======================================"
echo "⚠️  DESTRUCCIÓN DE RECURSOS SBS DOWNLOADER"
echo "======================================"
echo ""
echo "Esto eliminará:"
echo "  ❌ Cloud Scheduler job"
echo "  ❌ Cloud Function"
echo "  ❌ Service Accounts (2)"
echo "  ❌ IAM Policy Bindings"
echo ""

# Confirmación del usuario
read -p "⚠️  ¿Deseas ELIMINAR los archivos del bucket también? (s/N): " -n 1 -r
echo
DELETE_FILES=$REPLY

echo ""
read -p "¿Estás seguro de continuar con la destrucción? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]
then
    echo "❌ Destrucción cancelada."
    exit 1
fi

echo ""
echo "🗑️  Iniciando destrucción de recursos..."
echo ""

# 1. Eliminar Cloud Scheduler job
echo "⏰ Eliminando Cloud Scheduler job..."
if gcloud scheduler jobs describe sbs-downloader-monthly --location=$REGION > /dev/null 2>&1; then
    gcloud scheduler jobs delete sbs-downloader-monthly \
        --location=$REGION \
        --quiet
    echo "✓ Scheduler job eliminado"
else
    echo "⏭️  Scheduler job no existe"
fi

# 2. Eliminar Cloud Function
echo "🔧 Eliminando Cloud Function..."
if gcloud functions describe $FUNCTION_NAME --region=$REGION --gen2 > /dev/null 2>&1; then
    gcloud functions delete $FUNCTION_NAME \
        --region=$REGION \
        --gen2 \
        --quiet
    echo "✓ Cloud Function eliminada"
else
    echo "⏭️  Cloud Function no existe"
fi

# 3. Revocar permisos del Function Service Account
echo "🔐 Revocando permisos del Function Service Account..."
if gcloud iam service-accounts describe $SA_EMAIL > /dev/null 2>&1; then
    # Revocar rol de Storage Object Admin
    gcloud projects remove-iam-policy-binding $PROJECT_ID \
        --member="serviceAccount:$SA_EMAIL" \
        --role="roles/storage.objectAdmin" \
        --quiet 2>/dev/null || echo "  ⚠️  Permiso ya no existe o no se pudo revocar"
    
    echo "✓ Permisos revocados"
else
    echo "⏭️  Service Account no existe"
fi

# 4. Eliminar Function Service Account
echo "🗑️  Eliminando Function Service Account..."
if gcloud iam service-accounts describe $SA_EMAIL > /dev/null 2>&1; then
    gcloud iam service-accounts delete $SA_EMAIL --quiet
    echo "✓ Function Service Account eliminada: $SA_EMAIL"
else
    echo "⏭️  Function Service Account no existe"
fi

# 5. Eliminar Scheduler Service Account
echo "🗑️  Eliminando Scheduler Service Account..."
if gcloud iam service-accounts describe $SCHEDULER_SA_EMAIL > /dev/null 2>&1; then
    gcloud iam service-accounts delete $SCHEDULER_SA_EMAIL --quiet
    echo "✓ Scheduler Service Account eliminada: $SCHEDULER_SA_EMAIL"
else
    echo "⏭️  Scheduler Service Account no existe"
fi

# 6. Eliminar archivos del bucket (opcional)
if [[ $DELETE_FILES =~ ^[Ss]$ ]]; then
    echo "🗑️  Eliminando archivos del bucket..."
    
    # Eliminar carpeta de datos SBS
    if gsutil ls gs://$BUCKET_NAME/data/raw/SBS/ > /dev/null 2>&1; then
        gsutil -m rm -r gs://$BUCKET_NAME/data/raw/SBS/ || echo "⚠️  Error eliminando archivos SBS"
        echo "✓ Archivos SBS eliminados"
    else
        echo "⏭️  Carpeta SBS no existe"
    fi
    
    # Eliminar logs
    if gsutil ls gs://$BUCKET_NAME/logs/descargas_sbs.csv > /dev/null 2>&1; then
        gsutil rm gs://$BUCKET_NAME/logs/descargas_sbs.csv || echo "⚠️  Error eliminando log"
        echo "✓ Log CSV eliminado"
    else
        echo "⏭️  Log CSV no existe"
    fi
    
    echo ""
    read -p "⚠️  ¿Deseas eliminar el BUCKET COMPLETO? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        gsutil rb gs://$BUCKET_NAME/ || echo "⚠️  Error eliminando bucket (puede tener contenido)"
        echo "✓ Bucket eliminado"
    else
        echo "⏭️  Bucket preservado: gs://$BUCKET_NAME/"
    fi
else
    echo "⏭️  Archivos del bucket preservados"
fi

echo ""
echo "======================================"
echo "✅ DESTRUCCIÓN COMPLETADA"
echo "======================================"
echo ""
echo "Recursos eliminados:"
echo "  ✓ Cloud Scheduler job"
echo "  ✓ Cloud Function"
echo "  ✓ Service Account: $SA_EMAIL"
echo "  ✓ Service Account: $SCHEDULER_SA_EMAIL"
echo "  ✓ IAM Policy Bindings revocados"

if [[ $DELETE_FILES =~ ^[Ss]$ ]]; then
    echo "  ✓ Archivos eliminados"
else
    echo "  ⏭️  Archivos preservados en gs://$BUCKET_NAME/"
fi

echo ""
echo "📋 Para verificar que todo fue eliminado:"
echo ""
echo "  # Verificar funciones"
echo "  gcloud functions list --region=$REGION --gen2"
echo ""
echo "  # Verificar scheduler"
echo "  gcloud scheduler jobs list --location=$REGION"
echo ""
echo "  # Verificar service accounts"
echo "  gcloud iam service-accounts list --filter=\"email:sbs-*\""
echo ""
echo "  # Verificar archivos"
echo "  gsutil ls -r gs://$BUCKET_NAME/"
echo ""
echo "💡 Consejo: Puedes re-desplegar cuando quieras ejecutando:"
echo "  ./deploy.sh"
echo ""