## Justificación de la elección de Google Cloud Platform (GCP)

La elección de Google Cloud Platform (GCP) para el desarrollo del proyecto de Inteligencia de Negocios se fundamenta en su enfoque nativo hacia la analítica avanzada y el procesamiento de grandes volúmenes de datos. GCP ofrece BigQuery, un Data Warehouse completamente serverless que elimina la necesidad de administrar infraestructura y permite ejecutar consultas masivas con alto rendimiento. Asimismo, servicios como Dataflow y Dataproc proporcionan escalabilidad automática para procesos ETL/ELT, mientras que Looker Studio, integrado de forma nativa y sin costos adicionales, facilita la visualización de indicadores clave. En conjunto, el modelo de precios por consulta, la integración entre servicios y la capacidad de escalar bajo demanda hacen que GCP se alinee de manera óptima con los requerimientos del proyecto EsSalud, superando a alternativas como AWS y Azure en simplicidad, eficiencia y costo total de operación.

## Comparación técnica de plataformas cloud (GCP vs AWS vs Azure)

| Criterio técnico | Google Cloud Platform (GCP) | Amazon Web Services (AWS) | Microsoft Azure | Justificación técnica |
|------------------|-----------------------------|----------------------------|------------------|------------------------|
| Analítica y Big Data | BigQuery totalmente *serverless*, separación de cómputo y almacenamiento, alto rendimiento analítico | Athena sobre S3 y Redshift con nodos provisionados | Synapse Analytics con SQL on-demand y pools | GCP elimina la administración de infraestructura y optimiza consultas masivas |
| Escalabilidad | Autoscaling completo en BigQuery y Dataflow | Escala amplia pero requiere configuración de clusters | Escalabilidad parcial con capacidad reservada | GCP escala automáticamente en todas las capas |
| Modelo de costos | Pago por consulta y almacenamiento particionado | Costos por instancias y servicios intermedios | Costos por DWU y Spark pools | Menor costo total de operación en GCP |
| Integración BI | Looker Studio nativo y gratuito | QuickSight con licencias | Power BI con licencias externas | Visualización sin costos adicionales en GCP |
| ETL / ELT | Dataflow (*serverless*) y Dataproc (Spark gestionado) | Glue limitado y EMR complejo | ADF visual pero menos eficiente | Mayor flexibilidad y potencia de procesamiento en GCP |
| Facilidad de implementación | Arquitectura simple y altamente integrada | Mayor complejidad por número de servicios | Configuración pesada con AD y Synapse | Menor curva de aprendizaje en GCP |
| Seguridad e IAM | IAM unificado con Service Accounts | IAM robusto pero complejo | Azure AD + RBAC corporativo | GCP ofrece equilibrio entre control y simplicidad |
| Ecosistema ML | Vertex AI y BigQuery ML integrados | SageMaker potente pero costoso | Azure ML menos robusto | GCP facilita la evolución hacia analítica predictiva |
| Alineación al proyecto | Enfoque directo en BI y análisis epidemiológico | Enfoque más general de infraestructura | Enfoque corporativo Microsoft | GCP se adapta mejor a proyectos analíticos |

## CÓDIGOS  

. CONFIGURACIÓN GENERAL
En esta sección se inicializa una sesión Spark, necesaria para ejecutar transformaciones distribuidas sobre grandes volúmenes de datos.
El nombre de la aplicación (retail-medallion) permite identificar el job dentro del clúster Dataproc.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, to_date
from functools import reduce

spark = SparkSession.builder.appName("retail-medallion").getOrCreate()

PROJECT_ID = "finalcarhuasj"

BRONCE_DS = "bronce"
PLATA_DS  = "plata"
ORO_DS    = "oro"

spark.conf.set("temporaryGcsBucket", "bucketfinalbi")
```

. RAW → BRONCE

```python
RAW_PATH = "gs://bucketfinalbi/bronce/raw/Retail_Transactions_Dataset.csv"
PROCESSING_PATH = "gs://bucketfinalbi/processing/retail_transactions"

# Leer CSV RAW
df_raw = (
    spark.read
    .option("header", "true")
    .csv(RAW_PATH)
)

# Normalizar strings
for c, t in df_raw.dtypes:
    if t == "string":
        df_raw = df_raw.withColumn(c, trim(col(c)))

# Eliminar filas totalmente nulas
df_no_nulls = df_raw.dropna(how="all")

# Eliminar duplicados
df_clean = df_no_nulls.dropDuplicates()

# Guardar CSV limpio (processing)
df_clean.coalesce(1).write.mode("overwrite") \
    .option("header", "true") \
    .csv(PROCESSING_PATH)

