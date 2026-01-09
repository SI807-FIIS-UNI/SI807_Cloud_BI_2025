import pandas as pd
import sys
import os

try:
    BUCKET = sys.argv[1]
except IndexError:
    print("❌ Error: Faltó el nombre del bucket.")
    sys.exit(1)

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = "bi_examen_db"

print(f"🚀 INICIANDO ETL MODELO ESTRELLA (Bucket: {BUCKET})")

# 1. LEER RAW
ruta_raw = f"gs://{BUCKET}/bronce/raw/city_day.csv"
try:
    df = pd.read_csv(ruta_raw)
    
    # --- 🛠️ CORRECCIÓN CRÍTICA: RENOMBRAR COLUMNAS ---
    # BigQuery no acepta puntos. Cambiamos 'PM2.5' por 'PM2_5'
    df.columns = [c.replace('.', '_').replace(' ', '_') for c in df.columns]
    print("✅ Columnas corregidas (ej: PM2.5 -> PM2_5)")
    
    # 2. TRANSFORMACIÓN (PLATA)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Actualizamos la lista de métricas con los NUEVOS nombres (con guion bajo)
    cols_num = ['PM2_5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'AQI']
    
    # Limpieza de nulos
    for c in cols_num:
        if c in df.columns: df[c] = df[c].fillna(0)
    if 'AQI_Bucket' in df.columns: df['AQI_Bucket'] = df['AQI_Bucket'].fillna('Unknown')

    # Dimensiones
    dim_ciudad = df[['City']].drop_duplicates().sort_values('City').reset_index(drop=True)
    dim_ciudad['id_ciudad'] = dim_ciudad.index + 1
    # Usamos project_id explícito para evitar warnings
    dim_ciudad.to_gbq(f'{DATASET}.dim_ciudad', project_id=PROJECT_ID, if_exists='replace')

    dim_tiempo = df[['Date']].drop_duplicates().sort_values('Date').reset_index(drop=True)
    dim_tiempo['id_tiempo'] = dim_tiempo['Date'].dt.strftime('%Y%m%d').astype(int)
    dim_tiempo['anio'] = dim_tiempo['Date'].dt.year
    dim_tiempo['mes'] = dim_tiempo['Date'].dt.month
    dim_tiempo.to_gbq(f'{DATASET}.dim_tiempo', project_id=PROJECT_ID, if_exists='replace')

    # Hechos
    fact = df.merge(dim_ciudad, on='City', how='left')
    fact['id_tiempo'] = fact['Date'].dt.strftime('%Y%m%d').astype(int)
    
    # Seleccionamos columnas finales
    cols_fact = ['id_ciudad', 'id_tiempo', 'AQI_Bucket'] + [c for c in cols_num if c in df.columns]
    
    fact[cols_fact].to_gbq(f'{DATASET}.fact_calidad_aire', project_id=PROJECT_ID, if_exists='replace')
    fact[cols_fact].to_parquet(f"gs://{BUCKET}/bronce/processed/fact_calidad_aire.parquet")

    # 3. KPIs (ORO)
    # Top Ciudades
    kpi1 = df.groupby('City')['AQI'].mean().sort_values(ascending=False).reset_index()
    kpi1.columns = ['Ciudad', 'AQI_Promedio']
    kpi1.to_gbq(f'{DATASET}.kpi_top_ciudades', project_id=PROJECT_ID, if_exists='replace')
    kpi1.to_csv(f"gs://{BUCKET}/bronce/curated/reporte_top.csv", index=False)

    # Días Críticos
    criticos = df[df['AQI_Bucket'].isin(['Severe', 'Very Poor'])]
    if not criticos.empty:
        kpi2 = criticos.groupby(['City', df['Date'].dt.year])['Date'].count().reset_index()
        kpi2.columns = ['Ciudad', 'Anio', 'Dias_Criticos']
        kpi2.to_gbq(f'{DATASET}.kpi_dias_criticos', project_id=PROJECT_ID, if_exists='replace')

    # Tendencia
    kpi3 = df.groupby(df['Date'].dt.to_period('M'))['AQI'].mean().reset_index()
    kpi3['Date'] = kpi3['Date'].astype(str)
    kpi3.to_gbq(f'{DATASET}.kpi_tendencia', project_id=PROJECT_ID, if_exists='replace')

    print("✅ ETL FINALIZADO CON ÉXITO")

except Exception as e:
    print(f"❌ ERROR: {e}")
