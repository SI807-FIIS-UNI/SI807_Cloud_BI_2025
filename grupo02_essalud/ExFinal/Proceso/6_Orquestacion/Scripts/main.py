import functions_framework
from google.cloud import dataproc_v1 as dataproc
import uuid


@functions_framework.cloud_event
def validar_archivo(cloud_event):
    data = cloud_event.data
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"📂 Evento recibido para: {file_name}")

    # ==========================================
    # 1. ESCUDO ANTI-BUCLES
    # ==========================================
    archivos_validos = [
        "bronce/Diabetes.csv",
        "bronce/Hipertension.csv",
        "bronce/Obesidad.csv",
    ]

    if file_name not in archivos_validos:
        print(f"⛔ Archivo ignorado. No es parte del trigger.")
        return "Ignorado"

    # ==========================================
    # 2. CONFIGURACIÓN "LOW COST" (PARA EVITAR ERROR DE QUOTA)
    # ==========================================
    print(f"✅ Iniciando Dataproc modo económico...")

    project_id = "grupo2-essalud"
    region = "us-central1"

    client = dataproc.BatchControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )

    batch = dataproc.Batch()
    batch.pyspark_batch.main_python_file_uri = (
        f"gs://{bucket_name}/scripts/etl_script.py"
    )

    batch.runtime_config.properties = {
        "spark.driver.cores": "4",  # Mínimo permitido es 4
        "spark.executor.cores": "4",  # Mínimo permitido es 4
        "spark.executor.instances": "2",  # Mínimo inicial permitido es 2
        "spark.dynamicAllocation.mode": "OFF",  # Mantenemos esto OFF para que no escale y gastes de más
    }

    batch.runtime_config.version = "2.2"
    batch_id_seguro = f"etl-{uuid.uuid4().hex[:8]}"

    parent = f"projects/{project_id}/locations/{region}"

    try:
        operation = client.create_batch(
            request={"parent": parent, "batch": batch, "batch_id": batch_id_seguro}
        )
        print(f"🚀 Job enviado: {operation.operation.name}")
        return "Job Enviado"

    except Exception as e:
        print(f"❌ Error al enviar a Dataproc: {e}")
        raise e
