import pandas as pd
import logging
from io import StringIO, BytesIO
import matplotlib.pyplot as plt
import os
from google.cloud import storage

# =========================
# CONFIGURACIÓN
# =========================
BUCKET_NAME = "bi-examen-dataset-mauricio-otero"

RAW_GCS_PATH = "bronce/raw/KaggleV2-May-2016.csv"
PROCESSED_GCS_PATH = "bronce/processed/noshow_processed.csv"

LOG_DIR = "docs"
PLOTS_DIR = "docs"
LOG_FILE = f"{LOG_DIR}/eda_logs.txt"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# =========================
# LOGGING
# =========================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("INICIO EDA - NO SHOW APPOINTMENTS (GCS RAW)")

try:
    # =========================
    # CONECTAR A GCS
    # =========================
    print("Conectando a GCS...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    if not bucket.exists():
        raise RuntimeError(f"El bucket {BUCKET_NAME} no existe")

    blob = bucket.blob(RAW_GCS_PATH)

    if not blob.exists():
        raise RuntimeError(f"No existe el archivo RAW: {RAW_GCS_PATH}")

    # =========================
    # LEER CSV DESDE RAW (GCS)
    # =========================
    print("Leyendo dataset desde GCS RAW...")
    raw_bytes = blob.download_as_bytes()
    df = pd.read_csv(BytesIO(raw_bytes))

    print(f"Dataset cargado | Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    logging.info(f"Shape: {df.shape}")

    # =========================
    # EXPLORACIÓN
    # =========================
    logging.info("HEAD:\n" + df.head().to_string())

    buffer = StringIO()
    df.info(buf=buffer)
    logging.info("INFO:\n" + buffer.getvalue())

    # =========================
    # LIMPIEZA
    # =========================
    df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"], errors="coerce")
    df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"], errors="coerce")

    df = df[(df["Age"] >= 0) & (df["Age"] <= 120)]
    df["No-show"] = df["No-show"].map({"Yes": 1, "No": 0})

    df = df.drop_duplicates()

    logging.info("Limpieza completada")

    # =========================
    # GRÁFICOS
    # =========================
    df["No-show"].value_counts().plot(kind="bar", title="Distribución No-Show")
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/no_show_distribution.png")
    plt.close()

    df.boxplot(column="Age", by="No-show")
    plt.title("Edad vs No-Show")
    plt.suptitle("")
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/age_vs_noshow.png")
    plt.close()

    logging.info("Gráficos generados")

    # =========================
    # GUARDAR PROCESSED LOCAL
    # =========================
    output_local = "noshow_processed.csv"
    df.to_csv(output_local, index=False)

    print("Archivo PROCESSED generado localmente")

    # =========================
    # SUBIR A GCS PROCESSED
    # =========================
    print("Subiendo archivo a bronce/processed...")
    processed_blob = bucket.blob(PROCESSED_GCS_PATH)
    processed_blob.upload_from_filename(output_local)

    print("Archivo subido correctamente a GCS PROCESSED")
    logging.info(f"Archivo subido a gs://{BUCKET_NAME}/{PROCESSED_GCS_PATH}")

    print("EDA FINALIZADO CORRECTAMENTE")

except Exception as e:
    logging.error(f"Error en EDA: {e}", exc_info=True)
    print(f"ERROR: {e}")
