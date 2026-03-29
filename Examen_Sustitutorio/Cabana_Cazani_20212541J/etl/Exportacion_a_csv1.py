%pyspark
from pyspark.sql import SparkSession

# 1. Obtener la sesión actual
spark = SparkSession.builder.appName("Exportar_Directo").enableHiveSupport().getOrCreate()

# 2. Configuración
db_name = "db_cepreuni1"
ruta_salida_hdfs = "/user/alumno/entregable_final"

print("--- INICIANDO EXPORTACION ---")
print("Base de datos: " + db_name)
print("Ruta destino: " + ruta_salida_hdfs)

tablas = [
    "fact_admision", 
    "dim_carrera", 
    "dim_modalidad", 
    "dim_tiempo", 
    "dim_geografia"
]

# 3. Bucle de exportación
for tabla in tablas:
    # Construir nombre completo "db.tabla"
    nombre_tabla = db_name + "." + tabla
    ruta_tabla = ruta_salida_hdfs + "/" + tabla
    
    print("Procesando tabla: " + tabla + " ...")
    
    # Leer
    df = spark.table(nombre_tabla)
    
    # Escribir (Sobreescribir)
    df.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(ruta_tabla)
        
    print("--> Guardado en: " + ruta_tabla)

print("--- PROCESO TERMINADO ---")
print("Ahora ve a la terminal y ejecuta: hdfs dfs -get " + ruta_salida_hdfs + " .")