%spark2.pyspark
from pyspark.sql import functions as F
df = spark.table("tmp_master_limpia") 

print("--- BLOQUE 3: CARGA FINAL DE HECHOS ---")

# 1. Leemos las dimensiones para obtener los IDs
d_car = spark.table("db_cepreuni1.dim_carrera")
d_mod = spark.table("db_cepreuni1.dim_modalidad")
d_ins = spark.table("db_cepreuni1.dim_institucion")

# 2. Hacemos el Join (Cruce)
df_final = df.join(d_car, df.ESPECIALIDAD == d_car.nombre_carrera, "left") \
  .join(d_mod, df.MODO_INGRESO == d_mod.descripcion_modalidad, "left") \
  .join(d_ins, (df.COLEGIO == d_ins.nombre_colegio) & (df.geo_colegio == d_ins.id_geo_colegio), "left") \
  .select(
      df.id_tiempo, 
      df.IDHASH.alias("id_candidato"), 
      d_car.id_carrera, 
      d_ins.id_colegio, 
      d_mod.id_modalidad, 
      df.geo_domicilio.alias("id_geo_residencia"), 
      df.edad_calculada.alias("edad_postulacion"), 
      (df.ANIO_POSTULA - df.COLEGIO_ANIO_EGRESO).alias("anios_desde_egreso"), 
      df.CALIF_FINAL.alias("puntaje_final"), 
      df.flag_ingreso.alias("ingreso_flag"), 
      F.lit(1).alias("cantidad"), 
      df.ANIO_POSTULA.alias("anio")
  )

# 3. Escritura Final
print("Escribiendo datos en fact_admision...")
df_final.write.mode("overwrite").insertInto("db_cepreuni1.fact_admision")

print("🎉🎉 ¡PROYECTO TERMINADO! Base de datos db_cepreuni1 poblada.")