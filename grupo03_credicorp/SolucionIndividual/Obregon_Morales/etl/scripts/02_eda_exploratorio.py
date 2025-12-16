"""
SCRIPT 03: CAPA PLATA - AIR QUALITY
"""

from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import datetime
import io
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransformadorPlataAzure:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.container = "datalake"
        self.conn_str = "AZURE_CONNECTION_STRING"
        self.client = BlobServiceClient.from_connection_string(self.conn_str)
        self.container_client = self.client.get_container_client(self.container)

    def subir_dataframe(self, df, ruta):
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        self.container_client.upload_blob(ruta, buffer.getvalue(), overwrite=True)

if __name__ == "__main__":

    df = pd.read_csv("data/city_day.csv")

    # DIM CITY
    dim_city = df[["City"]].drop_duplicates().reset_index(drop=True)
    dim_city["city_id"] = dim_city.index + 1

    # DIM DATE
    df["Date"] = pd.to_datetime(df["Date"])
    dim_date = df[["Date"]].drop_duplicates().reset_index(drop=True)
    dim_date["date_id"] = dim_date.index + 1

    # FACT
    fact = (
        df.merge(dim_city, on="City")
          .merge(dim_date, on="Date")
    )

    fact = fact[
        ["city_id", "date_id", "PM2.5", "PM10", "NO2", "CO", "AQI"]
    ]

    os.makedirs("data/plata", exist_ok=True)
    dim_city.to_csv("data/plata/dim_city.csv", index=False)
    dim_date.to_csv("data/plata/dim_date.csv", index=False)
    fact.to_csv("data/plata/fact_air_quality.csv", index=False)

    plata = TransformadorPlataAzure()
    plata.subir_dataframe(dim_city, f"plata/dim_city_{plata.timestamp}.csv")
    plata.subir_dataframe(dim_date, f"plata/dim_date_{plata.timestamp}.csv")
    plata.subir_dataframe(fact, f"plata/fact_air_quality_{plata.timestamp}.csv")
