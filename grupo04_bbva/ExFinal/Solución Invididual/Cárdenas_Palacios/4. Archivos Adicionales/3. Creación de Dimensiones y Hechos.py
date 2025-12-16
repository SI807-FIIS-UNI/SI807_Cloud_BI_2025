# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window

storage_account = "azdatalakefinal"
container_bronze = "bronce"
container_silver = "plata"
storage_account_key = "s7afnbWsMe4zI5rLCHBhOW6fRHiaWfQOlDyp22jFA3152SrFkVQERlIIaVBgxAPRlJ0z/5NQu9fl+ASt5JBUQA=="

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    storage_account_key
)

# Leer datos curados
input_path = f"abfss://{container_bronze}@{storage_account}.dfs.core.windows.net/curated/dataset_validado.csv"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(input_path)

print("Columnas originales:", df.columns)
df.show(3)

# ============================================================
# DIMENSIONES
# ============================================================

# ----------------------------
# DIM TIEMPO (CORRECTA)
# ----------------------------
dim_tiempo = (
    df.select(F.to_date("Date").alias("fecha")).distinct()
    .withColumn("anio", F.year("fecha"))
    .withColumn("mes", F.month("fecha"))
    .withColumn("trimestre", F.quarter("fecha"))
    .withColumn("dia", F.dayofmonth("fecha"))
    .withColumn("dia_semana", F.dayofweek("fecha") - 1)
    .withColumn("mes_nombre", F.date_format("fecha", "MMMM"))
    .withColumn("dia_semana_nombre", F.date_format("fecha", "EEEE"))
    .withColumn("semana_anio", F.weekofyear("fecha"))
    .withColumn("es_fin_semana", F.when(F.col("dia_semana").isin(5,6), True).otherwise(False))
    .withColumn("tiempo_id", F.row_number().over(Window.orderBy("fecha")))
    .select(
        "tiempo_id","fecha","anio","mes","mes_nombre","trimestre",
        "dia","dia_semana","dia_semana_nombre","semana_anio","es_fin_semana"
    )
)

# ----------------------------
# DIM CLIENTE
# ----------------------------
dim_cliente = (
    df.select(
        F.col("Customer_Name").alias("nombre_cliente"),
        F.col("Customer_Category").alias("categoria_cliente")
    ).distinct()
    .withColumn("cliente_id", F.row_number().over(Window.orderBy("nombre_cliente")))
    .select("cliente_id","nombre_cliente","categoria_cliente")
)

# ----------------------------
# DIM TIENDA
# ----------------------------
dim_tienda = (
    df.select(
        F.col("City").alias("ciudad"),
        F.col("Store_Type").alias("tipo_tienda")
    ).distinct()
    .withColumn("tienda_id", F.row_number().over(Window.orderBy("ciudad","tipo_tienda")))
    .select("tienda_id","ciudad","tipo_tienda")
)

# ----------------------------
# DIM MÉTODO DE PAGO
# ----------------------------
dim_metodo_pago = (
    df.select(F.col("Payment_Method").alias("metodo_pago")).distinct()
    .withColumn("metodo_pago_id", F.row_number().over(Window.orderBy("metodo_pago")))
    .select("metodo_pago_id","metodo_pago")
)

# ----------------------------
# DIM TEMPORADA
# ----------------------------
dim_temporada = (
    df.select(F.col("Season").alias("nombre_temporada")).distinct()
    .withColumn("temporada_id", F.row_number().over(Window.orderBy("nombre_temporada")))
    .select("temporada_id","nombre_temporada")
)

# ----------------------------
# DIM PROMOCIÓN
# ----------------------------
dim_promocion = (
    df.select(F.col("Promotion").alias("nombre_promocion")).distinct()
    .withColumn("promocion_id", F.row_number().over(Window.orderBy("nombre_promocion")))
    .select("promocion_id","nombre_promocion")
)

