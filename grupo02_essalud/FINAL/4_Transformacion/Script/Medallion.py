#!/usr/bin/env python
# coding: utf-8

# # Transformación de Bronce a Plata

# In[31]:


spark.sparkContext.setLogLevel("ERROR")


# In[1]:


from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("ETL-Bronce-Plata") \
    .getOrCreate()

spark


# ## Cargando los datos del csv

# ### Diabetes

# In[2]:


df_bronce_diabetes = spark.read.csv(
    "gs://grupo2-essalud-datalake/bronce/Diabetes.csv",
    header=True,
    inferSchema=True,
    sep=";"
)

df_bronce_diabetes.show(5)
df_bronce_diabetes.printSchema()


# ### Hipertension

# In[3]:


df_bronce_hipertension = spark.read.csv(
    "gs://grupo2-essalud-datalake/bronce/Hipertension.csv",
    header=True,
    inferSchema=True,
    sep=";"
)

df_bronce_hipertension.show(5)
df_bronce_hipertension.printSchema()


# ### Obesidad

# In[4]:


df_bronce_obesidad = spark.read.csv(
    "gs://grupo2-essalud-datalake/bronce/Obesidad.csv",
    header=True,
    inferSchema=True,
    sep=";"
)

df_bronce_obesidad.show(5)
df_bronce_obesidad.printSchema()


# ## Carga de datos Bronce a Big Query

# In[5]:


print("Diabetes:", df_bronce_diabetes.count())
print("Hipertensión:", df_bronce_hipertension.count())
print("Obesidad:", df_bronce_obesidad.count())


# In[8]:


df_bronce_diabetes.write.format("bigquery") \
    .option("table", "grupo2-essalud.bronce.diabetes") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_bronce_hipertension.write.format("bigquery") \
    .option("table", "grupo2-essalud.bronce.hipertension") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_bronce_obesidad.write.format("bigquery") \
    .option("table", "grupo2-essalud.bronce.obesidad") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()


# ## Transformación de Datos de Bronce a Plata

# In[29]:


from pyspark.sql import functions as F
from pyspark.sql.window import Window

spark.sparkContext.setLogLevel("ERROR")


# ### Procedimiento

# In[15]:


df_union = (
    df_bronce_diabetes.select(F.col("PROCEDIMIENTO_1").alias("des_procedimiento"))
    .union(df_bronce_diabetes.select(F.col("PROCEDIMIENTO_2").alias("des_procedimiento")))
    .union(df_bronce_hipertension.select(F.col("PROCEDIMIENTO_1").alias("des_procedimiento")))
    .union(df_bronce_hipertension.select(F.col("PROCEDIMIENTO_2").alias("des_procedimiento")))
    .union(df_bronce_obesidad.select(F.col("PROCEDIMIENTO_1").alias("des_procedimiento")))
    .union(df_bronce_obesidad.select(F.col("PROCEDIMIENTO_2").alias("des_procedimiento")))
)

df_distinct = df_union.filter(F.col("des_procedimiento").isNotNull()).dropDuplicates()

df_plata_procedimiento = df_distinct.withColumn(
    "cod_procedimiento",
    F.row_number().over(Window.orderBy("des_procedimiento"))
)

df_plata_procedimiento.show(20, truncate=False)
df_plata_procedimiento.printSchema()


# ### Medico

# In[18]:


df_plata_medico = (
    df_bronce_diabetes.select(
        F.col("ID_MEDICO").alias("cod_medico"),
        F.col("EDAD_MEDICO").alias("edad_medico")
    )
    .union(
        df_bronce_hipertension.select(
            F.col("ID_MEDICO").alias("cod_medico"),
            F.col("EDAD_MEDICO").alias("edad_medico")
        )
    )
    .union(
        df_bronce_obesidad.select(
            F.col("ID_MEDICO").alias("cod_medico"),
            F.col("EDAD_MEDICO").alias("edad_medico")
        )
    )
    .dropDuplicates()
)

