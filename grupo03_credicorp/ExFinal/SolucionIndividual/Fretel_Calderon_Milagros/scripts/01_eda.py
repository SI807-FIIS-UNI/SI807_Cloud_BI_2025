import pandas as pd
import os
from datetime import datetime

# Ruta del dataset (repositorio local)
DATA_PATH = "bronce/raw/SuperMarket Analysis.csv"

# Crear carpeta de logs si no existe
os.makedirs("docs/logs", exist_ok=True)

# Cargar dataset
df = pd.read_csv(DATA_PATH)

# Información básica
print("=== INFO DEL DATASET ===")
print(df.info())

print("\n=== PRIMERAS FILAS ===")
print(df.head())

print("\n=== VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())

print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
print(df.describe())

# Guardar log simple
log_path = f"docs/logs/eda_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(log_path, "w", encoding="utf-8") as f:
    f.write("EDA ejecutado correctamente\n")
    f.write(f"Filas: {df.shape[0]}\n")
    f.write(f"Columnas: {df.shape[1]}\n")

print(f"\nEDA finalizado. Log guardado en {log_path}")
