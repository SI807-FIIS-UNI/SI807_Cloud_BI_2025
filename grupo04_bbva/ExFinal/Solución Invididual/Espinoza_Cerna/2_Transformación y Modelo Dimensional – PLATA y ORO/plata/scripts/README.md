# Scripts para generar tablas de hechos y dimensiones (SQL)

Este repositorio contiene los scripts necesarios para construir un **modelo dimensional (estrella)** orientado al análisis de **retrasos de vuelos**. En este modelo, la **tabla de hechos** actúa como la tabla central, mientras que las **tablas de dimensiones** proporcionan el contexto descriptivo. La relación entre ellas se realiza mediante identificadores, de forma similar a claves primarias (PK) y foráneas (FK).

Imagen de referencia del modelo estrella:

<img width="1568" height="1283" alt="Untitled" src="https://github.com/user-attachments/assets/6dbfc29b-11a6-4e23-82a0-7ffcca5d4996" />


A continuación, se detallan los scripts SQL utilizados para crear las dimensiones, la tabla de hechos y una vista semántica para análisis.

```sql
-- ============================================================
-- MODELO DE DATOS PARA RETRASOS DE VUELOS
-- ============================================================

-- Dimensión: Fecha del vuelo
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    flight_date DATE NOT NULL UNIQUE,
    day_of_week INT,
    month INT,
    year INT
);

-- Dimensión: Aerolíneas
CREATE TABLE dim_airline (
    airline_id SERIAL PRIMARY KEY,
    carrier_code VARCHAR(10) NOT NULL UNIQUE,
    airline_name VARCHAR(255)
);

-- Dimensión: Aeropuertos
CREATE TABLE dim_airport (
    airport_id SERIAL PRIMARY KEY,
    airport_code VARCHAR(10) NOT NULL UNIQUE,
    airport_name VARCHAR(255)
);

-- Dimensión: Aeronaves
CREATE TABLE dim_aircraft (
    aircraft_id SERIAL PRIMARY KEY,
    tail_num VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla de Hechos: Métricas y detalles de los vuelos
CREATE TABLE fact_flight_delays (
    flight_delay_id SERIAL PRIMARY KEY,
    date_id INT NOT NULL,
    airline_id INT NOT NULL,
    origin_airport_id INT NOT NULL,
    dest_airport_id INT NOT NULL,
    aircraft_id INT,

    flight_num VARCHAR(20),
    dep_time VARCHAR(4),
    arr_time VARCHAR(4),
    crs_arr_time VARCHAR(4),
    actual_elapsed_time INT,
    crs_elapsed_time INT,
    air_time INT,
    arr_delay INT,
    dep_delay INT,
    distance INT,
    taxi_in INT,
    taxi_out INT,
    cancelled BOOLEAN,
    diverted BOOLEAN,
    cancellation_code VARCHAR(5),
    carrier_delay INT,
    weather_delay INT,
    nas_delay INT,
    security_delay INT,
    late_aircraft_delay INT,

    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (airline_id) REFERENCES dim_airline(airline_id),
    FOREIGN KEY (origin_airport_id) REFERENCES dim_airport(airport_id),
    FOREIGN KEY (dest_airport_id) REFERENCES dim_airport(airport_id),
    FOREIGN KEY (aircraft_id) REFERENCES dim_aircraft(aircraft_id)
);

-- Vista Agregada (Capa Oro / Semántica)
CREATE OR REPLACE VIEW vw_flight_analytics AS
SELECT
    d.flight_date,
    d.day_of_week,
    al.airline_name,
    ao.airport_name AS origin_airport,
    ad.airport_name AS destination_airport,
    f.*
FROM fact_flight_delays f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_airline al ON f.airline_id = al.airline_id
JOIN dim_airport ao ON f.origin_airport_id = ao.airport_id
JOIN dim_airport ad ON f.dest_airport_id = ad.airport_id;
```

---

# Scripts para procesar y generar KPIs (Python / Databricks)

En esta sección se incluyen los scripts desarrollados en **PySpark**, ejecutados sobre **Databricks**, cuyo objetivo es transformar los datos limpios (capa Silver) almacenados en **ADLS**, construir las dimensiones y la tabla de hechos, y finalmente cargarlas en **PostgreSQL** (capa Oro).

