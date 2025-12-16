## Capa Bronce (Bronze) — Ingesta y almacenamiento RAW en Delta (Databricks)

En esta sección se documenta el proceso de **carga inicial del dataset en su estado original (RAW)** desde **Azure Data Lake Storage Gen2 (contenedor `raw`)** hacia **Databricks**, guardándolo como una **tabla Delta** en la **capa Bronce**.  
El objetivo es conservar los datos **sin transformaciones**, asegurando trazabilidad y disponibilidad para las siguientes capas (Silver/Gold).

### Notebook / Script de ingesta (Bronze)

```python
# -------------------------------------------------------------------------
# 1. Configuración de credenciales
# -------------------------------------------------------------------------
storage_account_name = "bronze1"
storage_account_access_key = "claveprivadammmmm=="

# -------------------------------------------------------------------------
# 2. Autenticar Spark
# -------------------------------------------------------------------------
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net",
    storage_account_access_key
)

# -------------------------------------------------------------------------
# 3. Lectura del archivo (Raw)
# -------------------------------------------------------------------------
ruta_csv = f"abfss://raw@{storage_account_name}.dfs.core.windows.net/Flight_delay.csv"
print(f"Leyendo desde: {ruta_csv}")

df = spark.read.csv(ruta_csv, header=True, inferSchema=True)

# -------------------------------------------------------------------------
# 4. Guardar en Databricks (Capa Bronce)
# -------------------------------------------------------------------------
# Nombre de la tabla que se creará en Databricks
nombre_tabla_bronze = "flight_delay_bronze"

# Guardamos en formato DELTA (el estándar de Databricks)
# mode("overwrite") borra la tabla anterior si existe y la crea de nuevo.
df.write.format("delta").mode("overwrite").saveAsTable(nombre_tabla_bronze)

print(f"¡Éxito! La tabla '{nombre_tabla_bronze}' se ha guardado correctamente.")

# -------------------------------------------------------------------------
# 5. Verificación
# -------------------------------------------------------------------------
# Hacemos una consulta SQL rápida para confirmar que los datos están guardados
display(spark.sql(f"SELECT * FROM {nombre_tabla_bronze} LIMIT 10"))






