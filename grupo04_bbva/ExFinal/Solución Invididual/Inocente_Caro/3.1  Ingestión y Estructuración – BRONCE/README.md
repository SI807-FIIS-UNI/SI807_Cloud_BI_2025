# Iniciamos el login d

```bash
az login
```
# Creamos las carpetas en la capa bronce

  <img width="2167" height="575" alt="image" src="https://github.com/user-attachments/assets/18c4ce5d-648e-4d2c-b0fb-e8d22db99d66" />

# Subimos el archivo csv. desde nuestro escritorio a la carpeta bronce/raw/
```bash
az storage blob upload `
  --account-name azuresi807miguel `
  --container-name bronce `
  --file "C:\Users\migue\Desktop\superstore.csv" `
  --name "raw/superstore.csv" `
  --auth-mode login
```

# Creamos nuestro cluster y un notebook para poder ejecurtas los siguientes bloques de codigos

## Vemos si hay valores nulo y mostramos los primeras filas

```bash
from datetime import datetime
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import IntegerType, DoubleType

# Asegurarse de tener SparkSession (en Databricks/Synapse ya existe)
spark = SparkSession.builder.getOrCreate()

# Configurar clave de Azure
spark.conf.set(
    "fs.azure.account.key.azuresi807miguel.blob.core.windows.net",
    "YOU_KEY"
)

print("📥 Leyendo datos RAW desde bronce/raw (sin limpieza)...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "false") \
    .csv("wasbs://bronce@azuresi807miguel.blob.core.windows.net/raw/Sample - Superstore.csv")

# Marca de tiempo
start = datetime.now()
print(f"🕒 EDA ejecutado el: {start.strftime('%Y-%m-%d %H:%M:%S')}")

# 1. Primeras filas
print("\n✅ Primeras 3 filas (datos crudos):")
df_raw.show(3, truncate=False)

# 2. Total de filas
total_filas = df_raw.count()
print(f"\n📊 Total filas en el archivo RAW: {total_filas}")

# 3. Esquema (todo es string)
print("\n🧩 Esquema RAW (sin inferencia):")
df_raw.printSchema()

# 4. Nulos por columna
print("\n1️⃣ Valores nulos por columna:")
df_raw.select([F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df_raw.columns]).show()

# 5. Estadísticas de Sales y Profit (convertir temporalmente a double para análisis)
print("\n2️⃣ Estadísticas de Sales y Profit (valores crudos):")
df_temp = df_raw \
    .withColumn("Sales_num", F.regexp_replace(F.col("Sales"), ",", "").cast("double")) \
    .withColumn("Profit_num", F.regexp_replace(F.col("Profit"), ",", "").cast("double"))

df_temp.select("Sales_num", "Profit_num").describe().show()

# 6. Top 5 categorías por frecuencia (solo para ver consistencia)
print("\n3️⃣ Top 5 categorías más frecuentes:")
df_raw.groupBy("Category").count().orderBy(F.desc("count")).show()

print(f"\n✅ EDA inicial completado en: {(datetime.now() - start).total_seconds():.2f} segundos")
```

## Aqui limpiamos la y lo Guardamos en la ruta bronce/processed

<img width="2559" height="1239" alt="image" src="https://github.com/user-attachments/assets/866327eb-c54b-4fe3-bf32-ebf619035ece" />


```bash
print("📥 Leyendo datos RAW desde bronce/raw...")
df_raw = spark.read \
    .option("header", "true") \
    .option("inferSchema", "false") \
    .csv("wasbs://bronce@azuresi807miguel.blob.core.windows.net/raw/Sample - Superstore.csv")

print("🔧 Aplicando limpieza y tipado explícito...")
df_processed = df_raw \
    .withColumn("Row ID", F.col("Row ID").cast(IntegerType())) \
    .withColumn("Order ID", F.trim(F.col("Order ID"))) \
    .withColumn("Order Date", F.to_date(F.col("Order Date"), "M/d/yyyy")) \
    .withColumn("Ship Date", F.to_date(F.col("Ship Date"), "M/d/yyyy")) \
    .withColumn("Ship Mode", F.trim(F.col("Ship Mode"))) \
    .withColumn("Customer ID", F.trim(F.col("Customer ID"))) \
    .withColumn("Customer Name", F.trim(F.col("Customer Name"))) \
    .withColumn("Segment", F.trim(F.col("Segment"))) \
    .withColumn("Country", F.trim(F.col("Country"))) \
    .withColumn("City", F.trim(F.col("City"))) \
    .withColumn("State", F.trim(F.col("State"))) \
    .withColumn("Postal Code", F.col("Postal Code").cast(IntegerType())) \
    .withColumn("Region", F.trim(F.col("Region"))) \
    .withColumn("Product ID", F.trim(F.col("Product ID"))) \
    .withColumn("Category", F.trim(F.col("Category"))) \
    .withColumn("Sub-Category", F.trim(F.col("Sub-Category"))) \
    .withColumn("Product Name", F.trim(F.col("Product Name"))) \
    .withColumn("Sales", F.regexp_replace(F.col("Sales"), ",", "").cast(DoubleType())) \
    .withColumn("Quantity", F.col("Quantity").cast(IntegerType())) \
    .withColumn("Discount", F.col("Discount").cast(DoubleType())) \
    .withColumn("Profit", F.regexp_replace(F.col("Profit"), ",", "").cast(DoubleType())) \
    .filter(F.col("Order Date").isNotNull())

# Guardar en BRONCE/processed
df_processed.write.mode("overwrite").parquet(
    "wasbs://bronce@azuresi807miguel.blob.core.windows.net/processed/superstore.parquet"
)
print("✅ BRONCE/processed guardado.")
```
## Validación Adicion y lo Guardamos en la ruta bronce/curated

<img width="2559" height="1319" alt="image" src="https://github.com/user-attachments/assets/be822de1-3049-4ae6-bbd1-15050d736ed3" />


```bash
df_curated = df_processed \
    .filter(F.col("Sales").isNotNull()) \
    .filter(F.col("Quantity").isNotNull()) \
    .filter(F.col("Sales") > 0) \
    .filter(F.col("Quantity") > 0) \
    .filter(F.col("Profit").isNotNull()) \
    .filter(F.col("Profit") >= -F.col("Sales"))

df_curated.write.mode("overwrite").parquet(
    "wasbs://bronce@azuresi807miguel.blob.core.windows.net/curated/superstore.parquet"
)
print("✅ BRONCE/curated guardado.")
```