El flujo general es el siguiente:

1. Lectura de datos desde Delta Lake (Silver).
2. Creación de dimensiones a partir de los atributos relevantes.
3. Carga de dimensiones en PostgreSQL.
4. Recuperación de los identificadores generados.
5. Construcción y carga de la tabla de hechos.

```python
# Databricks notebook source
# /Workspace/Shared/Apps/FlightDelays/Transformar.py

from pyspark.sql import functions as F
from pyspark.sql.window import Window
import psycopg2

# ==========================================
# 1️⃣ Leer datos desde ADLS (Silver)
# ==========================================
dbutils.widgets.text("adls_endpoint", "", "1. Endpoint del Data Lake (ej: stxxx.dfs.core.windows.net)")
dbutils.widgets.text("pg_host", "", "2. Host del servidor PostgreSQL")

adls_endpoint = dbutils.widgets.get("adls_endpoint")
silver_path = f"abfss://silver@{adls_endpoint}/flight_delays_clean"

df_silver = spark.read.format("delta").load(silver_path)

# ==========================================
# 2️⃣ Configuración de PostgreSQL
# ==========================================
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

# ==========================================
# 3️⃣ Creación de Dimensiones
# ==========================================
# Dimensión Fecha
dim_date = (
    df_silver.select("flight_date", "DayOfWeek")
    .distinct()
    .withColumn("month", F.month("flight_date"))
    .withColumn("year", F.year("flight_date"))
)

# Dimensión Aerolínea
dim_airline = (
    df_silver.select("UniqueCarrier", "airline_name")
    .distinct()
    .withColumnRenamed("UniqueCarrier", "carrier_code")
)

# Dimensión Aeropuerto
origin_airports = df_silver.select(
    F.col("Origin").alias("airport_code"),
    F.col("origin_airport_name").alias("airport_name")
)

dest_airports = df_silver.select(
    F.col("Dest").alias("airport_code"),
    F.col("destination_airport_name").alias("airport_name")
)

dim_airport = origin_airports.union(dest_airports).distinct()

# Dimensión Aeronave
dim_aircraft = df_silver.select("TailNum").distinct().withColumnRenamed("TailNum", "tail_num")

# ==========================================
# 4️⃣ Truncar tablas antes de la carga
# ==========================================
tables_to_truncate = [
    "fact_flight_delays",
    "dim_date",
    "dim_airline",
    "dim_airport",
    "dim_aircraft"
]

with psycopg2.connect(
    f"host={pg_host} dbname={db_name} user={pg_user} password={pg_pass} sslmode=require"
) as conn:
    with conn.cursor() as cur:
        for table in tables_to_truncate:
            cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
        conn.commit()

# ==========================================
# 5️⃣ Cargar Dimensiones
# ==========================================
dim_date.write.jdbc(jdbc_url, "dim_date", mode="append", properties=properties)
dim_airline.write.jdbc(jdbc_url, "dim_airline", mode="append", properties=properties)
dim_airport.write.jdbc(jdbc_url, "dim_airport", mode="append", properties=properties)
dim_aircraft.write.jdbc(jdbc_url, "dim_aircraft", mode="append", properties=properties)

# ==========================================
# 6️⃣ Leer Dimensiones con IDs
# ==========================================
dim_date_pg = spark.read.jdbc(jdbc_url, "dim_date", properties=properties)
dim_airline_pg = spark.read.jdbc(jdbc_url, "dim_airline", properties=properties)
dim_airport_pg = spark.read.jdbc(jdbc_url, "dim_airport", properties=properties)
dim_aircraft_pg = spark.read.jdbc(jdbc_url, "dim_aircraft", properties=properties)

# ==========================================
# 7️⃣ Construcción de la Tabla de Hechos
# ==========================================
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
        "FlightNum", "DepTime", "ArrTime", "CRSArrTime",
        "ActualElapsedTime", "CRSElapsedTime", "AirTime",
        "ArrDelay", "DepDelay", "Distance", "TaxiIn",
        "TaxiOut", "Cancelled", "Diverted",
        "CancellationCode", "CarrierDelay", "WeatherDelay",
        "NASDelay", "SecurityDelay", "LateAircraftDelay"
    )
)

# ==========================================
# 8️⃣ Cargar Tabla de Hechos
# ==========================================
fact_flight_delays.write.jdbc(jdbc_url, "fact_flight_delays", mode="append", properties=properties)
```