# ----------------------------
# DIM PRODUCTO (DESDE LISTA)
# ----------------------------
dim_producto = (
    df.select(
        F.explode(
            F.split(
                F.regexp_replace(F.col("Product"), r"[\[\]']", ""),
                r",\s*"
            )
        ).alias("nombre_producto")
    )
    .withColumn("nombre_producto", F.trim("nombre_producto"))
    .filter(F.col("nombre_producto") != "")
    .distinct()
    .withColumn("producto_id", F.row_number().over(Window.orderBy("nombre_producto")))
    .select("producto_id","nombre_producto")
)

# ============================================================
# FACT 1: FACT_TRANSACCIONES (1 FILA POR TRANSACCIÓN)
# ============================================================

df_fecha = df.withColumn("fecha", F.to_date("Date"))

fact_transacciones = (
    df_fecha
    .join(dim_tiempo, "fecha")
    .join(dim_cliente, df_fecha.Customer_Name == dim_cliente.nombre_cliente)
    .join(dim_tienda,
          (df_fecha.City == dim_tienda.ciudad) &
          (df_fecha.Store_Type == dim_tienda.tipo_tienda))
    .join(dim_metodo_pago, df_fecha.Payment_Method == dim_metodo_pago.metodo_pago)
    .join(dim_temporada, df_fecha.Season == dim_temporada.nombre_temporada)
    .join(dim_promocion, df_fecha.Promotion == dim_promocion.nombre_promocion)
    .select(
        F.col("Transaction_ID").cast("long").alias("transaccion_id"),
        "tiempo_id","cliente_id","tienda_id","metodo_pago_id","temporada_id","promocion_id",
        F.col("Total_Items").cast("int").alias("total_unidades"),
        F.col("Total_Cost").cast("double").alias("monto_total"),
        (F.col("Total_Cost") / F.col("Total_Items")).alias("precio_promedio_unitario"),
        F.when(F.col("Discount_Applied") == "Yes", True).otherwise(False).alias("descuento_aplicado")
    )
    .dropDuplicates(["transaccion_id"])
)

# ============================================================
# FACT 2: FACT_TRANSACCION_PRODUCTO (TABLA PUENTE)
# ============================================================

fact_transaccion_producto = (
    df.select(
        F.col("Transaction_ID").cast("long").alias("transaccion_id"),
        F.explode(
            F.split(
                F.regexp_replace(F.col("Product"), r"[\[\]']", ""),
                r",\s*"
            )
        ).alias("nombre_producto")
    )
    .withColumn("nombre_producto", F.trim("nombre_producto"))
    .filter(F.col("nombre_producto") != "")
    .join(dim_producto, "nombre_producto")
    .select("transaccion_id","producto_id")
    .dropDuplicates()
)

# ============================================================
# GUARDAR CSVs EN PLATA
# ============================================================

base_path = f"abfss://{container_silver}@{storage_account}.dfs.core.windows.net"

def save_csv(df, folder, name):
    temp = f"{base_path}/{folder}/temp_{name}"
    final = f"{base_path}/{folder}/{name}.csv"
    df.coalesce(1).write.mode("overwrite").option("header", True).csv(temp)
    file = [f.path for f in dbutils.fs.ls(temp) if f.path.endswith(".csv")][0]
    dbutils.fs.cp(file, final)
    dbutils.fs.rm(temp, recurse=True)
    print("✅ Guardado:", final)

# Dimensiones
save_csv(dim_tiempo, "dimensiones", "dim_tiempo")
save_csv(dim_cliente, "dimensiones", "dim_cliente")
save_csv(dim_tienda, "dimensiones", "dim_tienda")
save_csv(dim_metodo_pago, "dimensiones", "dim_metodo_pago")
save_csv(dim_temporada, "dimensiones", "dim_temporada")
save_csv(dim_promocion, "dimensiones", "dim_promocion")
save_csv(dim_producto, "dimensiones", "dim_producto")

# Hechos
save_csv(fact_transacciones, "hechos", "fact_transacciones")
save_csv(fact_transaccion_producto, "hechos", "fact_transaccion_producto")

print("🎉 NOTEBOOK COMPLETO Y CORRECTO")