# Iniciamos el login


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
from pyspark.sql.functions import *

# ✅ Autenticación con clave de acceso (reemplaza KEY1 por tu clave real)
spark.conf.set(
    "fs.azure.account.key.azuresi807miguel.blob.core.windows.net",
    "YOU_KEY"
)

df = spark.read.option("header", "true").csv(
    "wasbs://bronce@azuresi807miguel.blob.core.windows.net/raw/Sample - Superstore.csv"
)

start = datetime.now()
print(f"🕒 EDA ejecutado el: {start.strftime('%Y-%m-%d %H:%M:%S')}")

print("✅ Primeras filas:")
df.show(3)

print(f"\n📊 Total filas: {df.count()}")
print("\n🧩 Esquema:")
df.printSchema()

print("\n1️⃣ Nulos por columna:")
df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()

print("\n2️⃣ Estadísticas de ventas:")
df.select("Sales", "Profit").describe().show()

print("\n3️⃣ Top 5 categorías por ventas:")
df.groupBy("Category").agg(sum("Sales").alias("total_sales")).orderBy("total_sales", ascending=False).show()

print(f"\n✅ EDA completado en: {(datetime.now() - start).total_seconds():.2f} seg")
```

## Aqui limpiamos la y lo Guardamos en la ruta bronce/processed

<img width="2559" height="1239" alt="image" src="https://github.com/user-attachments/assets/866327eb-c54b-4fe3-bf32-ebf619035ece" />


```bash
# ✅ Leer desde bronce/raw
df_raw = spark.read.option("header", "true").option("inferSchema", "true").csv(
    "wasbs://bronce@azuresi807miguel.blob.core.windows.net/raw/Sample - Superstore.csv"
)

# ✅ Limpieza mínima (processed): corregir fechas, tipos, nulos críticos
df_processed = df_raw \
    .withColumn("Order_Date", to_date(col("Order Date"), "M/d/yyyy")) \
    .withColumn("Ship_Date", to_date(col("Ship Date"), "M/d/yyyy")) \
    .withColumn("Sales", col("Sales").cast("double")) \
    .withColumn("Profit", col("Profit").cast("double")) \
    .filter(col("Order_Date").isNotNull())  # ejemplo de validación

# ✅ Guardar en bronce/processed/ (como Parquet)
df_processed.write.mode("overwrite").parquet(
    "wasbs://bronce@azuresi807miguel.blob.core.windows.net/processed/superstore.parquet"
)

print("✅ Capa BRONCE/processed generada.")
```
## Validación Adicion y lo Guardamos en la ruta bronce/curated

<img width="2559" height="1319" alt="image" src="https://github.com/user-attachments/assets/be822de1-3049-4ae6-bbd1-15050d736ed3" />


```bash
# ✅ Curated: solo órdenes válidas (Sales > 0, Profit razonable)
df_curated = df_processed \
    .filter(col("Sales") > 0) \
    .filter(col("Profit") >= -col("Sales"))  # no pérdida > 100%

df_curated.write.mode("overwrite").parquet(
    "wasbs://bronce@azuresi807miguel.blob.core.windows.net/curated/superstore.parquet"
)

print("✅ Capa BRONCE/curated generada.")
```
