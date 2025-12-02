import logging
import pandas as pd
import io

from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound
from cloudevents.http import CloudEvent
from functions_framework import cloud_event


# --------------------------------------------------------
# CONFIG
# --------------------------------------------------------
BUCKET_MONITOREADO = "grupo6_scotiabank_bucket"
PREFIX_REFINED = "data/refined/"
TARGET_DATASET = "oro"
TARGET_TABLE = "hecho_riesgo"
BQ_LOCATION = "US"


# --------------------------------------------------------
# CARGA A BIGQUERY
# --------------------------------------------------------
def cargar_dataframe_bigquery(df, dataset_id, table_id):
    bq = bigquery.Client()
    project = bq.project

    table_ref = f"{project}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        autodetect=False,                    
        write_disposition="WRITE_APPEND",
        source_format=bigquery.SourceFormat.CSV,
    )

    job = bq.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    logging.info(f"Cargados {len(df)} registros en {table_ref}")


# --------------------------------------------------------
# CLOUD FUNCTION GEN2
# --------------------------------------------------------
@cloud_event
def refined_loader(event: CloudEvent):
    data = event.data
    bucket_name = data.get("bucket")
    file_name = data.get("name")

    logging.info(f"[GEN2] Evento recibido bucket={bucket_name}, file={file_name}")

    # Verifica bucket
    if bucket_name != BUCKET_MONITOREADO:
        logging.info("Ignorado: bucket diferente")
        return

    # Solo data/refined/data.csv
    if file_name != f"{PREFIX_REFINED}data.csv":
        logging.info(f"Ignorado: archivo no es data/refined/data.csv → {file_name}")
        return

    try:
        # Leer CSV desde GCS
        logging.info("Leyendo CSV desde GCS...")

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_bytes()

        df = pd.read_csv(io.BytesIO(content))

        logging.info(f"Archivo leído correctamente. Filas: {len(df)}")

        # Subir a BigQuery
        logging.info("Cargando a BigQuery (oro.hecho_riesgo)...")

        cargar_dataframe_bigquery(df, TARGET_DATASET, TARGET_TABLE)

        logging.info("Carga completada.")

    except Exception as e:
        logging.exception(f"ERROR procesando archivo {file_name}: {e}")
