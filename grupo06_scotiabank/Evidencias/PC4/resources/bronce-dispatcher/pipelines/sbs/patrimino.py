from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.types import Batch, PySparkBatch, RuntimeConfig
import logging
from datetime import datetime
import pandas as pd
from utils.gcs import leer_excel_desde_gcs
from utils.bigquery import cargar_dataframe_bigquery
from config.paths import DATASET_BRONCE, TABLE_PATRIMONIO


PROJECT_ID = "grupo6-scotiabank"
REGION = "southamerica-west1"
BUCKET_SCRIPT = "gs://grupo6_scotiabank_bucket/resources/jb_patrimonio.py"

BATCH_NAME = "jb-patrimonio"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BATCH_NAME = f"{BATCH_NAME}-{timestamp}"



def run_pipeline_patrimonio(bucket_name, file_name):
    logging.info(f"[PIPELINE] Procesando Patrimonio -> {file_name}")

    # --- Leer Excel desde GCS ---
    df_raw = leer_excel_desde_gcs(bucket_name, file_name, sheet_name="21")
    if df_raw is None:
        logging.error("No se pudo leer el Excel.")
        return

    # --- Transform ---
    df_transformado = _transformar_patrimonio(df_raw, file_name)
    if df_transformado is None or df_transformado.empty:
        logging.info("No hay datos transformados.")
        return

    # --- Cargar en BigQuery ---
    cargar_dataframe_bigquery(df_transformado, DATASET_BRONCE, TABLE_PATRIMONIO)

    # --- Lanzar Dataproc ---
    ejecutar_dataproc_patrimonio()



# --------------------------------------------------
# TRANSFORMACIÓN
# --------------------------------------------------
def _transformar_patrimonio(df, file_name):
    try:
        # Extraer fecha del nombre del archivo
        parts = file_name.replace(".XLS", "").replace(".xlsx", "").split("-")
        raw_date = parts[-1]
        mes = raw_date[:2]

        try:
            anio = int(raw_date[-4:])
        except:
            anio = None

        df[0] = df[0].astype(str).str.strip()

        # Ubicar bloque de datos
        inicio = 7
        fin_idx = df[df[0].str.contains("TOTAL BANCA MÚLTIPLE", case=False, na=False)].index
        if len(fin_idx) == 0:
            return None
        
        fin = fin_idx[0]
        bloque = df.iloc[inicio:fin, :]

        # --- Patrimonio en moneda nacional ---
        mn = bloque.iloc[:, [0, 1]]
        mn.columns = ["Institución", "Patrimonio"]
        mn["Moneda"] = "MN"

        # --- Patrimonio en moneda extranjera ---
        me = bloque.iloc[:, [0, 3]]
        me.columns = ["Institución", "Patrimonio"]
        me["Moneda"] = "ME"

        df_total = pd.concat([mn, me], ignore_index=True)
        df_total["Institución"] = df_total["Institución"].str.strip()

        # Limpiar filas no válidas
        df_total = df_total[~df_total["Institución"].str.contains(
            "TOTAL BANCA MÚLTIPLE", case=False, na=False
        )]

        # Limpiar valores numéricos
        df_total["Patrimonio"] = (
            df_total["Patrimonio"]
            .astype(str)
            .str.replace(",", "")
            .str.strip()
        )
        df_total["Patrimonio"] = pd.to_numeric(df_total["Patrimonio"], errors="coerce")

        # Agregar columnas estructurales
        df_total["anio"] = anio
        df_total["mes"] = mes
        df_total["fecha_carga"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        return df_total

    except Exception as e:
        logging.exception(f"Error transformando {file_name}: {e}")
        return None



# --------------------------------------------------
# JOB DATAPROC
# --------------------------------------------------
def ejecutar_dataproc_patrimonio():
    logging.info("[DATAPROC] Lanzando PySpark Batch Plata → Oro (Patrimonio)...")

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

    client.create_batch(
        parent=f"projects/{PROJECT_ID}/locations/{REGION}",
        batch=batch,
        batch_id=BATCH_NAME,
    )

    logging.info("[DATAPROC] Batch enviado correctamente.")
