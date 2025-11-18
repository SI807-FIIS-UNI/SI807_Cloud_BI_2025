"""
Cloud Function Trigger - Automatización de ETL
Proyecto: grupo09_retail_analytics
Autor: Grupo 9
"""

import functions_framework
from google.cloud import dataproc_v1
from datetime import datetime

@functions_framework.http
def trigger_etl(request):
    """
    Función que ejecuta el job de Dataproc Serverless
    """
    project_id = "etl-retail-analytics"
    region = "us-central1"
    
    # Crear nombre único con timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    batch_id = f"etl-curated-job-g9-{timestamp}"
    
    # Configurar cliente de Dataproc
    client = dataproc_v1.BatchControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )
    
    # Configurar el batch
    batch = dataproc_v1.Batch()
    batch.pyspark_batch = dataproc_v1.PySparkBatch()
    batch.pyspark_batch.main_python_file_uri = "gs://mi-etl-proyecto-2025/scripts/etl_curated_job.py"
    batch.pyspark_batch.jar_file_uris = [
        "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.32.2.jar"
    ]
    
    batch.runtime_config = dataproc_v1.RuntimeConfig()
    batch.runtime_config.version = "1.1"
    batch.runtime_config.properties = {
        "spark.executor.cores": "4",
        "spark.executor.memory": "16g",
        "spark.executor.instances": "2",
        "spark.dynamicAllocation.enabled": "false"
    }
    
    batch.environment_config = dataproc_v1.EnvironmentConfig()
    batch.environment_config.execution_config = dataproc_v1.ExecutionConfig()
    batch.environment_config.execution_config.subnetwork_uri = "default"
    
    # Enviar el batch
    parent = f"projects/{project_id}/locations/{region}"
    operation = client.create_batch(
        parent=parent,
        batch=batch,
        batch_id=batch_id
    )
    
    return {
        "status": "success",
        "batch_id": batch_id,
        "message": f"ETL job iniciado: {batch_id}"
    }
