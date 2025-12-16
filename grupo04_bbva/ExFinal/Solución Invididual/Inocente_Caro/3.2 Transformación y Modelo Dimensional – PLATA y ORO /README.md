 
# Modelo Estrella -> Capa Plata

```bash
# ✅ Leer desde bronce/curated (entrada para PLATA)
df = spark.read.parquet("wasbs://bronce@azuresi807miguel.blob.core.windows.net/curated/superstore.parquet")

# --- DIMENSIÓN TIEMPO (de Order_Date) ---
dim_tiempo = df.select("Order_Date").distinct() \
    .withColumn("fecha_id", date_format(col("Order_Date"), "yyyyMMdd")) \
    .withColumn("anio", year("Order_Date")) \
    .withColumn("mes", month("Order_Date")) \
    .select("fecha_id", "anio", "mes") \
    .dropDuplicates()

dim_tiempo.write.mode("overwrite").parquet(
    "wasbs://plata@azuresi807miguel.blob.core.windows.net/dim_tiempo/"
)

# --- DIMENSIÓN CLIENTE ---
dim_cliente = df.select("Customer ID", "Customer Name", "Segment", "Region").distinct() \
    .withColumnRenamed("Customer ID", "cliente_id") \
    .select("cliente_id", "Customer Name", "Segment", "Region")

dim_cliente.write.mode("overwrite").parquet(
    "wasbs://plata@azuresi807miguel.blob.core.windows.net/dim_cliente/"
)

# --- DIMENSIÓN PRODUCTO ---
dim_producto = df.select("Product ID", "Category", "Sub-Category").distinct() \
    .withColumnRenamed("Product ID", "producto_id") \
    .select("producto_id", "Category", "Sub-Category")

dim_producto.write.mode("overwrite").parquet(
    "wasbs://plata@azuresi807miguel.blob.core.windows.net/dim_producto/"
)

# --- HECHOS ---
f_ventas = df \
    .withColumn("fecha_id", date_format(col("Order_Date"), "yyyyMMdd")) \
    .withColumn("cliente_id", col("Customer ID")) \
    .withColumn("producto_id", col("Product ID")) \
    .select(
        "fecha_id", "cliente_id", "producto_id",
        col("Sales").cast("double").alias("ventas"),
        col("Profit").cast("double").alias("utilidad"),
        col("Quantity").cast("int").alias("cantidad")
    )

f_ventas.write.mode("overwrite").parquet(
    "wasbs://plata@azuresi807miguel.blob.core.windows.net/f_ventas/"
)

print("✅ Capa PLATA generada desde bronce/curated.")
```

## Se guarda en la capa plata 
<img width="2559" height="1466" alt="image" src="https://github.com/user-attachments/assets/d0038ab9-e565-47e0-813c-7e545ffddf7f" />

# KPIs -> Capa Oro
```bash
kpis = f_ventas.groupBy("fecha_id") \
    .agg(
        sum("ventas").alias("ingresos"),
        sum("utilidad").alias("utilidad_total"),
        count("*").alias("ordenes"),
        avg("ventas").alias("ticket_promedio")
    ) \
    .withColumn("margen", (col("utilidad_total") / col("ingresos")) * 100)

kpis.write.mode("overwrite").parquet(
    "wasbs://oro@azuresi807miguel.blob.core.windows.net/kpis_superstore.parquet"
)

print("✅ Capa ORO generada.")
```
# Vemos que se guardo en la capa oro
<img width="2559" height="908" alt="image" src="https://github.com/user-attachments/assets/47ce516f-e320-478d-a351-4cfac744bd4e" />


```bash
```
