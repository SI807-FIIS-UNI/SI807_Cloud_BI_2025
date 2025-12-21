%spark2.pyspark
# Recuperamos librerías y data del paso anterior
from pyspark.sql import functions as F
from pyspark.sql.window import Window
df = spark.table("tmp_master_limpia") 

print("--- BLOQUE 2: CARGA DE DIMENSIONES ---")

# 1. Carrera
print(" -> Procesando Carrera...")
w = Window.orderBy("ESPECIALIDAD")
df.select("ESPECIALIDAD").distinct().withColumn("id", F.row_number().over(w)) \
  .select(F.col("id"), F.col("ESPECIALIDAD").alias("nombre_carrera")) \
  .write.mode("overwrite").insertInto("db_cepreuni1.dim_carrera")

# 2. Modalidad
print(" -> Procesando Modalidad...")
w = Window.orderBy("MODO_INGRESO")
df.select("MODO_INGRESO").distinct().withColumn("id", F.row_number().over(w)) \
  .select(F.col("id"), F.col("MODO_INGRESO").alias("descripcion_modalidad")) \
  .write.mode("overwrite").insertInto("db_cepreuni1.dim_modalidad")

# 3. Tiempo
print(" -> Procesando Tiempo...")
df.select("id_tiempo", "ANIO_POSTULA", "CICLO_POSTULA").distinct() \
  .withColumn("desc", F.concat(F.lit("CICLO "), F.col("ANIO_POSTULA"), F.lit("-"), F.col("CICLO_POSTULA"))) \
  .select("id_tiempo", "ANIO_POSTULA", "CICLO_POSTULA", "desc") \
  .write.mode("overwrite").insertInto("db_cepreuni1.dim_tiempo")

# 4. Geografía
print(" -> Procesando Geografía...")
g1 = df.select(F.col("geo_domicilio").alias("id"), "DOMICILIO_DEPA", "DOMICILIO_PROV", "DOMICILIO_DIST")
g2 = df.select(F.col("geo_colegio").alias("id"), "COLEGIO_DEPA", "COLEGIO_PROV", "COLEGIO_DIST")
g1.union(g2).distinct().select("id", "DOMICILIO_DEPA", "DOMICILIO_PROV", "DOMICILIO_DIST", F.lit("PERU")) \
  .write.mode("overwrite").insertInto("db_cepreuni1.dim_geografia")

# 5. Institución
print(" -> Procesando Institución...")
w = Window.orderBy("COLEGIO")
df.select("COLEGIO", "geo_colegio").distinct().withColumn("id", F.row_number().over(w)) \
  .select(F.col("id"), F.col("COLEGIO").alias("nombre_colegio"), F.col("geo_colegio").alias("id_geo_colegio")) \
  .write.mode("overwrite").insertInto("db_cepreuni1.dim_institucion")

# 6. Candidato
print(" -> Procesando Candidato...")
df.select("IDHASH", "SEXO", "ANIO_NACIMIENTO", "NACIMIENTO_PAIS").distinct() \
  .select(F.col("IDHASH").alias("id_candidato"), F.col("SEXO"), F.col("ANIO_NACIMIENTO"), F.col("NACIMIENTO_PAIS").alias("pais_nacimiento")) \
  .write.mode("overwrite").insertInto("db_cepreuni1.dim_candidato")

print("✅ Bloque 2 Completado: Dimensiones cargadas.")