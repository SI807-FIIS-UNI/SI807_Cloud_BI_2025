# Databricks notebook source
from pyspark.sql import functions as F

storage_account = "azdatalakefinal"
container_silver = "plata"
storage_account_key = "s7afnbWsMe4zI5rLCHBhOW6fRHiaWfQOlDyp22jFA3152SrFkVQERlIIaVBgxAPRlJ0z/5NQu9fl+ASt5JBUQA=="

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    storage_account_key
)

base_path = f"abfss://{container_silver}@{storage_account}.dfs.core.windows.net"

postgres_host = "postgresql-final.postgres.database.azure.com"
postgres_port = "5432"
postgres_db = "data_oro"
postgres_user = "pgadmin"
postgres_password = "Password123!"

jdbc_url = f"jdbc:postgresql://{postgres_host}:{postgres_port}/{postgres_db}?sslmode=require"

print("✅ Configuración lista")

# ============================================================
# FUNCIÓN DE CARGA
# ============================================================

def load_csv(csv_path, table_name):
    print(f"\n📂 Cargando {table_name}...")
    
    df = spark.read.option("header", True).option("inferSchema", True).csv(csv_path)
    rows = df.count()
    print(f"   📊 {rows:,} registros")

    if rows == 0:
        print("   ⚠️ Archivo vacío, se omite")
        return

    df.write.jdbc(
        url=jdbc_url,
        table=table_name,
        mode="append",
        properties={
            "user": postgres_user,
            "password": postgres_password,
            "driver": "org.postgresql.Driver",
            "batchsize": "5000"
        }
    )

    print(f"   ✅ {table_name} cargada")

# ============================================================
# CARGA DE DIMENSIONES (SIN DEPENDENCIAS)
# ============================================================

print("\n" + "="*60)
print("DIMENSIONES")
print("="*60)

load_csv(f"{base_path}/dimensiones/dim_tiempo.csv", "dim_tiempo")
load_csv(f"{base_path}/dimensiones/dim_cliente.csv", "dim_cliente")
load_csv(f"{base_path}/dimensiones/dim_tienda.csv", "dim_tienda")
load_csv(f"{base_path}/dimensiones/dim_metodo_pago.csv", "dim_metodo_pago")
load_csv(f"{base_path}/dimensiones/dim_temporada.csv", "dim_temporada")
load_csv(f"{base_path}/dimensiones/dim_promocion.csv", "dim_promocion")
load_csv(f"{base_path}/dimensiones/dim_producto.csv", "dim_producto")

# ============================================================
# CARGA DE HECHOS (ORDEN CORRECTO)
# ============================================================

print("\n" + "="*60)
print("HECHOS")
print("="*60)

# 1️⃣ Fact principal (referencia solo dimensiones)
load_csv(f"{base_path}/hechos/fact_transacciones.csv", "fact_transacciones")

# 2️⃣ Fact puente (referencia fact + dim_producto)
load_csv(
    f"{base_path}/hechos/fact_transaccion_producto.csv",
    "fact_transaccion_producto"
)

print("\n🎉 CARGA COMPLETA Y CORRECTA")