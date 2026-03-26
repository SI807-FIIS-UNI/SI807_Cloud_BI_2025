import functions_framework
import json
import base64
from google.cloud import secretmanager
from google.cloud import dataproc_v1

def load_config():
    """
    Carga la configuración desde Secret Manager
    """
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/467475048380/secrets/nettalco_config/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return json.loads(response.payload.data.decode("utf-8"))

@functions_framework.cloud_event
def trigger_dataproc(cloud_event):
    """
    Cloud Function 2nd gen disparada por Pub/Sub cuando llega un archivo a raw/.
    Lanza un Job en Dataproc usando la configuración desde Secret Manager.
    """
    try:
        # Leer configuración
        config = load_config()
        project_id = config["PROJECT_ID"]
        region = config["REGION"]
        cluster_name = config["CLUSTER_NAME"]
        pyspark_file = config["PYSPARK_FILE"]

        # Extraer mensaje de Pub/Sub
        pubsub_message = cloud_event.data.get("message")
        if not pubsub_message or "data" not in pubsub_message:
            print("No se encontró el mensaje de Pub/Sub o 'data' vacío. Ignorando.")
            return

        # Decodificar base64 y parsear JSON
        payload = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        event_data = json.loads(payload)

        # Obtener el nombre real del archivo
        file_name = event_data.get("name")
        if not file_name:
            print("No se encontró el nombre del archivo en el evento. Ignorando.")
            return

        # Verificar que esté en raw/
        if "raw/" not in file_name:
            print(f"Ignorando archivo que no está en raw/: {file_name}")
            return

        print(f"Nuevo archivo detectado en raw/: {file_name}")

        # Crear cliente Dataproc
        job_client = dataproc_v1.JobControllerClient(
            client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
        )

        # Configurar Job PySpark
        job = {
            "placement": {"cluster_name": cluster_name},
            "pyspark_job": {
                "main_python_file_uri": pyspark_file,
                "args": [f"gs://{project_id}-bd_grupo05/{file_name}"]
            },
        }

        # Enviar Job a Dataproc
        response = job_client.submit_job(
            project_id=project_id,
            region=region,
            job=job
        )
        print(f"Dataproc Job lanzado correctamente: {response.reference.job_id}")

    except Exception as e:
        print(f"Error al lanzar Dataproc Job: {e}")
        raise