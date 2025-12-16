# Capa Oro (Gold): Dimensiones, Tabla de Hechos y KPIs (Databricks / PySpark)

En esta etapa se construye la **capa Gold**, orientada al consumo analítico y a dashboards.  
A partir de la tabla limpia en **capa Silver** (`flight_delay_silver`), se generan:

- **Dimensiones**: `dim_tiempo_gold`, `dim_aerolinea_gold`, `dim_origen_gold`, `dim_destino_gold`
- **Tabla de hechos**: `fact_vuelos_gold`
- **KPIs agregados**: `kpis_reporte_gold`

> Este script está diseñado para ser tolerante a variaciones en nombres de columnas (por ejemplo: `dep_delay` vs `depdelay`).

---

## Script completo (Gold)

```python
from pyspark.sql.functions import (
    col, year, month, dayofmonth, dayofweek, to_date,
    monotonically_increasing_id, when, count, avg, sum, lit
)

# ==========================================================
# CAPA GOLD (Dimensiones, tabla de hechos y KPIs)
# ==========================================================

# 1. Leer la capa Plata
df_silver = spark.read.table("flight_delay_silver")

# ==========================================
# FUNCIÓN DE AYUDA: BUSCAR COLUMNAS
# ==========================================
def buscar_columna(df, opciones):
    """
    Busca una columna en el DataFrame usando una lista de posibles nombres.
    Si no existe ninguna, retorna un literal 0 para evitar que falle el pipeline.
    """
    for opcion in opciones:
        if opcion in df.columns:
            return col(opcion)
        for c in df.columns:
            if c.lower() == opcion.lower():
                return col(c)

    print(f"⚠️ Advertencia: No se encontró ninguna de estas columnas: {opciones}. Se usará 0.")
    return lit(0.0)

# ==========================================
# 0. PASO PREVIO: ENRIQUECER DATA (TIME FEATURES)
# ==========================================
col_fecha = buscar_columna(df_silver, ["date", "flightdate", "flight_date"])

df_gold_base = (
    df_silver
    .withColumn("date_obj", to_date(col_fecha))
    .withColumn("year", year("date_obj"))
    .withColumn("month", month("date_obj"))
    .withColumn("day_of_month", dayofmonth("date_obj"))
    .withColumn("day_of_week", dayofweek("date_obj"))
)

# ==========================================
# 1. DIMENSIONES
# ==========================================

# Dim Tiempo
dim_tiempo = (
    df_gold_base
    .select("year", "month", "day_of_month", "day_of_week")
    .distinct()
    .withColumn("id_tiempo", monotonically_increasing_id())
)
dim_tiempo.write.format("delta").mode("overwrite").saveAsTable("dim_tiempo_gold")
print("✅ dim_tiempo creada.")

# Dim Aerolínea (carrier_code)
col_carrier = buscar_columna(df_gold_base, ["unique_carrier", "airline", "carrier"])
dim_aerolinea = df_gold_base.select(col_carrier.alias("carrier_code")).distinct()
dim_aerolinea.write.format("delta").mode("overwrite").saveAsTable("dim_aerolinea_gold")
print("✅ dim_aerolinea creada.")

# Dim Aeropuertos (Origen/Destino)
col_origin = buscar_columna(df_gold_base, ["origin", "originairportid"])
col_dest   = buscar_columna(df_gold_base, ["dest", "destairportid", "destination"])

catalog_airports = (
    df_gold_base.select(col_origin.alias("airport_code"))
    .union(df_gold_base.select(col_dest.alias("airport_code")))
    .distinct()
)

catalog_airports.write.format("delta").mode("overwrite").saveAsTable("dim_origen_gold")
catalog_airports.write.format("delta").mode("overwrite").saveAsTable("dim_destino_gold")
print("✅ dim_origen y dim_destino creadas.")

# ==========================================
# 2. TABLA DE HECHOS (fact_vuelos)
# ==========================================
fact_vuelos = df_gold_base.select(
    # Atributos temporales (útiles para análisis directo en BI)
    "year", "month", "day_of_month", "day_of_week",

    # Identificadores del evento (vuelo)
    col_carrier.alias("carrier_code"),
    col_origin.alias("origin"),
    col_dest.alias("dest"),

    # Retrasos y estado del vuelo
    buscar_columna(df_gold_base, ["dep_delay", "depdelay", "DepDelay"]).cast("double").alias("dep_delay"),
    buscar_columna(df_gold_base, ["arr_delay", "arrdelay", "ArrDelay"]).cast("double").alias("arr_delay"),
    buscar_columna(df_gold_base, ["cancelled", "canceled", "Cancelled"]).cast("int").alias("cancelled"),

    # Causas de retraso (minutos)
    buscar_columna(df_gold_base, ["carrier_delay", "carrierdelay"]).cast("double").alias("delay_carrier"),
    buscar_columna(df_gold_base, ["weather_delay", "weatherdelay"]).cast("double").alias("delay_weather"),
    buscar_columna(df_gold_base, ["nas_delay", "nasdelay"]).cast("double").alias("delay_nas"),
    buscar_columna(df_gold_base, ["security_delay", "securitydelay"]).cast("double").alias("delay_security"),
    buscar_columna(df_gold_base, ["late_aircraft_delay", "lateaircraftdelay"]).cast("double").alias("delay_late_aircraft")
)

fact_vuelos.write.format("delta").mode("overwrite").saveAsTable("fact_vuelos_gold")
print("✅ fact_vuelos creada (con detección automática de nombres de columnas).")

# ==========================================
# 3. KPIs (Reporte) - por aerolínea
# ==========================================
kpis_gold = fact_vuelos.groupBy("carrier_code").agg(
    # KPIs base
    (count(when(col("arr_delay") > 15, True)) / count("*") * 100).alias("porcentaje_retrasos"),
    avg("arr_delay").alias("retraso_promedio_llegada"),

    # KPIs adicionales
    (avg(col("cancelled").cast("double")) * 100).alias("tasa_cancelacion_pct"),
    (count(when(col("arr_delay") <= 0, True)) / count("*") * 100).alias("porcentaje_a_tiempo_pct"),
    avg(when(col("arr_delay") > 0, col("arr_delay"))).alias("retraso_promedio_solo_retrasados"),

    # Minutos totales por causa
    sum(col("delay_carrier")).alias("minutos_retraso_carrier"),
    sum(col("delay_weather")).alias("minutos_retraso_weather"),
    sum(col("delay_nas")).alias("minutos_retraso_nas"),
    sum(col("delay_security")).alias("minutos_retraso_security"),
    sum(col("delay_late_aircraft")).alias("minutos_retraso_late_aircraft")
)

kpis_gold.write.format("delta").mode("overwrite").saveAsTable("kpis_reporte_gold")
print("✅ Tabla de KPIs generada: kpis_reporte_gold (incluye KPIs adicionales).")

