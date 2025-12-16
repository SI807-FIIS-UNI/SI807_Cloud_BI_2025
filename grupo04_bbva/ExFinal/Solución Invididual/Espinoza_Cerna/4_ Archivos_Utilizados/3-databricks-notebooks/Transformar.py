# Databricks notebook source
# /Workspace/Shared/Apps/FlightDelays/Transformar.py

from pyspark.sql import functions as F
from pyspark.sql.window import Window
import psycopg2

# ==========================================
# 1️⃣ Leer CSV desde ADLS (Silver)
# ==========================================
dbutils.widgets.text("adls_endpoint", "", "1. Endpoint del Data Lake (ej: stxxx.dfs.core.windows.net)")
dbutils.widgets.text("pg_host", "", "2. Host del servidor PostgreSQL")
adls_endpoint = dbutils.widgets.get("adls_endpoint")
silver_path = f"abfss://silver@{adls_endpoint}/flight_delays_clean"

df_silver = spark.read.format("delta").load(silver_path)

# 2. Configuración de la conexión a PostgreSQL (usando Secrets)
pg_host = dbutils.widgets.get("pg_host")
pg_user = "adminuser"
pg_pass = "SecurePass123!"
db_name = "data_oro_db" # Asumiendo la base de datos unificada

jdbc_url = f"jdbc:postgresql://{pg_host}:5432/{db_name}?sslmode=require"
properties = {
    "user": "adminuser",
    "password": "SecurePass123!",
    "driver": "org.postgresql.Driver"
}

# 3. Crear Dimensiones
# Dimensión: Fecha
dim_date = (
    df_silver.select("flight_date", "DayOfWeek")
    .distinct()
    .withColumn("month", F.month("flight_date"))
    .withColumn("year", F.year("flight_date"))
)

# Dimensión: Aerolínea
dim_airline = df_silver.select("UniqueCarrier", "airline_name").distinct().withColumnRenamed("UniqueCarrier", "carrier_code")

# Dimensión: Aeropuerto (unificando origen y destino)
origin_airports = df_silver.select(F.col("Origin").alias("airport_code"), F.col("origin_airport_name").alias("airport_name"))
dest_airports = df_silver.select(F.col("Dest").alias("airport_code"), F.col("destination_airport_name").alias("airport_name"))
dim_airport = origin_airports.union(dest_airports).distinct()

# Dimensión: Aeronave
dim_aircraft = df_silver.select("TailNum").distinct().withColumnRenamed("TailNum", "tail_num")

# 4. Truncar tablas en PostgreSQL antes de la carga
tables_to_truncate = ["fact_flight_delays", "dim_date", "dim_airline", "dim_airport", "dim_aircraft"]
with psycopg2.connect(f"host={pg_host} dbname={db_name} user={pg_user} password={pg_pass} sslmode=require") as conn:
    with conn.cursor() as cur:
        for table in tables_to_truncate:
            print(f"Truncando tabla {table}...")
            cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
        conn.commit()

# 5. Cargar Dimensiones a PostgreSQL
dim_date.write.jdbc(url=jdbc_url, table="dim_date", mode="append", properties=properties)
dim_airline.write.jdbc(url=jdbc_url, table="dim_airline", mode="append", properties=properties)
dim_airport.write.jdbc(url=jdbc_url, table="dim_airport", mode="append", properties=properties)
dim_aircraft.write.jdbc(url=jdbc_url, table="dim_aircraft", mode="append", properties=properties)
print("Dimensiones cargadas exitosamente.")

# 6. Leer dimensiones desde PostgreSQL para obtener los IDs generados
dim_date_pg = spark.read.jdbc(url=jdbc_url, table="dim_date", properties=properties)
dim_airline_pg = spark.read.jdbc(url=jdbc_url, table="dim_airline", properties=properties)
dim_airport_pg = spark.read.jdbc(url=jdbc_url, table="dim_airport", properties=properties)
dim_aircraft_pg = spark.read.jdbc(url=jdbc_url, table="dim_aircraft", properties=properties)

# 7. Construir la Tabla de Hechos
fact_flight_delays = (
    df_silver
    .join(dim_date_pg, "flight_date")
    .join(dim_airline_pg, df_silver["UniqueCarrier"] == dim_airline_pg["carrier_code"])
    .join(dim_airport_pg.alias("origin"), df_silver["Origin"] == F.col("origin.airport_code"))
    .join(dim_airport_pg.alias("dest"), df_silver["Dest"] == F.col("dest.airport_code"))
    .join(dim_aircraft_pg, df_silver["TailNum"] == dim_aircraft_pg["tail_num"])
    .select(
        F.col("date_id"),
        F.col("airline_id"),
        F.col("origin.airport_id").alias("origin_airport_id"),
        F.col("dest.airport_id").alias("dest_airport_id"),
        F.col("aircraft_id"),
        "FlightNum", "DepTime", "ArrTime", "CRSArrTime", "ActualElapsedTime", "CRSElapsedTime",
        "AirTime", "ArrDelay", "DepDelay", "Distance", "TaxiIn", "TaxiOut", "Cancelled",
        "Diverted", "CancellationCode", "CarrierDelay", "WeatherDelay", "NASDelay",
        "SecurityDelay", "LateAircraftDelay"
    )
)

# 8. Cargar Tabla de Hechos a PostgreSQL
fact_flight_delays.write.jdbc(url=jdbc_url, table="fact_flight_delays", mode="append", properties=properties)
print("Tabla de hechos cargada exitosamente.")