df_plata_medico.show(10)


# ### Paciente

# In[19]:


df_plata_paciente = (
    df_bronce_diabetes.select(
        F.col("ID_PACIENTE").alias("cod_paciente"),
        F.col("EDAD_PACIENTE").alias("edad_paciente"),
        F.col("SEXO_PACIENTE").alias("sexo_paciente")
    )
    .union(
        df_bronce_hipertension.select(
            F.col("ID_PACIENTE").alias("cod_paciente"),
            F.col("EDAD_PACIENTE").alias("edad_paciente"),
            F.col("SEXO_PACIENTE").alias("sexo_paciente")
        )
    )
    .union(
        df_bronce_obesidad.select(
            F.col("ID_PACIENTE").alias("cod_paciente"),
            F.col("EDAD_PACIENTE").alias("edad_paciente"),
            F.col("SEXO_PACIENTE").alias("sexo_paciente")
        )
    )
    .dropDuplicates()
)

df_plata_paciente.show(10)


# ### Enfermedad

# In[20]:


df_plata_enfermedad = (
    df_bronce_diabetes.select(
        F.col("COD_DIAG").alias("cod_enfermedad"),
        F.col("DIAGNOSTICO").alias("enfermedad"),
        F.lit("Diabetes").alias("grupo_enfermedad")
    )
    .union(
        df_bronce_hipertension.select(
            F.col("COD_DIAG").alias("cod_enfermedad"),
            F.col("DIAGNOSTICO").alias("enfermedad"),
            F.lit("Hipertension").alias("grupo_enfermedad")
        )
    )
    .union(
        df_bronce_obesidad.select(
            F.col("COD_DIAG").alias("cod_enfermedad"),
            F.col("DIAGNOSTICO").alias("enfermedad"),
            F.lit("Obesidad").alias("grupo_enfermedad")
        )
    )
    .dropDuplicates()
)

df_plata_enfermedad.show(10)


# ### Ubigeo

# In[21]:


df_plata_ubigeo = (
    df_bronce_diabetes.select(
        F.col("UBIGEO").alias("cod_ubigeo"),
        F.col("DEPARTAMENTO").alias("departamento"),
        F.col("PROVINCIA").alias("provincia"),
        F.col("DISTRITO").alias("distrito")
    )
    .union(
        df_bronce_hipertension.select(
            F.col("UBIGEO").alias("cod_ubigeo"),
            F.col("DEPARTAMENTO").alias("departamento"),
            F.col("PROVINCIA").alias("provincia"),
            F.col("DISTRITO").alias("distrito")
        )
    )
    .union(
        df_bronce_obesidad.select(
            F.col("UBIGEO").alias("cod_ubigeo"),
            F.col("DEPARTAMENTO").alias("departamento"),
            F.col("PROVINCIA").alias("provincia"),
            F.col("DISTRITO").alias("distrito")
        )
    )
    .dropDuplicates()
)

df_plata_ubigeo.show(10)


# ### Diagnostico y Resultado

# In[23]:


df_diagnostico_union = (
    df_bronce_diabetes.select(
        F.col("COD_DIAG").alias("cod_enfermedad"),
        F.col("ID_PACIENTE").alias("cod_paciente"),
        F.col("ID_MEDICO").alias("cod_medico"),
        F.col("UBIGEO").alias("cod_ubigeo"),
        F.col("SERVICIO_HOSPITALARIO").alias("servicio_hospitalario"),
        F.col("ACTIVIDAD_HOSPITALARIA").alias("actividad_hospitalaria"),
        F.col("FECHA_MUESTRA").alias("fecha_muestra")
    )
    .unionByName(
        df_bronce_hipertension.select(
            F.col("COD_DIAG").alias("cod_enfermedad"),
            F.col("ID_PACIENTE").alias("cod_paciente"),
            F.col("ID_MEDICO").alias("cod_medico"),
            F.col("UBIGEO").alias("cod_ubigeo"),
            F.col("SERVICIO_HOSPITALARIO").alias("servicio_hospitalario"),
            F.col("ACTIVIDAD_HOSPITALARIA").alias("actividad_hospitalaria"),
            F.col("FECHA_MUESTRA").alias("fecha_muestra")
        )
    )
    .unionByName(
        df_bronce_obesidad.select(
            F.col("COD_DIAG").alias("cod_enfermedad"),
            F.col("ID_PACIENTE").alias("cod_paciente"),
            F.col("ID_MEDICO").alias("cod_medico"),
            F.col("UBIGEO").alias("cod_ubigeo"),
            F.col("SERVICIO_HOSPITALARIO").alias("servicio_hospitalario"),
            F.col("ACTIVIDAD_HOSPITALARIA").alias("actividad_hospitalaria"),
            F.col("FECHA_MUESTRA").alias("fecha_muestra")
        )
    )
)

# Window para ID incremental
w = Window.orderBy(F.monotonically_increasing_id())

df_plata_diagnostico = df_diagnostico_union.withColumn(
    "cod_diagnostico",
    F.row_number().over(w)
)

df_plata_diagnostico = df_plata_diagnostico.select(
    "cod_diagnostico",
    "cod_enfermedad",
    "cod_paciente",
    "cod_medico",
    "cod_ubigeo",
    "servicio_hospitalario",
    "actividad_hospitalaria",
    "fecha_muestra"
)

df_plata_diagnostico.show(10)
df_plata_diagnostico.printSchema()


# In[26]:


# DIABETES
df_join_diabetes = (
    df_bronce_diabetes.join(
        df_plata_diagnostico,
        (
            (df_bronce_diabetes.COD_DIAG == df_plata_diagnostico.cod_enfermedad) &
            (df_bronce_diabetes.ID_PACIENTE == df_plata_diagnostico.cod_paciente) &
            (df_bronce_diabetes.ID_MEDICO == df_plata_diagnostico.cod_medico) &
            (df_bronce_diabetes.UBIGEO == df_plata_diagnostico.cod_ubigeo) &
            (df_bronce_diabetes.FECHA_MUESTRA == df_plata_diagnostico.fecha_muestra)
        ),
        "inner"
    )
    .select(
        "cod_diagnostico",
        "PROCEDIMIENTO_1", "RESULTADO_1", "UNIDADES_1", "FEC_RESULTADO_1",
        "PROCEDIMIENTO_2", "RESULTADO_2", "UNIDADES_2", "FEC_RESULTADO_2"
    )
)

# HIPERTENSION
df_join_hipertension = (
    df_bronce_hipertension.join(
        df_plata_diagnostico,
        (
            (df_bronce_hipertension.COD_DIAG == df_plata_diagnostico.cod_enfermedad) &
            (df_bronce_hipertension.ID_PACIENTE == df_plata_diagnostico.cod_paciente) &
            (df_bronce_hipertension.ID_MEDICO == df_plata_diagnostico.cod_medico) &
            (df_bronce_hipertension.UBIGEO == df_plata_diagnostico.cod_ubigeo) &
            (df_bronce_hipertension.FECHA_MUESTRA == df_plata_diagnostico.fecha_muestra)
        ),
        "inner"
    )
    .select(
        "cod_diagnostico",
        "PROCEDIMIENTO_1", "RESULTADO_1", "UNIDADES_1", "FEC_RESULTADO_1",
        "PROCEDIMIENTO_2", "RESULTADO_2", "UNIDADES_2", "FEC_RESULTADO_2"
    )
)