# Guardar en BigQuery (Bronce)
(
    df_clean.write
    .format("bigquery")
    .option("table", f"{PROJECT_ID}.{BRONCE_DS}.retail_transactions")
    .mode("overwrite")
    .save()
)
```

. PROCESSING → CURATED

```python
CURATED_PATH = "gs://bucketfinalbi/curated/retail_transactions"

df_curated = (
    df_clean
    .withColumn("Date", to_date(col("Date")))
    .withColumn("Total_Items", col("Total_Items").cast("int"))
    .withColumn("Total_Cost", col("Total_Cost").cast("double"))
    .withColumn("Discount_Applied", col("Discount_Applied").cast("boolean"))
)

df_curated.coalesce(1).write.mode("overwrite") \
    .option("header", "true") \
    .csv(CURATED_PATH)
```

. CURATED → PLATA

```python
dim_customer = df_curated.select(
    col("Customer_Name").alias("customer_name"),
    col("Customer_Category").alias("customer_category")
).dropDuplicates()

dim_customer.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.dim_customer") \
    .mode("overwrite").save()
```

. DIM_PRODUCT

```python
dim_product = df_curated.select(
    col("Product").alias("product_name")
).dropDuplicates()

dim_product.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.dim_product") \
    .mode("overwrite").save()
```

. DIM_CITY

```python
dim_city = df_curated.select(
    col("City").alias("city_name")
).dropDuplicates()

dim_city.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.dim_city") \
    .mode("overwrite").save()
```

. DIM_TIME

```python
dim_time = df_curated.select(
    col("Date").alias("date")
).dropDuplicates()

dim_time.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.dim_time") \
    .mode("overwrite").save()
```


. FACT_TRANSACTION (PLATA)

```python
fact_transaction = df_curated.select(
    "Transaction_ID",
    "Date",
    "Total_Items",
    "Total_Cost",
    "Discount_Applied"
)

fact_transaction.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.fact_transaction") \
    .mode("overwrite").save()
```

. PLATA → ORO

- DIMENSIONES (ORO)

```python
dim_customer_oro = spark.read.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.dim_customer") \
    .load()

dim_customer_oro.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{ORO_DS}.dim_customer") \
    .mode("overwrite").save()
```

- FACT_SALES (ORO)

```python
fact_sales = spark.read.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{PLATA_DS}.fact_transaction") \
    .load()

fact_sales.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{ORO_DS}.fact_sales") \
    .mode("overwrite").save()
```

```python
fact_sales.coalesce(1).write.mode("overwrite") \
    .option("header", "true") \
    .csv("gs://bucketfinalbi/oro/fact_sales")
```

## KPIS
- Configuración
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg,
    to_date
)

spark = SparkSession.builder.appName("oro-kpis-retail").getOrCreate()

PROJECT_ID = "finalcarhuasj"
ORO_DS = "oro"

spark.conf.set("temporaryGcsBucket", "bucketfinalbi")
```

-  Leer fact_sales
```python
fact_sales = (
    spark.read.format("bigquery")
    .option("table", f"{PROJECT_ID}.{ORO_DS}.fact_sales")
    .load()
)

fact_sales = (
    fact_sales
    .withColumn("Date", to_date(col("Date")))
    .withColumn("Total_Items", col("Total_Items").cast("int"))
    .withColumn("Total_Cost", col("Total_Cost").cast("double"))
)
```

-  KPI 1:Ticket promedio (GLOBAL)

```python
kpi_ticket_promedio = fact_sales.agg(
    avg("Total_Cost").alias("ticket_promedio")
)

kpi_ticket_promedio.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{ORO_DS}.kpi_ticket_promedio") \
    .mode("overwrite").save()
```

- KPI 2: Frecuencia de compra (por día)
```python
kpi_frecuencia_compra = (
    fact_sales
    .groupBy("Date")
    .agg(
        count("*").alias("frecuencia_compra")
    )
    .orderBy("Date")
)

kpi_frecuencia_compra.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{ORO_DS}.kpi_frecuencia_compra") \
    .mode("overwrite").save()
```
- KPI 3: Ventas diarias
```python
kpi_ventas_diarias = (
    fact_sales
    .groupBy("Date")
    .agg(
        spark_sum("Total_Cost").alias("ventas_diarias")
    )
    .orderBy("Date")
)

kpi_ventas_diarias.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{ORO_DS}.kpi_ventas_diarias") \
    .mode("overwrite").save()
```

- KPI 4: Promedio de ítems por transacción
```python
kpi_items_promedio = fact_sales.agg(
    avg("Total_Items").alias("items_promedio_por_transaccion")
)

kpi_items_promedio.write.format("bigquery") \
    .option("table", f"{PROJECT_ID}.{ORO_DS}.kpi_items_promedio") \
    .mode("overwrite").save()
```