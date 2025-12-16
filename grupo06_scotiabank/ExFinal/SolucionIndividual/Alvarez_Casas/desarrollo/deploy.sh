#!/bin/bash
set -e

# ==============================
# VARIABLES DEL PROYECTO
# ==============================
PROJECT_ID="final-julio-alvarez"
PROJECT_NAME="Final Julio Alvarez"
BILLING_ACCOUNT="011771-C8B653-A0A413"

REGION="us-east1"
BUCKET_NAME="final-julio-alvarez-bucket"


# ==============================
# 1. CREAR PROYECTO
# ==============================
echo "Creando proyecto GCP..."
gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"

gcloud config set project $PROJECT_ID

# ==============================
# 2. ASOCIAR FACTURACIÓN
# ==============================
echo "Asociando cuenta de facturación..."
gcloud billing projects link $PROJECT_ID \
  --billing-account=$BILLING_ACCOUNT

# ==============================
# 3. HABILITAR SERVICIOS NECESARIOS
# ==============================
echo "Habilitando APIs necesarias..."
gcloud services enable \
  compute.googleapis.com \
  storage.googleapis.com \
  dataproc.googleapis.com

# ==============================
# 4. CREAR BUCKET (DATA LAKE - BRONCE)
# ==============================
echo "Creando bucket de almacenamiento..."
gsutil mb -p $PROJECT_ID -l $REGION gs://$BUCKET_NAME

# ==============================
# 5. CREAR ESTRUCTURA MEDALLION - BRONCE
# ==============================
echo "Creando estructura Bronce..."

gsutil cp /dev/null gs://$BUCKET_NAME/bronce/raw/.keep
gsutil cp /dev/null gs://$BUCKET_NAME/bronce/processed/.keep
gsutil cp /dev/null gs://$BUCKET_NAME/bronce/curated/.keep

# ==============================
# 6. CARGA DE CSV DESDE CLI
# ==============================
echo "Cargando archivos CSV a bronce/raw..."
gsutil cp ./csv/*.csv gs://$BUCKET_NAME/bronce/raw/

