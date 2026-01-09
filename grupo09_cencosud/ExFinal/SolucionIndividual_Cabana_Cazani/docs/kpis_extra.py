import pandas as pd
import sys
import os

try:
    BUCKET = sys.argv[1]
except:
    print("❌ Falta bucket")
    sys.exit(1)

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = "bi_examen_db"

print(f"🚀 GENERANDO KPIS EXTRA (Bucket: {BUCKET})")

# Leer datos raw
ruta_raw = f"gs://{BUCKET}/bronce/raw/city_day.csv"
try:
    df = pd.read_csv(ruta_raw)

    # Limpieza
    df.columns = [c.replace('.', '_').replace(' ', '_') for c in df.columns]
    
    # Validar columna AQI
    if 'AQI' in df.columns:
        df['AQI'] = df['AQI'].fillna(0)
    else:
        print("⚠️ No se encontró columna AQI, creando dummy con 0")
        df['AQI'] = 0

    if 'AQI_Bucket' in df.columns:
        df['AQI_Bucket'] = df['AQI_Bucket'].fillna('Unknown')
    else:
        df['AQI_Bucket'] = 'Unknown'

    # --- KPI 4: RESUMEN GLOBAL ---
    print("--> Generando KPI Resumen Global...")
    kpi_global = pd.DataFrame({
        'Total_Ciudades': [df['City'].nunique()],
        'Total_Registros': [len(df)],
        'AQI_Promedio_Hist': [df['AQI'].mean()],
        'AQI_Maximo_Reg': [df['AQI'].max()],
        'Peor_Ciudad': [df.loc[df['AQI'].idxmax(), 'City'] if not df.empty else 'N/A']
    })
    kpi_global.to_gbq(f'{DATASET}.kpi_resumen_global', project_id=PROJECT_ID, if_exists='replace')

    # --- KPI 5: DISTRIBUCIÓN ---
    print("--> Generando KPI Distribución...")
    kpi_dist = df['AQI_Bucket'].value_counts().reset_index()
    kpi_dist.columns = ['Calidad_Aire', 'Total_Dias']
    kpi_dist.to_gbq(f'{DATASET}.kpi_distribucion_calidad', project_id=PROJECT_ID, if_exists='replace')

    # --- KPI 6: MIX CONTAMINANTES ---
    print("--> Generando KPI Mix Contaminantes...")
    cols_pollutants = ['PM2_5', 'PM10', 'NO2', 'SO2', 'CO']
    cols_existentes = [c for c in cols_pollutants if c in df.columns]
    
    if cols_existentes:
        kpi_mix = df.groupby('City')[cols_existentes].mean().reset_index()
        kpi_mix.to_gbq(f'{DATASET}.kpi_mix_contaminantes', project_id=PROJECT_ID, if_exists='replace')
    
    print("✅ KPIS EXTRA CREADOS EXITOSAMENTE")

except Exception as e:
    print(f"❌ ERROR: {e}")
