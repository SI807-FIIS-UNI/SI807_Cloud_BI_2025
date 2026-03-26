# procesamiento_nettalco_etl.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count, round, when, to_timestamp, hour
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType
import logging
import os
import sys

# -----------------------------
# Logging (esto va a stdout -> Cloud Logging)
# -----------------------------
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("nettalcoproc")

logger.info("Iniciando job PySpark - Nettalco ETL")

# -----------------------------
# Configuración de Spark
# -----------------------------
spark = SparkSession.builder \
    .appName("Nettalco Big Data Processing - ETL") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
logger.info("SparkSession creada")

# -----------------------------
# Rutas (raw -> trusted -> refined)
# -----------------------------
PROJECT_BUCKET = os.environ.get("PROJECT_BUCKET", "nettalco-data-bd_grupo05")
RAW_PREFIX = f"gs://{PROJECT_BUCKET}/raw/"
TRUSTED_PREFIX = f"gs://{PROJECT_BUCKET}/trusted/"
REFINED_PREFIX = f"gs://{PROJECT_BUCKET}/refined/curated/"

detalle_path = f"{RAW_PREFIX}detalle-produccion-costura.csv"
cliente_path = f"{RAW_PREFIX}produccion-costura-cliente.csv"
linea_path = f"{RAW_PREFIX}produccion-costura-linea-cliente.csv"
segundas_path = f"{RAW_PREFIX}segundas-prendas.csv"

logger.info("Rutas establecidas: RAW=%s, TRUSTED=%s, REFINED=%s", RAW_PREFIX, TRUSTED_PREFIX, REFINED_PREFIX)

# -----------------------------
# Cargar los datos (raw)
# -----------------------------
logger.info("Leyendo archivos raw...")
detalle_produccion = spark.read.csv(detalle_path, header=True, inferSchema=True)
produccion_costura_cliente = spark.read.csv(cliente_path, header=True, inferSchema=True)
produccion_costura_linea_client = spark.read.csv(linea_path, header=True, inferSchema=True)
segundas_prendas = spark.read.csv(segundas_path, header=True, inferSchema=True)

logger.info("Lectura raw completa: detalle=%s, cliente=%s, linea=%s, segundas=%s",
            detalle_produccion.count(), produccion_costura_cliente.count(),
            produccion_costura_linea_client.count(), segundas_prendas.count())

# -----------------------------
# Data typing / limpieza mínima -> trusted
# -----------------------------
logger.info("Transformando datos y escribiendo trusted...")

detalle_produccion = detalle_produccion.withColumn("PRENDAS", col("PRENDAS").cast(IntegerType()))
produccion_costura_cliente = produccion_costura_cliente.withColumn("PRENDAS", col("PRENDAS").cast(IntegerType()))
produccion_costura_linea_client = produccion_costura_linea_client.withColumn("PRENDAS", col("PRENDAS").cast(IntegerType()))
segundas_prendas = segundas_prendas.withColumn("FALLAS_SEGUNDAS", col("FALLAS_SEGUNDAS").cast(IntegerType())) \
                                   .withColumn("INSPECCION_TOTAL", col("INSPECCION_TOTAL").cast(IntegerType()))

# Normalizar fecha a columna timestamp
detalle_produccion = detalle_produccion.withColumn(
    "FECHA_TERMINO_TS",
    to_timestamp("FECHA_TERMINO", "dd/MM/yyyy HH:mm:ss")
)

# Guardar copias "trusted" (formato parquet recomendado para downstream)
trusted_detalle = f"{TRUSTED_PREFIX}detalle-produccion-costura/"
trusted_cliente = f"{TRUSTED_PREFIX}produccion-costura-cliente/"
trusted_linea = f"{TRUSTED_PREFIX}produccion-costura-linea-cliente/"
trusted_segundas = f"{TRUSTED_PREFIX}segundas-prendas/"

detalle_produccion.write.mode("overwrite").parquet(trusted_detalle)
produccion_costura_cliente.write.mode("overwrite").parquet(trusted_cliente)
produccion_costura_linea_client.write.mode("overwrite").parquet(trusted_linea)
segundas_prendas.write.mode("overwrite").parquet(trusted_segundas)

