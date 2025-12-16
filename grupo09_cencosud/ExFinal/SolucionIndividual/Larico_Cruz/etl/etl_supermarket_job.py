import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, current_timestamp
from pyspark.sql.types import DoubleType, IntegerType

project_id = "$PROJECT_ID"
bucket_name = "$BUCKET_NAME"
dataset_name = "$DATASET_NAME"

spark = SparkSession.builder.appName("ETL-Supermarket").getOrCreate()

# A. LEER
df_raw = spark.read.option("header", True).option("inferSchema", True).csv(f"gs://{bucket_name}/raw/*.csv")

# B. TRANSFORMAR
df_curated = df_raw \\
    .withColumnRenamed("Invoice ID", "invoice_id") \\
    .withColumnRenamed("Customer type", "customer_type") \\
    .withColumnRenamed("Product line", "product_line") \\
    .withColumnRenamed("Unit price", "unit_price") \\
    .withColumnRenamed("Tax 5%", "tax_5_percent") \\
    .withColumnRenamed("Gross income", "gross_income") \\
    .withColumn("unit_price", col("unit_price").cast(DoubleType())) \\
    .withColumn("Quantity", col("Quantity").cast(IntegerType())) \\
    .withColumn("Sales", col("Sales").cast(DoubleType())) \\
    .withColumn("gross_income", col("gross_income").cast(DoubleType())) \\
    .withColumn("Rating", col("Rating").cast(DoubleType())) \\
    .withColumn("Branch", upper(trim(col("Branch")))) \\
    .withColumn("City", upper(trim(col("City")))) \\
    .withColumn("customer_type", upper(trim(col("customer_type")))) \\
    .withColumn("product_line", upper(trim(col("product_line")))) \\
    .withColumn("Payment", upper(trim(col("Payment")))) \\
    .na.drop(subset=["invoice_id"])

# C. ESCRIBIR
df_curated.write \\
    .format("bigquery") \\
    .option("table", f"{project_id}.{dataset_name}.tbl_supermarket_curated") \\
    .option("temporaryGcsBucket", bucket_name) \\
    .mode("overwrite") \\
    .save()
