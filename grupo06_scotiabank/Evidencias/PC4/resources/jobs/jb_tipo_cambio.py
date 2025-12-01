from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_date, lit, lpad, concat_ws, substring, regexp_replace,
    when, lower
)
from pyspark.sql.types import IntegerType, DoubleType
from google.cloud import bigquery
import pyspark.sql.functions as F


PROJECT_ID = "grupo6-scotiabank"
DATASET_PLATA = "plata"
DATASET_ORO = "oro"
TABLE_PLATA = "tipo_cambio"
TABLE_ORO = "hecho_tipo_cambio"


# ===============================================================
# INICIAR SPARK
# ===============================================================

spark = (
    SparkSession.builder
    .appName("TipoCambioBroncePlataOro")
    .enableHiveSupport()
    .getOrCreate()
)


# ===============================================================
# LEER BRONCE
# ===============================================================

df = (
    spark.read.format("bigquery")
    .option("table", f"{PROJECT_ID}.bronce.tipo_cambio")
    .load()
)

df = df.withColumn("mes_txt", substring(col("CODMES"), 1, 3))
df = df.withColumn("anio", substring(col("CODMES"), 4, 2))

df = df.withColumn(
    "anio",
    when(col("anio").cast("int") <= 30, concat_ws("", lit("20"), col("anio")))
    .otherwise(concat_ws("", lit("19"), col("anio")))
)

df = df.withColumn(
    "mes",
    when(col("mes_txt") == "Ene", 1)
    .when(col("mes_txt") == "Feb", 2)
    .when(col("mes_txt") == "Mar", 3)
    .when(col("mes_txt") == "Abr", 4)
    .when(col("mes_txt") == "May", 5)
    .when(col("mes_txt") == "Jun", 6)
    .when(col("mes_txt") == "Jul", 7)
    .when(col("mes_txt") == "Ago", 8)
    .when(col("mes_txt") == "Sep", 9)
    .when(col("mes_txt") == "Oct", 10)
    .when(col("mes_txt") == "Nov", 11)
    .when(col("mes_txt") == "Dic", 12)
)

df_plata = df.select(
    to_date(
        concat_ws("-", col("anio"), lpad(col("mes"), 2, "0"), lit("01")),
        "yyyy-MM-dd"
    ).alias("fecha"),
    col("anio").cast(IntegerType()),
    col("mes").cast(IntegerType()),
    col("Valor").cast(DoubleType()).alias("tipo_cambio")
)


# ===============================================================
# GUARDAR PLATA
# ===============================================================

df_plata.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{DATASET_PLATA}.{TABLE_PLATA}") \
    .option("writeMethod", "direct") \
    .mode("append") \
    .save()


# ===============================================================
# TRANSFORMACIÓN ORO
# ===============================================================

df_oro = df_plata.withColumn("id_indicador", lit(8))

df_oro = df_oro.select(
    col("fecha"),
    col("anio"),
    col("mes"),
    col("tipo_cambio"),
    col("id_indicador")
)


df_oro.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{DATASET_ORO}.{TABLE_ORO}") \
    .option("writeMethod", "direct") \
    .mode("append") \
    .save()


spark.stop()
