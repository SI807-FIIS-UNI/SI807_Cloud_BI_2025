import functions_framework
from google.cloud import bigquery
from datetime import datetime

# Configuración de tablas y carpetas
TABLES_TO_LOAD = {
    "total_prendas_por_talla": "ventas_nettalco.total_prendas_por_talla",
    "volumen_ventas_por_cliente": "ventas_nettalco.volumen_ventas_por_cliente",
    "fecha_ventas": "ventas_nettalco.fecha_ventas",
    "tendencias_ventas_por_franja_horaria": "ventas_nettalco.tendencias_ventas_por_franja_horaria",
    "productos_mas_vendidos": "ventas_nettalco.productos_mas_vendidos",
    "eficiencia_operativa": "ventas_nettalco.eficiencia_operativa",
    "indice_ventas_cliente": "ventas_nettalco.indice_ventas_cliente",
    "prediccion_ventas": "ventas_nettalco.prediccion_ventas",
    "comportamiento_clientes": "ventas_nettalco.comportamiento_clientes"
}

BUCKET = "nettalco-data-bd_grupo05"
PREFIX = "refined/curated"

client = bigquery.Client()
SCRIPT_NAME = "daily_bq_update.py"  # Para registrar en log

def load_csv_to_bq(table_name, gcs_path):
    """
    Carga CSV desde GCS a BigQuery y reemplaza datos existentes.
    """
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"  # reemplaza datos existentes
    )
    load_job = client.load_table_from_uri(
        gcs_path,
        table_name,
        job_config=job_config
    )
    load_job.result()  # espera a que termine
    print(f"Cargado {gcs_path} a {table_name}")
    log_update(table_name)

def log_update(table_name):
    table_id = "ventas_nettalco.log"
    rows_to_insert = [
        {
            "tabla": table_name,
            "fecha_actualizacion": datetime.utcnow().isoformat(),  # convierte a string
            "fuente": SCRIPT_NAME
        }
    ]
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print(f"Error insertando log para {table_name}: {errors}")
    else:
        print(f"Log insertado correctamente para {table_name}")

@functions_framework.http
def load_refined_to_bq(request):
    """
    Función HTTP que recorre todas las carpetas de refined/curated y carga CSV a BigQuery.
    Luego inserta un log por cada tabla cargada.
    """
    try:
        for folder, table in TABLES_TO_LOAD.items():
            gcs_path = f"gs://{BUCKET}/{PREFIX}/{folder}/*.csv"
            print(f"Cargando {gcs_path} a {table}")
            load_csv_to_bq(table, gcs_path)
        return "Carga completa a BigQuery y logs insertados", 200
    except Exception as e:
        print(f"Error ejecutando load_refined_to_bq: {e}")
        return f"Error en la carga: {e}", 500