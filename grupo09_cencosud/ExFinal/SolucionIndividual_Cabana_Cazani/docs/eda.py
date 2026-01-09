import pandas as pd

# CONFIGURACIÓN EXACTA SEGÚN TU IMAGEN
BUCKET = "examen-bi-practica-1765740324"
RUTA_ARCHIVO = f"gs://{BUCKET}/bronce/raw/ventas_examen.csv"

print(f"--- 1. LEYENDO DATOS DE: {RUTA_ARCHIVO} ---")

try:
    # Leer el CSV directamente desde Google Cloud Storage
    df = pd.read_csv(RUTA_ARCHIVO)
    
    # Análisis Exploratorio (EDA)
    print("\n--- [2] PRIMERAS 5 FILAS (HEAD) ---")
    print(df.head())
    
    print("\n--- [3] INFORMACIÓN (INFO) ---")
    print(df.info())
    
    print("\n--- [4] ESTADÍSTICAS (DESCRIBE) ---")
    print(df.describe())
    
    print("\n✅ ¡EDA FINALIZADO CORRECTAMENTE!")

except Exception as e:
    print(f"\n❌ ERROR CRÍTICO: {e}")
    print("Consejo: Verifica que el archivo exista en esa ruta exacta.")
