# 📝 Bitácora del Pipeline BI en AWS – Grupo 10
👥 Grupo: 10  
🗓️ Fecha: 09-11-2025  
📦 Proyecto: Pipeline de Business Intelligence Cloud  
🚀 Servicios utilizados: S3, Glue, Athena *(QuickSight: pendiente)*

---

## 📁 1. Ingesta de datos (S3 – zona *raw*)

- Se trabajó el archivo original `Amazon Sale Report.csv` desde el entorno local en **Visual Studio Code**.
- Se realizó limpieza de datos y ajustes de columnas.
- Se resolvieron errores en consola relacionados a:
  - Secuencias de escape en rutas (`\U`, `\n`) con uso de `r'path'`.
  - Unicode (`📦`) y codificación de consola Windows.
- Se exportó el archivo limpio como `ecommerce_clean.csv`.

### 🪣 Carga a S3
- Bucket: `si807u-10-bi`
- Ruta destino:  
```

s3://si807u-10-bi/raw/ecommerce/ecommerce_clean.csv

```
- Se configuró AWS CLI con `Access Key ID` y `Secret Access Key` generados por IAM.
- Se creó una política IAM inline llamada `AllowS3Grupo10` con permisos iniciales de:
- `s3:GetObject`
- `s3:PutObject`
- `s3:ListBucket`

---

## 🔍 2. Glue Crawler y Catálogo de Datos

### ✅ Base de datos
- Nombre: `raw_data`

### ✅ Crawler creado
- Nombre: `ecommerce_raw_crawler`
- Ruta: `s3://si807u-10-bi/raw/ecommerce/`
- Rol: `AWSGlueServiceRole-lider`
- Target: `raw_data`
- Tabla generada: `ecommerce_clean`

### ⚠️ Validaciones
- Se revisaron y ajustaron los tipos de datos.
- Se eliminó la columna innecesaria `unnamed:_22`.

---

## 🔁 3. Transformación con Glue Job (ETL – PySpark)

### 🧾 Script: `transform_raw_to_curated.py`

Ubicación:  
```
s3://si807u-10-bi/scripts/transform_raw_to_curated.py
```

### 🔧 Funcionalidad:
- Conversión de columna `date` a `order_date` (tipo fecha)
- Creación de columnas `year` y `month` para particionado
- Limpieza de columnas no necesarias
- Escritura en formato **Parquet particionado por año y mes**

### 📌 Código base:
```python
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import year, month, to_date, col
import sys

args = getResolvedOptions(sys.argv, ['SOURCE', 'TARGET'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

df = spark.read.option("header", True).csv(args['SOURCE'])

df = df.drop("unnamed:_22")
df = df.withColumn("order_date", to_date(col("date"), "yyyy-MM-dd"))
df = df.withColumn("year", year("order_date"))
df = df.withColumn("month", month("order_date"))

df.write.mode("overwrite").partitionBy("year", "month").parquet(args['TARGET'])
```

### ⚙️ Job ejecutado en Glue

* Nombre del Job: `transform_raw_to_curated`
* Parámetros:

  * `--SOURCE`: `s3://si807u-10-bi/raw/ecommerce/`
  * `--TARGET`: `s3://si807u-10-bi/curated/ecommerce/`

### ✅ Problemas solucionados:

* ❌ Error 403 al leer el script desde S3 → se agregó permiso `s3:GetObject`
* ❌ Error 403 al escribir en `curated/` → se amplió política con `s3:PutObject`

---

## 📊 4. Athena – Consultas analíticas

### ✅ `00_create_analytics_db.sql`

```sql
CREATE DATABASE IF NOT EXISTS analytics_db;
```

---

### ✅ `10_create_sales_curated.sql` (adaptado a columnas del dataset)

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS analytics_db.sales_curated (
  order_id string,
  order_date date,
  status string,
  fulfilment string,
  sales_channel string,
  ship_service_level string,
  style string,
  sku string,
  category string,
  size string,
  asin string,
  courier_status string,
  quantity int,
  currency string,
  sales double,
  ship_city string,
  ship_state string,
  ship_postal_code string,
  ship_country string,
  promotion_ids string,
  b2b boolean,
  fulfilled_by string
)
PARTITIONED BY (year int, month int)
STORED AS PARQUET
LOCATION 's3://si807u-10-bi/curated/ecommerce/';
```

### ✅ Particionado:

```sql
MSCK REPAIR TABLE analytics_db.sales_curated;
```

---

### ✅ `20_kpi_sales_summary.sql` (adaptado)

```sql
SELECT 
  category,
  SUM(sales) AS total_sales,
  COUNT(order_id) AS total_orders,
  SUM(quantity) AS total_quantity
FROM analytics_db.sales_curated
GROUP BY category
ORDER BY total_sales DESC;
```

---

## 📈 5. QuickSight – *Pendiente*

### ⚠️ No se pudo completar este paso

> Al intentar crear la cuenta de QuickSight, el formulario se recargaba sin avanzar. Por tanto, no se pudo conectar con Athena ni generar el Dashboard “Ventas por Categoría”.

Se deja la intención documentada para referencias futuras.

---

## 📌 Extras y mejoras realizadas

* Se consolidó una política IAM inline (`AllowScriptAccess`) con:

  * Acceso completo a `si807u-10-bi` (`Get`, `Put`, `Delete`, `List`)
  * Permisos para ejecutar Glue Jobs y ver logs (`glue:*`, `logs:*`)
* Se estructuró el código PySpark según buenas prácticas
* Se adaptaron scripts SQL para Athena según el dataset real

---

## ✅ Checklist Final de Entrega

| Tarea                               | Estado                             |
| ----------------------------------- | ---------------------------------- |
| CSV limpio cargado a S3/raw         | ✅                                  |
| Crawler creado y tabla en Glue      | ✅                                  |
| Glue Job ejecutado con particionado | ✅                                  |
| Tabla externa creada en Athena      | ✅                                  |
| Particiones registradas (`MSCK`)    | ✅                                  |
| KPIs ejecutados en Athena           | ✅                                  |
| Dashboard en QuickSight             | ⚠️ *Pendiente por error de cuenta* |
| Bitácora actualizada                | ✅                                  |

---

## 📌 Próximos pasos sugeridos

* Resolver problema de creación de cuenta QuickSight
* Crear dataset desde Athena
* Diseñar y publicar dashboard BI

