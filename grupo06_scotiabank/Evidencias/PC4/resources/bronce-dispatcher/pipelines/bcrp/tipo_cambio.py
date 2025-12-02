import logging
import io
from datetime import datetime
import pandas as pd
from google.cloud import storage
from google.cloud import dataproc_v1
from google.cloud import bigquery


PROJECT_ID = "grupo6-scotiabank"
REGION = "southamerica-west1"
BUCKET_SCRIPT = "gs://grupo6_scotiabank_bucket/resources/jb_tipo_cambio.py"

DATASET_BRONCE = "bronce"
TABLE_TC = "tipo_cambio"


def leer_csv_desde_gcs(bucket_name, file_name):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        data = blob.download_as_bytes()
        df = pd.read_csv(io.BytesIO(data), dtype=str)

        return df
    except Exception as e:
        logging.error(f"[ERROR] No se pudo leer CSV {file_name}: {e}")
        return None

def transformar_tipo_cambio(df, file_name):
    try:
        df.columns = ["CODMES", "Valor"]

        # Limpieza
        df = df[df["CODMES"].notna()]
        df = df[~df["CODMES"].str.contains("CODMES", na=False)]
        df["Valor"] = df["Valor"].str.replace(",", "").astype(float)

        df["fecha_carga"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        return df

    except Exception as e:
        logging.error(f"Error transformando {file_name}: {e}")
        return None



def cargar_bigquery(df, dataset, table):
    try:
        client = bigquery.Client()
        table_id = f"{PROJECT_ID}.{dataset}.{table}"

        job = client.load_table_from_dataframe(df, table_id)
        job.result()

        logging.info(f"Datos cargados en {table_id}")

    except Exception as e:
        logging.error(f"Error cargando BigQuery {table}: {e}")



# ============================================================
# JOB
# ============================================================

def ejecutar_dataproc_tipo_cambio():
    logging.info("[DATAPROC] Ejecutando procesamiento Plata → Oro...")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_name = f"jb-tipo-cambio-{timestamp}"

    client = dataproc_v1.BatchControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )

    pyspark_batch = dataproc_v1.PySparkBatch(
        main_python_file_uri=BUCKET_SCRIPT
    )

    runtime_cfg = dataproc_v1.RuntimeConfig(
        version="2.1",
        properties={
            "spark.jars": "gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"
        }
    )

    batch = dataproc_v1.Batch(
        pyspark_batch=pyspark_batch,
        runtime_config=runtime_cfg,
    )

    client.create_batch(
        parent=f"projects/{PROJECT_ID}/locations/{REGION}",
        batch=batch,
        batch_id=batch_name,
    )

    logging.info("[DATAPROC] Enviado correctamente.")
    

def bronce_tipo_cambio(event, context):
    bucket = event["bucket"]
    file_name = event["name"]

    logging.info(f"[START] Procesando archivo: {file_name}")

    df_raw = leer_csv_desde_gcs(bucket, file_name)
    if df_raw is None:
        return

    df_bronce = transformar_tipo_cambio(df_raw, file_name)
    if df_bronce is None or df_bronce.empty:
        logging.warning("No hay datos válidos en el archivo.")
        return

    cargar_bigquery(df_bronce, DATASET_BRONCE, TABLE_TC)

    ejecutar_dataproc_tipo_cambio()

    logging.info("[FIN] Pipeline completado.")