# OBESIDAD
df_join_obesidad = (
    df_bronce_obesidad.join(
        df_plata_diagnostico,
        (
            (df_bronce_obesidad.COD_DIAG == df_plata_diagnostico.cod_enfermedad) &
            (df_bronce_obesidad.ID_PACIENTE == df_plata_diagnostico.cod_paciente) &
            (df_bronce_obesidad.ID_MEDICO == df_plata_diagnostico.cod_medico) &
            (df_bronce_obesidad.UBIGEO == df_plata_diagnostico.cod_ubigeo) &
            (df_bronce_obesidad.FECHA_MUESTRA == df_plata_diagnostico.fecha_muestra)
        ),
        "inner"
    )
    .select(
        "cod_diagnostico",
        "PROCEDIMIENTO_1", "RESULTADO_1", "UNIDADES_1", "FEC_RESULTADO_1",
        "PROCEDIMIENTO_2", "RESULTADO_2", "UNIDADES_2", "FEC_RESULTADO_2"
    )
)


df_join_all = df_join_diabetes.unionByName(df_join_hipertension).unionByName(df_join_obesidad)

df_proc_1 = df_join_all.select(
    F.col("cod_diagnostico"),
    F.col("PROCEDIMIENTO_1").alias("des_procedimiento"),
    F.col("RESULTADO_1").alias("resultado"),
    F.col("UNIDADES_1").alias("unidades"),
    F.col("FEC_RESULTADO_1").alias("fecha_resultado")
).filter(F.col("des_procedimiento").isNotNull())

df_proc_2 = df_join_all.select(
    F.col("cod_diagnostico"),
    F.col("PROCEDIMIENTO_2").alias("des_procedimiento"),
    F.col("RESULTADO_2").alias("resultado"),
    F.col("UNIDADES_2").alias("unidades"),
    F.col("FEC_RESULTADO_2").alias("fecha_resultado")
).filter(F.col("des_procedimiento").isNotNull())

df_procedimientos = df_proc_1.unionByName(df_proc_2)

df_plata_resultado_procedimiento = df_procedimientos.join(
    df_plata_procedimiento,
    df_procedimientos.des_procedimiento == df_plata_procedimiento.des_procedimiento,
    "left"
).select(
    "cod_procedimiento",
    "cod_diagnostico",
    "resultado",
    "unidades",
    "fecha_resultado"
)

df_plata_resultado_procedimiento.show(10)


# In[32]:


df_plata_resultado_procedimiento.orderBy("cod_diagnostico").show(10)
df_plata_resultado_procedimiento.printSchema()


# ### Ajuste de Fechas

# In[33]:


from pyspark.sql.functions import to_date, col

df_plata_resultado_procedimiento = df_plata_resultado_procedimiento.withColumn(
    "fecha_resultado",
    to_date(col("fecha_resultado").cast("string"), "yyyyMMdd")
)

df_plata_diagnostico = df_plata_diagnostico.withColumn(
    "fecha_muestra",
    to_date(col("fecha_muestra").cast("string"), "yyyyMMdd")
)


# ## Ahora subiendo a BigQuery los datos Plata

# In[36]:


df_plata_procedimiento.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.procedimiento") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_plata_medico.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.medico") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_plata_paciente.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.paciente") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_plata_enfermedad.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.enfermedad") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_plata_ubigeo.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.ubigeo") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_plata_diagnostico.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.diagnostico") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_plata_resultado_procedimiento.write.format("bigquery") \
    .option("table", "grupo2-essalud.plata.resultado_procedimiento") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()


# ## Guardando los Plata como csv

# In[37]:


get_ipython().system('pip install google-cloud-storage')


# In[40]:


from google.cloud import storage

