import io
import logging
from datetime import datetime
import pandas as pd
from google.cloud import storage, bigquery, dataproc_v1
from google.cloud.dataproc_v1.types import Batch, PySparkBatch, RuntimeConfig
from google.cloud.exceptions import NotFound
from cloudevents.http import CloudEvent
from functions_framework import cloud_event
from config.paths import (
    PROJECT_ID,
    DATASET_BRONCE,
    TABLE_RATIO,
    BUCKET_MONITOREADO
)


# --------------------------------------------------------
# CONFIG PARA EL JOB
# --------------------------------------------------------
REGION = "southamerica-west1"
BUCKET_SCRIPT = f"gs://{BUCKET_MONITOREADO}/resources/jb_medallion.py"
BATCH_NAME = "jb-medallion"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BATCH_NAME = f"{BATCH_NAME}-{timestamp}"



# --------------------------------------------------------
# Función principal
# --------------------------------------------------------

def run_pipeline(bucket_name, file_name):
    logging.info(f"[PIPELINE] CSV → BigQuery: {file_name}")

    cargar_csv_gcs_a_bigquery(
        bucket_name,
        file_name,
        DATASET_BRONCE,
        TABLE_RATIO
    ) 

    ejecutar_dataproc()


# ----------------------- 
# JOB 
# -----------------------

def ejecutar_dataproc():
    logging.info("[DATAPROC] Lanzando PySpark Batch Plata → Oro...")

    client = dataproc_v1.BatchControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )

    pyspark_batch = PySparkBatch(
        main_python_file_uri=BUCKET_SCRIPT
    )

    runtime_cfg = RuntimeConfig(
        version="2.1",
        properties={
            "spark.jars": "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar",
            "spark.executor.instances": "2",
            "spark.executor.cores": "4",
            "spark.executor.memory": "4g",
            "spark.driver.cores": "4",
            "spark.driver.memory": "4g",
        }
    )

    batch = Batch(
        pyspark_batch=pyspark_batch,
        runtime_config=runtime_cfg,
    )

    operation = client.create_batch(
        parent=f"projects/{PROJECT_ID}/locations/{REGION}",
        batch=batch,
        batch_id=BATCH_NAME,
    )

    logging.info("[DATAPROC] Batch enviado correctamente.")


# --------------------------------------------------------
# CARGA A BIGQUERY
# --------------------------------------------------------
def cargar_csv_gcs_a_bigquery(bucket_name, file_name, dataset_id, table_id):
    bq = bigquery.Client()
    project = bq.project

    dataset_ref = f"{project}.{dataset_id}"
    table_ref = f"{project}.{dataset_id}.{table_id}"
    uri = f"gs://{bucket_name}/{file_name}"

    # Crear dataset si no existe
    try:
        bq.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "southamerica-west1"
        bq.create_dataset(dataset, exists_ok=True)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True
    )

    job = bq.load_table_from_uri(
        uri,
        table_ref,
        job_config=job_config
    )

    job.result()

    logging.info(f"CSV cargado desde GCS a BigQuery: {uri}")
