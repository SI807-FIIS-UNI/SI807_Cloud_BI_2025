import sys
import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.functions import col, to_date
from google.cloud import storage

# Configuración de Logging para Cloud Composer / Dataproc
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constantes de Configuración
BUCKET_DATALAKE = "grupo2-essalud-datalake"
PROJECT_ID = "grupo2-essalud"
TEMP_BUCKET = "grupo2-essalud-datalake"  # Usado por el conector de BigQuery


def get_spark_session():
    """Inicia o recupera la sesión de Spark."""
    return SparkSession.builder.appName("ETL-Essalud-Master").getOrCreate()


def write_to_bigquery(df, table_id, mode="overwrite"):
    """Escribe un DataFrame en BigQuery."""
    logger.info(f"Escribiendo en BigQuery tabla: {table_id}")
    df.write.format("bigquery").option("table", table_id).option(
        "temporaryGcsBucket", TEMP_BUCKET
    ).mode(mode).save()


def export_single_csv(df, bucket_name, folder, final_filename):
    """
    Exporta un DF como un único archivo CSV renombrándolo en GCS.
    Nota: Esto es costoso para grandes volúmenes, usar con cuidado.
    """
    logger.info(f"Exportando CSV: gs://{bucket_name}/{folder}/{final_filename}")

    output_path = f"gs://{bucket_name}/{folder}/temp_export"

    # Escribir como un solo archivo particionado
    df.coalesce(1).write.option("header", "true").mode("overwrite").csv(output_path)

    # Lógica para renombrar usando la API de GCS (Python Client)
    client = storage.Client()
    bucket_ref = client.bucket(bucket_name)
    blobs = list(bucket_ref.list_blobs(prefix=f"{folder}/temp_export/"))

    part_file = None
    for b in blobs:
        if b.name.endswith(".csv"):
            part_file = b.name
            break

    if part_file is None:
        logger.warning(f"No se generó CSV para {final_filename}")
        return

    # Copiar (Renombrar) y Limpiar
    source_blob = bucket_ref.blob(part_file)
    destination_path = f"{folder}/{final_filename}"
    bucket_ref.copy_blob(source_blob, bucket_ref, destination_path)

    # Eliminar temporales
    for b in blobs:
        try:
            b.delete()
        except Exception:
            pass

    logger.info(
        f"Archivo final generado exitosamente: gs://{bucket_name}/{destination_path}"
    )


