#!/bin/bash
# ====================================
# DEPLOY CLOUD FUNCTION - BIGQUERY
# ====================================
# Deploya la Cloud Function que carga los datos refinados
# desde el Data Lake al Data Warehouse (BigQuery)

cd ~/nettalco-bq

gcloud functions deploy daily-bq-update \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --timeout 540s \
  --memory 1024MB \
  --entry-point load_refined_to_bq \
  --source ./
