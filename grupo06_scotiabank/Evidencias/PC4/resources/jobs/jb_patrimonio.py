from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lower, trim, when, lit, to_date, concat_ws, lpad,
    create_map, coalesce
)
from itertools import chain

spark = SparkSession.builder.getOrCreate()

# ----------------------------------------------------
# Cargar tabla BRONCE
# ----------------------------------------------------
df_patrimonio = spark.table("bronce.sbs_patrimonio")

print("Columnas originales:", df_patrimonio.columns)

# Normalizar columnas a minúsculas
df_patrimonio = df_patrimonio.toDF(*[c.lower() for c in df_patrimonio.columns])
print("Columnas normalizadas:", df_patrimonio.columns)


# ----------------------------------------------------
# Normalizar nombre de institución
# ----------------------------------------------------
df_patrimonio = df_patrimonio.withColumn(
    "institucion",
    when(lower(col("institución")).like("%bcp%"), "BCP")
    .when(lower(col("institución")).like("%crédito%"), "BCP")
    .when(lower(col("institución")).like("%credito%"), "BCP")

    .when(lower(col("institución")).like("%interbank%"), "Interbank")

    .when((lower(col("institución")).like("%bbva%")) |
          (lower(col("institución")).like("%continental%")), "BBVA")

    .when(lower(col("institución")).like("%scotiabank%"), "Scotiabank")

    .when(lower(col("institución")).like("%interamericano%"), "BanBif")
    .when(lower(col("institución")).like("%mibanco%"), "Mibanco")

    .otherwise("Otros")
)

# ----------------------------------------------------
# Mapeo abreviado del mes → número
# ----------------------------------------------------
mes_map = {
    "en": "01", "fe": "02", "ma": "03", "ab": "04",
    "my": "05", "jn": "06", "jl": "07", "ag": "08",
    "se": "09", "oc": "10", "no": "11", "di": "12"
}
mapping_expr = create_map([lit(x) for x in chain(*mes_map.items())])

df_patrimonio = df_patrimonio.withColumn(
    "mes",
    coalesce(
        mapping_expr.getItem(lower(trim(col("mes").cast("string")))),
        trim(col("mes").cast("string"))
    )
)

# ----------------------------------------------------
# Filtrar instituciones válidas
# ----------------------------------------------------
df_filtered = df_patrimonio.filter(col("institucion") != "Otros")


# ----------------------------------------------------
# Calcular patrimonio total
# ----------------------------------------------------
df_result = df_filtered.withColumn(
    "patrimonio_monto",
    (
        coalesce(col("activos_líquidos").cast("double"), lit(0.0))
        + coalesce(col("pasivos_líquidos").cast("double"), lit(0.0))
    )
)


# ----------------------------------------------------
# Construcción de fecha (YYYY-MM-01)
# ----------------------------------------------------
df_final = df_result.select(
    to_date(
        concat_ws(
            "-",
            col("anio").cast("string"),
            lpad(col("mes").cast("string"), 2, "0"),
            lit("01")
        ),
        "yyyy-MM-dd"
    ).alias("fecha"),

    col("anio").cast("int"),
    col("mes").cast("int"),
    col("institucion"),
    col("patrimonio_monto").cast("double")
).orderBy("institucion", "anio", "mes")


# ----------------------------------------------------
# Guardar tabla en PLATA
# ----------------------------------------------------
df_final.write.mode("overwrite").format("parquet").saveAsTable("plata.sbs_patrimonio")

print("TABLA 'plata.sbs_patrimonio' generada correctamente")
df_final.show(10, False)
