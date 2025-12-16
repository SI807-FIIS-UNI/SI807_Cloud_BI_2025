# Databricks notebook source
from pyspark.sql import functions as F

storage_account = "azdatalakefinal"
container_oro = "oro"
storage_account_key = "s7afnbWsMe4zI5rLCHBhOW6fRHiaWfQOlDyp22jFA3152SrFkVQERlIIaVBgxAPRlJ0z/5NQu9fl+ASt5JBUQA=="

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    storage_account_key
)

kpis_dir  = f"abfss://{container_oro}@{storage_account}.dfs.core.windows.net/kpis"
final_file = f"{kpis_dir}/kpis.json"
tmp_dir   = f"{kpis_dir}/_tmp_kpis_json"

# ============================================================
# CONFIG POSTGRES
# ============================================================
postgres_host = "postgresql-final.postgres.database.azure.com"
postgres_port = "5432"
postgres_db = "data_oro"
postgres_user = "pgadmin"
postgres_password = "Password123!"

jdbc_url = f"jdbc:postgresql://{postgres_host}:{postgres_port}/{postgres_db}?sslmode=require"
jdbc_props = {"user": postgres_user, "password": postgres_password, "driver": "org.postgresql.Driver"}

print("✅ Configuración lista")

# ============================================================
# LEER TABLAS DESDE POSTGRES
# ============================================================
fact_transacciones = spark.read.jdbc(jdbc_url, "fact_transacciones", properties=jdbc_props)
fact_transaccion_producto = spark.read.jdbc(jdbc_url, "fact_transaccion_producto", properties=jdbc_props)

# ============================================================
# KPIs POR TRANSACCIÓN
# ============================================================
productos_distintos = (
    fact_transaccion_producto
    .groupBy("transaccion_id")
    .agg(F.countDistinct("producto_id").alias("productos_distintos"))
)

fact_kpis = (
    fact_transacciones
    .join(productos_distintos, on="transaccion_id", how="left")
    .fillna({"productos_distintos": 0})
    .withColumn(
        "kpis",
        F.struct(
            F.col("monto_total"),
            F.col("total_unidades"),
            F.col("precio_promedio_unitario"),
            F.col("descuento_aplicado"),
            F.col("productos_distintos")
        )
    )
    .select(
        "transaccion_id","tiempo_id","cliente_id","tienda_id",
        "metodo_pago_id","temporada_id","promocion_id","kpis"
    )
)

# ============================================================
# LIMPIEZA TOTAL: borrar TODO /kpis (incluye archivos viejos)
# ============================================================
try:
    dbutils.fs.rm(kpis_dir, recurse=True)
except:
    pass

# recrear carpeta vacía
dbutils.fs.mkdirs(kpis_dir)

# ============================================================
# ESCRIBIR TEMP, EXTRAER PART-JSON, RENOMBRAR A kpis.json
# ============================================================
fact_kpis.coalesce(1).write.mode("overwrite").json(tmp_dir)

files = dbutils.fs.ls(tmp_dir)
part_json = [f.path for f in files if f.name.startswith("part-") and f.name.endswith(".json")]
if not part_json:
    raise Exception("No se encontró part-*.json en la carpeta temporal")

dbutils.fs.mv(part_json[0], final_file)

# borrar temp (se lleva _SUCCESS, _started, etc. del temp)
dbutils.fs.rm(tmp_dir, recurse=True)

print("🎉 Listo. Solo debe quedar:")
print(final_file)
