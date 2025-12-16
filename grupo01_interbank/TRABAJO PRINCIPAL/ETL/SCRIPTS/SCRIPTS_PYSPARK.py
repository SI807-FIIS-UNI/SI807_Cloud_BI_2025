# LIMPIEZA INICIAL
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

spark = (
    SparkSession.builder
    .appName("limpieza_csv_kpis")
    .getOrCreate()
)

# ========= RUTAS DEL PROYECTO =========
raw_bucket = "project-sin-477115-raw"
refined_bucket = "project-sin-477115-refined"
fecha_path = "ingesta/2025-11-30"   # carpeta que se ve en tu screenshot

base_path = f"gs://{raw_bucket}/{fecha_path}"
output_clean_base = f"gs://{refined_bucket}/{fecha_path}/clean"
output_kpi_path = f"gs://{refined_bucket}/{fecha_path}/kpis"

# ========= ARCHIVOS =========
files = {
    "cli_cambios": f"{base_path}/cli_cambios.csv",
    "registro_comunicaciones_new_v2": f"{base_path}/registro_comunicaciones_new_v2.csv",
    "segmentos_v2": f"{base_path}/segmentos_v2.csv",
    "tiendas_ranking_propio_updated": f"{base_path}/tiendas_ranking_propio_updated.csv",
    "tlv_ranking_propio_updated": f"{base_path}/tlv_ranking_propio_updated.csv",
    "virtual_ranking_propio_updated": f"{base_path}/virtual_ranking_propio_updated.csv",
}

# ========= FUNCIÓN DE LIMPIEZA + KPIs =========
def clean_and_kpi(table_name: str, path: str):
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(path)
    )

    original_rows = df.count()
    num_columns = len(df.columns)
    string_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, StringType)]
    num_string_cols = len(string_cols)

    # Métricas antes
    if string_cols:
        len_before_row = (
            df.agg(*[F.sum(F.length(F.col(c))).alias(c) for c in string_cols])
              .collect()[0]
              .asDict()
        )
        total_len_before = sum(v for v in len_before_row.values() if v is not None)

        empty_before_row = (
            df.agg(
                *[
                    F.sum(
                        F.when(F.trim(F.col(c)) == "", 1).otherwise(0)
                    ).alias(c)
                    for c in string_cols
                ]
            ).collect()[0].asDict()
        )
        total_empty_before = sum(v for v in empty_before_row.values() if v is not None)
    else:
        len_before_row = {}
        total_len_before = 0
        empty_before_row = {}
        total_empty_before = 0

    # Limpieza columnas string
    df_clean = df
    for c in string_cols:
        df_clean = df_clean.withColumn(
            c,
            F.trim(F.regexp_replace(F.col(c), r"\s+", " "))
        )
        df_clean = df_clean.withColumn(
            c,
            F.when(F.col(c) == "", F.lit(None)).otherwise(F.col(c))
        )

    # Duplicados
    df_clean_count = df_clean.count()
    df_no_dups = df_clean.dropDuplicates()
    df_no_dups_count = df_no_dups.count()
    duplicates_removed = df_clean_count - df_no_dups_count

    # Filas totalmente nulas
    df_final = df_no_dups.na.drop("all")
    rows_after_cleaning = df_final.count()
    null_rows_removed = df_no_dups_count - rows_after_cleaning
    rows_removed_total = original_rows - rows_after_cleaning

    # Métricas después
    if string_cols:
        len_after_row = (
            df_final.agg(*[F.sum(F.length(F.col(c))).alias(c) for c in string_cols])
                    .collect()[0]
                    .asDict()
        )
        total_len_after = sum(v for v in len_after_row.values() if v is not None)

        spaces_removed_by_col = {}
        for c in string_cols:
            before = (len_before_row.get(c, 0) or 0)
            after = (len_after_row.get(c, 0) or 0)
            spaces_removed_by_col[c] = max(before - after, 0)

        total_spaces_removed = sum(spaces_removed_by_col.values())
        columns_with_spaces_cleaned = sum(1 for v in spaces_removed_by_col.values() if v > 0)
        columns_with_empty_to_null = sum(
            1 for c, v in empty_before_row.items() if (v or 0) > 0
        )
    else:
        total_spaces_removed = 0
        columns_with_spaces_cleaned = 0
        columns_with_empty_to_null = 0
        total_empty_before = 0

    # KPIs
    kpi_df = spark.createDataFrame(
        [
            (
                table_name,
                original_rows,
                rows_after_cleaning,
                rows_removed_total,
                duplicates_removed,
                null_rows_removed,
                num_columns,
                num_string_cols,
                total_spaces_removed,
                columns_with_spaces_cleaned,
                total_empty_before,
                columns_with_empty_to_null,
            )
        ],
        [
            "tabla",
            "filas_originales",
            "filas_finales",
            "filas_eliminadas_total",
            "filas_duplicadas_eliminadas",
            "filas_nulas_eliminadas",
            "columnas_totales",
            "columnas_string",
            "espacios_eliminados_total",
            "columnas_con_espacios_limpiados",
            "valores_vacios_a_null_total",
            "columnas_con_vacios_a_null",
        ],
    )

    # Guardar data limpia (formato parquet)
    df_final.write.mode("overwrite").parquet(f"{output_clean_base}/{table_name}")

    return kpi_df


