%pyspark
from pyspark.sql import SparkSession

# 1. Conexión a la sesión existente
spark = SparkSession.builder.appName("Exportar_Faltantes").enableHiveSupport().getOrCreate()

# 2. Configuración
db_name = "db_cepreuni1"
ruta_salida_hdfs = "/user/alumno/entregable_final"

print("--- EXPORTANDO TABLAS FALTANTES ---")

# Solo las tablas que te faltaron
tablas_faltantes = [
    "dim_candidato", 
    "dim_institucion"
]

for tabla in tablas_faltantes:
    nombre_completo = db_name + "." + tabla
    ruta_tabla = ruta_salida_hdfs + "/" + tabla
    
    print("Exportando: " + tabla + "...")
    
    # Leemos de Hive (Solo lectura, muy seguro)
    df = spark.table(nombre_completo)
    
    # Escribimos en HDFS con overwrite para evitar cualquier duplicidad
    df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(ruta_tabla)
        
    print("--> Guardado exitosamente en: " + ruta_tabla)

print("--- PROCESO FINALIZADO ---")
print("Ahora puedes bajarlos con: hdfs dfs -get " + ruta_salida_hdfs + "/dim_candidato .")
print("Y también: hdfs dfs -get " + ruta_salida_hdfs + "/dim_institucion .")