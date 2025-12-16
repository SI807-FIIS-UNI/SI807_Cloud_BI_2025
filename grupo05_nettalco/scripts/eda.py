import pandas as pd
import logging
from io import StringIO
import os


BUCKET_NAME = "bi-examen-final" 
NUEVO_ARCHIVO = "Flight_delay.csv"
LOCAL_RAW_PATH = f"./{NUEVO_ARCHIVO}" 

PROCESSED_FILENAME = f"processed_{NUEVO_ARCHIVO}"
LOCAL_PROCESSED_PATH = f"./{PROCESSED_FILENAME}" 

logging.basicConfig(filename='docs/eda_logs.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info(f"Iniciando EDA desde archivo local: {LOCAL_RAW_PATH}")

try:
    df = pd.read_csv(LOCAL_RAW_PATH, encoding='utf-8')
    
    logging.info("--- HEAD (Primeras 5 filas) ---")
    logging.info('\n' + df.head().to_string())

    logging.info("\n--- INFO (Tipos de Datos y Nulos) ---")
    buffer = StringIO()
    df.info(buf=buffer)
    logging.info('\n' + buffer.getvalue())
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    
    delay_cols = ['ArrDelay', 'DepDelay', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    
    for col in delay_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0).astype(int) 
    
    total_flights = len(df)
    delayed_flights = df[df['DepDelay'] > 0].shape[0]
    percent_delayed = (delayed_flights / total_flights) * 100
    
    logging.info("\n--- Estadísticas Descriptivas de Retrasos (Minutos) ---")
    logging.info(df[delay_cols].describe().to_string())
    logging.info(f"\nKPI EDA: Porcentaje de vuelos con retraso en salida (>0 min): {percent_delayed:.2f}%")

    df.to_csv(LOCAL_PROCESSED_PATH, index=False)
    logging.info(f"\nArchivo procesado guardado localmente en: {LOCAL_PROCESSED_PATH}")
    logging.info("EDA finalizado. Listo para subir a GCS y continuar con el ETL.")

except Exception as e:
    logging.error(f"Error durante el EDA: {e}")