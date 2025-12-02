from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.types import Batch, PySparkBatch, RuntimeConfig
import logging
from datetime import datetime
import pandas as pd
from utils.gcs import leer_excel_desde_gcs
from utils.bigquery import cargar_dataframe_bigquery
from config.paths import DATASET_BRONCE, TABLE_credito
import re


PROJECT_ID = "grupo6-scotiabank"
REGION = "southamerica-west1"
BUCKET_SCRIPT = "gs://grupo6_scotiabank_bucket/resources/jb_creditos.py"

BATCH_NAME = "jb_creditos"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BATCH_NAME = f"{BATCH_NAME}-{timestamp}"



def run_pipeline_creditos(bucket_name, file_name):
    logging.info(f"[PIPELINE] Procesando creditos -> {file_name}")

    df_raw = leer_excel_desde_gcs(bucket_name, file_name, "36")
    if df_raw is None:
        logging.error("No se pudo leer el Excel.")
        return

    df_transformado = _transformar_creditos(df_raw, file_name)
    if df_transformado is None or df_transformado.empty:
        logging.info("No hay datos transformados.")
        return

    cargar_dataframe_bigquery(df_transformado, DATASET_BRONCE, TABLE_credito)

    ejecutar_dataproc_credito()




# ----------------------- 
# TRANSFORM 
# -----------------------

def _transformar_creditos(df, file_name):
    try:
        # --------------------------------------
        # 1. Estructura: tomar desde fila 7
        # --------------------------------------
        df = df.iloc[7:].reset_index(drop=True)

        df.columns = [
            "Empresa",
            "Vigentes_Corto_Plazo",
            "Vigentes_Largo_Plazo",
            "Reestructurados",
            "Refinanciados",
            "Vencidos",
            "Cobranza_Judicial",
            "Total_Creditos_Directos"
        ]

        # --------------------------------------
        # 2. Cortar al TOTAL
        # --------------------------------------
        idx_total = df[df["Empresa"].str.startswith("TOTAL", na=False)].index

        if len(idx_total) == 0:
            return None

        df = df.iloc[:idx_total[0] + 1]

        # --------------------------------------
        # 3. Obtener mes y año del nombre archivo
        # --------------------------------------
        nombre = file_name.replace(".XLS", "").replace(".xlsx", "")

        sufijo = nombre.split("-")[-1]
        mes_abrev = sufijo[:2].lower()
        anio_str = sufijo[2:]

        mes_map = {
            "en": 1, "fe": 2, "ma": 3, "ab": 4,
            "my": 5, "jn": 6, "jl": 7, "ag": 8,
            "se": 9, "oc": 10, "no": 11, "di": 12
        }

        mes = mes_map.get(mes_abrev, None)
        anio = int(anio_str) if anio_str.isdigit() and len(anio_str) == 4 else None

        # --------------------------------------
        # 4. Normalización numérica
        # --------------------------------------
        cols_numeric = [
            "Vigentes_Corto_Plazo",
            "Vigentes_Largo_Plazo",
            "Reestructurados",
            "Refinanciados",
            "Vencidos",
            "Cobranza_Judicial",
            "Total_Creditos_Directos"
        ]

        for col in cols_numeric:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # --------------------------------------
        # 5. Agregar metadata
        # --------------------------------------
        df["Anio"] = anio
        df["Mes"] = mes
        df["fecha_carga"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        df["Archivo_Origen"] = file_name

        return df

    except Exception as e:
        logging.exception(f"Error transformando créditos {file_name}: {e}")
        return None



# ----------------------- 
# JOB 
# -----------------------

def ejecutar_dataproc_credito():
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