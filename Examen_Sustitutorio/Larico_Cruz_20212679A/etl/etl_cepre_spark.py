import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim

# Configuración
BUCKET_NAME = "$BUCKET_NAME"
DATASET_NAME = "$DATASET_NAME"
TABLE_NAME = "$TABLE_NAME"
CSV_PATH = f"gs://{BUCKET_NAME}/raw/$CSV_FILE"

spark = SparkSession.builder.appName("ETL-CepreUni").getOrCreate()

# 1. EXTRACT
df_raw = spark.read.option("header", True).option("inferSchema", True).csv(CSV_PATH)

# 2. TRANSFORM (Limpieza Básica)
df_curated = df_raw \\
    .withColumnRenamed("IDHASH", "id_hash") \\
    .withColumn("COLEGIO", upper(trim(col("COLEGIO")))) \\
    .withColumn("ESPECIALIDAD", upper(trim(col("ESPECIALIDAD")))) \\
    .withColumn("INGRESO", upper(trim(col("INGRESO"))))

# 3. LOAD (Escritura en BigQuery)
df_curated.write \\
    .format("bigquery") \\
    .option("table", f"{DATASET_NAME}.{TABLE_NAME}") \\
    .option("temporaryGcsBucket", BUCKET_NAME) \\
    .mode("overwrite") \\
    .save()
