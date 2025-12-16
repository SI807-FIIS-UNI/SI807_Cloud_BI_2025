# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.types import *

# 1. Configuración

storage_account = "azdatalakefinal"
container = "bronce"

storage_account_key = "s7afnbWsMe4zI5rLCHBhOW6fRHiaWfQOlDyp22jFA3152SrFkVQERlIIaVBgxAPRlJ0z/5NQu9fl+ASt5JBUQA=="
spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    storage_account_key
)

# 2. Leer datos de /bronce/processed

input_path = f"abfss://{container}@{storage_account}.dfs.core.windows.net/processed/data_procesada.csv"

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(input_path)

print(f"Registros leídos: {df.count()}")
display(df.limit(5))

# 3. Validaciones de calidad de datos

# Validar que no haya Transaction_ID duplicados
duplicates = df.groupBy("Transaction_ID").count().filter(F.col("count") > 1)
num_duplicates = duplicates.count()

if num_duplicates > 0:
    print(f"⚠️ Se encontraron {num_duplicates} Transaction_IDs duplicados")
    display(duplicates)
else:
    print("✅ No hay Transaction_IDs duplicados")

# Validar valores nulos en columnas críticas
critical_columns = ["Transaction_ID", "Date", "Customer_Name", "Total_Cost", "Total_Items"]

print("\n=== VALIDACIÓN DE NULOS ===")

for col in critical_columns:
    null_count = df.filter(F.col(col).isNull()).count()
    if null_count > 0:
        print(f"⚠️ {col}: {null_count} valores nulos")
    else:
        print(f"✅ {col}: Sin valores nulos")

# 4. Validar rangos de valores

print("\n=== VALIDACIÓN DE RANGOS ===")

# Total_Cost debe ser positivo
negative_cost = df.filter(F.col("Total_Cost") <= 0).count()
if negative_cost > 0:
    print(f"⚠️ {negative_cost} registros con Total_Cost <= 0")
else:
    print("✅ Todos los Total_Cost son positivos")

# Total_Items debe ser positivo
negative_items = df.filter(F.col("Total_Items") <= 0).count()
if negative_items > 0:
    print(f"⚠️ {negative_items} registros con Total_Items <= 0")
else:
    print("✅ Todos los Total_Items son positivos")

# Verificar fechas válidas
invalid_dates = df.filter(F.col("Date").isNull()).count()
if invalid_dates > 0:
    print(f"⚠️ {invalid_dates} fechas inválidas")
else:
    print("✅ Todas las fechas son válidas")

# 5. Validar valores categóricos

print("\n=== VALORES ÚNICOS EN COLUMNAS CATEGÓRICAS ===")

categorical_cols = ["Payment_Method", "City", "Store_Type", "Discount_Applied", 
                   "Customer_Category", "Season"]

for col in categorical_cols:
    unique_values = df.select(col).distinct().count()
    print(f"{col}: {unique_values} valores únicos")

print("\nPayment Methods:")
df.groupBy("Payment_Method").count().orderBy(F.desc("count")).show()

print("Cities:")
df.groupBy("City").count().orderBy(F.desc("count")).show()

print("Store Types:")
df.groupBy("Store_Type").count().orderBy(F.desc("count")).show()

# 6. Estadísticas básicas

print("\n=== ESTADÍSTICAS GENERALES ===")
print(f"Total de registros: {df.count():,}")
print(f"Clientes únicos: {df.select('Customer_Name').distinct().count():,}")
print(f"Rango de fechas: {df.select(F.min('Date')).collect()[0][0]} a {df.select(F.max('Date')).collect()[0][0]}")

print("\nEstadísticas de Total_Cost:")
df.select(
    F.min("Total_Cost").alias("Min"),
    F.avg("Total_Cost").alias("Avg"),
    F.max("Total_Cost").alias("Max")
).show()

print("Estadísticas de Total_Items:")
df.select(
    F.min("Total_Items").alias("Min"),
    F.avg("Total_Items").alias("Avg"),
    F.max("Total_Items").alias("Max")
).show()

# 7. Verificar consistencia de datos

# Verificar que Product no esté vacío
empty_products = df.filter((F.col("Product").isNull()) | (F.col("Product") == "")).count()
if empty_products > 0:
    print(f"⚠️ {empty_products} registros sin productos")
else:
    print("✅ Todos los registros tienen productos")

# Verificar consistencia: si Discount_Applied es "Yes", debería haber descuento reflejado
discount_yes = df.filter(F.col("Discount_Applied") == "Yes").count()
discount_no = df.filter(F.col("Discount_Applied") == "No").count()
print(f"\nTransacciones con descuento: {discount_yes}")
print(f"Transacciones sin descuento: {discount_no}")

df_validated = df
print(f"✅ {df_validated.count()} registros validados")

# 8. Guardar CSV en /bronce/curated

output_path = f"abfss://{container}@{storage_account}.dfs.core.windows.net/curated"

# Guardar como CSV único
df_validated.coalesce(1) \
    .write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", "true") \
    .save(output_path + "/temp_dataset_validado")

# 9. Renombrar archivo a dataset_validado.csv

# Listar archivos en la carpeta temporal
files = dbutils.fs.ls(output_path + "/temp_dataset_validado")
csv_file = [f for f in files if f.name.endswith('.csv')][0]

# Copiar el CSV con el nombre correcto
dbutils.fs.cp(csv_file.path, output_path + "/dataset_validado.csv")

# Eliminar carpeta temporal
dbutils.fs.rm(output_path + "/temp_dataset_validado", recurse=True)

print(f"Archivo guardado en: {output_path}/dataset_validado.csv")

# 10. Verificación final

df_verify = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(output_path + "/dataset_validado.csv")

print(f"Registros en dataset_validado.csv: {df_verify.count()}")
display(df_verify.limit(10))

# 11. Resumen de validación

# COMMAND ----------
print("=" * 60)
print("RESUMEN DE VALIDACIÓN")
print("=" * 60)
print(f"✅ Datos validados exitosamente")
print(f"✅ Total de registros validados: {df_verify.count():,}")
print(f"✅ Archivo guardado en: /bronce/curated/dataset_validado.csv")
print("=" * 60)