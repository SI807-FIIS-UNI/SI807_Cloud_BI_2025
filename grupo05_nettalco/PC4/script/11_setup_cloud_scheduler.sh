#!/bin/bash
# ====================================
# SETUP CLOUD SCHEDULER
# ====================================
# Configura el Cloud Scheduler para ejecutar diariamente
# la carga de datos refinados a BigQuery a las 00:00 UTC

gcloud scheduler jobs create http daily-bq-load \
  --schedule "0 0 * * *" \
  --uri "https://us-central1-nettalco-data-478503.cloudfunctions.net/daily-bq-update" \
  --http-method GET \
  --location us-central1
