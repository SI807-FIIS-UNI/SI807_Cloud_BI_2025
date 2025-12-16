import pandas as pd
import sys

# Recibimos el bucket como argumento
BUCKET = sys.argv[1]
RUTA = f"gs://{BUCKET}/bronce/raw/city_day.csv"

print(f"--- 🔎 REPORTE DE CALIDAD DE DATOS (EDA) ---")
print(f"Archivo: {RUTA}")

try:
    df = pd.read_csv(RUTA)
    
    print("\n[1] VISTA PREVIA:")
    print(df.head(3))
    
    print("\n[2] ESTRUCTURA:")
    print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
    
    print("\n[3] CONTEO DE NULOS (Importante para limpieza):")
    # Filtramos solo las que tienen nulos para que sea legible
    nulos = df.isnull().sum()
    print(nulos[nulos > 0])
    
    print("\n[4] ESTADÍSTICAS BÁSICAS (AQI):")
    print(df['AQI'].describe())
    
    print("\n✅ EDA COMPLETADO")

except Exception as e:
    print(f"❌ Error leyendo el archivo: {e}")
