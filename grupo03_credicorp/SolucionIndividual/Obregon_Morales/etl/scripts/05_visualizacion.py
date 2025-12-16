"""
SCRIPT 05: DASHBOARD - AIR QUALITY INDIA
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class DashboardAirQuality:
    def __init__(self):
        self.df = pd.read_csv("data/oro/kpi_air_quality.csv")
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        os.makedirs("dashboards", exist_ok=True)

    def generar(self):
        fig, ax = plt.subplots(figsize=(10,6))

        valores = [
            self.df["AQI_promedio"][0],
            self.df["PM25_promedio"][0],
            self.df["PM10_promedio"][0]
        ]

        ax.bar(
            ["AQI", "PM2.5", "PM10"],
            valores
        )

        ax.set_title("Indicadores Promedio de Calidad del Aire - India")
        plt.savefig(f"dashboards/air_quality_{self.timestamp}.png", dpi=300)
        plt.close()

if __name__ == "__main__":
    DashboardAirQuality().generar()
