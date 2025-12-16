import io
import logging
import pandas as pd
from google.cloud import storage


# -----------------------
# UTIL: leer excel desde GCS
# -----------------------

def leer_excel_desde_gcs(bucket_name, file_name, sheet_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        content = blob.download_as_bytes()

        try:
            # XLS (solo funciona con xlrd==1.2.0)
            return pd.read_excel(io.BytesIO(content), sheet_name=sheet_name, header=None, dtype=str, engine="xlrd")
        except Exception:
            # XLSX
            return pd.read_excel(io.BytesIO(content), sheet_name=sheet_name, header=None, dtype=str)

    except Exception as e:
        logging.exception(f"Error al leer archivo {file_name}: {e}")
        return None