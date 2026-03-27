from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
import logging
from google.cloud import logging as cloud_logging

# =========================================================
# CLOUD LOGGING
# =========================================================
client = cloud_logging.Client()
client.setup_logging()

logger = logging.getLogger("etl-bronce")
logger.setLevel(logging.INFO)

# =========================================================
# SPARK SESSION
# =========================================================
spark = SparkSession.builder \
    .appName("ETL_Bronce_US_Accidents") \
    .getOrCreate()

# SOLUCIÓN PARA TIMESTAMPS CON NANOSEGUNDOS (Spark 3.x)
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

try:
    # =====================================================
    # RUTAS GCS
    # =====================================================
    RAW_PATH = "gs://us-accidents-bd/bronce/raw/US_Accidents_March23.csv"
    PROCESSED_PATH = "gs://us-accidents-bd/bronce/processed/"
    CURATED_PATH = "gs://us-accidents-bd/bronce/curated/"

    # =====================================================
    # BRONCE RAW
    # =====================================================
    logger.info("Leyendo datos desde BRONCE RAW")

    df_raw = spark.read \
        .option("header", True) \
        .csv(RAW_PATH)

    raw_count = df_raw.count()
    logger.info(f"Registros leídos desde RAW: {raw_count}")

    # =====================================================
    # BRONCE PROCESSED
    # =====================================================
    logger.info("Iniciando transformación BRONCE PROCESSED")

    df_processed = (
        df_raw
        .withColumnRenamed("Distance(mi)", "Distance_mi")
        .withColumn("Severity", col("Severity").cast("int"))
        .withColumn("Start_Lat", col("Start_Lat").cast("double"))
        .withColumn("Start_Lng", col("Start_Lng").cast("double"))
        .withColumn("End_Lat", col("End_Lat").cast("double"))
        .withColumn("End_Lng", col("End_Lng").cast("double"))
        .withColumn(
            "Start_Time",
            to_timestamp(col("Start_Time"), "yyyy-MM-dd HH:mm:ss")
        )
        .withColumn(
            "End_Time",
            to_timestamp(col("End_Time"), "yyyy-MM-dd HH:mm:ss")
        )
    )

    logger.info("Escribiendo BRONCE PROCESSED en Parquet")

    df_processed.write \
        .mode("overwrite") \
        .parquet(PROCESSED_PATH)

    processed_count = df_processed.count()
    logger.info(f"Registros escritos en PROCESSED: {processed_count}")

    # =====================================================
    # BRONCE CURATED
    # =====================================================
    logger.info("Iniciando transformación BRONCE CURATED")

    df_curated = (
        df_processed
        .filter(col("ID").isNotNull())
        .filter(col("Severity").between(1, 4))
        .dropDuplicates(["ID"])
        .select(
            "ID",
            "Source",
            "Severity",
            "Start_Time",
            "End_Time",
            "Start_Lat",
            "Start_Lng",
            "End_Lat",
            "End_Lng",
            "Distance_mi"
        )
    )

    logger.info("Escribiendo BRONCE CURATED en Parquet")

    df_curated.write \
        .mode("overwrite") \
        .parquet(CURATED_PATH)

    curated_count = df_curated.count()
    logger.info(f"Registros escritos en CURATED: {curated_count}")

    logger.info("ETL BRONCE COMPLETADO CORRECTAMENTE")

except Exception as e:
    logger.error("Error durante ETL BRONCE", exc_info=True)
    raise

finally:
    spark.stop()