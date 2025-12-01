#!/bin/bash
# ====================================
# SETUP SECRET MANAGER
# ====================================
# Configura las credenciales y configuración en Secret Manager
# para su uso en los jobs ETL de Dataproc

echo -n '{
  "PROJECT_ID": "nettalco-data-478503",
  "REGION": "us-east1",
  "CLUSTER_NAME": "nettalco-cluster",
  "PYSPARK_FILE": "gs://nettalco-data-bd_grupo05/job/procesamiento_nettalco_etl.py"
}' | gcloud secrets versions add nettalco_config --data-file=-
