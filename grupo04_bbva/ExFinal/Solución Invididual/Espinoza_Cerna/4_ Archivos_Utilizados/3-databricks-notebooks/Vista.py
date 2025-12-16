# Databricks notebook source
from pyspark.sql import functions as F
import psycopg2

# 1. Configuración de la conexión a PostgreSQL (usando Secrets)
dbutils.widgets.text("pg_host", "", "2. Host del servidor PostgreSQL")
pg_host = dbutils.widgets.get("pg_host")
pg_user = "adminuser"
pg_pass = "SecurePass123!"
db_name = "data_oro_db"

jdbc_url = f"jdbc:postgresql://{pg_host}:5432/{db_name}?sslmode=require"
properties = {
    "user": pg_user,
    "password": pg_pass,
    "driver": "org.postgresql.Driver"
}

# 2. Leer tablas de hechos y dimensiones desde PostgreSQL
fact_flights = spark.read.jdbc(url=jdbc_url, table="fact_flight_delays", properties=properties)
dim_date = spark.read.jdbc(url=jdbc_url, table="dim_date", properties=properties)
dim_airline = spark.read.jdbc(url=jdbc_url, table="dim_airline", properties=properties)
dim_airport_origin = spark.read.jdbc(url=jdbc_url, table="dim_airport", properties=properties).alias("origin")
dim_airport_dest = spark.read.jdbc(url=jdbc_url, table="dim_airport", properties=properties).alias("dest")

# 3. Unir tablas (Modelo en Estrella)
df_joined = (
    fact_flights
    .join(dim_date, fact_flights.date_id == dim_date.date_id)
    .join(dim_airline, fact_flights.airline_id == dim_airline.airline_id)
    .join(dim_airport_origin, fact_flights.origin_airport_id == dim_airport_origin.airport_id)
    .join(dim_airport_dest, fact_flights.dest_airport_id == dim_airport_dest.airport_id)
)

# 4. Calcular KPIs Agregados
df_kpis = (
    df_joined
    .groupBy("flight_date", "airline_name", "origin.airport_name")
    .agg(
        F.count("*").alias("total_flights"),
        F.round(F.avg(F.when(F.col("arr_delay") <= 0, 1).otherwise(0)) * 100, 2).alias("on_time_arrival_pct"),
        F.round(F.avg(F.col("cancelled").cast("int")) * 100, 2).alias("cancellation_rate_pct"),
        F.round(F.avg("arr_delay"), 2).alias("avg_arrival_delay"),
        F.sum("carrier_delay").alias("total_carrier_delay"),
        F.sum("weather_delay").alias("total_weather_delay"),
        F.sum("nas_delay").alias("total_nas_delay"),
        F.sum("security_delay").alias("total_security_delay"),
        F.sum("late_aircraft_delay").alias("total_late_aircraft_delay")
    )
    .withColumnRenamed("airport_name", "origin_airport")
)

# Calcular porcentajes de causa de retraso
df_kpis = df_kpis.withColumn("total_delay_minutes", 
    F.col("total_carrier_delay") + F.col("total_weather_delay") + F.col("total_nas_delay") + 
    F.col("total_security_delay") + F.col("total_late_aircraft_delay")
)

delay_causes = ["carrier", "weather", "nas", "security", "late_aircraft"]
for cause in delay_causes:
    df_kpis = df_kpis.withColumn(f"{cause}_delay_pct",
        F.when(F.col("total_delay_minutes") > 0,
               F.round(F.col(f"total_{cause}_delay") / F.col("total_delay_minutes") * 100, 2)
        ).otherwise(0)
    )

# 5. Escribir la tabla de KPIs en la capa ORO
table_name = "gold_flight_kpis"
df_kpis.write.jdbc(url=jdbc_url, table=table_name, mode="overwrite", properties=properties)
print(f"Tabla de KPIs '{table_name}' escrita exitosamente en la base de datos.")

# 6. Crear/Reemplazar las Vistas en PostgreSQL
with psycopg2.connect(f"host={pg_host} dbname={db_name} user={pg_user} password={pg_pass} sslmode=require") as conn:
    with conn.cursor() as cur:
        # Vista de KPIs Agregados
        view_kpi_sql = f"CREATE OR REPLACE VIEW vw_flight_kpis AS SELECT * FROM {table_name};"
        cur.execute(view_kpi_sql)
        print("Vista 'vw_flight_kpis' creada/actualizada exitosamente.")
        
        # Vista de Exploración (Star Schema)
        view_analytics_sql = """
        CREATE OR REPLACE VIEW vw_flight_analytics AS
        SELECT
            d.flight_date, d.day_of_week,
            al.airline_name,
            ao.airport_name AS origin_airport,
            ad.airport_name AS destination_airport,
            f.*
        FROM fact_flight_delays f
        JOIN dim_date d ON f.date_id = d.date_id
        JOIN dim_airline al ON f.airline_id = al.airline_id
        JOIN dim_airport ao ON f.origin_airport_id = ao.airport_id
        JOIN dim_airport ad ON f.dest_airport_id = ad.airport_id;
        """
        cur.execute(view_analytics_sql)
        print("Vista 'vw_flight_analytics' creada/actualizada exitosamente.")