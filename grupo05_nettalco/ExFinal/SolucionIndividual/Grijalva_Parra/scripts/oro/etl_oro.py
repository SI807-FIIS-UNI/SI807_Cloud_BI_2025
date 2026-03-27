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
    count, avg, hour, col , round
)

try:
    logger.info("ETL ORO iniciado")

    fact = spark.read.parquet(
        "gs://us-accidents-bd/plata/fact_accidentes"
    )

    # ---------- KPI 1 ----------
    kpi_ubicacion = fact.groupBy(
        "lat_bucket", "lng_bucket"
    ).agg(count("*").alias("total_accidentes"))

    kpi_ubicacion.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/oro/kpi_accidentes_ubicacion")

    kpi_ubicacion.write.format("bigquery") \
        .option("table", "us_accidents_dw.kpi_accidentes_ubicacion") \
        .mode("overwrite").save()

    log_bq("kpi_accidentes_ubicacion", "ORO", kpi_ubicacion.count(), "OK")
    logger.info("KPI accidentes por ubicación")

    # ---------- KPI 2 ----------
    kpi_severidad = fact.agg(
        avg("Severity").alias("severidad_promedio")
    )

    kpi_severidad.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/oro/kpi_severidad_promedio")

    kpi_severidad.write.format("bigquery") \
        .option("table", "us_accidents_dw.kpi_severidad_promedio") \
        .mode("overwrite").save()

    log_bq("kpi_severidad_promedio", "ORO", kpi_severidad.count(), "OK")

    # ---------- KPI 3 ----------
    kpi_horas = fact.groupBy(
        hour("Start_Time_ts").alias("hora")
    ).agg(count("*").alias("total_accidentes"))

    kpi_horas.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/oro/kpi_horas_criticas")

    kpi_horas.write.format("bigquery") \
        .option("table", "us_accidents_dw.kpi_horas_criticas") \
        .mode("overwrite").save()

    log_bq("kpi_horas_criticas", "ORO", kpi_horas.count(), "OK")

    # ---------- KPI 4 ----------
    kpi_clima = fact.groupBy(
        "Source"
    ).agg(count("*").alias("total_accidentes"))

    kpi_clima.write.mode("overwrite") \
        .parquet("gs://us-accidents-bd/oro/kpi_accidentes_clima")

    kpi_clima.write.format("bigquery") \
        .option("table", "us_accidents_dw.kpi_accidentes_clima") \
        .mode("overwrite").save()

    log_bq("kpi_accidentes_clima", "ORO", kpi_clima.count(), "OK")

    logger.info("ETL ORO completado")

except Exception:
    logger.error("ETL ORO falló", exc_info=True)
    log_bq("ETL_ORO", "ORO", 0, "ERROR")
    raise