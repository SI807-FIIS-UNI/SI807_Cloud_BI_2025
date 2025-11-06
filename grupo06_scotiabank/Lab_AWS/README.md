# 🧪 Laboratorio AWS – Configuración Inicial (S3, Glue, IAM y Athena)

## 🗂️ 1. Creación del Bucket S3

El primer paso consistió en crear un **bucket S3** que servirá como almacenamiento principal para los datos utilizados en el laboratorio.  
Este bucket será el origen desde el cual **AWS Glue** obtendrá los archivos para el proceso de catalogación y análisis.

### 🔧 Detalles de configuración
Durante la creación del bucket, se completaron los siguientes campos solicitados por AWS:

- **Bucket name:** `s3-grupo-6-vf`  
- **AWS Region:** `us-east-1` (N. Virginia)  
- **Block Public Access:** Habilitado  
- **Bucket versioning:** Deshabilitado  
- **Default encryption:** Deshabilitado  


Dentro del bucket, se creó la siguiente estructura de carpetas:

```json
s3-grupo-6-vf/
 └── archive/
      └── Amazon Sale Report.csv
```


# 🤖 2. Configuración del Crawler en AWS Glue

El siguiente paso fue configurar un AWS Glue Crawler, encargado de escanear el bucket S3 y generar automáticamente una tabla de metadatos en el Glue Data Catalog.

## ⚙️ Campos configurados al crear el Crawler

Durante la creación del Crawler, se completaron los siguientes campos requeridos:

- **Name**: crawler-grupo-6

- **Data source**: S3

- **S3 path**: s3://s3-grupo-6-vf/archive/

- **IAM role**: AWSGlueServiceRole-grupo6 (rol creado con permisos específicos para acceder al bucket)

- **Schedule**: Ejecutar bajo demanda (no programado automáticamente)

- **Database**: grupo6_db (base de datos creada en Glue para almacenar los metadatos)

- **Output**: Sobrescribir tablas existentes en caso de cambios detectados

Una vez configurado, el crawler fue ejecutado manualmente para detectar el archivo Amazon Sale Report.csv dentro del bucket, generando automáticamente la estructura de columnas y tipos de datos en Glue Catalog.

# 🔐 3. Configuración de IAM Policy

Como parte del uso del Crawler, fue necesario definir una política de permisos IAM que permita al rol de Glue acceder correctamente al bucket S3.
Esta política garantiza que el servicio tenga los permisos mínimos necesarios para listar, leer, escribir y eliminar objetos dentro del bucket.

```json
# 📜 Política IAM utilizada
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-grupo-6-vf",
                "arn:aws:s3:::s3-grupo-6-vf/*",
                "arn:aws:s3:::s3-grupo-6-vf/archive/Amazon Sale Report.csv/*",
                "arn:aws:s3:::s3-grupo-6-vf/archive/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "877617909831"
                }
            }
        }
    ]
}
```
# 🔎 Aspectos destacados

Action: Define las operaciones permitidas sobre los recursos de S3:

- **GetObject**: Leer objetos del bucket

- **PutObject**: Escribir nuevos objetos

- **ListBucket**: Listar el contenido del bucket

- **DeleteObject**: Eliminar objetos existentes

- **Resource**: Especifica los recursos de S3 a los cuales el rol tiene acceso.
Incluye el bucket principal (s3-grupo-6-vf) y sus subrutas dentro de archive/.

# ⚙️ 4. Desarrollo del Script de Transformación (AWS Glue Job)

En esta fase se desarrolló un **script en Python** que ejecuta un **Glue Job** para leer, transformar y escribir los datos del bucket S3 en formato **Parquet**, optimizado para ser consultado desde **Athena**.

El propósito del script es **limpiar**, **renombrar columnas**, **normalizar fechas**, **convertir tipos de datos**, y **generar particiones** por año y mes para mejorar el rendimiento en consultas posteriores.

