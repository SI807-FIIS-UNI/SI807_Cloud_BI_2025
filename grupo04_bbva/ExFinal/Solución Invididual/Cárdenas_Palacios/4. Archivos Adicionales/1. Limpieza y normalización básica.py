# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.sql.types import *

# 1. Configuración de Storage Account

storage_account = "azdatalakefinal"
container = "bronce"

storage_account_key = "s7afnbWsMe4zI5rLCHBhOW6fRHiaWfQOlDyp22jFA3152SrFkVQERlIIaVBgxAPRlJ0z/5NQu9fl+ASt5JBUQA=="

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    storage_account_key
)

# 2. Leer datos crudos (Bronze)

input_path = f"abfss://{container}@{storage_account}.dfs.core.windows.net/raw/Retail_Transactions_Dataset.csv"

df_raw = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "false") \
    .load(input_path)

# 3. Parsear columnas

columns = ["Transaction_ID", "Date", "Customer_Name", "Product", "Total_Items", 
           "Total_Cost", "Payment_Method", "City", "Store_Type", "Discount_Applied",
           "Customer_Category", "Season", "Promotion"]

# Si todo está en una columna, separar
first_col = df_raw.columns[0]
if len(df_raw.columns) == 1:
    df_split = df_raw.withColumn("split_col", F.split(F.col(first_col), ","))
    for idx, col_name in enumerate(columns):
        df_split = df_split.withColumn(col_name, F.col("split_col").getItem(idx))
    df_parsed = df_split.drop("split_col", first_col)
else:
    df_parsed = df_raw

# 4. Limpiar columna Product

# Limpiar la columna Product (remover __[' y ']__)
df_cleaned = df_parsed.withColumn(
    "Product",
    F.regexp_replace(
        F.regexp_replace(F.col("Product"), "__\\['", ""),
        "'\\]__", ""
    )
)

# 5. Convertir tipos de datos y limpiar

df_processed = df_cleaned \
    .withColumn("Transaction_ID", F.col("Transaction_ID").cast(LongType())) \
    .withColumn("Date", F.to_timestamp(F.col("Date"), "yyyy-MM-dd HH:mm:ss")) \
    .withColumn("Customer_Name", F.trim(F.col("Customer_Name"))) \
    .withColumn("Product", F.trim(F.col("Product"))) \
    .withColumn("Total_Items", F.col("Total_Items").cast(IntegerType())) \
    .withColumn("Total_Cost", F.col("Total_Cost").cast(DoubleType())) \
    .withColumn("Payment_Method", F.trim(F.col("Payment_Method"))) \
    .withColumn("City", F.trim(F.col("City"))) \
    .withColumn("Store_Type", F.trim(F.col("Store_Type"))) \
    .withColumn("Discount_Applied", F.when(F.col("Discount_Applied") == "True", "Yes").otherwise("No")) \
    .withColumn("Customer_Category", F.trim(F.col("Customer_Category"))) \
    .withColumn("Season", F.trim(F.col("Season"))) \
    .withColumn("Promotion", F.when(F.col("Promotion") == "None", "No Promotion").otherwise(F.trim(F.col("Promotion"))))

# 6. Limpieza de datos

# Eliminar duplicados
df_processed = df_processed.dropDuplicates(["Transaction_ID"])

# Eliminar registros con valores nulos en campos críticos
df_processed = df_processed.filter(
    F.col("Transaction_ID").isNotNull() &
    F.col("Date").isNotNull() &
    F.col("Total_Cost").isNotNull()
)

# Validar que Total_Cost y Total_Items sean positivos
df_processed = df_processed.filter(
    (F.col("Total_Cost") > 0) &
    (F.col("Total_Items") > 0)
)

print(f"Registros después de limpieza: {df_processed.count()}")

# 7. Guardar CSV en /processed
output_path = f"abfss://{container}@{storage_account}.dfs.core.windows.net/processed"

# 8. Guardar como CSV único
df_processed.coalesce(1) \
    .write \
    .format("csv") \
    .mode("overwrite") \
    .option("header", "true") \
    .save(output_path + "/temp_data_procesada")

# 9. Renombrar archivo a data_procesada.csv

# Listar archivos en la carpeta temporal
files = dbutils.fs.ls(output_path + "/temp_data_procesada")
csv_file = [f for f in files if f.name.endswith('.csv')][0]

# Copiar el CSV con el nombre correcto
dbutils.fs.cp(csv_file.path, output_path + "/data_procesada.csv")

# Eliminar carpeta temporal
dbutils.fs.rm(output_path + "/temp_data_procesada", recurse=True)

print(f"Archivo guardado en: {output_path}/data_procesada.csv")