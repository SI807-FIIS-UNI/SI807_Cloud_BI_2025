from google.cloud import bigquery
import logging
import os

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
PROJECT_ID = "examen-final-20252"
BUCKET_NAME = "bi-examen-dataset-mauricio-otero"

PROCESSED_PATH = f"gs://{BUCKET_NAME}/bronce/processed/noshow_processed.csv"
CURATED_PATH = f"gs://{BUCKET_NAME}/bronce/curated"

LOG_DIR = "../docs"
LOG_FILE = f"{LOG_DIR}/etl_logs.txt"

os.makedirs(LOG_DIR, exist_ok=True)

# =====================================================
# LOGGING
# =====================================================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = bigquery.Client(project=PROJECT_ID)

# =====================================================
# DATASETS
# =====================================================
def create_datasets():
    for ds in ["plata", "oro"]:
        dataset_id = f"{PROJECT_ID}.{ds}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)
        logging.info(f"Dataset {ds} listo")

# =====================================================
# STAGING
# =====================================================
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

    logging.info("STAGING cargado correctamente")
    return table_id

# =====================================================
# DIMENSIONES
# =====================================================
def create_dimensions(stg):

    # DIM TIME
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_time` AS
    SELECT DISTINCT
        FORMAT_DATE('%Y%m%d', DATE(AppointmentDay)) AS id_time,
        DATE(AppointmentDay) AS fecha,
        EXTRACT(YEAR FROM DATE(AppointmentDay)) AS anio,
        EXTRACT(MONTH FROM DATE(AppointmentDay)) AS mes,
        EXTRACT(DAY FROM DATE(AppointmentDay)) AS dia
    FROM `{stg}`;
    """).result()

    # DIM PATIENT
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_patient` AS
    SELECT DISTINCT
        PatientId AS id_patient,
        Gender,
        Age,
        Scholarship
    FROM `{stg}`;
    """).result()

    # DIM CONDITIONS
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_conditions` AS
    SELECT DISTINCT
        PatientId AS id_patient,
        Hipertension,
        Diabetes,
        Alcoholism,
        Handcap
    FROM `{stg}`;
    """).result()

    # DIM COMMUNICATION
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_communication` AS
    SELECT DISTINCT
        AppointmentID AS id_communication,
        SMS_received
    FROM `{stg}`;
    """).result()

    # DIM NEIGHBOURHOOD
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_neighbourhood` AS
    SELECT DISTINCT
        Neighbourhood AS id_neighbourhood
    FROM `{stg}`;
    """).result()

    logging.info("Dimensiones creadas")

# =====================================================
# FACT TABLE
# =====================================================
def create_fact(stg):
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.fact_citas` AS
    SELECT
        AppointmentID,
        PatientId AS id_patient,
        Neighbourhood AS id_neighbourhood,
        FORMAT_DATE('%Y%m%d', DATE(AppointmentDay)) AS id_time,
        AppointmentID AS id_communication,
        `No-show` AS no_show
    FROM `{stg}`;
    """).result()

    logging.info("FACT creada")

# =====================================================
# KPIs – CAPA ORO (2 DASHBOARDS)
# =====================================================
def create_kpis():

    # KPI GLOBAL
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_global` AS
    SELECT
        COUNT(*) AS total_citas,
        SUM(no_show) AS total_no_show,
        ROUND(SUM(no_show)/COUNT(*),3) AS tasa_no_show,
        ROUND(1 - SUM(no_show)/COUNT(*),3) AS tasa_asistencia
    FROM `{PROJECT_ID}.plata.fact_citas`;
    """).result()

    # KPI TIEMPO
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_tiempo` AS
    SELECT
        id_time,
        COUNT(*) AS total_citas,
        SUM(no_show) AS total_no_show,
        ROUND(SUM(no_show)/COUNT(*),3) AS tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas`
    GROUP BY id_time
    ORDER BY id_time;
    """).result()

    # KPI SMS
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_sms` AS
    SELECT
        c.SMS_received,
        COUNT(*) AS total_citas,
        SUM(f.no_show) AS total_no_show,
        ROUND(SUM(f.no_show)/COUNT(*),3) AS tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas` f
    JOIN `{PROJECT_ID}.plata.dim_communication` c
        ON f.id_communication = c.id_communication
    GROUP BY c.SMS_received;
    """).result()

    # KPI EDAD
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_edad` AS
    SELECT
        CASE
            WHEN Age < 18 THEN 'Menor de 18'
            WHEN Age BETWEEN 18 AND 35 THEN '18-35'
            WHEN Age BETWEEN 36 AND 60 THEN '36-60'
            ELSE 'Mayor de 60'
        END AS rango_edad,
        COUNT(*) AS total_citas,
        SUM(f.no_show) AS total_no_show,
        ROUND(SUM(f.no_show)/COUNT(*),3) AS tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas` f
    JOIN `{PROJECT_ID}.plata.dim_patient` p
        ON f.id_patient = p.id_patient
    GROUP BY rango_edad
    ORDER BY rango_edad;
    """).result()

    # KPI GÉNERO
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_genero` AS
    SELECT
        p.Gender,
        COUNT(*) AS total_citas,
        SUM(f.no_show) AS total_no_show,
        ROUND(SUM(f.no_show)/COUNT(*),3) AS tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas` f
    JOIN `{PROJECT_ID}.plata.dim_patient` p
        ON f.id_patient = p.id_patient
    GROUP BY p.Gender;
    """).result()

    # KPI UBICACIÓN
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_ubicacion` AS
    SELECT
        id_neighbourhood,
        COUNT(*) AS total_citas,
        SUM(no_show) AS total_no_show,
        ROUND(SUM(no_show)/COUNT(*),3) AS tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas`
    GROUP BY id_neighbourhood
    ORDER BY tasa_no_show DESC;
    """).result()

    # KPI CONDICIONES MÉDICAS
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_condiciones` AS
    SELECT 'Hipertension' AS condicion, Hipertension AS valor,
           COUNT(*) total_citas, SUM(f.no_show) total_no_show,
           ROUND(SUM(f.no_show)/COUNT(*),3) tasa_no_show
    FROM `{PROJECT_ID}.plata.fact_citas` f
    JOIN `{PROJECT_ID}.plata.dim_conditions` c
      ON f.id_patient = c.id_patient
    GROUP BY Hipertension

    UNION ALL

    SELECT 'Diabetes', Diabetes,
           COUNT(*), SUM(f.no_show),
           ROUND(SUM(f.no_show)/COUNT(*),3)
    FROM `{PROJECT_ID}.plata.fact_citas` f
    JOIN `{PROJECT_ID}.plata.dim_conditions` c
      ON f.id_patient = c.id_patient
    GROUP BY Diabetes;
    """).result()

    logging.info("KPIs creados en ORO")

# =====================================================
# EXPORTAR A CURATED
# =====================================================
def export_curated():
    tables = [
        "dim_time",
        "dim_patient",
        "dim_conditions",
        "dim_communication",
        "dim_neighbourhood",
        "fact_citas"
    ]

    for t in tables:
        client.extract_table(
            f"{PROJECT_ID}.plata.{t}",
            f"{CURATED_PATH}/{t}.csv"
        ).result()

        logging.info(f"{t} exportada a curated")

# =====================================================
# MAIN
# =====================================================
def main():
    logging.info("===== INICIO ETL NOSHOW =====")
    create_datasets()
    stg = load_staging()
    create_dimensions(stg)
    create_fact(stg)
    create_kpis()
    export_curated()
    logging.info("===== ETL FINALIZADO CORRECTAMENTE =====")

if __name__ == "__main__":
    main()