## 🧩 Script Python – Transformación de datos
```python
import sys
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME","SOURCE","TARGET"])
sc = SparkContext()
glue = GlueContext(sc)
spark = glue.spark_session

print("🚀 Iniciando Glue Job de transformación...")

df = (spark.read
      .option("header", True)
      .option("inferSchema", True)
      .csv(args["SOURCE"]))

print(f"📊 Registros iniciales: {df.count()}")

df2 = (df
    .withColumnRenamed("index", "index_id")
    .withColumnRenamed("Order ID", "order_id")
    .withColumnRenamed("Date", "order_date_raw")
    .withColumnRenamed("Status", "order_status")
    .withColumnRenamed("Fulfilment", "fulfilment_type")
    .withColumnRenamed("Sales Channel", "sales_channel")
    .withColumnRenamed("ship-service-level", "ship_service_level")
    .withColumnRenamed("Style", "style")
    .withColumnRenamed("SKU", "sku")
    .withColumnRenamed("Category", "category")
    .withColumnRenamed("Size", "size")
    .withColumnRenamed("ASIN", "asin")
    .withColumnRenamed("Courier Status", "courier_status")
    .withColumnRenamed("Qty", "quantity")
    .withColumnRenamed("currency", "currency_code")
    .withColumnRenamed("Amount", "amount")
    .withColumnRenamed("ship-city", "ship_city")
    .withColumnRenamed("ship-state", "ship_state")
    .withColumnRenamed("ship-postal-code", "ship_postal_code")
    .withColumnRenamed("ship-country", "ship_country")
    .withColumnRenamed("promotion-ids", "promotion_ids")
    .withColumnRenamed("B2B", "is_b2b")
    .withColumnRenamed("fulfilled-by", "fulfilled_by")
    # 🧩 Convertir fechas con múltiples formatos posibles
    .withColumn(
        "order_date",
        F.coalesce(
            F.to_date("order_date_raw", "MM-dd-yy"),
            F.to_date("order_date_raw", "M/d/yyyy"),
            F.to_date("order_date_raw", "MM/dd/yyyy")
        )
    )
    # 🔍 Crear particiones derivadas
    .withColumn("anio", F.year("order_date"))
    .withColumn("mes", F.date_format("order_date", "MM"))
    # 💰 Convertir monto numérico
    .withColumn("amount_numeric", F.col("amount").cast("double"))
    # ⚙️ Filtrar registros con fechas válidas
    .filter(F.col("order_date").isNotNull())
    # Eliminar celdas vacías en la columna de montos
    .withColumn(
        "amount",
        F.when(F.col("amount").cast("double").isNotNull(), F.col("amount").cast("double"))
         .otherwise(F.lit(0.0))
    )
)

(df2.write.mode("overwrite")
    .partitionBy("anio","mes")
    .parquet(args["TARGET"]))

print("✅ Transformación completada. Datos guardados en ruta de destino.")

```

| Parámetro  | Descripción                      | Ejemplo                                             |
| ---------- | -------------------------------- | --------------------------------------------------- |
| `JOB_NAME` | Nombre del job en Glue           | `job-transform-orders`                              |
| `SOURCE`   | Ruta S3 de origen (archivo CSV)  | `s3://s3-grupo-6-vf/archive/Amazon Sale Report.csv` |
| `TARGET`   | Ruta S3 destino (salida Parquet) | `s3://s3-grupo-6-vf/curated/`                       |


## 5. Consumo de datos en AWS Athena

Una vez transformados los datos y almacenados en formato Parquet, se procedió a crear una tabla externa en Athena que permita consultarlos eficientemente.

```sql
DROP TABLE IF EXISTS base_prueba.orders_parquet

CREATE EXTERNAL TABLE IF NOT EXISTS base_prueba.orders_parquet (
    index_id               int,
    order_id               string,
    order_date             date,
    order_status           string,
    fulfilment_type        string,
    sales_channel          string,
    ship_service_level     string,
    style                  string,
    sku                    string,
    category               string,
    size                   string,
    asin                   string,
    courier_status         string,
    quantity               int,
    currency_code          string,
    amount                 double,
    ship_city              string,
    ship_state             string,
    ship_postal_code       double,
    ship_country           string,
    promotion_ids          string,
    is_b2b                 boolean,
    fulfilled_by           string,
    amount_numeric         double
)
PARTITIONED BY (
    anio                   int,
    mes                    string
)
STORED AS PARQUET
LOCATION 's3://s3-grupo-6-vf/curated/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');


MSCK REPAIR TABLE base_prueba.orders_parquet;

SELECT *
FROM base_prueba.orders_parquet
LIMIT 20;
```

## 🧰 Actualización de particiones

Después de crear la tabla, se debe ejecutar el siguiente comando para que Athena reconozca las nuevas particiones generadas por el Glue Job:

```sql
MSCK REPAIR TABLE base_prueba.orders_parquet;
```

## 🔎 Consulta de verificación

```sql
SELECT *
FROM base_prueba.orders_parquet
LIMIT 20;
```