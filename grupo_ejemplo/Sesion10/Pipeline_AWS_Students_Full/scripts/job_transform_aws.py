
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
    .withColumnRenamed("Order ID", "order_id")
    .withColumnRenamed("Order Date", "order_date")
    .withColumnRenamed("Ship Date", "ship_date")
    .withColumnRenamed("Customer ID", "customer_id")
    .withColumnRenamed("Customer Name", "customer_name")
    .withColumnRenamed("Product ID", "product_id")
    .withColumnRenamed("Sub-Category", "sub_category")
    .withColumn("anio", F.year(F.to_date("order_date", "MM/dd/yyyy")))
    .withColumn("mes", F.date_format(F.to_date("order_date", "MM/dd/yyyy"), "MM"))
    .withColumn("margen", F.round(F.col("Profit") / F.when(F.col("Sales") != 0, F.col("Sales")).otherwise(1), 3))
)

(df2.write.mode("overwrite")
    .partitionBy("anio","mes")
    .parquet(args["TARGET"]))

print("✅ Transformación completada. Datos guardados en ruta de destino.")
