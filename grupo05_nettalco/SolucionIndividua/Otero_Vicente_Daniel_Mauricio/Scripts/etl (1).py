from google.cloud import bigquery
import logging
import os

# =========================
# CONFIGURACIÓN
# =========================
PROJECT_ID = "examen-final-20252"
BUCKET_NAME = "bi-examen-dataset-mauricio-otero"

PROCESSED_PATH = f"gs://{BUCKET_NAME}/bronce/processed/noshow_processed.csv"
CURATED_PATH = f"gs://{BUCKET_NAME}/bronce/curated"

LOG_DIR = "../docs"
LOG_FILE = f"{LOG_DIR}/etl_logs.txt"

os.makedirs(LOG_DIR, exist_ok=True)

# =========================
# LOGGING
# =========================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = bigquery.Client(project=PROJECT_ID)

# =========================
# CREAR DATASETS SI NO EXISTEN
# =========================
def create_datasets():
    for ds in ["plata", "oro"]:
        dataset_id = f"{PROJECT_ID}.{ds}"
        try:
            client.get_dataset(dataset_id)
            logging.info(f"Dataset {ds} ya existe")
        except:
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            client.create_dataset(dataset)
            logging.info(f"Dataset {ds} creado")

# =========================
# STAGING
# =========================
def load_staging():
    table_id = f"{PROJECT_ID}.plata.stg_noshow"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_uri(
        PROCESSED_PATH,
        table_id,
        job_config=job_config
    )
    job.result()

    logging.info("Tabla STAGING cargada")
    return table_id

# =========================
# DIMENSIONES
# =========================
def create_dimensions(stg):

    # Dim Tiempo
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_tiempo` AS
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
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_paciente` AS
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
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_ubicacion` AS
    SELECT DISTINCT
        Neighbourhood
    FROM `{stg}`;
    """).result()

    logging.info("Dimensiones creadas")

# =========================
# FACT TABLE
# =========================
def create_fact(stg):
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.fact_citas` AS
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
# KPIs ORO
# =========================
def create_kpis():
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_noshow` AS
    SELECT
        id_tiempo,
        COUNT(*) AS total_citas,
        SUM(no_show) AS total_no_show,
        ROUND(SUM(no_show)/COUNT(*), 3) AS tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas`
    GROUP BY id_tiempo
    ORDER BY id_tiempo;
    """).result()

    logging.info("KPIs creados en ORO")

# =========================
# EXPORTAR A CURATED
# =========================
def export_curated():
    tables = [
        "dim_tiempo",
        "dim_paciente",
        "dim_ubicacion",
        "fact_citas"
    ]

    for t in tables:
        destination = f"{CURATED_PATH}/{t}.csv"
        extract_job = client.extract_table(
            f"{PROJECT_ID}.plata.{t}",
            destination
        )
        extract_job.result()
        logging.info(f"Tabla {t} exportada a CURATED")

# =========================
# MAIN
# =========================
def main():
    logging.info("=== INICIO ETL ===")

    create_datasets()
    stg = load_staging()
    create_dimensions(stg)
    create_fact(stg)
    create_kpis()
    export_curated()

    logging.info("=== ETL FINALIZADO CORRECTAMENTE ===")

if __name__ == "__main__":
    main()
