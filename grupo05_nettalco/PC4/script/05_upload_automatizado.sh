#!/bin/bash
# ====================================
# UPLOAD AUTOMATIZADO CON GSUTIL
# ====================================
# Script que automatiza la carga de archivos locales al bucket raw/
# en Google Cloud Storage

BUCKET=gs://nettalco-data-bd_grupo05/raw
LOCAL_PATH=/ruta/a/archivos

for file in $LOCAL_PATH/*; do
  gsutil cp $file $BUCKET/
done
