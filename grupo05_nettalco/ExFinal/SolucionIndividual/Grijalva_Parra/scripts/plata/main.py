from google.cloud import dataproc_v1
import os

PROJECT_ID = "us-accidents-481401"
REGION = "us-central1"
CLUSTER = "us-accidents-cluster"

def run_etl_plata(request):
    client = dataproc_v1.JobControllerClient(
        client_options={"api_endpoint": f"{REGION}-dataproc.googleapis.com:443"}
    )

    job = {
        "placement": {"cluster_name": CLUSTER},
        "pyspark_job": {
            "main_python_file_uri": "gs://us-accidents-bd/scripts/etl_plata.py"
        }
    }

    client.submit_job(
        project_id=PROJECT_ID,
        region=REGION,
        job=job
    )

    return "ETL PLATA LANZADO", 200