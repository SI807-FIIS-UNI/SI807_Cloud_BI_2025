%spark2.pyspark
from pyspark.sql import functions as F
from pyspark.sql.window import Window

print("--- BLOQUE 1: LECTURA Y LIMPIEZA ---")

# 1. Configuración para Hive
spark.conf.set("hive.exec.dynamic.partition", "true")
spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")

# 2. Lectura del CSV (Ruta 20212541J)
ruta_csv = "/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/raw"
df_raw = spark.read.option("header", "true").csv(ruta_csv)

# 3. Limpieza de Textos (Mayúsculas y espacios)
cols_texto = ["ESPECIALIDAD", "MODO_INGRESO", "SEXO", "COLEGIO", 
              "DOMICILIO_DEPA", "DOMICILIO_PROV", "DOMICILIO_DIST",
              "COLEGIO_DEPA", "COLEGIO_PROV", "COLEGIO_DIST"]

df_limpio = df_raw
for c in cols_texto:
    df_limpio = df_limpio.withColumn(c, F.upper(F.trim(F.col(c))))

# 4. Rellenar Nulos, Tipos de Dato y Columnas Nuevas
df_limpio = df_limpio.fillna({"CALIF_FINAL": "0.0", "INGRESO": "NO"}) \
    .withColumn("ANIO_POSTULA", F.col("ANIO_POSTULA").cast("int")) \
    .withColumn("CICLO_POSTULA", F.col("CICLO_POSTULA").cast("int")) \
    .withColumn("ANIO_NACIMIENTO", F.col("ANIO_NACIMIENTO").cast("int")) \
    .withColumn("COLEGIO_ANIO_EGRESO", F.col("COLEGIO_ANIO_EGRESO").cast("int")) \
    .withColumn("CALIF_FINAL", F.col("CALIF_FINAL").cast("double")) \
    .withColumn("id_tiempo", F.concat(F.col("ANIO_POSTULA"), F.col("CICLO_POSTULA")).cast("int")) \
    .withColumn("edad_calculada", (F.col("ANIO_POSTULA") - F.col("ANIO_NACIMIENTO")).cast("int")) \
    .withColumn("geo_domicilio", F.concat_ws("-", "DOMICILIO_DEPA", "DOMICILIO_PROV", "DOMICILIO_DIST")) \
    .withColumn("geo_colegio", F.concat_ws("-", "COLEGIO_DEPA", "COLEGIO_PROV", "COLEGIO_DIST")) \
    .withColumn("flag_ingreso", F.when(F.col("INGRESO") == "SI", 1).otherwise(0))

# 5. Guardar en Memoria y Vista Temporal (Clave para compartir entre bloques)
df_limpio.cache()
df_limpio.createOrReplaceTempView("tmp_master_limpia")

print("✅ Bloque 1 Completado. Registros listos: {}".format(df_limpio.count()))
df_limpio.show(3)