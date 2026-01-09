"""
ETL Curated Job - Transformación de Datos RAW a CURATED
Proyecto: etl-retail-analytics
Dataset: dataset_si807_g9
Bucket: mi-etl-proyecto-2025
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, upper, when, to_date, 
    regexp_replace, coalesce, lit, current_timestamp
)
from pyspark.sql.types import IntegerType, FloatType, DateType
import sys

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

def create_spark_session():
    """Crea y configura la sesión de Spark con el conector de BigQuery"""
    spark = SparkSession.builder \
        .appName("ETL-Curated-Job-G9") \
        .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12.jar") \
        .getOrCreate()
    
    # Configurar nivel de log
    spark.sparkContext.setLogLevel("WARN")
    
    print(f"[INFO] Sesión Spark iniciada: {spark.version}")
    return spark

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================

PROJECT_ID = "etl-retail-analytics"
DATASET_RAW = "dataset_si807_g9"
DATASET_CURATED = "dataset_si807_g9"
BUCKET = "mi-etl-proyecto-2025"

# Rutas GCS para archivos CSV
GCS_PATHS = {
    "dim_cliente": f"gs://{BUCKET}/raw/dim_cliente/*.csv",
    "dim_periodo": f"gs://{BUCKET}/raw/dim_periodo/*.csv",
    "dim_producto": f"gs://{BUCKET}/raw/dim_producto/*.csv",
    "dim_promocion": f"gs://{BUCKET}/raw/dim_promocion_precio/*.csv",
    "dim_tienda": f"gs://{BUCKET}/raw/dim_tienda_canal/*.csv",
    "fact_venta": f"gs://{BUCKET}/raw/fact_hecho_venta/*.csv"
}

# Tablas de destino en BigQuery
BQ_TABLES = {
    "dim_cliente": f"{PROJECT_ID}.{DATASET_CURATED}.dim_cliente_curated",
    "dim_periodo": f"{PROJECT_ID}.{DATASET_CURATED}.dim_periodo_curated",
    "dim_producto": f"{PROJECT_ID}.{DATASET_CURATED}.dim_producto_curated",
    "dim_promocion": f"{PROJECT_ID}.{DATASET_CURATED}.dim_promocion_precio_curated",
    "dim_tienda": f"{PROJECT_ID}.{DATASET_CURATED}.dim_tienda_canal_curated",
    "fact_venta": f"{PROJECT_ID}.{DATASET_CURATED}.fact_hecho_venta_curated"
}

# ============================================================================
# FUNCIONES DE CARGA DESDE GCS
# ============================================================================

def load_csv_from_gcs(spark, path, table_name):
    """Carga un CSV desde GCS y retorna un DataFrame"""
    try:
        print(f"[INFO] Cargando {table_name} desde {path}")
        df = spark.read \
            .option("header", "true") \
            .option("inferSchema", "false") \
            .option("delimiter", ",") \
            .option("encoding", "UTF-8") \
            .csv(path)
        
        count = df.count()
        print(f"[SUCCESS] {table_name} cargada: {count} registros")
        return df
    except Exception as e:
        print(f"[ERROR] Error al cargar {table_name}: {str(e)}")
        raise

# ============================================================================
# TRANSFORMACIONES POR TABLA
# ============================================================================

def transform_dim_cliente(df):
    """Limpieza y transformación de dim_cliente"""
    print("[INFO] Transformando dim_cliente...")
    
    df_clean = df.select(
        col("sk_cliente").cast(IntegerType()).alias("sk_cliente"),
        trim(upper(col("cod_cliente"))).alias("cod_cliente"),
        trim(upper(col("cod_tipo_cliente"))).alias("cod_tipo_cliente"),
        trim(col("desc_tipo_cliente")).alias("desc_tipo_cliente"),
        trim(upper(col("estado_cliente"))).alias("estado_cliente"),
        trim(col("numero_tarjeta_bonus")).alias("numero_tarjeta_bonus"),
        to_date(col("fecha_alta_cliente"), "yyyy-MM-dd").alias("fecha_alta_cliente_dt"),
        col("recencia").cast(IntegerType()).alias("recencia")
    )
    
    # Filtrar registros con SK nulo
    df_clean = df_clean.filter(col("sk_cliente").isNotNull())
    
    # Manejo de valores nulos en campos críticos
    df_clean = df_clean.fillna({
        "cod_tipo_cliente": "DESCONOCIDO",
        "desc_tipo_cliente": "Sin Información",
        "estado_cliente": "INACTIVO",
        "numero_tarjeta_bonus": "SIN_TARJETA",
        "recencia": 9999
    })
    
    print(f"[SUCCESS] dim_cliente transformada: {df_clean.count()} registros")
    return df_clean


def transform_dim_periodo(df):
    """Limpieza y transformación de dim_periodo"""
    print("[INFO] Transformando dim_periodo...")
    
    df_clean = df.select(
        col("sk_periodo").cast(IntegerType()).alias("sk_periodo"),
        col("anio").cast(IntegerType()).alias("anio"),
        col("mes").cast(IntegerType()).alias("mes"),
        trim(col("nombre_mes")).alias("nombre_mes"),
        col("trimestre").cast(IntegerType()).alias("trimestre"),
        col("es_mes_cerrado").cast(IntegerType()).alias("es_mes_cerrado"),
        to_date(col("inicio_mes"), "yyyy-MM-dd").alias("inicio_mes_dt"),
        to_date(col("fin_mes"), "yyyy-MM-dd").alias("fin_mes_dt")
    )
    
    df_clean = df_clean.filter(col("sk_periodo").isNotNull())
    
    print(f"[SUCCESS] dim_periodo transformada: {df_clean.count()} registros")
    return df_clean


def transform_dim_producto(df):
    """Limpieza y transformación de dim_producto"""
    print("[INFO] Transformando dim_producto...")
    
    df_clean = df.select(
        col("sk_producto").cast(IntegerType()).alias("sk_producto"),
        trim(upper(col("cod_material"))).alias("cod_material"),
        trim(col("desc_material")).alias("desc_material"),
        trim(upper(col("categoria"))).alias("categoria"),
        trim(upper(col("subcategoria"))).alias("subcategoria"),
        # Transformación: Si marca es NULL o vacía, poner 'SIN MARCA'
        when(
            (col("marca").isNull()) | (trim(col("marca")) == ""),
            lit("SIN MARCA")
        ).otherwise(upper(col("marca"))).alias("marca"),
        # Transformación: Si unidad_medida es NULL o vacía, poner 'N/A'
        when(
            (col("unidad_medida").isNull()) | (trim(col("unidad_medida")) == ""),
            lit("N/A")
        ).otherwise(upper(col("unidad_medida"))).alias("unidad_medida"),
        # Transformación: Si pack_size es NULL o vacía, poner 'N/A'
        when(
            (col("pack_size").isNull()) | (trim(col("pack_size")) == ""),
            lit("N/A")
        ).otherwise(upper(col("pack_size"))).alias("pack_size")
    )
    
    # Filtrar registros con SK nulo
    df_clean = df_clean.filter(col("sk_producto").isNotNull())
    
    print(f"[SUCCESS] dim_producto transformada: {df_clean.count()} registros")
    return df_clean


def transform_dim_promocion(df):
    """Limpieza y transformación de dim_promocion_precio"""
    print("[INFO] Transformando dim_promocion_precio...")
    
    df_clean = df.select(
        col("sk_promocion").cast(IntegerType()).alias("sk_promocion"),
        trim(upper(col("cod_promocion"))).alias("cod_promocion"),
        trim(upper(col("cod_tipo_precio"))).alias("cod_tipo_precio"),
        trim(upper(col("desc_tipo_precio"))).alias("desc_tipo_precio"),
        col("flag_ticket_con_promocion").cast(IntegerType()).alias("flag_ticket_con_promocion"),
        to_date(col("vigencia_inicio"), "yyyy-MM-dd").alias("vigencia_inicio_dt"),
        to_date(col("vigencia_fin"), "yyyy-MM-dd").alias("vigencia_fin_dt")
    )
    
    # Filtrar registros con SK nulo
    df_clean = df_clean.filter(col("sk_promocion").isNotNull())
    
    print(f"[SUCCESS] dim_promocion transformada: {df_clean.count()} registros")
    return df_clean


def transform_dim_tienda(df):
    """Limpieza y transformación de dim_tienda_canal"""
    print("[INFO] Transformando dim_tienda_canal...")
    
    df_clean = df.select(
        col("sk_tienda").cast(IntegerType()).alias("sk_tienda"),
        trim(upper(col("cod_tienda"))).alias("cod_tienda"),
        trim(col("nombre_tienda")).alias("nombre_tienda"),
        trim(upper(col("cadena"))).alias("cadena"),
        trim(upper(col("cod_canal"))).alias("cod_canal"),
        trim(upper(col("desc_canal"))).alias("desc_canal"),
        trim(upper(col("ciudad"))).alias("ciudad"),
        # Corrección de encoding: Reemplazar 'AlmacÃ©n' por 'Almacén'
        regexp_replace(trim(upper(col("formato"))), "ALMACÃ©N", "ALMACÉN").alias("formato")
    )
    
    # Filtrar registros con SK nulo
    df_clean = df_clean.filter(col("sk_tienda").isNotNull())
    
    print(f"[SUCCESS] dim_tienda transformada: {df_clean.count()} registros")
    return df_clean


def transform_fact_venta(df):
    """Limpieza y transformación de fact_hecho_venta"""
    print("[INFO] Transformando fact_hecho_venta...")
    
    df_clean = df.select(
        trim(upper(col("cod_ticket"))).alias("cod_ticket"),
        col("sk_cliente").cast(IntegerType()).alias("sk_cliente"),
        col("sk_producto").cast(IntegerType()).alias("sk_producto"),
        col("sk_tienda").cast(IntegerType()).alias("sk_tienda"),
        col("sk_periodo").cast(IntegerType()).alias("sk_periodo"),
        # Transformación CRÍTICA: Si sk_promocion es NULL, poner -1 (para integridad referencial)
        when(
            col("sk_promocion").isNull(),
            lit(-1)
        ).otherwise(col("sk_promocion")).cast(IntegerType()).alias("sk_promocion"),
        col("num_secuencia").cast(IntegerType()).alias("num_secuencia"),
        col("monto_venta_bruta").cast(FloatType()).alias("monto_venta_bruta"),
        col("monto_venta_neta").cast(FloatType()).alias("monto_venta_neta"),
        col("monto_margen").cast(FloatType()).alias("monto_margen"),
        col("monto_descuento").cast(FloatType()).alias("monto_descuento")
    )
    
    # Filtrar registros con claves foráneas nulas (excepto sk_promocion que ya manejamos)
    df_clean = df_clean.filter(
        col("sk_cliente").isNotNull() &
        col("sk_producto").isNotNull() &
        col("sk_tienda").isNotNull() &
        col("sk_periodo").isNotNull()
    )
    
    # Rellenar montos nulos con 0 y num_secuencia por defecto a 1
    df_clean = df_clean.fillna({
        "monto_venta_bruta": 0.0,
        "monto_venta_neta": 0.0,
        "monto_margen": 0.0,
        "monto_descuento": 0.0,
        "num_secuencia": 1
    })
    
    # Validación de negocio: montos no pueden ser negativos
    df_clean = df_clean.filter(
        (col("monto_venta_bruta") >= 0) &
        (col("monto_venta_neta") >= 0)
    )
    
    print(f"[SUCCESS] fact_venta transformada: {df_clean.count()} registros")
    return df_clean

# ============================================================================
# ESCRITURA A BIGQUERY
# ============================================================================

def write_to_bigquery(df, table_name, bq_table):
    """Escribe un DataFrame a BigQuery"""
    try:
        print(f"[INFO] Escribiendo {table_name} a BigQuery: {bq_table}")
        
        df.write \
            .format("bigquery") \
            .option("table", bq_table) \
            .option("temporaryGcsBucket", BUCKET) \
            .mode("overwrite") \
            .save()
        
        print(f"[SUCCESS] {table_name} escrita exitosamente")
        
    except Exception as e:
        print(f"[ERROR] Error al escribir {table_name}: {str(e)}")
        raise

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del ETL"""
    print("="*80)
    print("INICIANDO ETL CURATED JOB")
    print("="*80)
    
    # 1. Crear sesión Spark
    spark = create_spark_session()
    
    try:
        # 2. DIMENSIÓN CLIENTE
        df_cliente_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_cliente"], "dim_cliente")
        df_cliente_curated = transform_dim_cliente(df_cliente_raw)
        write_to_bigquery(df_cliente_curated, "dim_cliente", BQ_TABLES["dim_cliente"])
        
        # 3. DIMENSIÓN PERIODO
        df_periodo_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_periodo"], "dim_periodo")
        df_periodo_curated = transform_dim_periodo(df_periodo_raw)
        write_to_bigquery(df_periodo_curated, "dim_periodo", BQ_TABLES["dim_periodo"])
        
        # 4. DIMENSIÓN PRODUCTO
        df_producto_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_producto"], "dim_producto")
        df_producto_curated = transform_dim_producto(df_producto_raw)
        write_to_bigquery(df_producto_curated, "dim_producto", BQ_TABLES["dim_producto"])
        
        # 5. DIMENSIÓN PROMOCIÓN
        df_promocion_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_promocion"], "dim_promocion")
        df_promocion_curated = transform_dim_promocion(df_promocion_raw)
        write_to_bigquery(df_promocion_curated, "dim_promocion", BQ_TABLES["dim_promocion"])
        
        # 6. DIMENSIÓN TIENDA
        df_tienda_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_tienda"], "dim_tienda")
        df_tienda_curated = transform_dim_tienda(df_tienda_raw)
        write_to_bigquery(df_tienda_curated, "dim_tienda", BQ_TABLES["dim_tienda"])
        
        # 7. TABLA DE HECHOS (FACT)
        df_venta_raw = load_csv_from_gcs(spark, GCS_PATHS["fact_venta"], "fact_venta")
        df_venta_curated = transform_fact_venta(df_venta_raw)
        write_to_bigquery(df_venta_curated, "fact_venta", BQ_TABLES["fact_venta"])
        
        print("="*80)
        print("ETL COMPLETADO EXITOSAMENTE")
        print("="*80)
        
    except Exception as e:
        print(f"[FATAL ERROR] El ETL falló: {str(e)}")
        sys.exit(1)
    
    finally:
        spark.stop()
        print("[INFO] Sesión Spark cerrada")

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
