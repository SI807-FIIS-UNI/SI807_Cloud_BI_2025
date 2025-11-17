from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    upper,
    lit,
    monotonically_increasing_id,
    regexp_replace,
)
from pyspark.sql.types import *

spark = SparkSession.builder.appName("normalize_to_silver").getOrCreate()

# ---------------------------
# CONFIG
# ---------------------------
bronze_bucket = "gs://grupo2-essalud-datalake/bronce"
silver_bucket = "gs://grupo2-essalud-datalake/plata"

files = {
    "diabetes": f"{bronze_bucket}/Diabetes.csv",
    "obesidad": f"{bronze_bucket}/Obesidad.csv",
    "hipertension": f"{bronze_bucket}/Hipertension.csv",
}

ubigeo_file = f"{bronze_bucket}/ubigeo.csv"

# ---------------------------
# SCHEMA
# ---------------------------
schema = StructType(
    [
        StructField("Fecha_corte", StringType(), True),
        StructField("Departamento", StringType(), True),
        StructField("Provincia", StringType(), True),
        StructField("Distrito", StringType(), True),
        StructField("Ubigeo", StringType(), True),
        StructField("Red", StringType(), True),
        StructField("Ipress", StringType(), True),
        StructField("ID_Paciente", StringType(), True),
        StructField("Edad_Paciente", IntegerType(), True),
        StructField("Sexo_Paciente", StringType(), True),
        StructField("Edad_Medico", IntegerType(), True),
        StructField("ID_Medico", StringType(), True),
        StructField("Cod_Diagnostico", StringType(), True),
        StructField("Diagnostico", StringType(), True),
        StructField("Area_Hospitalaria", StringType(), True),
        StructField("Servicio_Hospitalario", StringType(), True),
        StructField("Actividad_Hospitalaria", StringType(), True),
        StructField("Fecha_Muestra", StringType(), True),
        StructField("Fecha_Resultado_1", StringType(), True),
        StructField("Procedimiento_1", StringType(), True),
        StructField("Resultado_1", StringType(), True),
        StructField("Unidades_1", StringType(), True),
        StructField("Fecha_Resultado_2", StringType(), True),
        StructField("Procedimiento_2", StringType(), True),
        StructField("Resultado_2", StringType(), True),
        StructField("Unidades_2", StringType(), True),
    ]
)

# ---------------------------
# LECTURA DE LOS 3 CSV
# ---------------------------
dfs = []
for enfermedad, path in files.items():
    df = spark.read.option("header", "true").schema(schema).csv(path)

    # Normalizar strings
    for c in df.columns:
        df = df.withColumn(c, trim(col(c)))

    # Añadir columna cod_enfermedad según archivo
    if enfermedad == "diabetes":
        df = df.withColumn("grupo_enfermedad", lit("E1"))
    elif enfermedad == "obesidad":
        df = df.withColumn("grupo_enfermedad", lit("E2"))
    elif enfermedad == "hipertension":
        df = df.withColumn("grupo_enfermedad", lit("E3"))

    dfs.append(df)

df_all = (
    dfs[0]
    .unionByName(dfs[1], allowMissingColumns=True)
    .unionByName(dfs[2], allowMissingColumns=True)
)

# ---------------------------
# LECTURA UBIGEO
# ---------------------------
ubigeo = spark.read.option("header", "true").csv(ubigeo_file)
ubigeo = ubigeo.select(
    col("Ubigeo").alias("ubigeo"),
    col("Departamento").alias("departamento"),
    col("Provincia").alias("provincia"),
    col("Distrito").alias("distrito"),
    col("Poblacion").alias("poblacion"),
)

# ---------------------------
# TABLA PACIENTE
# ---------------------------
paciente = df_all.select(
    col("ID_Paciente").alias("id_paciente"),
    col("Edad_Paciente").alias("edad_paciente"),
    col("Sexo_Paciente").alias("sexo_paciente"),
).dropDuplicates()

paciente.write.mode("overwrite").parquet(f"{silver_bucket}/paciente")

# ---------------------------
# TABLA MEDICO
# ---------------------------
medico = df_all.select(
    col("ID_Medico").alias("id_medico"), col("Edad_Medico").alias("edad")
).dropDuplicates()

medico.write.mode("overwrite").parquet(f"{silver_bucket}/medico")

# ---------------------------
# TABLA CIE10
# ---------------------------
cie10 = df_all.select(
    col("cod_diagnostico").alias("cod_enfermedad"),
    col("Diagnostico").alias("des_enfermedad"),
    col("grupo_enfermedad").alias("grupo_enfermedad"),
).dropDuplicates()

cie10.write.mode("overwrite").parquet(f"{silver_bucket}/cie10")

# ---------------------------
# TABLA UBIGEO
# ---------------------------
ubigeo.write.mode("overwrite").parquet(f"{silver_bucket}/ubigeo")

# ---------------------------
# TABLA DIAGNOSTICO
# ---------------------------
diagnostico = df_all.select(
    col("cod_enfermedad"),
    col("ID_Paciente").alias("id_paciente"),
    col("Ubigeo").alias("ubigeo"),
    col("ID_Medico").alias("id_medico"),
    col("Servicio_Hospitalario").alias("servicio_hospitalario"),
    col("Actividad_Hospitalaria").alias("actividad_hospitalaria"),
    col("Fecha_Muestra").alias("fecha_muestra"),
)

diagnostico = diagnostico.withColumn("diagnostico_id", monotonically_increasing_id())


diagnostico.write.mode("overwrite").parquet(f"{silver_bucket}/diagnostico")

# ---------------------------
# TABLA PROCEDIMIENTO
# ---------------------------
proc1 = df_all.select(col("Procedimiento_1").alias("cod_procedimiento")).where(
    col("Procedimiento_1").isNotNull()
)

proc2 = df_all.select(col("Procedimiento_2").alias("cod_procedimiento")).where(
    col("Procedimiento_2").isNotNull()
)

procedimiento = (
    proc1.union(proc2)
    .dropDuplicates()
    .withColumn("procedimiento_id", monotonically_increasing_id())
)

procedimiento.write.mode("overwrite").parquet(f"{silver_bucket}/procedimiento")

# ---------------------------
# TABLA RESULTADO_PROCEDIMIENTO (PLATA)
# ---------------------------
res1 = df_all.select(
    col("Cod_Diagnostico").alias("cod_diagnostico"),
    col("Procedimiento_1").alias("cod_procedimiento"),
    col("Resultado_1").alias("resultado"),
    col("Unidades_1").alias("unidades"),
    col("Fecha_Resultado_1").alias("fecha_resultado"),
)

res2 = df_all.select(
    col("Cod_Diagnostico").alias("cod_diagnostico"),
    col("Procedimiento_2").alias("cod_procedimiento"),
    col("Resultado_2").alias("resultado"),
    col("Unidades_2").alias("unidades"),
    col("Fecha_Resultado_2").alias("fecha_resultado"),
)

resultado_proc = (
    res1.union(res2)
    .where(col("cod_procedimiento").isNotNull())
    .withColumn("resultado_id", monotonically_increasing_id())
)

resultado_proc.write.mode("overwrite").parquet(
    f"{silver_bucket}/resultado_procedimiento"
)

spark.stop()
