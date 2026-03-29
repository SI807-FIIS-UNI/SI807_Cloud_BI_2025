%pyspark
from pyspark.sql import SparkSession

# 1. Conexión a la sesión
spark = SparkSession.builder.appName("Exportar_Reportes_Finales").enableHiveSupport().getOrCreate()

# 2. Configuración
db_name = "db_cepreuni1"
ruta_salida_hdfs = "/user/alumno/entregable_final/reportes_kpi"

print("--- EXPORTANDO TABLAS DE REPORTE (CURATED) ---")

# Las tablas de resumen que creamos
tablas_reporte = [
    "cur_reporte_carreras",
    "cur_reporte_colegios"
]

for tabla in tablas_reporte:
    print("Procesando: " + tabla + " ...")
    
    # Leemos la tabla de resumen de tu DB
    df = spark.table(db_name + "." + tabla)
    
    # Exportamos a un solo CSV
    df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(ruta_salida_hdfs + "/" + tabla)
        
    print("--> Exportada exitosamente a HDFS")

print("--- PROCESO TERMINADO ---")
print("Ruta de descarga: " + ruta_salida_hdfs)