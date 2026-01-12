# etl_master.py

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def limpiar_columnas(df):
    for c in df.columns:
        df = df.withColumnRenamed(c, c.strip().lower().replace(" ", "_").replace("á", "a").replace("é", "e")
                                                .replace("í", "i").replace("ó", "o").replace("ú", "u")
                                                .replace("ñ", "n"))
    return df

def write_to_bq(df, table_name, project_id, dataset_bq):
    df.write \
      .format("bigquery") \
      .option("table", f"{project_id}.{dataset_bq}.{table_name}") \
      .option("writeMethod", "direct") \
      .mode("overwrite") \
      .save()

if __name__ == "__main__":
    spark = SparkSession.builder.appName("ETL Sutran").getOrCreate()

    # Parámetros de entrada
    input_file = sys.argv[1]  # Ej: raw/BBDD_ONSV-PERSONAS_2021-2023.csv
    bucket = "sutran-bucket-mr"
    project_id = "shaped-icon-478404-p0"
    dataset_bq = "sutran_mr"

    input_path = f"gs://{bucket}/{input_file}"
    trusted_path = f"gs://{bucket}/trusted/"
    refined_path = f"gs://{bucket}/refined/"

    # Leer archivo
    df = spark.read.option("header", True).option("encoding", "ISO-8859-1").csv(input_path)

    # Tipo de archivo
    if "PERSONAS" in input_file:
        df_clean = df \
            .drop("LUGAR_ATENCION_LESIONADO", "LUGAR_DE_DEFUNCION", "SE_SOMETIO_A_DOSAJE_ETILICO_CUALITATIVO") \
            .filter(~(col("EDAD") == "No indica")) \
            .withColumn("EDAD", when(col("EDAD") == "No indica", None).otherwise(col("EDAD"))) \
            .dropna(how="all")
        df_clean = limpiar_columnas(df_clean)
        df_clean.write.mode("overwrite").option("header", True).csv(f"{trusted_path}personas/")

    elif "VEHICULOS" in input_file:
        df_clean = df.drop("ELEMENTO_TRANSPORTADO", "AMBITO_SERVICIO").dropna(how="all")
        df_clean = limpiar_columnas(df_clean)
        df_clean.write.mode("overwrite").option("header", True).csv(f"{trusted_path}vehiculos/")

    elif "SINIESTROS" in input_file:
        df_clean = df.drop("EXISTE_SENAL_VERTICAL", "CLASIFICACION_DE_LA_SENAL_VERTICAL_N_1", 
                           "CLASIFICACION_DE_LA_SENAL_VERTICAL_N_2", "EXISTE_SENAL_HORIZONTAL") \
                     .dropna(how="all")
        df_clean = limpiar_columnas(df_clean)
        df_clean.write.mode("overwrite").option("header", True).csv(f"{trusted_path}siniestros/")

    else:
        print(f"❌ Archivo no reconocido: {input_file}")
        sys.exit(1)

    print(f"✅ Limpieza y carga a trusted completada para: {input_file}")
