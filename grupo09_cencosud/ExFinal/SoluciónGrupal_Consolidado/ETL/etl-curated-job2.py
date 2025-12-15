"""
ETL Curated Job 
Proyecto: pc4-si807-g9
Script: etl_curated_job2.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, upper, lower, when, to_date, 
    regexp_replace, lit
)
from pyspark.sql.types import IntegerType, FloatType
import sys

def create_spark_session():
    spark = SparkSession.builder \
        .appName("ETL-PC4-Job-G9-V2") \
        .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12.jar") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    print(f"[INFO] Sesión Spark iniciada: {spark.version}")
    return spark

# CONFIGURACIÓN
PROJECT_ID = "pc4-si807-g9"
DATASET = "dataset_si807_g9"
BUCKET = "pc4-si807-g9-bucket"

GCS_PATHS = {
    "dim_cliente": f"gs://{BUCKET}/raw/dim_cliente/*.csv",
    "dim_periodo": f"gs://{BUCKET}/raw/dim_periodo/*.csv",
    "dim_producto": f"gs://{BUCKET}/raw/dim_producto/*.csv",
    "dim_promocion": f"gs://{BUCKET}/raw/dim_promocion_precio/*.csv",
    "dim_tienda": f"gs://{BUCKET}/raw/dim_tienda_canal/*.csv",
    "fact_venta": f"gs://{BUCKET}/raw/fact_hecho_venta/*.csv"
}

BQ_TABLES = {
    "dim_cliente": f"{PROJECT_ID}.{DATASET}.dim_cliente_curated",
    "dim_periodo": f"{PROJECT_ID}.{DATASET}.dim_periodo_curated",
    "dim_producto": f"{PROJECT_ID}.{DATASET}.dim_producto_curated",
    "dim_promocion": f"{PROJECT_ID}.{DATASET}.dim_promocion_precio_curated",
    "dim_tienda": f"{PROJECT_ID}.{DATASET}.dim_tienda_canal_curated",
    "fact_venta": f"{PROJECT_ID}.{DATASET}.fact_hecho_venta_curated"
}

def load_csv_from_gcs(spark, path, table_name):
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

def transform_dim_cliente(df):
    print("[INFO] Transformando dim_cliente...")
    df_clean = df.select(
        col("sk_cliente").cast(IntegerType()).alias("sk_cliente"),
        trim(upper(col("cod_cliente"))).alias("cod_cliente"),
        trim(upper(col("cod_tipo_cliente"))).alias("cod_tipo_cliente"),
        when(
            (col("desc_tipo_cliente").isNull()) | (trim(col("desc_tipo_cliente")) == ""),
            upper(col("cod_tipo_cliente"))
        ).otherwise(upper(col("desc_tipo_cliente"))).alias("desc_tipo_cliente"),
        when(
            (col("estado_cliente").isNull()) | (trim(col("estado_cliente")) == ""),
            lit("DESCONOCIDO")
        ).otherwise(upper(col("estado_cliente"))).alias("estado_cliente"),
        when(
            (col("numero_tarjeta_bonus").isNull()) | 
            (trim(col("numero_tarjeta_bonus")) == "") |
            (lower(col("numero_tarjeta_bonus")) == "nan"),
            lit("SIN TARJETA")
        ).otherwise(col("numero_tarjeta_bonus").cast("bigint").cast("string")).alias("numero_tarjeta_bonus"),
        to_date(col("fecha_alta_cliente"), "yyyy-MM-dd").alias("fecha_alta_cliente_dt"),
        col("recencia").cast(IntegerType()).alias("recencia")
    )
    df_clean = df_clean.filter(col("sk_cliente").isNotNull())
    print(f"[SUCCESS] dim_cliente transformada: {df_clean.count()} registros")
    return df_clean

def transform_dim_periodo(df):
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
    print("[INFO] Transformando dim_producto...")
    df_clean = df.select(
        col("sk_producto").cast(IntegerType()).alias("sk_producto"),
        trim(upper(col("cod_material"))).alias("cod_material"),
        trim(upper(col("desc_material"))).alias("desc_material"),
        trim(upper(col("categoria"))).alias("categoria"),
        trim(upper(col("subcategoria"))).alias("subcategoria"),
        when(
            (col("marca").isNull()) | (trim(col("marca")) == ""),
            lit("SIN MARCA")
        ).otherwise(upper(col("marca"))).alias("marca"),
        when(
            (col("unidad_medida").isNull()) | (trim(col("unidad_medida")) == ""),
            lit("N/A")
        ).otherwise(upper(col("unidad_medida"))).alias("unidad_medida"),
        when(
            (col("pack_size").isNull()) | (trim(col("pack_size")) == ""),
            lit("N/A")
        ).otherwise(upper(col("pack_size"))).alias("pack_size")
    )
    df_clean = df_clean.filter(col("sk_producto").isNotNull())
    print(f"[SUCCESS] dim_producto transformada: {df_clean.count()} registros")
    return df_clean

def transform_dim_promocion(df):
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
    df_clean = df_clean.filter(col("sk_promocion").isNotNull())
    print(f"[SUCCESS] dim_promocion transformada: {df_clean.count()} registros")
    return df_clean

def transform_dim_tienda(df):
    print("[INFO] Transformando dim_tienda_canal...")
    df_clean = df.select(
        col("sk_tienda").cast(IntegerType()).alias("sk_tienda"),
        trim(upper(col("cod_tienda"))).alias("cod_tienda"),
        trim(col("nombre_tienda")).alias("nombre_tienda"),
        trim(upper(col("cadena"))).alias("cadena"),
        trim(upper(col("cod_canal"))).alias("cod_canal"),
        trim(upper(col("desc_canal"))).alias("desc_canal"),
        trim(upper(col("ciudad"))).alias("ciudad"),
        regexp_replace(trim(upper(col("formato"))), "ALMACÃ©N", "ALMACÉN").alias("formato")
    )
    df_clean = df_clean.filter(col("sk_tienda").isNotNull())
    print(f"[SUCCESS] dim_tienda transformada: {df_clean.count()} registros")
    return df_clean

def transform_fact_venta(df):
    print("[INFO] Transformando fact_hecho_venta...")
    df_clean = df.select(
        trim(upper(col("cod_ticket"))).alias("cod_ticket"),
        col("sk_cliente").cast(IntegerType()).alias("sk_cliente"),
        col("sk_producto").cast(IntegerType()).alias("sk_producto"),
        col("sk_tienda").cast(IntegerType()).alias("sk_tienda"),
        col("sk_periodo").cast(IntegerType()).alias("sk_periodo"),
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
    
    df_clean = df_clean.filter(
        col("sk_cliente").isNotNull() &
        col("sk_producto").isNotNull() &
        col("sk_tienda").isNotNull() &
        col("sk_periodo").isNotNull()
    )
    
    df_clean = df_clean.fillna({
        "monto_venta_bruta": 0.0,
        "monto_venta_neta": 0.0,
        "monto_margen": 0.0,
        "monto_descuento": 0.0,
        "num_secuencia": 1
    })
    
    df_clean = df_clean.filter(
        (col("monto_venta_bruta") >= 0) &
        (col("monto_venta_neta") >= 0)
    )
    
    print(f"[SUCCESS] fact_venta transformada: {df_clean.count()} registros")
    return df_clean

def write_to_bigquery(df, table_name, bq_table):
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

def main():
    print("="*80)
    print("INICIANDO ETL-PC4-JOB - GRUPO 9 - V2")
    print("="*80)
    
    spark = create_spark_session()
    
    try:
        # CLIENTE
        df_cliente_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_cliente"], "dim_cliente")
        df_cliente_curated = transform_dim_cliente(df_cliente_raw)
        write_to_bigquery(df_cliente_curated, "dim_cliente", BQ_TABLES["dim_cliente"])
        
        # PERIODO
        df_periodo_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_periodo"], "dim_periodo")
        df_periodo_curated = transform_dim_periodo(df_periodo_raw)
        write_to_bigquery(df_periodo_curated, "dim_periodo", BQ_TABLES["dim_periodo"])
        
        # PRODUCTO
        df_producto_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_producto"], "dim_producto")
        df_producto_curated = transform_dim_producto(df_producto_raw)
        write_to_bigquery(df_producto_curated, "dim_producto", BQ_TABLES["dim_producto"])
        
        # PROMOCIÓN
        df_promocion_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_promocion"], "dim_promocion")
        df_promocion_curated = transform_dim_promocion(df_promocion_raw)
        write_to_bigquery(df_promocion_curated, "dim_promocion", BQ_TABLES["dim_promocion"])
        
        # TIENDA
        df_tienda_raw = load_csv_from_gcs(spark, GCS_PATHS["dim_tienda"], "dim_tienda")
        df_tienda_curated = transform_dim_tienda(df_tienda_raw)
        write_to_bigquery(df_tienda_curated, "dim_tienda", BQ_TABLES["dim_tienda"])
        
        # FACT
        df_venta_raw = load_csv_from_gcs(spark, GCS_PATHS["fact_venta"], "fact_venta")
        df_venta_curated = transform_fact_venta(df_venta_raw)
        write_to_bigquery(df_venta_curated, "fact_venta", BQ_TABLES["fact_venta"])
        
        print("="*80)
        print("ETL-PC4-JOB-V2 COMPLETADO EXITOSAMENTE")
        print("="*80)
        
    except Exception as e:
        print(f"[FATAL ERROR] El ETL falló: {str(e)}")
        sys.exit(1)
        
    finally:
        spark.stop()
        print("[INFO] Sesión Spark cerrada")

if __name__ == "__main__":
    main()
