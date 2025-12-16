from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("clean_flight_delay").getOrCreate()

# =========================
# 1) Rutas
# =========================
bucket_raw = "bronce-raw"
bucket_processed = "bronce_processed"
file_name = "Flight_delay.csv"

input_path = f"gs://{bucket_raw}/{file_name}"
output_dir = f"gs://{bucket_processed}/flight_delay_clean_csv"  # carpeta de salida (Spark crea part-*.csv)

# =========================
# 2) Leer CSV desde GCS
# =========================
df0 = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .option("multiLine", "true")
    .option("quote", "\"")
    .option("escape", "\"")
    .option("mode", "PERMISSIVE")
    # .option("sep", ";")  # descomenta si tu CSV usa ;
    .csv(input_path)
)

# =========================
# 3) Funciones de apoyo
# =========================
def normalize_col(name: str) -> str:
    name = name.strip().lower()
    name = "".join(ch if ch.isalnum() else "_" for ch in name)
    while "__" in name:
        name = name.replace("__", "_")
    return name.strip("_")

def agg_null_counts(df):
    return df.agg(*[
        F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
        for c in df.columns
    ])

# =========================
# 4) Normalizar nombres de columnas
# =========================
df = df0
for old in df.columns:
    df = df.withColumnRenamed(old, normalize_col(old))

# Recalcular lista de columnas string después del renombre
str_cols = [f.name for f in df.schema.fields if isinstance(f.dataType, StringType)]

# Tokens string que se tratarán como null
null_tokens = ["", "null", "none", "nan"]

# =========================
# 5) Métricas BEFORE
# =========================
rows_in = df.count()

# filas completamente nulas
rows_no_all_null = df.na.drop("all").count()
removed_all_null = rows_in - rows_no_all_null

# duplicados (sobre fila completa, antes de limpiar)
dedup_pre = df.dropDuplicates().count()
dupes_pre = rows_in - dedup_pre

# cuántas celdas string parecen "null-like" (se convertirán a null)
null_like_exprs = []
whitespace_change_exprs = []
for c in str_cols:
    cleaned_str = F.regexp_replace(F.trim(F.col(c)), r"\s+", " ")
    null_like = (
        F.col(c).isNotNull() &
        (F.lower(F.trim(F.col(c))).isin(null_tokens))
    )
    whitespace_changed = (
        F.col(c).isNotNull() &
        (F.col(c) != cleaned_str)
    )
    null_like_exprs.append(F.sum(F.when(null_like, 1).otherwise(0)).alias(c))
    whitespace_change_exprs.append(F.sum(F.when(whitespace_changed, 1).otherwise(0)).alias(c))

null_like_by_col_before = df.agg(*null_like_exprs).collect()[0].asDict() if str_cols else {}
whitespace_changed_by_col_before = df.agg(*whitespace_change_exprs).collect()[0].asDict() if str_cols else {}

total_null_like_cells_before = int(sum(null_like_by_col_before.values())) if null_like_by_col_before else 0
total_whitespace_cells_before = int(sum(whitespace_changed_by_col_before.values())) if whitespace_changed_by_col_before else 0

# nulls por columna (antes)
nulls_before_df = agg_null_counts(df)
nulls_before = nulls_before_df.collect()[0].asDict()

# =========================
# 6) Limpieza general
# =========================
# 6.1 Metadatos de ingesta
df = (
    df.withColumn("_source_path", F.lit(input_path))
      .withColumn("_ingestion_ts", F.current_timestamp())
)

# 6.2 Limpieza de strings: trim + colapsar espacios + tokens -> null
out = df
for c in str_cols:
    col = F.col(c)
    col = F.trim(col)
    col = F.regexp_replace(col, r"\s+", " ")
    col_lower = F.lower(col)
    col = F.when(col.isNull() | col_lower.isin(null_tokens), F.lit(None)).otherwise(col)
    out = out.withColumn(c, col)

# 6.3 Quitar filas totalmente nulas
out1 = out.na.drop("all")

# 6.4 Eliminar duplicados (fila completa)
out2 = out1.dropDuplicates()

# =========================
# 7) Métricas AFTER
# =========================
rows_after_drop_all_null = out1.count()
rows_final = out2.count()

removed_all_null_after = rows_in - rows_after_drop_all_null
removed_dupes_after = rows_after_drop_all_null - rows_final
total_removed = rows_in - rows_final

# nulls por columna (después)
nulls_after_df = agg_null_counts(out2)
nulls_after = nulls_after_df.collect()[0].asDict()

# =========================
# 8) Guardar CSV limpio en bronce-processed
# =========================
(
    out2.coalesce(1)
       .write
       .mode("overwrite")
       .option("header", "true")
       .csv(output_dir)
)

# =========================
# 9) Reporte de limpieza (NÚMEROS)
# =========================
print("========== LIMPIEZA Flight_delay.csv ==========")
print("Input:", input_path)
print("Output:", output_dir, "(carpeta con part-*.csv)")

print("\n--- Filas ---")
print("Filas originales:", rows_in)
print("Filas eliminadas (todas null):", removed_all_null_after)
print("Filas eliminadas (duplicados):", removed_dupes_after)
print("Filas finales:", rows_final)
print("Total filas eliminadas:", total_removed)

print("\n--- Celdas string (estimación de cambios) ---")
print('Celdas "null-like" detectadas (\"\", null, none, nan) -> NULL:', total_null_like_cells_before)
print("Celdas con cambio por trim/espacios normalizados:", total_whitespace_cells_before)

print("\n--- Nulls por columna (Top 15 con más nulls DESPUÉS) ---")
top_after = sorted(nulls_after.items(), key=lambda x: x[1], reverse=True)[:15]
for k, v in top_after:
    print(f"{k}: {v}")