# ========= EJECUTAR PARA TODOS LOS ARCHIVOS =========
kpi_dfs = [clean_and_kpi(name, path) for name, path in files.items()]

kpis_df = kpi_dfs[0]
for other in kpi_dfs[1:]:
    kpis_df = kpis_df.unionByName(other)

kpis_df.show(truncate=False)

# Guardar KPIs en REFINED
kpis_df.write.mode("overwrite").option("header", "true").csv(output_kpi_path)

# VISTA CON PANDAS
from IPython.display import display
import pandas as pd

# Opcional: reordenar columnas
kpis_df = kpis_df.select(
    "tabla",
    "filas_originales",
    "filas_finales",
    "filas_eliminadas_total",
    "filas_duplicadas_eliminadas",
    "filas_nulas_eliminadas",
    "columnas_totales",
    "columnas_string",
    "espacios_eliminados_total",
    "columnas_con_espacios_limpiados",
    "valores_vacios_a_null_total",
    "columnas_con_vacios_a_null",
)

# Pasar a pandas 
pdf = kpis_df.toPandas()

display(pdf)

# KPIS MEJORADOS
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Opcional: solo funcionará el display si estás en Jupyter
try:
    from IPython.display import display
    import pandas as pd
    IN_NOTEBOOK = True
except ImportError:
    IN_NOTEBOOK = False

spark = (
    SparkSession.builder
    .appName("limpieza_csv_kpis")
    .getOrCreate()
)

# ========= RUTAS DE TU PROYECTO =========
raw_bucket = "project-sin-477115-raw"
trusted_bucket = "project-sin-477115-trusted"
fecha_path = "ingesta/2025-11-30"   # carpeta donde están los CSV

base_path = f"gs://{raw_bucket}/{fecha_path}"
output_clean_base = f"gs://{trusted_bucket}/{fecha_path}/clean"
output_kpi_path = f"gs://{trusted_bucket}/{fecha_path}/kpis"

# ========= ARCHIVOS QUE MOSTRASTE =========
files = {
    "cli_cambios": f"{base_path}/cli_cambios.csv",
    "registro_comunicaciones_new_v2": f"{base_path}/registro_comunicaciones_new_v2.csv",
    "segmentos_v2": f"{base_path}/segmentos_v2.csv",
    "tiendas_ranking_propio_updated": f"{base_path}/tiendas_ranking_propio_updated.csv",
    "tlv_ranking_propio_updated": f"{base_path}/tlv_ranking_propio_updated.csv",
    "virtual_ranking_propio_updated": f"{base_path}/virtual_ranking_propio_updated.csv",
}

