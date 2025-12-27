#!/bin/bash
# ====================================
# SETUP AUTOSCALING POLICY
# ====================================
# Configura la política de autoscaling en el cluster Dataproc
# para escalar automáticamente según la carga de trabajo

gcloud dataproc clusters update nettalco-cluster \
    --region us-east1 \
    --autoscaling-policy nettalo-autoscale
