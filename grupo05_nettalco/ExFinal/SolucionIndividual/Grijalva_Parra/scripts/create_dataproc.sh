#!/bin/bash
set -e

# Crear cluster Dataproc

gcloud dataproc clusters create us-accidents-cluster \
    --region=us-central1 \
    --zone=us-central1-a \
    --master-machine-type=e2-standard-4 \
    --master-boot-disk-size=100 \
    --num-workers=2 \
    --worker-machine-type=e2-standard-4 \
    --worker-boot-disk-size=100 \
    --image-version=2.1-debian11 \
    --bucket=us-accidents-bd \
    --optional-components=JUPYTER \
    --enable-component-gateway \
    --max-idle=336h \
    --project=us-accidents-481401
