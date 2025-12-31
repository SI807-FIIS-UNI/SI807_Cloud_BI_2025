from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, to_date, lit, row_number
)
from google.cloud import bigquery
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
from pyspark.sql.window import Window
from itertools import chain

# =====================================================
# Inicializar Spark
# =====================================================
spark = (
    SparkSession.builder
    .appName("BroncePlataOro_FlightDelay2")
    .enableHiveSupport()
    .getOrCreate()
)

# =====================================================
# Parámetros BigQuery
# =====================================================
project_id = "final-espinal-aguilar"

dataset_bronce = "bronce"
dataset_plata = "plata"
dataset_oro = "oro"

table_bronce = "flight_delay"
table_plata = "flight_delay_plata"

bq_client = bigquery.Client(project=project_id)

# =====================================================
# Crear datasets si no existen
# =====================================================
def create_dataset_if_not_exists(dataset_name):
    dataset_ref = f"{project_id}.{dataset_name}"
    try:
        bq_client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "southamerica-west1"
        bq_client.create_dataset(dataset)

create_dataset_if_not_exists(dataset_plata)
create_dataset_if_not_exists(dataset_oro)

# =====================================================
# Cargar Bronce desde BigQuery
# =====================================================
df_bronce = (
    spark.read.format("bigquery")
    .option("table", f"{project_id}.{dataset_bronce}.{table_bronce}")
    .load()
)

# Normalizar nombres de columnas
df_bronce = df_bronce.toDF(*[c.lower() for c in df_bronce.columns])


# =====================================================
# ================== CAPA PLATA =======================
# =====================================================


# =====================================================
# 1. Eliminación de duplicados
# =====================================================
df_silver = df_bronce.dropDuplicates()


# =====================================================
# 2. Conversión de horas hhmm a minutos desde medianoche
# =====================================================
def hhmm_to_minutes(col_name):
    return (
        (F.floor(F.col(col_name) / 100) * 60) +
        (F.col(col_name) % 100)
    )

time_cols = ["DepTime", "ArrTime", "CRSArrTime"]

for c in time_cols:
    df_silver = df_silver.withColumn(
        c.lower() + "_min",
        F.when(F.col(c).isNotNull(), hhmm_to_minutes(c))
    )

# =====================================================
# 3. Reemplazo de aeropuertos nulos
# =====================================================

airport_map = {
    "MOD": "Modesto City–County Airport",
    "OXR": "Oxnard Airport",
    "PFN": "Panama City–Bay County International Airport",
    "PMD": "Palmdale Regional Airport",
    "RFD": "Chicago Rockford International Airport",
    "SLE": "Salem Municipal Airport",
    "YKM": "Yakima Air Terminal",
    "CIC": "Chico Municipal Airport",
    "FLO": "Florence Regional Airport",
    "HHH": "Hilton Head Island Airport",
    "IPL": "Imperial County Airport",
    "IYK": "Inyokern Airport",
    "LWB": "Greenbrier Valley Airport",
    "LYH": "Lynchburg Regional Airport",
    "MCN": "Middle Georgia Regional Airport"
}

airport_map_expr = F.create_map(
    [F.lit(x) for x in chain(*airport_map.items())]
)

df_silver = df_silver.withColumn(
    "Org_Airport",
    F.when(
        F.col("Org_Airport").isNull(),
        airport_map_expr[F.col("Origin")]
    ).otherwise(F.col("Org_Airport"))
)

df_silver = df_silver.withColumn(
    "Dest_Airport",
    F.when(
        F.col("Dest_Airport").isNull(),
        airport_map_expr[F.col("Dest")]
    ).otherwise(F.col("Dest_Airport"))
)


# =====================================================
# 4. Cast de columnas numéricas
# =====================================================
numeric_cols = [
    "ArrDelay", "DepDelay",
    "CarrierDelay", "WeatherDelay",
    "NASDelay", "SecurityDelay",
    "LateAircraftDelay",
    "Distance", "TaxiIn", "TaxiOut",
    "ActualElapsedTime", "CRSElapsedTime", "AirTime"
]

for c in numeric_cols:
    df_silver = df_silver.withColumn(
        c,
        F.col(c).cast(DoubleType())
    )

# =====================================================
# 5. Flag de retraso
# =====================================================
df_silver = df_silver.withColumn(
    "vuelo_retrasado",
    F.when(F.col("ArrDelay") > 15, 1).otherwise(0)
)

