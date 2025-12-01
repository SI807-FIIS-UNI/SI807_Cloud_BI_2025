"""
DAG de Airflow para ejecutar el ETL de Interbank Trading usando un clúster
efímero de Dataproc en Google Cloud Platform.

Este pipeline realiza lo siguiente:

1. Crea dinámicamente un clúster Dataproc (patrón efímero).
2. Ejecuta un job PySpark ubicado en Cloud Storage (etl_completo.py),
   el cual contiene las transformaciones del ETL:
      - limpieza
      - tipificación
      - joins
      - normalización
      - carga a BigQuery
3. Elimina el clúster después de la ejecución para reducir costos.
4. Está programado para ejecutarse automáticamente cada día a la 1 AM.

"""

from __future__ import annotations
import datetime

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
)

# ----------------- ⚙ VARIABLES DE GCP -----------------
PROJECT_ID = "project-sin-477115"
REGION = "us-central1"
CLUSTER_NAME = "etl-cluster-batch"
DATAPROC_SA = "sagr01-dataproc-job@project-sin-477115.iam.gserviceaccount.com"

# Ruta en Cloud Storage donde estará el script PySpark del ETL
SPARK_ETL_SCRIPT = "gs://project-sin-477115-staging/scripts/etl_completo.py"

# Configuración del clúster Dataproc
CLUSTER_CONFIG = {
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "n2-standard-2",
        "disk_config": {"boot_disk_size_gb": 100},
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "n2-standard-2",
        "disk_config": {"boot_disk_size_gb": 100},
    },
    "software_config": {"image_version": "2.1-debian11"},
    "gce_cluster_config": {
        "service_account": DATAPROC_SA,
        "subnetwork_uri": (
            f"projects/{PROJECT_ID}/regions/{REGION}/subnetworks/my-subnet-private-01"
        ),
        "tags": ["dataproc-cluster-tag"],
        "metadata": {"enable-component-gateway": "true"},
    },
}

# Definición del job PySpark
SPARK_JOB = {
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {
        "main_python_file_uri": SPARK_ETL_SCRIPT,
        "args": [
            f"gs://{PROJECT_ID}-raw/ingesta/",
            f"{PROJECT_ID}:refined_data.fact_ventas_diarias",
        ],
    },
}

# ----------------- 🛠 DEFINICIÓN DEL WORKFLOW -----------------
with DAG(
    dag_id="etl_trading_interbank_gcp",
    description="Pipeline ETL completo con Dataproc (clúster efímero)",
    schedule_interval="0 1 * * *",  # Se ejecuta todos los días a la 1 AM
    start_date=datetime.datetime(2025, 12, 1),
    catchup=False,
    tags=["dataproc", "etl", "spark"],
):

    # Crear clúster Dataproc
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME,
    )

    # Ejecutar el ETL PySpark
    submit_spark_job = DataprocSubmitJobOperator(
        task_id="submit_spark_job",
        job=SPARK_JOB,
        region=REGION,
        project_id=PROJECT_ID,
    )

    # Eliminar clúster al finalizar
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_dataproc_cluster",
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=REGION,
        trigger_rule="all_done",
    )

    # Flujo del pipeline
    create_cluster >> submit_spark_job >> delete_cluster
