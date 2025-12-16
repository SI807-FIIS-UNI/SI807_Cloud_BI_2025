"""
SCRIPT 01: INGESTA - CAPA BRONCE (AIR QUALITY - INDIA)
"""

from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import pandas as pd
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestorBronceAzure:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.container = "datalake"

        self.conn_str = ""
        if not self.conn_str:
            raise ValueError("Falta AZURE_STORAGE_CONNECTION_STRING")

        self.blob_service = BlobServiceClient.from_connection_string(self.conn_str)
        self.container_client = self.blob_service.get_container_client(self.container)

        try:
            self.container_client.create_container()
        except ResourceExistsError:
            pass

    def cargar_csv_local(self, path):
        df = pd.read_csv(path)
        logger.info(f"✓ CSV cargado: {df.shape}")
        return df

    def subir_a_bronce_raw(self, filepath, dataset_name):
        blob_path = f"bronce/raw/{dataset_name}.csv"
        with open(filepath, "rb") as data:
            self.container_client.upload_blob(
                name=blob_path,
                data=data,
                overwrite=True
            )
        logger.info(f"✓ Subido a Bronce: {blob_path}")
        self._guardar_evidencia(blob_path)

    def _guardar_evidencia(self, mensaje):
        os.makedirs("docs/evidencias_ingesta", exist_ok=True)
        with open(f"docs/evidencias_ingesta/log_{self.timestamp}.txt", "w") as f:
            f.write(f"Ingesta completada\nArchivo: {mensaje}")

if __name__ == "__main__":
    ingestor = IngestorBronceAzure()
    ingestor.cargar_csv_local("data/city_day.csv")
    ingestor.subir_a_bronce_raw(
        "data/city_day.csv",
        "finalbi"
    )