def rename_gcs_file(bucket_name, source_path, destination_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    source_blob = bucket.blob(source_path)
    bucket.copy_blob(source_blob, bucket, destination_path)
    source_blob.delete()
    print(f"Renombrado: {source_path}  →  {destination_path}")

def export_single_csv(df, bucket, folder, final_filename):
    output_path = f"gs://{bucket}/{folder}/temp_export"

    df.coalesce(1).write \
        .option("header", "true") \
        .mode("overwrite") \
        .csv(output_path)

    client = storage.Client()
    bucket_ref = client.bucket(bucket)
    blobs = list(bucket_ref.list_blobs(prefix=f"{folder}/temp_export/"))

    part_file = None
    for b in blobs:
        if b.name.endswith(".csv"):
            part_file = b.name
            break

    if part_file is None:
        raise Exception("No se encontró el archivo CSV exportado.")

    final_path = f"{folder}/{final_filename}"
    rename_gcs_file(bucket, part_file, final_path)

    for b in blobs:
        try:
            b.delete()
        except Exception:
            pass  # si ya fue borrado, seguimos normal

    print(f"Archivo final generado: gs://{bucket}/{final_path}")


# In[41]:


bucket = "grupo2-essalud-datalake"

export_single_csv(df_plata_procedimiento, bucket, "plata/procedimiento", "procedimiento.csv")
export_single_csv(df_plata_medico, bucket, "plata/medico", "medico.csv")
export_single_csv(df_plata_paciente, bucket, "plata/paciente", "paciente.csv")
export_single_csv(df_plata_enfermedad, bucket, "plata/enfermedad", "enfermedad.csv")
export_single_csv(df_plata_ubigeo, bucket, "plata/ubigeo", "ubigeo.csv")
export_single_csv(df_plata_diagnostico, bucket, "plata/diagnostico", "diagnostico.csv")
export_single_csv(df_plata_resultado_procedimiento, bucket, "plata/resultado_procedimiento", "resultado_procedimiento.csv")


# # De Plata a Oro

# In[43]:


df_plata_procedimiento.printSchema()
df_plata_medico.printSchema()
df_plata_paciente.printSchema()
df_plata_enfermedad.printSchema()
df_plata_ubigeo.printSchema()
df_plata_diagnostico.printSchema()
df_plata_resultado_procedimiento.printSchema()


# ### Dim_Tiempo

# In[45]:


from pyspark.sql import functions as F

df_fechas = (
    df_plata_diagnostico.select(F.col("fecha_muestra").alias("fecha"))
    .union(df_plata_resultado_procedimiento.select(F.col("fecha_resultado").alias("fecha")))
    .dropna()
    .distinct()
)

df_oro_tiempo = (
    df_fechas
    .withColumn("SK_Tiempo", F.monotonically_increasing_id())
    .withColumn("año", F.year("fecha"))
    .withColumn("mes", F.month("fecha"))
    .withColumn("dia", F.dayofmonth("fecha"))
    .withColumn("semana", F.weekofyear("fecha"))
    .withColumn("trimestre", F.quarter("fecha"))
    .withColumn("fin_de_mes", F.last_day("fecha"))
)


# ### Dim_Paciente

# In[46]:


df_oro_paciente = (
    df_plata_paciente
    .withColumn("SK_Paciente", F.monotonically_increasing_id())
    .withColumn(
        "grupo_etario",
        F.when(F.col("edad_paciente") < 18, "Menor")
         .when(F.col("edad_paciente") < 60, "Adulto")
         .otherwise("Adulto Mayor")
    )
)


# ### Dim_Enfermedad

# In[49]:


df_oro_enfermedad = (
    df_plata_enfermedad
    .withColumn("SK_Enfermedad", F.monotonically_increasing_id())
    .withColumnRenamed("enfermedad", "des_enfermedad")
)


# ### Dim_Ubigeo

# In[50]:


df_oro_ubigeo = (
    df_plata_ubigeo
    .withColumn("SK_Ubigeo", F.monotonically_increasing_id())
    .withColumnRenamed("cod_ubigeo", "ubigeo")
    .withColumn("macroRegion",
                F.when(F.col("departamento").isin("LIMA", "CALLAO"), "Costa Central")
                 .otherwise("Otra"))
)


# ### Dim_Procedimiento

# In[55]:


df_resul_enriched = (
    df_plata_resultado_procedimiento
        .join(
            df_plata_procedimiento,
            "cod_procedimiento",
            "left"
        )
)

df_oro_procedimiento = (
    df_resul_enriched
        .select("des_procedimiento", "unidades")
        .distinct()
        .withColumn("SK_Procedimiento", F.monotonically_increasing_id())
)


# ### Fact_Diagnostico

# In[59]:


# Join con dimensiones para traer SKs
df_oro_fact_diagnostico = (
    df_plata_diagnostico
    # Tiempo
    .join(df_oro_tiempo.select("fecha", "SK_Tiempo"),
          df_plata_diagnostico.fecha_muestra == df_oro_tiempo.fecha,
          "left")
    # Paciente
    .join(df_oro_paciente.select("cod_paciente", "SK_Paciente"),
          "cod_paciente",
          "left")
    # Enfermedad
    .join(df_oro_enfermedad.select("cod_enfermedad", "SK_Enfermedad"),
          "cod_enfermedad",
          "left")
    # Ubigeo
    .join(df_oro_ubigeo.select("ubigeo", "SK_Ubigeo"),
          df_plata_diagnostico.cod_ubigeo == df_oro_ubigeo.ubigeo,
          "left")
    .withColumn("SK_Diagnostico", F.monotonically_increasing_id())
    .select(
        F.col("cod_diagnostico"),
        "SK_Diagnostico",
        "SK_Tiempo",
        "SK_Paciente",
        "SK_Enfermedad",
        "SK_Ubigeo",
        "servicio_hospitalario",
        "actividad_hospitalaria"
    )
)


# ### Fact_Resultado

# In[61]:


df_oro_fact_resultado = (
    df_resul_enriched
        .join(
            df_oro_procedimiento,
            ["des_procedimiento", "unidades"],
            "left"
        )
        .join(
            df_oro_tiempo.select("fecha", "SK_Tiempo"),
            df_resul_enriched.fecha_resultado == F.col("fecha"),
            "left"
        )
        .join(
            df_oro_fact_diagnostico.select("SK_Diagnostico", "cod_diagnostico"),
            "cod_diagnostico",
            "left"
        )
        .withColumn("SK_Resultado", F.monotonically_increasing_id())
        .select(
            "SK_Resultado",
            "SK_Tiempo",
            "SK_Diagnostico",
            F.col("resultado").alias("medida_resultado")
        )
)


# ## Carga a BigQuery

# In[62]:


df_oro_tiempo.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.dim_tiempo") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_oro_paciente.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.dim_paciente") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_oro_ubigeo.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.dim_ubigeo") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_oro_procedimiento.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.dim_procedimiento") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_oro_fact_diagnostico.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.fact_diagnostico") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()

