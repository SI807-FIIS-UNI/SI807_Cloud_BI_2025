 
# Modelo Estrella -> Capa Plata ffff

## Justificación

Para la capa PLATA, implementé un modelo estrella mínimo, compuesto por una tabla de hechos (f_ventas) y tres dimensiones (dim_tiempo, dim_cliente, dim_producto). Esta elección responde a criterios técnicos fundamentados en escalabilidad, rendimiento y mantenibilidad:

1. Alto rendimiento en consultas analíticas:
El modelo estrella elimina las complejas uniones en cascada del modelo normalizado (3FN), reduciendo el número de joins a solo tres (uno por dimensión), lo que mejora significativamente el tiempo de respuesta en agregaciones típicas de BI (por ejemplo: "ventas por región y categoría"). Esto es crítico en entornos de visualización interactiva como Power BI o dashboards en React.

2. Simplicidad y claridad para el negocio:
La estructura estrella con una tabla central de hechos rodeada de dimensiones descriptivas es intuitiva para analistas y stakeholders, facilitando la comprensión del modelo sin necesidad de expertise en diseño de bases de datos. Por ejemplo, dim_tiempo expone directamente anio, mes, y dia, evitando cálculos repetitivos en el frontend.

3. Escalabilidad horizontal:
El modelo permite añadir nuevas dimensiones (como dim_ubicacion o dim_promocion) sin alterar la estructura existente, simplemente extendiendo las claves foráneas en f_ventas. Esto garantiza evolución a futuro sin refactorización costosa.

4. Optimización para procesamiento en la nube:
Al usar formatos columnares (Parquet) y claves de particionado (fecha_id), el modelo se alinea con las mejores prácticas de Azure Data Lake: lecturas eficientes, compresión nativa y soporte para predicate pushdown. Las dimensiones pequeñas (dim_tiempo, dim_producto) se benefician de broadcast joins en Spark, mejorando aún más el rendimiento del ETL.

5. Garantía de integridad sin sobreingeniería:
Se optó por usar los identificadores naturales del dominio (Customer ID, Product ID, fecha_id = YYYYMMDD) como claves primarias, evitando surrogate keys innecesarios para este contexto académico. Esto mantiene la trazabilidad con la fuente original y reduce complejidad, sin sacrificar la unicidad ni la integridad referencial (validada mediante dropDuplicates() y filter() en las capas bronce/curated y plata).

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

# Capa Oro 

## Generamos el Json y lo guardamos en la capa de oro 

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
### Vemos que se guardo en la capa oro

<img width="2559" height="1386" alt="image" src="https://github.com/user-attachments/assets/09c430fd-fd9c-457c-802f-287b2bd7c54b" />

El josn generado es superstore_dashboard.json
que se usara para realizar el dashboard y los kpis

## GENERAR KPIs PARA CAPA ORO 

Se creo los kpis_resumen.json que seran consumidos por el dashboard para su visualización.

<img width="2559" height="1388" alt="image" src="https://github.com/user-attachments/assets/67a0ca13-ac4d-4911-8935-d7d4aed6c124" />

```bash
print("📈 Generando KPIs precalculados para capa ORO...")

# Leer datos limpios
df = spark.read.parquet("wasbs://bronce@azuresi807miguel.blob.core.windows.net/curated/superstore.parquet")

# Calcular KPIs globales
total_filas = df.count()
agg_result = df.agg(
    F.sum("Sales").alias("total_ventas"),
    F.sum("Profit").alias("total_utilidad"),
    F.countDistinct("Order ID").alias("total_ordenes"),
    F.countDistinct("Customer ID").alias("total_clientes"),
    F.sum("Quantity").alias("total_articulos"),
    F.count(F.when(F.col("Profit") < 0, 1)).alias("ordenes_con_perdida")
).collect()[0]

# Extraer y calcular
total_ventas = float(agg_result["total_ventas"])
total_utilidad = float(agg_result["total_utilidad"])
total_ordenes = int(agg_result["total_ordenes"])
total_clientes = int(agg_result["total_clientes"])
total_articulos = int(agg_result["total_articulos"])
ordenes_con_perdida = int(agg_result["ordenes_con_perdida"])

margen_promedio = (total_utilidad / total_ventas) * 100 if total_ventas > 0 else 0.0
ticket_promedio = total_ventas / total_ordenes if total_ordenes > 0 else 0.0
pct_perdida = (ordenes_con_perdida / total_filas) * 100 if total_filas > 0 else 0.0

# Top categorías
top_categorias = (df.groupBy("Category")
                  .agg(F.sum("Sales").alias("ventas"))
                  .orderBy(F.desc("ventas"))
                  .limit(3)
                  .collect())
top_categorias_dict = {row["Category"]: float(row["ventas"]) for row in top_categorias}

# Construir diccionario de KPIs
kpis_resumen = {
    "metadata": {
        "descripcion": "KPIs precalculados para dashboard - Generado desde script Python",
        "generado_el": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fuente": "bronce/curated/superstore.parquet"
    },
    "kpis": {
        "total_ventas": round(total_ventas, 2),
        "total_utilidad": round(total_utilidad, 2),
        "margen_promedio_pct": round(margen_promedio, 2),
        "total_ordenes": total_ordenes,
        "total_clientes": total_clientes,
        "ticket_promedio": round(ticket_promedio, 2),
        "total_articulos_vendidos": total_articulos,
        "pct_ordenes_con_perdida": round(pct_perdida, 2)
    },
    "top_categorias_por_ventas": top_categorias_dict
}

# Guardar KPIs en ORO como JSON
dbutils.fs.put(
    "wasbs://oro@azuresi807miguel.blob.core.windows.net/kpis_resumen.json",
    json.dumps(kpis_resumen, indent=2, ensure_ascii=False),
    overwrite=True
)

# Opcional: también guardar como Parquet (más eficiente para Spark)
kpis_df = spark.createDataFrame([(
    total_ventas,
    total_utilidad,
    margen_promedio,
    total_ordenes,
    total_clientes,
    ticket_promedio,
    total_articulos,
    pct_perdida
)], [
    "total_ventas", "total_utilidad", "margen_promedio_pct",
    "total_ordenes", "total_clientes", "ticket_promedio",
    "total_articulos_vendidos", "pct_ordenes_con_perdida"
])

kpis_df.write.mode("overwrite").parquet(
    "wasbs://oro@azuresi807miguel.blob.core.windows.net/kpis_resumen.parquet"
)

print("✅ KPIs precalculados guardados en ORO:")
print("   - kpis_resumen.json")
print("   - kpis_resumen.parquet")
```

# Logs

Podemos visualizar los log, del notebook EDA_Superstore

<img width="2559" height="1359" alt="image" src="https://github.com/user-attachments/assets/46b13d01-adf5-48c7-9c20-bcf0600ea93d" />

```bash
```