# =====================================================
# 6. Selección final + renombrado a español
# =====================================================
df_plata = df_silver.select(
    F.col("Date").alias("fecha"),
    F.col("DayOfWeek").alias("dia_semana"),
    F.col("UniqueCarrier").alias("codigo_aerolinea"),
    F.col("Airline").alias("aerolinea"),
    F.col("FlightNum").alias("numero_vuelo"),
    F.col("TailNum").alias("matricula_avion"),

    F.col("Origin").alias("origen_codigo"),
    F.col("Org_Airport").alias("origen_aeropuerto"),
    F.col("Dest").alias("destino_codigo"),
    F.col("Dest_Airport").alias("destino_aeropuerto"),

    F.col("Distance").alias("distancia_millas"),

    F.col("DepTime_min").alias("salida_minutos"),
    F.col("ArrTime_min").alias("llegada_minutos"),
    F.col("CRSArrTime_min").alias("llegada_programada_minutos"),

    F.col("ActualElapsedTime").alias("tiempo_real_total"),
    F.col("CRSElapsedTime").alias("tiempo_programado"),
    F.col("AirTime").alias("tiempo_vuelo"),

    F.col("TaxiIn").alias("taxi_entrada"),
    F.col("TaxiOut").alias("taxi_salida"),

    F.col("DepDelay").alias("retraso_salida"),
    F.col("ArrDelay").alias("retraso_llegada"),

    F.col("CarrierDelay").alias("retraso_aerolinea"),
    F.col("WeatherDelay").alias("retraso_clima"),
    F.col("NASDelay").alias("retraso_nas"),
    F.col("SecurityDelay").alias("retraso_seguridad"),
    F.col("LateAircraftDelay").alias("retraso_avion_tardio"),

    F.col("Cancelled").alias("cancelado"),
    F.col("Diverted").alias("desviado"),

    F.col("vuelo_retrasado")
)

# =====================================================
# 7. Escritura capa Plata en BigQuery
# =====================================================
(
    df_plata.write
    .format("bigquery")
    .option("table", f"{project_id}.{dataset_plata}.{table_plata}")
    .option("writeMethod", "direct")
    .mode("overwrite")
    .save()
)

print("Capa Plata Flight Delay creada correctamente")


# =====================================================
# =================== CAPA ORO ========================
# =====================================================


# =====================================================
# 1. DIMENSION TIEMPO
# =====================================================
df_dim_tiempo = (
    df_plata
    .select("fecha", "dia_semana")
    .dropDuplicates()
    .withColumn("anio", F.year("fecha"))
    .withColumn("mes", F.month("fecha"))
    .withColumn("dia", F.dayofmonth("fecha"))
    .withColumn(
        "sk_tiempo",
        F.row_number().over(Window.orderBy("fecha"))
    )
)

df_dim_tiempo.write.format("bigquery") \
    .option("table", f"{project_id}.{dataset_oro}.dim_tiempo") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()


# =====================================================
# 2. DIMENSION AEROLÍNEA
# =====================================================
df_dim_aerolinea = (
    df_plata
    .select("codigo_aerolinea", "aerolinea")
    .dropDuplicates()
    .withColumn(
        "sk_aerolinea",
        F.row_number().over(Window.orderBy("codigo_aerolinea"))
    )
)

df_dim_aerolinea.write.format("bigquery") \
    .option("table", f"{project_id}.{dataset_oro}.dim_aerolinea") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()


# =====================================================
# 3. DIMENSION ORIGEN
# =====================================================
df_dim_origen = (
    df_plata
    .select("origen_codigo", "origen_aeropuerto")
    .dropDuplicates()
    .withColumn(
        "sk_origen",
        F.row_number().over(Window.orderBy("origen_codigo"))
    )
)

df_dim_origen.write.format("bigquery") \
    .option("table", f"{project_id}.{dataset_oro}.dim_origen") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()


# =====================================================
# 4. DIMENSION DESTINO
# =====================================================
df_dim_destino = (
    df_plata
    .select("destino_codigo", "destino_aeropuerto")
    .dropDuplicates()
    .withColumn(
        "sk_destino",
        F.row_number().over(Window.orderBy("destino_codigo"))
    )
)

df_dim_destino.write.format("bigquery") \
    .option("table", f"{project_id}.{dataset_oro}.dim_destino") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()


# =====================================================
# 5. DIMENSION CAUSA DE RETRASO
# =====================================================
df_dim_causa = spark.createDataFrame(
    [
        (1, "Retraso por aerolínea"),
        (2, "Retraso por clima"),
        (3, "Retraso por NAS"),
        (4, "Retraso por seguridad"),
        (5, "Retraso por avión tardío")
    ],
    ["sk_causa", "descripcion_causa"]
)

df_dim_causa.write.format("bigquery") \
    .option("table", f"{project_id}.{dataset_oro}.dim_causa") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()


# =====================================================
# 6. TABLA DE HECHOS
# =====================================================

# Join con dimensiones
df_fact = (
    df_plata
    .join(df_dim_tiempo.select("fecha", "sk_tiempo"), "fecha", "left")
    .join(df_dim_aerolinea.select("codigo_aerolinea", "sk_aerolinea"),
          "codigo_aerolinea", "left")
    .join(df_dim_origen.select("origen_codigo", "sk_origen"),
          "origen_codigo", "left")
    .join(df_dim_destino.select("destino_codigo", "sk_destino"),
          "destino_codigo", "left")
)

# Métricas del fact
df_fact_vuelos = (
    df_fact
    .withColumn(
        "retraso_por_causa",
        F.col("retraso_aerolinea")
        + F.col("retraso_clima")
        + F.col("retraso_nas")
        + F.col("retraso_seguridad")
        + F.col("retraso_avion_tardio")
    )
    .select(
        "sk_tiempo",
        "sk_aerolinea",
        "sk_origen",
        "sk_destino",

        F.col("retraso_llegada"),
        F.col("retraso_salida"),
        F.col("retraso_por_causa"),

        F.col("cancelado"),
        F.col("desviado")
    )
)

df_fact_vuelos.write.format("bigquery") \
    .option("table", f"{project_id}.{dataset_oro}.fact_vuelos") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()


print("CAPA ORO creada correctamente")

spark.stop()