df_oro_fact_resultado.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.fact_resultado") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()


# In[64]:


df_oro_enfermedad.write.format("bigquery") \
    .option("table", "grupo2-essalud.oro.dim_enfermedad") \
    .option("temporaryGcsBucket", "grupo2-essalud-datalake") \
    .mode("overwrite") \
    .save()


# ## Guardando los Oro como csv

# In[63]:


bucket = "grupo2-essalud-datalake"

export_single_csv(df_oro_tiempo, bucket, "oro/dim_tiempo", "dim_tiempo.csv")
export_single_csv(df_oro_paciente, bucket, "oro/dim_paciente", "dim_paciente.csv")
export_single_csv(df_oro_ubigeo, bucket, "oro/dim_ubigeo", "dim_ubigeo.csv")
export_single_csv(df_oro_procedimiento, bucket, "oro/dim_procedimiento", "dim_procedimiento.csv")
export_single_csv(df_oro_fact_diagnostico, bucket, "oro/fact_diagnostico", "fact_diagnostico.csv")
export_single_csv(df_oro_fact_resultado, bucket, "oro/fact_resultado", "fact_resultado.csv")


# In[65]:


export_single_csv(df_oro_enfermedad, bucket, "oro/dim_enfermedad", "dim_enfermedad.csv")

