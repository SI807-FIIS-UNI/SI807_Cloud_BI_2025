from google.cloud import dataproc_v1

PROJECT_ID = "us-accidents-481401"
REGION = "us-central1"
CLUSTER_NAME = "us-accidents-cluster"

def run_etl_oro(request):
    client = dataproc_v1.JobControllerClient(
        client_options={
            "api_endpoint": f"{REGION}-dataproc.googleapis.com:443"
        }
    )

    job = {
        "placement": {
            "cluster_name": CLUSTER_NAME
        },
        "pyspark_job": {
            "main_python_file_uri": "gs://us-accidents-bd/scripts/etl_oro.py"
        }
    }

    client.submit_job(
        project_id=PROJECT_ID,
        region=REGION,
        job=job
    )

    return "ETL ORO lanzado correctamente", 200