def process_etl(spark):
    # ==========================================
    # 1. CAPA BRONCE (Ingesta y Carga Inicial)
    # ==========================================
    logger.info("Inicio Procesamiento Capa BRONCE")

    # Lectura
    df_bronce_diabetes = spark.read.csv(
        f"gs://{BUCKET_DATALAKE}/bronce/Diabetes.csv",
        header=True,
        inferSchema=True,
        sep=";",
    )
    df_bronce_hipertension = spark.read.csv(
        f"gs://{BUCKET_DATALAKE}/bronce/Hipertension.csv",
        header=True,
        inferSchema=True,
        sep=";",
    )
    df_bronce_obesidad = spark.read.csv(
        f"gs://{BUCKET_DATALAKE}/bronce/Obesidad.csv",
        header=True,
        inferSchema=True,
        sep=";",
    )

    # Escritura a BQ (Bronce)
    write_to_bigquery(df_bronce_diabetes, f"{PROJECT_ID}.bronce.diabetes")
    write_to_bigquery(df_bronce_hipertension, f"{PROJECT_ID}.bronce.hipertension")
    write_to_bigquery(df_bronce_obesidad, f"{PROJECT_ID}.bronce.obesidad")

    # ==========================================
    # 2. CAPA PLATA (Transformación)
    # ==========================================
    logger.info("Inicio Procesamiento Capa PLATA")

    # --- Dimensión: Procedimiento ---
    df_union_proc = (
        df_bronce_diabetes.select(F.col("PROCEDIMIENTO_1").alias("des_procedimiento"))
        .union(
            df_bronce_diabetes.select(
                F.col("PROCEDIMIENTO_2").alias("des_procedimiento")
            )
        )
        .union(
            df_bronce_hipertension.select(
                F.col("PROCEDIMIENTO_1").alias("des_procedimiento")
            )
        )
        .union(
            df_bronce_hipertension.select(
                F.col("PROCEDIMIENTO_2").alias("des_procedimiento")
            )
        )
        .union(
            df_bronce_obesidad.select(
                F.col("PROCEDIMIENTO_1").alias("des_procedimiento")
            )
        )
        .union(
            df_bronce_obesidad.select(
                F.col("PROCEDIMIENTO_2").alias("des_procedimiento")
            )
        )
    )

    df_plata_procedimiento = (
        df_union_proc.filter(F.col("des_procedimiento").isNotNull())
        .dropDuplicates()
        .withColumn(
            "cod_procedimiento",
            F.row_number().over(Window.orderBy("des_procedimiento")),
        )
    )

    # --- Dimensión: Medico ---
    df_plata_medico = (
        df_bronce_diabetes.select(
            col("ID_MEDICO").alias("cod_medico"),
            col("EDAD_MEDICO").alias("edad_medico"),
        )
        .union(
            df_bronce_hipertension.select(
                col("ID_MEDICO").alias("cod_medico"),
                col("EDAD_MEDICO").alias("edad_medico"),
            )
        )
        .union(
            df_bronce_obesidad.select(
                col("ID_MEDICO").alias("cod_medico"),
                col("EDAD_MEDICO").alias("edad_medico"),
            )
        )
        .dropDuplicates()
    )

    # --- Dimensión: Paciente ---
    df_plata_paciente = (
        df_bronce_diabetes.select(
            col("ID_PACIENTE").alias("cod_paciente"),
            col("EDAD_PACIENTE").alias("edad_paciente"),
            col("SEXO_PACIENTE").alias("sexo_paciente"),
        )
        .union(
            df_bronce_hipertension.select(
                col("ID_PACIENTE").alias("cod_paciente"),
                col("EDAD_PACIENTE").alias("edad_paciente"),
                col("SEXO_PACIENTE").alias("sexo_paciente"),
            )
        )
        .union(
            df_bronce_obesidad.select(
                col("ID_PACIENTE").alias("cod_paciente"),
                col("EDAD_PACIENTE").alias("edad_paciente"),
                col("SEXO_PACIENTE").alias("sexo_paciente"),
            )
        )
        .dropDuplicates()
    )

    # --- Dimensión: Enfermedad ---
    df_plata_enfermedad = (
        df_bronce_diabetes.select(
            col("COD_DIAG").alias("cod_enfermedad"),
            col("DIAGNOSTICO").alias("enfermedad"),
            F.lit("Diabetes").alias("grupo_enfermedad"),
        )
        .union(
            df_bronce_hipertension.select(
                col("COD_DIAG").alias("cod_enfermedad"),
                col("DIAGNOSTICO").alias("enfermedad"),
                F.lit("Hipertension").alias("grupo_enfermedad"),
            )
        )
        .union(
            df_bronce_obesidad.select(
                col("COD_DIAG").alias("cod_enfermedad"),
                col("DIAGNOSTICO").alias("enfermedad"),
                F.lit("Obesidad").alias("grupo_enfermedad"),
            )
        )
        .dropDuplicates()
    )

    # --- Dimensión: Ubigeo ---
    cols_ubigeo = [
        col("UBIGEO").alias("cod_ubigeo"),
        col("DEPARTAMENTO").alias("departamento"),
        col("PROVINCIA").alias("provincia"),
        col("DISTRITO").alias("distrito"),
    ]
    df_plata_ubigeo = (
        df_bronce_diabetes.select(*cols_ubigeo)
        .union(df_bronce_hipertension.select(*cols_ubigeo))
        .union(df_bronce_obesidad.select(*cols_ubigeo))
        .dropDuplicates()
    )

    # --- Tabla: Diagnostico (Intermedia) ---
    cols_diag = [
        col("COD_DIAG").alias("cod_enfermedad"),
        col("ID_PACIENTE").alias("cod_paciente"),
        col("ID_MEDICO").alias("cod_medico"),
        col("UBIGEO").alias("cod_ubigeo"),
        col("SERVICIO_HOSPITALARIO").alias("servicio_hospitalario"),
        col("ACTIVIDAD_HOSPITALARIA").alias("actividad_hospitalaria"),
        col("FECHA_MUESTRA").alias("fecha_muestra"),
    ]

    df_diagnostico_union = (
        df_bronce_diabetes.select(*cols_diag)
        .unionByName(df_bronce_hipertension.select(*cols_diag))
        .unionByName(df_bronce_obesidad.select(*cols_diag))
    )

    w_id = Window.orderBy(F.monotonically_increasing_id())
    df_plata_diagnostico = df_diagnostico_union.withColumn(
        "cod_diagnostico", F.row_number().over(w_id)
    ).withColumn(
        "fecha_muestra", to_date(col("fecha_muestra").cast("string"), "yyyyMMdd")
    )

    # --- Tabla: Resultado Procedimiento (Join complejo) ---
    # Helper interno para evitar repetir lógica de join
    def join_and_extract(df_source, df_diag):
        return df_source.join(
            df_diag,
            (
                (df_source.COD_DIAG == df_diag.cod_enfermedad)
                & (df_source.ID_PACIENTE == df_diag.cod_paciente)
                & (df_source.ID_MEDICO == df_diag.cod_medico)
                & (df_source.UBIGEO == df_diag.cod_ubigeo)
                & (
                    df_source.FECHA_MUESTRA
                    == F.date_format(df_diag.fecha_muestra, "yyyyMMdd").cast("int")
                )  # Ajuste de tipo para match
            ),
            "inner",
        ).select(
            "cod_diagnostico",
            "PROCEDIMIENTO_1",
            "RESULTADO_1",
            "UNIDADES_1",
            "FEC_RESULTADO_1",
            "PROCEDIMIENTO_2",
            "RESULTADO_2",
            "UNIDADES_2",
            "FEC_RESULTADO_2",
        )

    df_join_all = (
        join_and_extract(df_bronce_diabetes, df_plata_diagnostico)
        .unionByName(join_and_extract(df_bronce_hipertension, df_plata_diagnostico))
        .unionByName(join_and_extract(df_bronce_obesidad, df_plata_diagnostico))
    )

    df_proc_unpivot = (
        df_join_all.select(
            "cod_diagnostico",
            col("PROCEDIMIENTO_1").alias("des_procedimiento"),
            col("RESULTADO_1").alias("resultado"),
            col("UNIDADES_1").alias("unidades"),
            col("FEC_RESULTADO_1").alias("fecha_resultado"),
        )
        .filter(col("des_procedimiento").isNotNull())
        .unionByName(
            df_join_all.select(
                "cod_diagnostico",
                col("PROCEDIMIENTO_2").alias("des_procedimiento"),
                col("RESULTADO_2").alias("resultado"),
                col("UNIDADES_2").alias("unidades"),
                col("FEC_RESULTADO_2").alias("fecha_resultado"),
            ).filter(col("des_procedimiento").isNotNull())
        )
    )

    df_plata_resultado_procedimiento = (
        df_proc_unpivot.join(df_plata_procedimiento, "des_procedimiento", "left")
        .select(
            "cod_procedimiento",
            "cod_diagnostico",
            "resultado",
            "unidades",
            "fecha_resultado",
        )
        .withColumn(
            "fecha_resultado",
            to_date(col("fecha_resultado").cast("string"), "yyyyMMdd"),
        )
    )

    # Escritura a BQ (Plata)
    logger.info("Escribiendo datos PLATA en BigQuery...")
    write_to_bigquery(df_plata_procedimiento, f"{PROJECT_ID}.plata.procedimiento")
    write_to_bigquery(df_plata_medico, f"{PROJECT_ID}.plata.medico")
    write_to_bigquery(df_plata_paciente, f"{PROJECT_ID}.plata.paciente")
    write_to_bigquery(df_plata_enfermedad, f"{PROJECT_ID}.plata.enfermedad")
    write_to_bigquery(df_plata_ubigeo, f"{PROJECT_ID}.plata.ubigeo")
    write_to_bigquery(df_plata_diagnostico, f"{PROJECT_ID}.plata.diagnostico")
    write_to_bigquery(
        df_plata_resultado_procedimiento, f"{PROJECT_ID}.plata.resultado_procedimiento"
    )

    # Exportación CSV (Plata)
    logger.info("Exportando CSVs PLATA a GCS...")
    export_single_csv(
        df_plata_procedimiento,
        BUCKET_DATALAKE,
        "plata/procedimiento",
        "procedimiento.csv",
    )
    export_single_csv(df_plata_medico, BUCKET_DATALAKE, "plata/medico", "medico.csv")
    export_single_csv(
        df_plata_paciente, BUCKET_DATALAKE, "plata/paciente", "paciente.csv"
    )
    export_single_csv(
        df_plata_enfermedad, BUCKET_DATALAKE, "plata/enfermedad", "enfermedad.csv"
    )
    export_single_csv(df_plata_ubigeo, BUCKET_DATALAKE, "plata/ubigeo", "ubigeo.csv")
    export_single_csv(
        df_plata_diagnostico, BUCKET_DATALAKE, "plata/diagnostico", "diagnostico.csv"
    )
    export_single_csv(
        df_plata_resultado_procedimiento,
        BUCKET_DATALAKE,
        "plata/resultado_procedimiento",
        "resultado_procedimiento.csv",
    )

    # ==========================================
    # 3. CAPA ORO (Modelado Dimensional)
    # ==========================================
    logger.info("Inicio Procesamiento Capa ORO")

    # Dim_Tiempo
    df_fechas = (
        df_plata_diagnostico.select(col("fecha_muestra").alias("fecha"))
        .union(
            df_plata_resultado_procedimiento.select(
                col("fecha_resultado").alias("fecha")
            )
        )
        .dropna()
        .distinct()
    )

    df_oro_tiempo = (
        df_fechas.withColumn("SK_Tiempo", F.monotonically_increasing_id())
        .withColumn("año", F.year("fecha"))
        .withColumn("mes", F.month("fecha"))
        .withColumn("dia", F.dayofmonth("fecha"))
        .withColumn("semana", F.weekofyear("fecha"))
        .withColumn("trimestre", F.quarter("fecha"))
        .withColumn("fin_de_mes", F.last_day("fecha"))
    )

    # Dim_Paciente
    df_oro_paciente = df_plata_paciente.withColumn(
        "SK_Paciente", F.monotonically_increasing_id()
    ).withColumn(
        "grupo_etario",
        F.when(col("edad_paciente") < 18, "Menor")
        .when(col("edad_paciente") < 60, "Adulto")
        .otherwise("Adulto Mayor"),
    )

    # Dim_Enfermedad
    df_oro_enfermedad = df_plata_enfermedad.withColumn(
        "SK_Enfermedad", F.monotonically_increasing_id()
    ).withColumnRenamed("enfermedad", "des_enfermedad")

    # Dim_Ubigeo
    df_oro_ubigeo = (
        df_plata_ubigeo.withColumn("SK_Ubigeo", F.monotonically_increasing_id())
        .withColumnRenamed("cod_ubigeo", "ubigeo")
        .withColumn(
            "macroRegion",
            F.when(
                col("departamento").isin("LIMA", "CALLAO"), "Costa Central"
            ).otherwise("Otra"),
        )
    )

    # Dim_Procedimiento
    df_resul_enriched = df_plata_resultado_procedimiento.join(
        df_plata_procedimiento, "cod_procedimiento", "left"
    )

    df_oro_procedimiento = (
        df_resul_enriched.select("des_procedimiento", "unidades")
        .distinct()
        .withColumn("SK_Procedimiento", F.monotonically_increasing_id())
    )

    # Fact_Diagnostico
    df_oro_fact_diagnostico = (
        df_plata_diagnostico.join(
            df_oro_tiempo.select("fecha", "SK_Tiempo"),
            df_plata_diagnostico.fecha_muestra == df_oro_tiempo.fecha,
            "left",
        )
        .join(
            df_oro_paciente.select("cod_paciente", "SK_Paciente"),
            "cod_paciente",
            "left",
        )
        .join(
            df_oro_enfermedad.select("cod_enfermedad", "SK_Enfermedad"),
            "cod_enfermedad",
            "left",
        )
        .join(
            df_oro_ubigeo.select("ubigeo", "SK_Ubigeo"),
            df_plata_diagnostico.cod_ubigeo == df_oro_ubigeo.ubigeo,
            "left",
        )
        .withColumn("SK_Diagnostico", F.monotonically_increasing_id())
        .select(
            "cod_diagnostico",
            "SK_Diagnostico",
            "SK_Tiempo",
            "SK_Paciente",
            "SK_Enfermedad",
            "SK_Ubigeo",
            "servicio_hospitalario",
            "actividad_hospitalaria",
        )
    )

    # Fact_Resultado
    df_oro_fact_resultado = (
        df_resul_enriched.join(
            df_oro_procedimiento, ["des_procedimiento", "unidades"], "left"
        )
        .join(
            df_oro_tiempo.select("fecha", "SK_Tiempo"),
            df_resul_enriched.fecha_resultado == col("fecha"),
            "left",
        )
        .join(
            df_oro_fact_diagnostico.select("SK_Diagnostico", "cod_diagnostico"),
            "cod_diagnostico",
            "left",
        )
        .withColumn("SK_Resultado", F.monotonically_increasing_id())
        .select(
            "SK_Resultado",
            "SK_Tiempo",
            "SK_Diagnostico",
            col("resultado").alias("medida_resultado"),
        )
    )

    # Escritura a BQ (Oro)
    logger.info("Escribiendo datos ORO en BigQuery...")
    write_to_bigquery(df_oro_tiempo, f"{PROJECT_ID}.oro.dim_tiempo")
    write_to_bigquery(df_oro_paciente, f"{PROJECT_ID}.oro.dim_paciente")
    write_to_bigquery(df_oro_ubigeo, f"{PROJECT_ID}.oro.dim_ubigeo")
    write_to_bigquery(df_oro_procedimiento, f"{PROJECT_ID}.oro.dim_procedimiento")
    write_to_bigquery(df_oro_enfermedad, f"{PROJECT_ID}.oro.dim_enfermedad")
    write_to_bigquery(df_oro_fact_diagnostico, f"{PROJECT_ID}.oro.fact_diagnostico")
    write_to_bigquery(df_oro_fact_resultado, f"{PROJECT_ID}.oro.fact_resultado")

    # Exportación CSV (Oro)
    logger.info("Exportando CSVs ORO a GCS...")
    export_single_csv(
        df_oro_tiempo, BUCKET_DATALAKE, "oro/dim_tiempo", "dim_tiempo.csv"
    )
    export_single_csv(
        df_oro_paciente, BUCKET_DATALAKE, "oro/dim_paciente", "dim_paciente.csv"
    )
    export_single_csv(
        df_oro_ubigeo, BUCKET_DATALAKE, "oro/dim_ubigeo", "dim_ubigeo.csv"
    )
    export_single_csv(
        df_oro_procedimiento,
        BUCKET_DATALAKE,
        "oro/dim_procedimiento",
        "dim_procedimiento.csv",
    )
    export_single_csv(
        df_oro_enfermedad, BUCKET_DATALAKE, "oro/dim_enfermedad", "dim_enfermedad.csv"
    )
    export_single_csv(
        df_oro_fact_diagnostico,
        BUCKET_DATALAKE,
        "oro/fact_diagnostico",
        "fact_diagnostico.csv",
    )
    export_single_csv(
        df_oro_fact_resultado,
        BUCKET_DATALAKE,
        "oro/fact_resultado",
        "fact_resultado.csv",
    )

    logger.info("Proceso ETL finalizado exitosamente.")


if __name__ == "__main__":
    spark = get_spark_session()
    try:
        process_etl(spark)
    except Exception as e:
        logger.error(f"Error durante la ejecución del ETL: {e}")
        sys.exit(1)
    finally:
        spark.stop()
