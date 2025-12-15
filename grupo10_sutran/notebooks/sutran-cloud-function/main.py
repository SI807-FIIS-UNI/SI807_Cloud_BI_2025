import os
from google.cloud import dataproc_v1

def trigger_dataproc_job(event, context):
    file = event
    file_name = file['name']  # ej: raw/BBDD_ONSV-PERSONAS_2021-2023.csv
    print(f"Archivo detectado: {file_name}")

    if not file_name.startswith("raw/"):
        print("Archivo fuera de /raw/, se ignora.")
        return

    project_id = os.environ['PROJECT_ID']
    region = os.environ['REGION']
    cluster = os.environ['CLUSTER']

    job_client = dataproc_v1.JobControllerClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )

    job = {
        "placement": {"cluster_name": cluster},
        "pyspark_job": {
            "main_python_file_uri": f"gs://sutran-bucket-mr/scripts/etl_master.py",
            "args": [file_name]
        },
    }

    result = job_client.submit_job(
        project_id=project_id,
        region=region,
        job=job
    )

    print(f"✅ Job lanzado: {result.reference.job_id}")