Este conjunto de scripts permite disponer de una **base analítica consistente**, preparada para la construcción de **KPIs**, dashboards y análisis avanzados sobre los retrasos de vuelos.

---

## KPIs Analíticos (Capa Oro)

A partir del modelo dimensional y de la tabla de hechos `fact_flight_delays`, se implementa un notebook adicional en Databricks orientado al **cálculo de KPIs agregados**, los cuales permiten evaluar puntualidad, cancelaciones y causas de retraso por aerolínea, aeropuerto de origen y fecha.

```python
# Databricks notebook source
from pyspark.sql import functions as F
import psycopg2

# 1. Configuración de PostgreSQL
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

# 2. Lectura de tablas
fact_flights = spark.read.jdbc(jdbc_url, "fact_flight_delays", properties=properties)
dim_date = spark.read.jdbc(jdbc_url, "dim_date", properties=properties)
dim_airline = spark.read.jdbc(jdbc_url, "dim_airline", properties=properties)
dim_airport_origin = spark.read.jdbc(jdbc_url, "dim_airport", properties=properties).alias("origin")
dim_airport_dest = spark.read.jdbc(jdbc_url, "dim_airport", properties=properties).alias("dest")

# 3. Unión del modelo estrella
df_joined = (
    fact_flights
    .join(dim_date, "date_id")
    .join(dim_airline, "airline_id")
    .join(dim_airport_origin, fact_flights.origin_airport_id == F.col("origin.airport_id"))
    .join(dim_airport_dest, fact_flights.dest_airport_id == F.col("dest.airport_id"))
)

# 4. KPIs agregados
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

# 5. Persistencia en la capa Oro
df_kpis.write.jdbc(jdbc_url, "gold_flight_kpis", mode="overwrite", properties=properties)
```

---

## Análisis de KPIs

Los KPIs definidos se alinean con el análisis del dataset **Flight Delay and Causes** (Kaggle), el cual permite identificar el comportamiento operativo de las aerolíneas y las principales causas de retraso.

### KPI 1: Total de vuelos

**Objetivo:** Medir el volumen de operaciones aéreas por aerolínea y aeropuerto de origen.

Este indicador permite contextualizar el resto de métricas, ya que aerolíneas con mayor número de vuelos presentan una mayor exposición a retrasos y cancelaciones.

### KPI 2: Porcentaje de llegadas a tiempo

**Objetivo:** Evaluar el nivel de puntualidad operacional.

Se considera un vuelo puntual cuando el retraso de llegada es menor o igual a cero minutos. Un valor alto refleja una operación eficiente y una adecuada planificación de recursos.

### KPI 3: Tasa de cancelación

**Objetivo:** Identificar el impacto de cancelaciones en la experiencia del pasajero.

Este KPI mide el porcentaje de vuelos cancelados sobre el total. Tasas elevadas suelen asociarse a problemas climáticos severos, fallas operativas o congestión del sistema aéreo.

### KPI 4: Retraso promedio de llegada

**Objetivo:** Cuantificar la magnitud promedio de los retrasos.

A diferencia del KPI de puntualidad, este indicador permite analizar la severidad de los retrasos cuando estos ocurren, proporcionando una visión más precisa del impacto real en minutos.

### KPI 5: Distribución de causas de retraso

**Objetivo:** Analizar el origen de los retrasos operativos.

Este conjunto de KPIs descompone el total de minutos de retraso en cinco categorías: **Carrier**, **Weather**, **NAS**, **Security** y **Late Aircraft**. El análisis permite identificar si los retrasos se deben principalmente a factores internos de la aerolínea o a causas externas al operador.

En conjunto, estos indicadores constituyen una base sólida para la construcción de tableros ejecutivos y análisis comparativos entre aerolíneas, aeropuertos y periodos de tiempo.
