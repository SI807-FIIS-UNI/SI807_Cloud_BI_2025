%spark2.pyspark
from pyspark.sql import functions as F

print("--- 🏆 GENERANDO REPORTES FINAL (CURATED) ---")

# 1. Leemos la data limpia (Processed) de tu base de datos
df_fact = spark.table("db_cepreuni1.fact_admision")
df_carrera = spark.table("db_cepreuni1.dim_carrera")
df_tiempo = spark.table("db_cepreuni1.dim_tiempo")
df_col = spark.table("db_cepreuni1.dim_institucion")
df_geo = spark.table("db_cepreuni1.dim_geografia")

# --- REPORTE 1: KPI POR CARRERA ---
print("1. Calculando KPIs por Carrera...")

# Cruzamos Hechos + Tiempo + Carrera
df_rep_carrera = df_fact.alias("F") \
    .join(df_tiempo.alias("T"), F.col("F.id_tiempo") == F.col("T.id_tiempo")) \
    .join(df_carrera.alias("C"), F.col("F.id_carrera") == F.col("C.id_carrera")) \
    .groupBy(F.col("T.anio"), F.col("C.nombre_carrera")) \
    .agg(
        F.count("*").alias("total_postulantes"),
        F.sum("F.ingreso_flag").alias("total_ingresantes")
    ) \
    .withColumn("tasa_ingreso_pct", F.round((F.col("total_ingresantes") / F.col("total_postulantes")) * 100, 2)) \
    .orderBy(F.col("total_postulantes").desc())

# Guardamos en la tabla Hive Curated
df_rep_carrera.write.mode("overwrite").insertInto("db_cepreuni1.cur_reporte_carreras")


# --- REPORTE 2: RANKING DE COLEGIOS ---
print("2. Calculando Ranking de Colegios...")

# Cruzamos Hechos + Colegio + Geografia (del colegio)
# Nota: id_geo_colegio en dim_institucion conecta con dim_geografia
df_rep_colegio = df_fact.alias("F") \
    .join(df_col.alias("I"), F.col("F.id_colegio") == F.col("I.id_colegio")) \
    .join(df_geo.alias("G"), F.col("I.id_geo_colegio") == F.col("G.id_geo")) \
    .groupBy(F.col("I.nombre_colegio"), F.col("G.departamento")) \
    .agg(
        F.count("*").alias("total_postulantes"),
        F.sum("F.ingreso_flag").alias("total_ingresantes")
    ) \
    .orderBy(F.col("total_postulantes").desc())

# Guardamos en la tabla Hive Curated
df_rep_colegio.write.mode("overwrite").insertInto("db_cepreuni1.cur_reporte_colegios")

print("--- ✅ ¡REPORTES GENERADOS EXITOSAMENTE! ---")