import pandas as pd
import logging
from io import StringIO
import matplotlib.pyplot as plt
import os
import subprocess


# CONFIGURACIÓN

INPUT_PATH = "KaggleV2-May-2016.csv"

BUCKET_NAME = "bi-examen-dataset-mauricio-otero"
OUTPUT_LOCAL = "noshow_processed.csv"
OUTPUT_GCS = f"gs://{BUCKET_NAME}/bronce/processed/{OUTPUT_LOCAL}"

LOG_DIR = "docs"
PLOTS_DIR = "docs"
LOG_FILE = f"{LOG_DIR}/eda_logs.txt"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)


# LOGGING

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("INICIO EDA - NO SHOW APPOINTMENTS (LOCAL)")

try:

    
    # LECTURA

    print(" Leyendo dataset LOCAL...")
    df = pd.read_csv(INPUT_PATH)

    print(f" Dataset cargado | Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
    logging.info(f"Shape: {df.shape}")


    # EXPLORACIÓN

    print("\n Columnas:")
    print(df.columns.tolist())

    print("\n Nulos por columna:")
    print(df.isna().sum())

    logging.info("HEAD:")
    logging.info("\n" + df.head().to_string())

    buffer = StringIO()
    df.info(buf=buffer)
    logging.info("INFO:")
    logging.info("\n" + buffer.getvalue())

    logging.info("DESCRIBE:")
    logging.info("\n" + df.describe(include="number").to_string())

    # LIMPIEZA

    df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"], errors="coerce")
    df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"], errors="coerce")

    df = df[(df["Age"] >= 0) & (df["Age"] <= 120)]
    df["No-show"] = df["No-show"].map({"Yes": 1, "No": 0})

    df = df.drop_duplicates()

    print("\n Limpieza aplicada")
    logging.info("Limpieza completada")


    # GRÁFICOS

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

    # GUARDAR LOCAL

    df.to_csv(OUTPUT_LOCAL, index=False)
    print(f"\n Archivo limpio generado: {OUTPUT_LOCAL}")
    logging.info("CSV limpio generado")


    # SUBIR A GCS (PROCESSED)

    print("\n Subiendo archivo a BRONCE/processed...")
    subprocess.run(
        ["gcloud", "storage", "cp", OUTPUT_LOCAL, OUTPUT_GCS],
        check=True
    )

    print(" Archivo subido a bronce/processed")
    logging.info(f"Archivo subido a {OUTPUT_GCS}")

    print("\n EDA FINALIZADO CORRECTAMENTE")

except Exception as e:
    logging.error(f"Error en EDA: {e}")
    print(f" Error: {e}")
