# Scripts de procesamiento (Silver) — PySpark / Databricks

En esta carpeta se incluyen los scripts en **PySpark** ejecutados en **Databricks** para transformar el dataset **Flight Delay and Causes** siguiendo la lógica de capa:

- **Silver:** limpieza y estandarización de la tabla Bronze (`flight_delay_bronze`) para generar una tabla Delta consistente (`flight_delay_silver`).

---

## Script  (Silver)

```python
from pyspark.sql.functions import (
    col, year, month, dayofmonth, dayofweek, to_date,
    monotonically_increasing_id, when, count, avg, lit
)

# ==========================================================
# CAPA SILVER (Limpieza y estandarización)
# ==========================================================

# 1. Leer la tabla de la Capa Bronce
df_bronze = spark.read.table("flight_delay_bronze")

# 2. Estandarizar nombres de columnas (snake_case)
nuevas_columnas = [col(c).alias(c.lower().replace(" ", "_")) for c in df_bronze.columns]
df_silver = df_bronze.select(*nuevas_columnas)

# 3. Eliminar filas duplicadas
count_inicial = df_silver.count()
df_silver = df_silver.dropDuplicates()
count_final = df_silver.count()
print(f"Se eliminaron {count_inicial - count_final} filas duplicadas.")

# 4. Guardar en Databricks (Capa Plata)
nombre_tabla_silver = "flight_delay_silver"
df_silver.write.format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable(nombre_tabla_silver)
print(f"✅ Tabla Silver '{nombre_tabla_silver}' creada exitosamente.")


