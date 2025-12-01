from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, to_date, concat_ws, lpad, lit,
    lower, trim, create_map, coalesce
)
from itertools import chain
from google.cloud import bigquery
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, DoubleType, StringType



# -----------------------------
# Inicializar Spark
# -----------------------------
spark = SparkSession.builder.appName("PlataDepositos").enableHiveSupport().getOrCreate()


# -----------------------------
# Parámetros BigQuery
# -----------------------------
project_id = "grupo6-scotiabank"
dataset_plata = "plata"
dataset_oro = "oro"
table_plata = "sbs_deposito"
table_oro = "hecho_riesgo"
minutos = 10


# -----------------------------
# Oro
# -----------------------------
ID_MONEDA = 1
ID_INDICADOR = 7
ID_LIMITE = 7


bq_client = bigquery.Client(project=project_id)



# -----------------------------
# Verificar si dataset Plata existe
# -----------------------------
def create_dataset_if_not_exists(dataset_name):
    dataset_ref = f"{project_id}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_ref)
    try:
        bq_client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_name} ya existe.")
    except Exception:
        print(f"Dataset {dataset_name} no existe. Creando...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "southamerica-west1"
        bq_client.create_dataset(dataset)
        print(f"Dataset {dataset_name} creado.")

create_dataset_if_not_exists(dataset_plata)

# -----------------------------
# Cargar tabla Bronce
# -----------------------------
df_dep = (
    spark.read.format("bigquery")
    .option("table", f"{project_id}.bronce.sbs_deposito")
    .load()
)
df_dep = df_dep.filter(
    F.col("fecha_carga") >= F.current_timestamp() - F.expr(f"INTERVAL {minutos} MINUTE")
)


print("Columnas originales df_liquidez:", df_dep.columns)


df_dep = df_dep.toDF(*[c.lower() for c in df_dep.columns])


# Limpiar instituciones

df_dep = (
    df_dep
    .filter(F.col("institucion").isNotNull())
    .filter(~F.col("institucion").rlike("(?i)NOTA|Incluye|^$"))
)


# Mapeo mes → número

mes_map = {
    "en": "01", "fe": "02", "ma": "03", "ab": "04",
    "my": "05", "jn": "06", "jl": "07", "ag": "08",
    "se": "09", "oc": "10", "no": "11", "di": "12"
}

mapping_expr = create_map([lit(x) for x in chain(*mes_map.items())])

df_dep = df_dep.withColumn(
    "mes",
    mapping_expr.getItem(lower(trim(col("mes").cast("string"))))
)


# Normalizar bancos

df_dep = df_dep.withColumn(
    "institucion",
    when(lower(col("institucion")).like("%crédito%"), "BCP")
    .when(lower(col("institucion")).like("%credito%"), "BCP")
    .when(lower(col("institucion")).like("%interbank%"), "Interbank")
    .when((lower(col("institucion")).like("%bbva%")) | (lower(col("institucion")).like("%continental%")), "BBVA")
    .when(lower(col("institucion")).like("%scotiabank%"), "Scotiabank")
    .when(lower(col("institucion")).like("%interamericano%"), "BanBif")
    .when(lower(col("institucion")).like("%mibanco%"), "Mibanco")
    .otherwise("Otros")
)

# Selección final

df_plata = df_dep.select(
    to_date(
        concat_ws("-", col("anio").cast("string"), lpad(col("mes"), 2, "0"), lit("01")),
        "yyyy-MM-dd"
    ).alias("fecha"),
    col("anio").cast(IntegerType()),
    col("mes").cast(IntegerType()),
    col("institucion"),
    col("depositostotales").cast(DoubleType())
).orderBy("institucion", "anio", "mes")


# Guardar en Plata

(
    df_plata.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_plata}.{table_plata}")
    .option("writeMethod", "direct")
    .mode("append")
    .save()
)

print("Plata → sbs_depositos: COMPLETADO.")




# -----------------------------
# Transformación Oro
# -----------------------------

df_dep_oro = df_plata

# Total mensual del sistema financiero
df_totales = (
    df_dep_oro.groupBy("anio", "mes")
    .agg(F.sum("DepositosTotales").alias("total_mes"))
)


# Unir a cada institución
df_ratio = (
    df_dep_oro.alias("d")
    .join(
        df_totales.alias("t"),
        (F.col("d.anio") == F.col("t.anio")) &
        (F.col("d.mes") == F.col("t.mes")),
        "left"
    )
    .select(
        "d.*",
        F.col("t.total_mes")
    )
)


# Ratio participación
df_ratio = df_ratio.withColumn(
    "participacion_depositos",
    F.when(
        (F.col("total_mes").isNotNull()) & (F.col("total_mes") != 0),
        (F.col("DepositosTotales") / F.col("total_mes")).cast(DoubleType())
    ).otherwise(None)
)


# Filtrar "Otros"
df_ratio = df_ratio.filter(F.col("institucion") != "Otros")



# Mapeo de bancos
bancos_map = {
    "Scotiabank": 1,
    "BCP": 2,
    "Banco de Crédito del Perú": 2,
    "BBVA": 3,
    "Interbank": 4,
    "BanBif": 5,
    "Banco Interamericano de Finanzas": 5,
    "Mibanco": 6
}


map_items = sum([[F.lit(k), F.lit(v)] for k, v in bancos_map.items()], [])
bancos_map_expr = F.create_map(*map_items)


df_ratio = df_ratio.withColumn("id_banco", bancos_map_expr.getItem(F.col("institucion")).cast("int"))


# Dimensión fecha
df_fecha = (
    spark.read.format("bigquery")
    .option("table", f"{project_id}.{dataset_oro}.dim_fecha")
    .load()
    .select("id_fecha", "anio", "mes")
)

df_ratio = (
    df_ratio
    .join(
        df_fecha,
        (df_ratio.anio == df_fecha.anio) &
        (df_ratio.mes == df_fecha.mes),
        "left"
    )
)



df_final = df_ratio.select(
    F.col("id_banco").cast("int"),
    F.col("id_fecha").cast("int"),
    F.col("id_moneda").cast("int"),
    F.col("id_indicador").cast("int"),
    F.col("id_limite").cast("int"),
    F.col("DepositosTotales").cast("float").alias("numerador"),
    F.col("total_mes").cast("float").alias("denominador"),
    F.col("participacion_depositos").cast("float").alias("valor")
)


df_final.show(20, False)


(
    df_final.write.format("bigquery")
    .option("table", f"{project_id}.{dataset_oro}.hecho_riesgo")
    .option("writeMethod", "direct")
    .mode("append")
    .save()
)


print("Transformación Oro COMPLETADA.")


spark.stop()