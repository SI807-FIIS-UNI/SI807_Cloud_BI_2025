#!/bin/bash
set -e

# Crear dataset en BigQuery
auth_info="us-accidents-481401:us_accidents_dw"

bq mk \
  --dataset \
  --location=US \
  ${auth_info}

# Crear tabla de logs

bq mk --table \
${auth_info}.etl_logs \
table_name:STRING,layer:STRING,update_timestamp:TIMESTAMP,row_count:INTEGER,status:STRING