logger.info("Trusted escritos en parquet en: %s, %s, %s, %s",
            trusted_detalle, trusted_cliente, trusted_linea, trusted_segundas)

# -----------------------------
# Procesos analíticos -> refined (curated outputs)
# -----------------------------
logger.info("Generando datasets refinados (refined)...")

# Total prendas por talla
detalle_produccion.groupBy("TALLA") \
    .agg(_sum("PRENDAS").alias("TOTAL_PRENDAS")) \
    .orderBy("TALLA") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}total_prendas_por_talla")

# Volumen de ventas por cliente
produccion_costura_cliente.groupBy("TCODICLIE") \
    .agg(_sum("PRENDAS").alias("TOTAL_PRENDAS")) \
    .orderBy("TCODICLIE") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}volumen_ventas_por_cliente")

# Fecha ventas
produccion_costura_cliente.groupBy("FECHA") \
    .agg(_sum("PRENDAS").alias("TOTAL_PRENDAS")) \
    .orderBy("FECHA") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}fecha_ventas")

# Tendencias por franja horaria
detalle_produccion = detalle_produccion.withColumn("HORA", hour("FECHA_TERMINO_TS"))
tendencias = detalle_produccion.withColumn(
    "FRANJA_HORARIA",
    when((col("HORA") >= 6) & (col("HORA") <= 11), "Mañana")
    .when((col("HORA") >= 12) & (col("HORA") <= 17), "Tarde")
    .when((col("HORA") >= 18) & (col("HORA") <= 23), "Noche")
    .otherwise("Madrugada")
).groupBy("ORDEN_PRODUCCION", "FRANJA_HORARIA") \
 .agg(count("*").alias("TRANSACCIONES"), _sum("PRENDAS").alias("TOTAL_PRENDAS")) \
 .orderBy("ORDEN_PRODUCCION", "FRANJA_HORARIA")

tendencias.write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}tendencias_ventas_por_franja_horaria")

# Productos más vendidos
detalle_produccion.groupBy("ESTILO") \
    .agg(_sum("PRENDAS").alias("TOTAL_PRENDAS")) \
    .orderBy("ESTILO") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}productos_mas_vendidos")

# Eficiencia operativa
segundas_prendas.groupBy("FECHA") \
    .agg(
        round(
            (1 - (_sum("FALLAS_SEGUNDAS") / _sum("INSPECCION_TOTAL"))) * 100, 2
        ).alias("EFICIENCIA_PORCENTUAL")
    ) \
    .orderBy("FECHA") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}eficiencia_operativa")

# Índice de ventas por cliente y línea
produccion_costura_linea_client.groupBy("TCODICLIE", "LINEA") \
    .agg(_sum("PRENDAS").alias("TOTAL_PRENDAS")) \
    .orderBy("TCODICLIE") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}indice_ventas_cliente")

# Predicción de ventas (promedio móvil 7 días)
detalle_produccion.groupBy("FECHA_TERMINO_TS", "ESTILO") \
    .agg(_sum("PRENDAS").alias("TOTAL_PRENDAS")) \
    .withColumn(
        "PROMEDIO_MOVIL",
        avg("TOTAL_PRENDAS").over(Window.partitionBy("ESTILO").orderBy("FECHA_TERMINO_TS").rowsBetween(-6, 0))
    ) \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}prediccion_ventas")

# Comportamiento de clientes
produccion_costura_cliente.groupBy("TCODICLIE") \
    .agg(count("FECHA").alias("FRECUENCIA_COMPRA"), avg("PRENDAS").alias("PROMEDIO_PRENDAS")) \
    .orderBy("TCODICLIE") \
    .write.mode("overwrite").option("header", "true").csv(f"{REFINED_PREFIX}comportamiento_clientes")

logger.info("Refined outputs escritos en %s", REFINED_PREFIX)

logger.info("Job finalizado correctamente")
spark.stop()