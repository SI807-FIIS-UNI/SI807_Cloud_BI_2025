from pyspark.sql import SparkSession
from datetime import datetime
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
import logging

# ---------- SPARK ----------
spark = (
    SparkSession.builder
    .appName("ETL")
    .config("temporaryGcsBucket", "us-accidents-bd")
    .getOrCreate()
)

# ---------- CLOUD LOGGING ----------
client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
logger = logging.getLogger("etl_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# ---------- LOG A BIGQUERY ----------
def log_bq(table_name, layer, row_count, status):
    spark.createDataFrame(
        [(table_name, layer, datetime.now(), row_count, status)],
        ["table_name", "layer", "update_timestamp", "row_count", "status"]
    ).write.format("bigquery") \
     .option("table", "us_accidents_dw.etl_logs") \
     .mode("append").save()

from pyspark.sql.functions import (
    to_timestamp, year, month, hour, col, round
)

try:
    logger.info("ETL PLATA iniciado")

    df = spark.read.parquet("gs://us-accidents-bd/bronce/curated")

    df = df.withColumn(
        "Start_Time_ts",
        to_timestamp(col("Start_Time"), "yyyy-MM-dd HH:mm:ss")
    ).withColumn(
        "Duration_minutes",
        (col("End_Time").cast("long") - col("Start_Time").cast("long")) / 60
    ).withColumn(
        "lat_bucket", round(col("Start_Lat"), 1)
    ).withColumn(
        "lng_bucket", round(col("Start_Lng"), 1)
    )

    # ---------- DIM TIEMPO ----------
    dim_tiempo = df.select(
        col("Start_Time_ts").alias("fecha"),
        year("Start_Time_ts").alias("anio"),
        month("Start_Time_ts").alias("mes"),
        hour("Start_Time_ts").alias("hora")
    ).dropna().dropDuplicates()

    dim_tiempo.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/plata/dim_tiempo")

    dim_tiempo.write.format("bigquery") \
        .option("table", "us_accidents_dw.dim_tiempo") \
        .mode("overwrite").save()

    log_bq("dim_tiempo", "PLATA", dim_tiempo.count(), "OK")
    logger.info("dim_tiempo procesada")

    # ---------- DIM UBICACION ----------
    dim_ubicacion = df.select(
        "lat_bucket", "lng_bucket"
    ).dropna().dropDuplicates()

    dim_ubicacion.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/plata/dim_ubicacion")

    dim_ubicacion.write.format("bigquery") \
        .option("table", "us_accidents_dw.dim_ubicacion") \
        .mode("overwrite").save()

    log_bq("dim_ubicacion", "PLATA", dim_ubicacion.count(), "OK")
    logger.info("dim_ubicacion procesada")

    # ---------- DIM CLIMA ----------
    dim_clima = df.select("Source").dropna().dropDuplicates()

    dim_clima.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/plata/dim_clima")

    dim_clima.write.format("bigquery") \
        .option("table", "us_accidents_dw.dim_clima") \
        .mode("overwrite").save()

    log_bq("dim_clima", "PLATA", dim_clima.count(), "OK")
    logger.info("dim_clima procesada")

    # ---------- FACT ----------
    fact = df.select(
        "Severity",
        "Distance_mi",
        "Duration_minutes",
        "Source",
        "lat_bucket",
        "lng_bucket",
        "Start_Time_ts"
    ).dropna()

    fact.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/plata/fact_accidentes")

    fact.write.format("bigquery") \
        .option("table", "us_accidents_dw.fact_accidentes") \
        .mode("overwrite").save()

    log_bq("fact_accidentes", "PLATA", fact.count(), "OK")
    logger.info("fact_accidentes procesada")

except Exception as e:
    logger.error("ETL PLATA falló", exc_info=True)
    log_bq("ETL_PLATA", "PLATA", 0, "ERROR")
    raise