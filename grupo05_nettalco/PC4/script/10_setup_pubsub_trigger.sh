#!/bin/bash
# ====================================
# SETUP PUB/SUB TRIGGER
# ====================================
# Configura el tópico de Pub/Sub y la notificación del bucket
# para disparar automáticamente cuando llega un archivo a raw/

gcloud pubsub topics create nettalco-raw-topic

gsutil notification create \
  -t nettalco-raw-topic \
  -f json \
  -p raw/ \
  gs://nettalco-data-bd_grupo05
