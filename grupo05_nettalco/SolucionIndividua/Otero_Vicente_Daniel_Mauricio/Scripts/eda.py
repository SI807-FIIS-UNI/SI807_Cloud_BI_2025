import pandas as pd
import logging
from io import StringIO
import matplotlib.pyplot as plt
import os

# CONFIGURACIÓN

BUCKET_NAME = "bi-examen-dataset-mauricio-otero"

INPUT_PATH = f"gs://{BUCKET_NAME}/bronce/raw/KaggleV2-May-2016.csv"
OUTPUT_PATH = f"gs://{BUCKET_NAME}/bronce/processed/noshow_processed.csv"

LOG_FILE = "../docs/eda_logs.txt"
PLOTS_DIR = "../docs"

os.makedirs(PLOTS_DIR, exist_ok=True)


# LOGGING

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("INICIO EDA - NO SHOW APPOINTMENTS")

try:

    # LECTURA

    print(" Leyendo dataset desde GCS...")
    df = pd.read_csv(INPUT_PATH)

    print(" Dataset cargado correctamente")
    print(f" Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

    logging.info(f"Shape del dataset: {df.shape}")


    # EDA MÍNIMO (RÚBRICA)

    print("\n Columnas:")
    print(df.columns.tolist())

    print("\n Valores nulos por columna:")
    print(df.isna().sum())

    logging.info("HEAD:")
    logging.info("\n" + df.head().to_string())

    buffer = StringIO()
    df.info(buf=buffer)
    logging.info("INFO:")
    logging.info("\n" + buffer.getvalue())

    logging.info("DESCRIBE:")
    logging.info("\n" + df.describe(include="number").to_string())


    # LIMPIEZA BÁSICA

    # Fechas
    df["ScheduledDay"] = pd.to_datetime(df["ScheduledDay"], errors="coerce")
    df["AppointmentDay"] = pd.to_datetime(df["AppointmentDay"], errors="coerce")

    # Edad válida
    df = df[(df["Age"] >= 0) & (df["Age"] <= 120)]

    # Normalizar No-show
    df["No-show"] = df["No-show"].map({"Yes": 1, "No": 0})

    df = df.drop_duplicates()

    print("\n Limpieza básica aplicada")
    print(f" Filas luego de limpieza: {df.shape[0]}")

    logging.info("Limpieza básica completada")


    # GRÁFICOS (EVIDENCIA)

    # Gráfico 1: Asistencia vs No-show
    plt.figure()
    df["No-show"].value_counts().plot(kind="bar")
    plt.title("Asistencia vs No-Show")
    plt.xlabel("No-Show (1 = No asistió)")
    plt.ylabel("Cantidad de Citas")
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/no_show_distribution.png")
    plt.close()

    # Gráfico 2: Edad vs No-show
    plt.figure()
    df.boxplot(column="Age", by="No-show")
    plt.title("Distribución de Edad por No-Show")
    plt.suptitle("")
    plt.xlabel("No-Show")
    plt.ylabel("Edad")
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/age_vs_noshow.png")
    plt.close()

    print("\n Gráficos generados en docs/")
    logging.info("Gráficos EDA generados")

    # GUARDAR EN PROCESSED
    df.to_csv(OUTPUT_PATH, index=False)
    logging.info(f"Archivo procesado guardado en {OUTPUT_PATH}")

    print("\n Archivo procesado cargado a BRONCE/processed")
    print(" EDA FINALIZADO CORRECTAMENTE")

except Exception as e:
    logging.error(f"Error durante el EDA: {e}")
    print(f" Error durante el EDA: {e}")
