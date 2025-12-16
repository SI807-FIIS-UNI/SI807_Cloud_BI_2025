from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, to_date, lit, row_number
)
from google.cloud import bigquery
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType
from pyspark.sql.window import Window

# =====================================================
# Inicializar Spark
# =====================================================
spark = (
    SparkSession.builder
    .appName("BroncePlataOro_FlightDelay")
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
# Limpieza básica (Plata)
# =====================================================

# Control de fechas inválidas
df_bronce = df_bronce.withColumn(
    "date",
    when(
        col("date").rlike("^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
        to_date(col("date"), "yyyy-MM-dd")
    )
)

# Eliminar duplicados operativos
df_bronce = df_bronce.dropDuplicates(
    ["date", "flightnum", "origin", "dest"]
)

# Reemplazar aeropuertos nulos
df_bronce = (
    df_bronce
    .withColumn(
        "org_airport",
        F.coalesce(col("org_airport"), lit("Other Origin Airport"))
    )
    .withColumn(
        "dest_airport",
        F.coalesce(col("dest_airport"), lit("Other Destination Airport"))
    )
)

# Cast de columnas numéricas
numeric_cols = [
    "arrdelay", "carrierdelay", "weatherdelay",
    "nasdelay", "securitydelay", "lateaircraftdelay",
    "distance", "taxiin", "taxiout"
]

for c in numeric_cols:
    df_bronce = df_bronce.withColumn(
        c,
        when(col(c).isNotNull(), col(c).cast(DoubleType()))
    )

# Flag de retraso
df_bronce = df_bronce.withColumn(
    "delayed",
    when(col("arrdelay") > 0, 1).otherwise(0)
)

# =====================================================
# Selección final capa Plata
# =====================================================
df_plata = df_bronce.select(
    "date",
    "dayofweek",
    "airline",
    "uniquecarrier",
    "flightnum",
    "origin",
    "org_airport",
    "dest",
    "dest_airport",
    "distance",
    "arrdelay",
    "carrierdelay",
    "weatherdelay",
    "nasdelay",
    "securitydelay",
    "lateaircraftdelay",
    "delayed",
    "cancelled",
    "diverted"
)

# =====================================================
# Guardar capa Plata
# =====================================================
(
    df_plata.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_plata}.{table_plata}")
    .option("writeMethod", "direct")
    .mode("overwrite")  # cambiar a append en producción
    .save()
)

print("Capa Plata Flight Delay creada correctamente")

# =====================================================
# =================== CAPA ORO ========================
# =====================================================

# =====================================================
# DIM TIEMPO
# =====================================================
data_tiempo = [
    (1, "Lunes"),
    (2, "Martes"),
    (3, "Miércoles"),
    (4, "Jueves"),
    (5, "Viernes"),
    (6, "Sábado"),
    (7, "Domingo")
]

df_dim_tiempo = spark.createDataFrame(
    data_tiempo,
    ["dayofweek", "nombre_dia"]
)

df_dim_tiempo = df_dim_tiempo.withColumn(
    "id_tiempo",
    row_number().over(Window.orderBy(lit(1)))
)

df_dim_tiempo = df_dim_tiempo.select(
    "id_tiempo",
    "dayofweek",
    "nombre_dia"
)

(
    df_dim_tiempo.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_oro}.dim_tiempo")
    .option("writeMethod", "direct")
    .mode("overwrite")
    .save()
)

# =====================================================
# DIM PRODUCTO (Aerolínea)
# =====================================================
data_producto = [
    ("AA", "American Airlines"),
    ("DL", "Delta Airlines"),
    ("UA", "United Airlines"),
    ("WN", "Southwest Airlines"),
    ("B6", "JetBlue"),
    ("OTH", "Other Airlines")
]

df_dim_producto = spark.createDataFrame(
    data_producto,
    ["codigo", "nombre"]
)

df_dim_producto = df_dim_producto.withColumn(
    "id_producto",
    row_number().over(Window.orderBy(lit(1)))
)

df_dim_producto = df_dim_producto.select(
    "id_producto",
    "codigo",
    "nombre"
)

(
    df_dim_producto.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_oro}.dim_producto")
    .option("writeMethod", "direct")
    .mode("overwrite")
    .save()
)

# =====================================================
# DIM SEGMENTO (Distancia)
# =====================================================
data_segmento = [
    ("Corto", "Vuelos menores a 500 millas"),
    ("Medio", "Vuelos entre 500 y 1500 millas"),
    ("Largo", "Vuelos mayores a 1500 millas")
]

df_dim_segmento = spark.createDataFrame(
    data_segmento,
    ["segmento", "descripcion"]
)

df_dim_segmento = df_dim_segmento.withColumn(
    "id_segmento",
    row_number().over(Window.orderBy(lit(1)))
)

df_dim_segmento = df_dim_segmento.select(
    "id_segmento",
    "segmento",
    "descripcion"
)

(
    df_dim_segmento.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_oro}.dim_cliente_segmento")
    .option("writeMethod", "direct")
    .mode("overwrite")
    .save()
)

# =====================================================
# DIM REGIÓN (Aeropuertos)
# =====================================================
data_region = [
    ("JFK", "John F. Kennedy International Airport"),
    ("LAX", "Los Angeles International Airport"),
    ("ORD", "O'Hare International Airport"),
    ("ATL", "Hartsfield–Jackson Atlanta International Airport"),
    ("DFW", "Dallas/Fort Worth International Airport"),
    ("OTH", "Other Airports")
]

df_dim_region = spark.createDataFrame(
    data_region,
    ["codigo_aeropuerto", "nombre"]
)

df_dim_region = df_dim_region.withColumn(
    "id_region",
    row_number().over(Window.orderBy(lit(1)))
)

df_dim_region = df_dim_region.select(
    "id_region",
    "codigo_aeropuerto",
    "nombre"
)

(
    df_dim_region.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_oro}.dim_region")
    .option("writeMethod", "direct")
    .mode("overwrite")
    .save()
)

print("Capa Oro creada correctamente")

spark.stop()
