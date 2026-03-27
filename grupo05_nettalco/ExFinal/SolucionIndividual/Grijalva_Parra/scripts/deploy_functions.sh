#!/bin/bash
set -e

# Deploy de Cloud Functions para cada capa

pushd bronce >/dev/null
gcloud functions deploy run_etl_bronce \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1
popd >/dev/null

pushd plata >/dev/null
gcloud functions deploy run_etl_plata \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1
popd >/dev/null

pushd oro >/dev/null
gcloud functions deploy run_etl_oro \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1
popd >/dev/null
