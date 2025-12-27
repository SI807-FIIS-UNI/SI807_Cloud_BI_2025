#!/bin/bash
# ====================================
# SETUP DATA LAKE BUCKETS
# ====================================
# Crea la estructura inicial de buckets (raw, trusted, refined)
# en Google Cloud Storage

mkdir -p raw trusted refined
gsutil cp -r raw gs://nettalco-data-bd_grupo05/raw/
gsutil cp -r trusted gs://nettalco-data-bd_grupo05/trusted/
gsutil cp -r refined gs://nettalco-data-bd_grupo05/refined/
