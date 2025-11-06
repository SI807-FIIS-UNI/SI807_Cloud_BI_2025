
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
