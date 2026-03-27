#!/bin/bash
set -e

# Crear jobs del scheduler

gcloud scheduler jobs create http etl-bronce \
  --location us-central1 \
  --schedule "0 2 * * *" \
  --uri https://us-central1-us-accidents-481401.cloudfunctions.net/run_etl_bronce \
  --http-method GET \
  --time-zone "America/Lima"

gcloud scheduler jobs create http etl-plata \
  --location us-central1 \
  --schedule "0 3 * * *" \
  --uri https://us-central1-us-accidents-481401.cloudfunctions.net/run_etl_plata \
  --http-method GET \
  --time-zone "America/Lima"

gcloud scheduler jobs create http etl-oro \
  --location us-central1 \
  --schedule "0 4 * * *" \
  --uri https://us-central1-us-accidents-481401.cloudfunctions.net/run_etl_oro \
  --http-method GET \
  --time-zone "America/Lima"
