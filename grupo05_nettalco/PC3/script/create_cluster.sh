#!/bin/bash
gcloud dataproc clusters create nettalco-cluster \
    --region=us-east1 \
    --zone=us-east1-c \
    --master-machine-type=n1-standard-2 \
    --master-boot-disk-size=100 \
    --num-workers=2 \
    --worker-machine-type=n1-standard-2 \
    --worker-boot-disk-size=100 \
    --image-version=2.1-debian11 \
    --bucket=nettalco-data-bd_grupo05 \
    --optional-components=JUPYTER \
    --enable-component-gateway \
    --max-idle=336h \
    --project=nettalco-data-478503