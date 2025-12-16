from google.cloud import bigquery
import logging
import os

# =====================================================
# CONFIGURACIÓN
# =====================================================
PROJECT_ID = "ef-si807u-20220018k"
BUCKET_NAME = "bi-examen-final"

PROCESSED_GCS_PATH = (
    f"gs://{BUCKET_NAME}/bronce/processed/processed_Flight_delay.csv"
)

# =====================================================
# LOGGING (EN scripts/)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "etl_logs.txt")

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
        dataset = bigquery.Dataset(f"{PROJECT_ID}.{ds}")
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)
        logging.info(f"Dataset {ds} listo")

# =====================================================
# STAGING
# =====================================================
def load_staging():
    table_id = f"{PROJECT_ID}.plata.stg_flight_delay"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"
    )

    client.load_table_from_uri(
        PROCESSED_GCS_PATH,
        table_id,
        job_config=job_config
    ).result()

    logging.info("STAGING cargado")
    return table_id

# =====================================================
# DIMENSIONES
# =====================================================
def create_dimensions(stg):

    # DIM TIEMPO
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_tiempo` AS
    SELECT DISTINCT
        FORMAT_DATE('%Y%m%d', DATE(Date)) AS id_tiempo,
        DATE(Date) AS fecha,
        EXTRACT(YEAR FROM DATE(Date)) AS anio,
        EXTRACT(MONTH FROM DATE(Date)) AS mes,
        EXTRACT(DAY FROM DATE(Date)) AS dia,
        DayOfWeek AS dia_semana
    FROM `{stg}`
    WHERE Date IS NOT NULL;
    """).result()

    # DIM AEROLÍNEA
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_aerolinea` AS
    SELECT DISTINCT
        UniqueCarrier AS carrier_code,
        Airline AS airline_name
    FROM `{stg}`;
    """).result()

    # DIM AEROPUERTO
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_aeropuerto` AS
    SELECT DISTINCT Origin AS airport_code, Org_Airport AS airport_name
    FROM `{stg}`
    UNION DISTINCT
    SELECT DISTINCT Dest AS airport_code, Dest_Airport AS airport_name
    FROM `{stg}`;
    """).result()

    # DIM CAUSA (CATÁLOGO)
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.dim_causa` AS
    SELECT 'Carrier' AS causa UNION ALL
    SELECT 'Weather' UNION ALL
    SELECT 'NAS' UNION ALL
    SELECT 'Security' UNION ALL
    SELECT 'Late Aircraft';
    """).result()

    logging.info("Dimensiones creadas")

# =====================================================
# FACT TABLE
# =====================================================
def create_fact(stg):

    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.plata.fact_flight` AS
    SELECT
        FORMAT_DATE('%Y%m%d', DATE(Date)) AS id_tiempo,
        UniqueCarrier AS carrier_code,
        Origin AS origin_airport,
        Dest AS dest_airport,

        FlightNum,
        TailNum,

        SAFE_CAST(DepDelay AS FLOAT64) AS dep_delay,
        SAFE_CAST(ArrDelay AS FLOAT64) AS arr_delay,
        SAFE_CAST(Distance AS FLOAT64) AS distance,

        SAFE_CAST(TaxiIn AS FLOAT64) AS taxi_in,
        SAFE_CAST(TaxiOut AS FLOAT64) AS taxi_out,

        SAFE_CAST(CarrierDelay AS FLOAT64) AS carrier_delay,
        SAFE_CAST(WeatherDelay AS FLOAT64) AS weather_delay,
        SAFE_CAST(NASDelay AS FLOAT64) AS nas_delay,
        SAFE_CAST(SecurityDelay AS FLOAT64) AS security_delay,
        SAFE_CAST(LateAircraftDelay AS FLOAT64) AS late_aircraft_delay

    FROM `{stg}`
    WHERE Date IS NOT NULL;
    """).result()

    logging.info("FACT creada")

# =====================================================
# KPIs – ORO
# =====================================================
def create_kpis():

    # KPI GLOBAL
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_global` AS
    SELECT
        COUNT(*) AS total_flights,
        AVG(dep_delay) AS avg_dep_delay,
        AVG(arr_delay) AS avg_arr_delay
    FROM `{PROJECT_ID}.plata.fact_flight`;
    """).result()

    # KPI TIEMPO
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_tiempo` AS
    SELECT
        id_tiempo,
        COUNT(*) AS total_flights,
        AVG(dep_delay) AS avg_dep_delay,
        AVG(arr_delay) AS avg_arr_delay
    FROM `{PROJECT_ID}.plata.fact_flight`
    GROUP BY id_tiempo
    ORDER BY id_tiempo;
    """).result()

    # KPI AEROLÍNEA
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_aerolinea` AS
    SELECT
        carrier_code,
        COUNT(*) AS total_flights,
        AVG(arr_delay) AS avg_arr_delay
    FROM `{PROJECT_ID}.plata.fact_flight`
    GROUP BY carrier_code
    ORDER BY total_flights DESC;
    """).result()

    # KPI CAUSA (DESPIVOTADO)
    client.query(f"""
    CREATE OR REPLACE TABLE `{PROJECT_ID}.oro.kpi_causa` AS
    SELECT 'Carrier' AS causa, AVG(carrier_delay) AS avg_delay FROM `{PROJECT_ID}.plata.fact_flight`
    UNION ALL
    SELECT 'Weather', AVG(weather_delay) FROM `{PROJECT_ID}.plata.fact_flight`
    UNION ALL
    SELECT 'NAS', AVG(nas_delay) FROM `{PROJECT_ID}.plata.fact_flight`
    UNION ALL
    SELECT 'Security', AVG(security_delay) FROM `{PROJECT_ID}.plata.fact_flight`
    UNION ALL
    SELECT 'Late Aircraft', AVG(late_aircraft_delay) FROM `{PROJECT_ID}.plata.fact_flight`;
    """).result()

    logging.info("KPIs creados en ORO")

# =====================================================
# MAIN
# =====================================================
def main():
    logging.info("===== INICIO ETL FLIGHT DELAY =====")

    create_datasets()
    stg = load_staging()
    create_dimensions(stg)
    create_fact(stg)
    create_kpis()

    logging.info("===== ETL FINALIZADO CORRECTAMENTE =====")

if __name__ == "__main__":
    main()