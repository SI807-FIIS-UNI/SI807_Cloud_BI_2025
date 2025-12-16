from google.cloud import bigquery
import logging
import os

# =========================
# CONFIGURACIÓN
# =========================
PROJECT_ID = "examen-final-20252"
BUCKET_NAME = "bi-examen-dataset-mauricio-otero"

GCS_PROCESSED_PATH = (
    f"gs://{BUCKET_NAME}/bronce/processed/noshow_processed.csv"
)

PLATA_DATASET = "plata"
ORO_DATASET = "oro"

LOG_DIR = "../docs"
LOG_FILE = f"{LOG_DIR}/etl_logs.txt"

# =========================
# PREPARACIÓN LOCAL
# =========================
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = bigquery.Client(project=PROJECT_ID)

# =========================
# CREAR DATASET SI NO EXISTE
# =========================
def create_dataset(dataset_id):
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{dataset_id}")
    dataset_ref.location = "US"

    try:
        client.get_dataset(dataset_ref)
        logging.info(f"Dataset {dataset_id} ya existe")
    except Exception:
        client.create_dataset(dataset_ref)
        logging.info(f"Dataset {dataset_id} creado")

# =========================
# CARGA A STAGING (PLATA)
# =========================
def load_staging():
    table_id = f"{PROJECT_ID}.{PLATA_DATASET}.stg_noshow"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"
    )

    logging.info("Cargando datos a staging")

    job = client.load_table_from_uri(
        GCS_PROCESSED_PATH,
        table_id,
        job_config=job_config
    )
    job.result()

    logging.info("Staging cargado correctamente")
    return table_id

# =========================
# DIMENSIONES
# =========================
def create_dimensions(stg):

    # Dim Tiempo
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{PLATA_DATASET}.dim_tiempo` AS
    SELECT DISTINCT
        FORMAT_DATE('%Y%m%d', DATE(AppointmentDay)) AS id_tiempo,
        DATE(AppointmentDay) AS fecha,
        EXTRACT(YEAR FROM DATE(AppointmentDay)) AS anio,
        EXTRACT(MONTH FROM DATE(AppointmentDay)) AS mes,
        EXTRACT(DAY FROM DATE(AppointmentDay)) AS dia
    FROM `{stg}`;
    """).result()

    # Dim Paciente
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{PLATA_DATASET}.dim_paciente` AS
    SELECT DISTINCT
        PatientId,
        Gender,
        Age,
        Scholarship,
        Hipertension,
        Diabetes,
        Alcoholism,
        Handcap
    FROM `{stg}`;
    """).result()

    # Dim Ubicación
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{PLATA_DATASET}.dim_ubicacion` AS
    SELECT DISTINCT
        Neighbourhood
    FROM `{stg}`;
    """).result()

    logging.info("Dimensiones creadas")

# =========================
# TABLA DE HECHOS
# =========================
def create_fact(stg):

    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{PLATA_DATASET}.fact_citas` AS
    SELECT
        AppointmentID,
        PatientId,
        Neighbourhood,
        FORMAT_DATE('%Y%m%d', DATE(AppointmentDay)) AS id_tiempo,
        SMS_received,
        `No-show` AS no_show
    FROM `{stg}`;
    """).result()

    logging.info("Tabla de hechos creada")

# =========================
# KPIs (ORO)
# =========================
def create_kpis():

    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.{ORO_DATASET}.kpi_noshow` AS
    SELECT
        id_tiempo,
        COUNT(*) AS total_citas,
        SUM(no_show) AS total_no_show,
        SAFE_DIVIDE(SUM(no_show), COUNT(*)) AS tasa_no_show
    FROM `{PROJECT_ID}.{PLATA_DATASET}.fact_citas`
    GROUP BY id_tiempo
    ORDER BY id_tiempo;
    """).result()

    logging.info("KPIs creados en ORO")

# =========================
# MAIN
# =========================
def main():
    logging.info("INICIO ETL BIGQUERY")

    create_dataset(PLATA_DATASET)
    create_dataset(ORO_DATASET)

    stg = load_staging()
    create_dimensions(stg)
    create_fact(stg)
    create_kpis()

    logging.info("ETL FINALIZADO CORRECTAMENTE")
    print("✅ ETL ejecutado correctamente")

if __name__ == "__main__":
    main()
