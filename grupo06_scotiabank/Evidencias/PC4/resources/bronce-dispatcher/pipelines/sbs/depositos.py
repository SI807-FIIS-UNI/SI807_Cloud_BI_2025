from google.cloud import dataproc_v1
from google.cloud.dataproc_v1.types import Batch, PySparkBatch, RuntimeConfig
import logging
from datetime import datetime
import pandas as pd
from utils.gcs import leer_excel_desde_gcs
from utils.bigquery import cargar_dataframe_bigquery
from config.paths import DATASET_BRONCE, TABLE_DEPOSITO
import re


PROJECT_ID = "grupo6-scotiabank"
REGION = "southamerica-west1"
BUCKET_SCRIPT = "gs://grupo6_scotiabank_bucket/resources/jb_depositos.py"

BATCH_NAME = "jb-depositos"
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BATCH_NAME = f"{BATCH_NAME}-{timestamp}"



def run_pipeline_depositos(bucket_name, file_name):
    logging.info(f"[PIPELINE] Procesando Depositos -> {file_name}")

    df_raw = leer_excel_desde_gcs(bucket_name, file_name, "36")
    if df_raw is None:
        logging.error("No se pudo leer el Excel.")
        return

    df_transformado = _transformar_depositos(df_raw, file_name)
    if df_transformado is None or df_transformado.empty:
        logging.info("No hay datos transformados.")
        return

    cargar_dataframe_bigquery(df_transformado, DATASET_BRONCE, TABLE_DEPOSITO)

    ejecutar_dataproc_deposito()




# ----------------------- 
# TRANSFORM 
# -----------------------

def _transformar_depositos(df, file_name):
    
    # 1. Extraer MES y AÑO

    match = re.search(r'B-\d+-(\w{2})(\d{4})', file_name)
    if match:
        mes = match.group(1)
        anio = match.group(2)
    else:
        mes = None
        anio = None


    # 2. Combinar encabezados

    encabezado_1 = df.iloc[5].fillna("")
    encabezado_2 = df.iloc[6].fillna("")

    columnas = []
    for c1, c2 in zip(encabezado_1, encabezado_2):
        if c1 == "":
            columnas.append(c2.strip())
        elif c2 == "":
            columnas.append(c1.strip())
        else:
            columnas.append(f"{c1.strip()}_{c2.strip()}")

    df.columns = columnas

    # Eliminar filas de encabezado
    df = df.iloc[9:, :]
    df = df.rename(columns=lambda x: str(x).strip())


    # 3. Renombrar columnas

    df = df.rename(columns={
        "Empresas": "Institucion",
        "Depósitos del Público_Vista": "Vista",
        "Depósitos del Público_Ahorros": "Ahorros",
        "Depósitos del Público_Plazo": "Plazo",
        "Depósitos del Público_Restringidos 1/": "Restringidos 1/",
        "Depósitos del Sist. Financiero y Org. Internacionales_Total":
            "Depósitos del Sist. Financiero y Org. Internacionales"
    })



    # 4. Buscar columna de "Depósitos Totales"

    col_totales = next(
        (c for c in df.columns if str(c).startswith("Depósitos Totales")),
        None
    )
    if col_totales:
        df = df.rename(columns={col_totales: "Depósitos Totales (En miles de soles)"})


    # 5. Seleccionar columnas válidas
    columnas_finales = [
        "Institucion", "Vista", "Ahorros", "Plazo", "Restringidos 1/",
        "Depósitos del Sist. Financiero y Org. Internacionales",
        "Depósitos Totales (En miles de soles)"
    ]

    columnas_presentes = [c for c in columnas_finales if c in df.columns]
    df = df[columnas_presentes]


    # 6. Agregar mes y año
    df["anio"] = anio
    df["mes"] = mes

    df = df[["anio", "mes"] + columnas_presentes]


    # 7. Limpiar filas sin institución

    df = df.dropna(subset=["Institucion"], how="all")

    # 8. Renombrar columnas problemáticas

    df = df.rename(columns={
        "Restringidos 1/": "restringidos",
        "Depósitos del Sist. Financiero y Org. Internacionales": "DepositosSFOI",
        "Depósitos Totales (En miles de soles)": "DepositosTotales"
    })

    df = df.dropna(subset=["DepositosTotales"], how="all")
    df["fecha_carga"] = datetime.now()


    return df



# ----------------------- 
# JOB 
# -----------------------

def ejecutar_dataproc_deposito():
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