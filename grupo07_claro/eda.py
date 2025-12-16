import pandas as pd
import sys
from google.cloud import storage
import io

# Recibimos el nombre del bucket como argumento
BUCKET_NAME = sys.argv[1]
FILE_PATH = "bronce/raw/dataset_citas.csv"

def run_eda():
    print(f"--- INICIANDO EDA PARA: {FILE_PATH} ---")
    
    # 1. Conectar a Cloud Storage y descargar el archivo en memoria
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_PATH)
    content = blob.download_as_string()
    
    # 2. Leer con Pandas
    df = pd.read_csv(io.BytesIO(content))

    # 3. Generar Reporte de Calidad
    buffer = io.StringIO()
    
    buffer.write("=== REPORTE EDA (EVIDENCIA) ===\n")
    buffer.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}\n\n")
    
    buffer.write("--- 1. Primeras 5 filas ---\n")
    buffer.write(df.head().to_string() + "\n\n")
    
    buffer.write("--- 2. Tipos de Datos e Info ---\n")
    df.info(buf=buffer)
    buffer.write("\n\n")
    
    buffer.write("--- 3. Conteo de Nulos ---\n")
    nulls = df.isnull().sum()
    buffer.write(nulls[nulls > 0].to_string() if nulls.sum() > 0 else "Sin nulos encontrados")
    buffer.write("\n\n")

    buffer.write("--- 4. Estadisticas Numericas ---\n")
    buffer.write(df.describe().to_string() + "\n")

    # 4. Mostrar en pantalla y guardar en archivo
    reporte = buffer.getvalue()
    print(reporte)
    
    # Guardar evidencia en la carpeta docs (Requisito del examen)
    with open("docs/evidencia_eda.txt", "w") as f:
        f.write(reporte)
    print("\n[EXITO] Evidencia guardada en: docs/evidencia_eda.txt")

if __name__ == "__main__":
    run_eda()
