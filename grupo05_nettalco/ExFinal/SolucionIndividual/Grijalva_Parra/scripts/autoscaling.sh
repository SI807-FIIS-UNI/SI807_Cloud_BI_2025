#!/bin/bash
set -e

# Asignar política autoscaling al cluster

gcloud dataproc clusters update us-accidents-cluster \
  --region us-central1 \
  --autoscaling-policy etl-autoscaling
