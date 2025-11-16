# 🧪 Laboratorio GRPO 05 AWS – Configuración Inicial 
En este laboratorio enseñan a implementar un pipeline de datos usando S3, Glue, IAM y Athena sobre AWS. 
Paso a paso, se desarrollara desde la configuración segura del almacenamiento, hasta la automatización del catálogo,
la transformación eficiente y el análisis con consultas SQL.

## 🗂️ 1. Creación del Bucket S3
El primer paso consistió en crear un bucket S3 que servirá como almacenamiento principal para los datos utilizados en el laboratorio.  
Este bucket será el origen desde el cual AWS Glue obtendrá los archivos para el proceso de catalogación y análisis.
El bucket de S3 funciona como data lake. Ahí almacenan tanto los datos crudos (raw) como los procesados (curated).

### 🔧Completamos los campos solicitados por AWS
- **Bucket name:** `s3-grupo-5-vf`  
- **AWS Region:** `sa-east-1` (Sudamérica – São Paulo)  
- **Block Public Access:** Habilitado  
- **Bucket versioning:** Deshabilitado  
- **Default encryption:** Deshabilitado  

Dentro del bucket, se creó la siguiente estructura de carpetas:

```
├── data/
│   └── raw/
├── evidencias/
├── script/
└── README.md
```
![Bucket](/grupo05_nettalco/Lab_AWS/evidencias/S3_archive_subidos.jpg)

# 🤖 2. Configuración del Crawler en AWS Glue
A continuación, se utiliza un crawler de Glue para explorar automáticamente la estructura de los datos y alimentar el Glue Data Catalog con los metadatos.
## ⚙️ Campos configurados al crear el Crawler

Se completaron los siguientes campos requeridos:
- **Name**: crawler_grupo5

- **Data source**: S3

- **S3 path**: s3://s3-grupo-5-vf/archive/

- **IAM role**: AWSGlueServiceRole-grupo5 (rol creado con permisos específicos para acceder al bucket)

- **Schedule**: Ejecutar bajo demanda (no programado automáticamente)

- **Database**: base_prueba (base de datos creada en Glue para almacenar los metadatos)

- **Output**: Sobrescribir tablas existentes en caso de cambios detectados


Una vez se completa la configuración del crawler, lo ejecutan manualmente para que explore el bucket, detecte el archivo 'Amazon Sale Report.csv' y genere automáticamente en el Glue Data Catalog una tabla con la estructura de columnas y tipos de datos correspondiente. De esta manera, establecen un 
esquema organizado que facilita futuras etapas de procesamiento y análisis.

![Crawler](/grupo05_nettalco/Lab_AWS/evidencias/Creacion_crawler.jpg)

# 🔐 3. Configuración de IAM Policy

Ahora nos toca definir una política IAM que le dé al rol de Glue los permisos necesarios para trabajar con el bucket S3. En este punto debemos asegurarnos de que el rol pueda listar, leer, escribir y eliminar objetos, pero sin otorgar permisos que no sean necesarios.

Una vez que tenemos claro qué necesita acceder el Crawler, procedemos a crear la política con los permisos mínimos. Después de este paso, asignamos esta política al rol que utilizará Glue, de modo que el servicio pueda interactuar correctamente con el bucket durante la ejecución de los crawlers y jobs.


## 📜 Política IAM utilizada
```json
{
    "Version": "2012-10-17",
    "statement": [
        {
            "Effect": "Allow",
            "Action": [
              "s3:GetObject",
              "s3:Putobject",
              "s3:ListBucket",
              "s3:Deleteobject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-grupo-5-vf/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws: ResourceAccount": "581983650106"
                }
            }
        }
    ]
}
```
Otorgan permisos de lectura, escritura, listado y eliminación solo sobre el bucket y sus subcarpetas. Así, aplican el principio de privilegios mínimos.

![IAM](/grupo05_nettalco/Lab_AWS/evidencias/Politicas_IAM.jpg)


# 🔎 Aspectos destacados

"Action" Define las operaciones permitidas sobre los recursos de S3:

- **GetObject**: Leer objetos del bucket

- **PutObject**: Escribir nuevos objetos

- **ListBucket**: Listar el contenido del bucket

- **DeleteObject**: Eliminar objetos existentes

- **Resource**: Especifica los recursos de S3 a los cuales el rol tiene acceso.
Incluye el bucket principal (s3-grupo-5-vf) y sus subrutas dentro de archive/.


# ⚙️ 4. Desarrollo del Script de Transformación (AWS Glue Job)

En esta parte avanzamos con la creación de un **script en Python** que será ejecutado por un **Glue Job**. Primero configuramos el job para que pueda leer los datos almacenados en el bucket S3; luego incorporamos las transformaciones necesarias dentro del script y, finalmente, preparamos la salida en formato **Parquet**, que es el formato ideal para consultarlo desde **Athena**.

Después de completar esta etapa, lo que sigue es validar que el job se ejecute sin errores y que los archivos Parquet generados estén correctamente organizados en el bucket.

![Evidencia job](/grupo06_scotiabank/Lab_AWS/evidences/Evidencia_04_Job.png)

En esta parte nos enfocamos en definir claramente qué hará el script del Glue Job. Aquí debemos indicar que el objetivo del código es limpiar los datos, renombrar columnas, normalizar formatos de fecha, convertir tipos de datos y generar particiones por año y mes, con el fin de mejorar el rendimiento en las consultas posteriores.

Una vez descrito esto, lo siguiente es configurar los parámetros que el job necesita para funcionar correctamente. En este punto debemos establecer, por ejemplo:

- **--SOURCE**: Archivo a consumir

- **--TARGET**: Archivo de salida

![Parámetros](/grupo05_nettalco/Lab_AWS/evidencias/Script_parametros.jpg)

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
![Evidencia Ejecucion](/grupo05_nettalco/Lab_AWS/evidencias/Script_ejecuccion_exitosa.jpg)



