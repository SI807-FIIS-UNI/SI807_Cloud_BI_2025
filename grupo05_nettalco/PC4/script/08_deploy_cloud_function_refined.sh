#!/bin/bash
# ====================================
# DEPLOY CLOUD FUNCTION - REFINED ETL
# ====================================
# Deploya la Cloud Function que dispara el job Dataproc
# cuando llega un archivo nuevo al bucket raw/

cd ~/nettalco-fn
gcloud functions deploy nettalco-dataproc-raw-trigger \
  --runtime python311 \
  --trigger-topic nettalco-raw-topic \
  --region us-central1 \
  --timeout 540s \
  --memory 1024MB \
  --entry-point trigger_dataproc \
  --source ./
