# Databricks notebook source
# /Workspace/Shared/Apps/FlightDelays/Limpiar.py

from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, BooleanType, DateType

# 1. Definir rutas de entrada (Bronce) y salida (Plata)
dbutils.widgets.text("adls_endpoint", "", "ADLS Endpoint (ej: stxxx.dfs.core.windows.net)")
adls_endpoint = dbutils.widgets.get("adls_endpoint")

bronze_path = f"abfss://bronze@{adls_endpoint}/flight_delay.csv"
silver_path = f"abfss://silver@{adls_endpoint}/flight_delays_clean"

# 2. Leer datos crudos de la capa Bronce
df_raw = spark.read.csv(bronze_path, header=True, inferSchema=False)

# 3. Limpieza y Transformación de Datos
df_clean = (
    df_raw
    # Corregir tipos de datos
    .withColumn("Date", F.to_date(F.col("Date"), "dd-MM-yyyy"))
    .withColumn("DayOfWeek", F.col("DayOfWeek").cast(IntegerType()))
    .withColumn("ArrDelay", F.col("ArrDelay").cast(IntegerType()))
    .withColumn("DepDelay", F.col("DepDelay").cast(IntegerType()))
    .withColumn("Distance", F.col("Distance").cast(IntegerType()))
    .withColumn("ActualElapsedTime", F.col("ActualElapsedTime").cast(IntegerType()))
    .withColumn("CRSElapsedTime", F.col("CRSElapsedTime").cast(IntegerType()))
    .withColumn("AirTime", F.col("AirTime").cast(IntegerType()))
    .withColumn("TaxiIn", F.col("TaxiIn").cast(IntegerType()))
    .withColumn("TaxiOut", F.col("TaxiOut").cast(IntegerType()))
    .withColumn("Cancelled", (F.col("Cancelled") == "1").cast(BooleanType()))
    .withColumn("Diverted", (F.col("Diverted") == "1").cast(BooleanType()))
    .withColumn("CarrierDelay", F.col("CarrierDelay").cast(IntegerType()))
    .withColumn("WeatherDelay", F.col("WeatherDelay").cast(IntegerType()))
    .withColumn("NASDelay", F.col("NASDelay").cast(IntegerType()))
    .withColumn("SecurityDelay", F.col("SecurityDelay").cast(IntegerType()))
    .withColumn("LateAircraftDelay", F.col("LateAircraftDelay").cast(IntegerType()))
    
    # Renombrar columnas para mayor claridad
    .withColumnRenamed("Date", "flight_date")
    .withColumnRenamed("Airline", "airline_name")
    .withColumnRenamed("Org_Airport", "origin_airport_name")
    .withColumnRenamed("Dest_Airport", "destination_airport_name")
    
    # Rellenar valores nulos en columnas de retraso con 0
    .fillna(0, subset=[
        "CarrierDelay", "WeatherDelay", "NASDelay", 
        "SecurityDelay", "LateAircraftDelay", "ArrDelay", "DepDelay"
    ])
    # Rellenar nulos en TailNum para evitar problemas en joins
    .fillna("Unknown", subset=["TailNum"])
)

# 4. Escribir datos limpios en la capa Plata (formato Delta)
(
    df_clean.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(silver_path)
)

print(f"Datos limpios guardados exitosamente en: {silver_path}")