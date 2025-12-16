 
# Modelo Estrella -> Capa Plata
## Justificación


<img width="1681" height="837" alt="image" src="https://github.com/user-attachments/assets/b160668f-eaa4-47ff-83e0-9fdca7b6bd01" />

```bash
df = spark.read.parquet("wasbs://bronce@azuresi807miguel.blob.core.windows.net/curated/superstore.parquet")

# Dimensión Tiempo
dim_tiempo = df.select("Order Date").distinct() \
    .withColumn("fecha_id", F.date_format(F.col("Order Date"), "yyyyMMdd")) \
    .withColumn("anio", F.year(F.col("Order Date"))) \
    .withColumn("mes", F.month(F.col("Order Date"))) \
    .select("fecha_id", "anio", "mes") \
    .dropDuplicates()
dim_tiempo.write.mode("overwrite").parquet("wasbs://plata@azuresi807miguel.blob.core.windows.net/dim_tiempo/")

# Dimensión Cliente
dim_cliente = df.select("Customer ID", "Customer Name", "Segment", "Region").distinct() \
    .withColumnRenamed("Customer ID", "cliente_id") \
    .select("cliente_id", "Customer Name", "Segment", "Region")
dim_cliente.write.mode("overwrite").parquet("wasbs://plata@azuresi807miguel.blob.core.windows.net/dim_cliente/")

# Dimensión Producto
dim_producto = df.select("Product ID", "Category", "Sub-Category").distinct() \
    .withColumnRenamed("Product ID", "producto_id") \
    .select("producto_id", "Category", "Sub-Category")
dim_producto.write.mode("overwrite").parquet("wasbs://plata@azuresi807miguel.blob.core.windows.net/dim_producto/")

# Tabla de Hechos
f_ventas = df \
    .withColumn("fecha_id", F.date_format(F.col("Order Date"), "yyyyMMdd")) \
    .withColumn("cliente_id", F.col("Customer ID")) \
    .withColumn("producto_id", F.col("Product ID")) \
    .select(
        "fecha_id",
        "cliente_id",
        "producto_id",
        F.col("Sales").alias("ventas"),
        F.col("Profit").alias("utilidad"),
        F.col("Quantity").alias("cantidad")
    )
f_ventas.write.mode("overwrite").parquet("wasbs://plata@azuresi807miguel.blob.core.windows.net/f_ventas/")

print("✅ Capa PLATA generada.")
```

## Se guarda en la capa plata 
<img width="2559" height="1466" alt="image" src="https://github.com/user-attachments/assets/d0038ab9-e565-47e0-813c-7e545ffddf7f" />

# Capa Oro -> Generamos el Json y lo guardamos en la capa de oro 
```bash
import json

print("⚙️ Generando JSON detallado desde capa curated...")

# Leer datos limpios (nivel de transacción)
df = spark.read.parquet("wasbs://bronce@azuresi807miguel.blob.core.windows.net/curated/superstore.parquet")

# Añadir campos calculados
df_enriquecido = df \
    .withColumn("margen", (F.col("Profit") / F.col("Sales")) * 100) \
    .withColumn("anio", F.year(F.col("Order Date"))) \
    .withColumn("mes", F.month(F.col("Order Date"))) \
    .withColumn("dia_semana", F.date_format(F.col("Order Date"), "EEEE"))

# Seleccionar columnas finales
df_final = df_enriquecido.select(
    "Row ID",
    "Order ID",
    F.col("Order Date").alias("Order Date"),
    F.col("Ship Date").alias("Ship Date"),
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "Country",
    "City",
    "State",
    "Region",
    "Category",
    "Sub-Category",
    "Product Name",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
    F.round("margen", 2).alias("margen"),  # Margen en %
    "anio",
    "mes",
    "dia_semana"
)

# Convertir a Pandas y luego a JSON
pdf = df_final.toPandas()
pdf = pdf.where(pdf.notnull(), None)  # NaN → null
json_records = pdf.to_dict(orient='records')

# Guardar en disco
with open("/databricks/driver/superstore_dashboard.json", "w", encoding="utf-8") as f:
    json.dump(json_records, f, indent=2, ensure_ascii=False, default=str)

# Subir a capa ORO
dbutils.fs.put(
    "wasbs://oro@azuresi807miguel.blob.core.windows.net/superstore_dashboard.json",
    json.dumps(json_records, indent=2, ensure_ascii=False, default=str),
    overwrite=True
)

print(f"✅ JSON detallado generado con {len(json_records)} registros.")
print("📄 Ruta local: /databricks/driver/superstore_dashboard.json")
print("☁️ Guardado en ORO: wasbs://oro@.../superstore_dashboard.json")
```
# Vemos que se guardo en la capa oro

<img width="2559" height="1386" alt="image" src="https://github.com/user-attachments/assets/09c430fd-fd9c-457c-802f-287b2bd7c54b" />

El josn generado es superstore_dashboard.json
que se usara para realizar el dashboard y los kpis

# Logs

Podemos visualizar los log, del notebook EDA_Superstore

<img width="2559" height="1359" alt="image" src="https://github.com/user-attachments/assets/46b13d01-adf5-48c7-9c20-bcf0600ea93d" />

```bash
```
