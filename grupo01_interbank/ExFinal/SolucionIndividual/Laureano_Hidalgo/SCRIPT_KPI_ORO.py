from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum, when, round, lit

# Iniciar sesión de Spark
spark = SparkSession.builder.appName("KPIs_de_Vuelos").getOrCreate()

# Ruta del archivo CSV limpio en GCS
ruta_entrada = "gs://bronce_processed/flight_delay_clean_csv/*.csv"

# Leer el archivo limpio
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(ruta_entrada)
)

# Preparar datos (asegurar que las columnas estén bien tipadas)
df = (
    df.withColumn("arrdelay", col("arrdelay").cast("int"))
      .withColumn("depdelay", col("depdelay").cast("int"))
      .withColumn("cancelled", col("cancelled").cast("int"))
      .withColumn("distance", col("distance").cast("int"))
      .withColumn("taxiin", col("taxiin").cast("int"))
      .withColumn("taxiout", col("taxiout").cast("int"))
      .withColumn("weatherdelay", col("weatherdelay").cast("int"))
      .withColumn("carrierdelay", col("carrierdelay").cast("int"))
      .withColumn("lateaircraftdelay", col("lateaircraftdelay").cast("int"))
      .withColumn("diverted", col("diverted").cast("int"))
)

# 1) Demora promedio por aerolínea
demora_promedio_por_aerolinea = df.groupBy("uniquecarrier").agg(
    round(avg("arrdelay"), 2).alias("demora_promedio_llegada"),
    round(avg("depdelay"), 2).alias("demora_promedio_salida")
)

# 2) Porcentaje de vuelos cancelados por aerolínea
porcentaje_cancelados_por_aerolinea = df.groupBy("uniquecarrier").agg(
    (sum(when(col("cancelled") == 1, 1).otherwise(0)) / count("*") * 100).alias("porcentaje_cancelados")
)

# 3) Promedio de demora por aeropuerto (origen)
demora_promedio_por_origen = df.groupBy("origin").agg(
    round(avg("arrdelay"), 2).alias("demora_promedio_llegada_origen"),
    round(avg("depdelay"), 2).alias("demora_promedio_salida_origen")
)

# 4) Distancia promedio de vuelos por aerolínea
distancia_promedio_por_aerolinea = df.groupBy("uniquecarrier").agg(
    round(avg("distance"), 2).alias("distancia_promedio")
)

# 5) Tiempo promedio de taxi por ruta (origen y destino)
tiempo_promedio_taxi_por_ruta = df.groupBy("origin", "dest").agg(
    round(avg("taxiin"), 2).alias("taxi_in_promedio"),
    round(avg("taxiout"), 2).alias("taxi_out_promedio")
)

# 6) Demora promedio por día de la semana
demora_promedio_por_dia_semana = df.groupBy("dayofweek").agg(
    round(avg("arrdelay"), 2).alias("demora_promedio_llegada_dia"),
    round(avg("depdelay"), 2).alias("demora_promedio_salida_dia")
)

# 7) Número de vuelos desviados por aerolínea
cantidad_desviados_por_aerolinea = df.groupBy("uniquecarrier").agg(
    sum(when(col("diverted") == 1, 1).otherwise(0)).alias("cantidad_vuelos_desviados")
)

# Mostrar resultados de los KPIs
print("1) Demora promedio por aerolínea:")
demora_promedio_por_aerolinea.show()

print("2) Porcentaje de vuelos cancelados por aerolínea:")
porcentaje_cancelados_por_aerolinea.show()

print("3) Promedio de demora por aeropuerto (origen):")
demora_promedio_por_origen.show()

print("4) Distancia promedio de vuelos por aerolínea:")
distancia_promedio_por_aerolinea.show()

print("5) Tiempo promedio de taxi por ruta (origen y destino):")
tiempo_promedio_taxi_por_ruta.show()

print("6) Demora promedio por día de la semana:")
demora_promedio_por_dia_semana.show()

print("7) Número de vuelos desviados por aerolínea:")
cantidad_desviados_por_aerolinea.show()
