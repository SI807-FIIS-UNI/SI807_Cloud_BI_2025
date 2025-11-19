import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import year, month, to_date, col

args = getResolvedOptions(sys.argv, ['SOURCE', 'TARGET'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

df = spark.read.option("header", True).csv(args['SOURCE'])

# Limpiar columna innecesaria
df = df.drop("unnamed:_22")

# Convertir columna 'date' a tipo fecha
df = df.withColumn("order_date", to_date(col("date"), "yyyy-MM-dd"))

# Extraer año y mes para particionar
df = df.withColumn("year", year("order_date"))
df = df.withColumn("month", month("order_date"))

# Guardar en formato Parquet particionado
df.write.mode("overwrite").partitionBy("year", "month").parquet(args['TARGET'])

print("✅ Transformación completada. Datos guardados en ruta de destino.")