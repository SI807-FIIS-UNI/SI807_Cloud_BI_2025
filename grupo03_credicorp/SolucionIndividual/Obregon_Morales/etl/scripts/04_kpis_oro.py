"""
SCRIPT 04: KPIs - AIR QUALITY (POR FECHA Y CIUDAD)
Capa ORO - Azure Blob Storage
"""

from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import datetime
import io
import os
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class KPIsOroAzure:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        logger.info("Inicializando conexión a Azure Blob Storage")

        self.client = BlobServiceClient.from_connection_string(
            ""
        )

        self.container_client = self.client.get_container_client("datalake")
        logger.info("Conexión a Azure Blob Storage establecida correctamente")

    def subir(self, df, nombre):
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)

        ruta_blob = f"oro/kpis/{nombre}_{self.timestamp}.csv"

        self.container_client.upload_blob(
            name=ruta_blob,
            data=buffer.getvalue(),
            overwrite=True
        )

        logger.info(f"KPI subido correctamente a Azure Blob: {ruta_blob}")


if __name__ == "__main__":

    logger.info("INICIANDO GENERACIÓN DE KPIs - CAPA ORO")


    logger.info("Cargando tablas de la capa PLATA")

    fact = pd.read_csv("data/plata/fact_air_quality.csv")
    dim_city = pd.read_csv("data/plata/dim_city.csv")
    dim_date = pd.read_csv("data/plata/dim_date.csv")

    logger.info(f"Fact cargada: {fact.shape}")
    logger.info(f"Dim City cargada: {dim_city.shape}")
    logger.info(f"Dim Date cargada: {dim_date.shape}")

    dim_city.columns = dim_city.columns.str.strip().str.lower()
    dim_date.columns = dim_date.columns.str.strip().str.lower()

 
    col_city_name = next(c for c in dim_city.columns if c != "city_id")
    col_date_value = next(c for c in dim_date.columns if c != "date_id")

    logger.info(f"Columna ciudad detectada: {col_city_name}")
    logger.info(f"Columna fecha detectada: {col_date_value}")

    logger.info("Enriqueciendo tabla de hechos con dimensiones")

    df = (
        fact
        .merge(dim_city, on="city_id", how="left")
        .merge(dim_date, on="date_id", how="left")
    )

    logger.info(f"Dataset luego de cruzar dimenciones por hechos: {df.shape}")


    kpi = (
        df
        .groupby([col_date_value, col_city_name])
        .agg(
            AQI_promedio=("AQI", "mean"),
            PM25_promedio=("PM2.5", "mean"),
            PM10_promedio=("PM10", "mean"),
            NO2_promedio=("NO2", "mean"),
            CO_promedio=("CO", "mean")
        )
        .reset_index()
    )

    kpi[
        [
            "AQI_promedio",
            "PM25_promedio",
            "PM10_promedio",
            "NO2_promedio",
            "CO_promedio"
        ]
    ] = kpi[
        [
            "AQI_promedio",
            "PM25_promedio",
            "PM10_promedio",
            "NO2_promedio",
            "CO_promedio"
        ]
    ].round(2)

    kpi["fecha_proceso"] = datetime.now()

    logger.info(f"KPIs generados: {kpi.shape}")


    os.makedirs("data/oro", exist_ok=True)
    kpi_path = "data/oro/kpi_air_quality_fecha_ciudad.csv"
    kpi.to_csv(kpi_path, index=False)

    logger.info(f"KPI guardado localmente en: {kpi_path}")

    oro = KPIsOroAzure()
    oro.subir(kpi, "kpi_air_quality_fecha_ciudad")

    logger.info("✓ PROCESO CAPA ORO FINALIZADO CORRECTAMENTE")
