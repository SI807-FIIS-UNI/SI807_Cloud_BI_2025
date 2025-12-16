import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when

# Argumentos
bucket = sys.argv[1].replace('gs://', '').strip()
input_path = f"gs://{bucket}/bronze"
temp_bucket = f"{bucket}/tmp"

spark = SparkSession.builder.appName("ETL_SOT").getOrCreate()

# 1. Carga Contratas
spark.read.json(f"{input_path}/bronze_contratas.json") \
    .write.format("bigquery") \
    .option("table", "sot_analytics.stg_contratas") \
    .option("temporaryGcsBucket", temp_bucket).mode("overwrite").save()

# 2. Carga SOTS y Transformación
df = spark.read.json(f"{input_path}/bronze_sots.json")

df_clean = df \
    .withColumn("fecha_creacion", to_date(col("fecha_creacion"))) \
    .withColumn("fecha_planificada", to_date(col("fecha_planificada"))) \
    .withColumn("fecha_cierre", to_date(col("fecha_cierre"))) \
    .withColumn("tiempo_excedente", col("tiempo_real_min") - col("tiempo_planificado_min")) \
    .withColumn("tiempo_excedente", when(col("tiempo_excedente") < 0, 0).otherwise(col("tiempo_excedente")))

df_clean.write.format("bigquery") \
    .option("table", "sot_analytics.stg_sots") \
    .option("temporaryGcsBucket", temp_bucket).mode("overwrite").save()