# ========= FUNCIÓN DE LIMPIEZA + KPIs =========
def clean_and_kpi(table_name: str, path: str):
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(path)
    )

    original_rows = df.count()
    num_columns = len(df.columns)
    string_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, StringType)]
    num_string_cols = len(string_cols)

    # Métricas antes
    if string_cols:
        len_before_row = (
            df.agg(*[F.sum(F.length(F.col(c))).alias(c) for c in string_cols])
              .collect()[0]
              .asDict()
        )

        empty_before_row = (
            df.agg(
                *[
                    F.sum(
                        F.when(F.trim(F.col(c)) == "", 1).otherwise(0)
                    ).alias(c)
                    for c in string_cols
                ]
            ).collect()[0].asDict()
        )
        total_empty_before = sum(v for v in empty_before_row.values() if v is not None)
    else:
        len_before_row = {}
        empty_before_row = {}
        total_empty_before = 0

    # Limpieza columnas string
    df_clean = df
    for c in string_cols:
        df_clean = df_clean.withColumn(
            c,
            F.trim(F.regexp_replace(F.col(c), r"\s+", " "))
        )
        df_clean = df_clean.withColumn(
            c,
            F.when(F.col(c) == "", F.lit(None)).otherwise(F.col(c))
        )

    # Duplicados
    df_clean_count = df_clean.count()
    df_no_dups = df_clean.dropDuplicates()
    df_no_dups_count = df_no_dups.count()
    duplicates_removed = df_clean_count - df_no_dups_count

    # Filas totalmente nulas
    df_final = df_no_dups.na.drop("all")
    rows_after_cleaning = df_final.count()
    null_rows_removed = df_no_dups_count - rows_after_cleaning
    rows_removed_total = original_rows - rows_after_cleaning

    # Métricas después (para espacios)
    if string_cols:
        len_after_row = (
            df_final.agg(*[F.sum(F.length(F.col(c))).alias(c) for c in string_cols])
                    .collect()[0]
                    .asDict()
        )

        spaces_removed_by_col = {}
        for c in string_cols:
            before = (len_before_row.get(c, 0) or 0)
            after = (len_after_row.get(c, 0) or 0)
            spaces_removed_by_col[c] = max(before - after, 0)

        total_spaces_removed = sum(spaces_removed_by_col.values())
        columns_with_spaces_cleaned = sum(1 for v in spaces_removed_by_col.values() if v > 0)
        columns_with_empty_to_null = sum(
            1 for c, v in empty_before_row.items() if (v or 0) > 0
        )
    else:
        total_spaces_removed = 0
        columns_with_spaces_cleaned = 0
        columns_with_empty_to_null = 0
        total_empty_before = 0

    # ===== FLAGS (SI / NO) PARA DUPLICADOS Y NULOS =====
    tiene_filas_duplicadas = "SI" if duplicates_removed > 0 else "NO"
    tiene_filas_nulas = "SI" if null_rows_removed > 0 else "NO"
    tiene_filas_eliminadas = "SI" if rows_removed_total > 0 else "NO"

    # KPIs
    kpi_df = spark.createDataFrame(
        [
            (
                table_name,
                tiene_filas_duplicadas,
                tiene_filas_nulas,
                tiene_filas_eliminadas,
                original_rows,
                rows_after_cleaning,
                rows_removed_total,
                duplicates_removed,
                null_rows_removed,
                num_columns,
                num_string_cols,
                total_spaces_removed,
                columns_with_spaces_cleaned,
                total_empty_before,
                columns_with_empty_to_null,
            )
        ],
        [
            "tabla",
            "tiene_filas_duplicadas",
            "tiene_filas_nulas",
            "tiene_filas_eliminadas",
            "filas_originales",
            "filas_finales",
            "filas_eliminadas_total",
            "filas_duplicadas_eliminadas",
            "filas_nulas_eliminadas",
            "columnas_totales",
            "columnas_string",
            "espacios_eliminados_total",
            "columnas_con_espacios_limpiados",
            "valores_vacios_a_null_total",
            "columnas_con_vacios_a_null",
        ],
    )

    # Guardar data limpia en el bucket TRUSTED (formato parquet)
    df_final.write.mode("overwrite").parquet(f"{output_clean_base}/{table_name}")

    return kpi_df


# ========= EJECUTAR PARA TODOS LOS ARCHIVOS =========
kpi_dfs = [clean_and_kpi(name, path) for name, path in files.items()]

kpis_df = kpi_dfs[0]
for other in kpi_dfs[1:]:
    kpis_df = kpis_df.unionByName(other)

# --- Mostrar como tabla si estás en Jupyter ---
if IN_NOTEBOOK:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    display(kpis_df.toPandas())
else:
    # fallback si no hay Jupyter (job batch): texto
    kpis_df.show(truncate=False)

# Guardar KPIs EN TRUSTED
kpis_df.write.mode("overwrite").option("header", "true").csv(output_kpi_path)

#VISTA DEL TIPO DE DATO
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ver_esquemas_trusted").getOrCreate()

base_trusted = "gs://project-sin-477115-trusted/ingesta/2025-11-30/clean"

tablas = [
    "cli_cambios",
    "registro_comunicaciones_new_v2",
    "segmentos_v2",
    "tiendas_ranking_propio_updated",
    "tlv_ranking_propio_updated",
    "virtual_ranking_propio_updated",
]

for t in tablas:
    print(f"\n========== ESQUEMA PARQUET TRUSTED -> {t} ==========")
    df = spark.read.parquet(f"{base_trusted}/{t}")
    df.printSchema()
