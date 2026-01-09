import pandas as pd
import sys
import os

try:
    BUCKET = sys.argv[1]
except IndexError:
    print("❌ Error: Falta bucket")
    sys.exit(1)

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = "bi_examen_db"

print(f"🔧 REPARANDO KPIs - INTENTO FINAL (Bucket: {BUCKET})")

# 1. LEER RAW
ruta_raw = f"gs://{BUCKET}/bronce/raw/city_day.csv"
df = pd.read_csv(ruta_raw)

# 2. LIMPIEZA
df.columns = [c.replace('.', '_').replace(' ', '_') for c in df.columns]
df['Date'] = pd.to_datetime(df['Date'])
df['AQI'] = df['AQI'].fillna(0)

# --- REPARACIÓN KPI 1: DÍAS CRÍTICOS ---
print("--> Generando KPI Días Críticos...")
# Filtramos días malos (AQI > 200)
criticos = df[df['AQI'] > 200].copy()

if not criticos.empty:
    # CREAMOS LA COLUMNA ANTES PARA EVITAR EL ERROR DE PANDAS
    criticos['Anio'] = criticos['Date'].dt.year
    
    # Agrupamos de forma explícita y contamos
    # name='Dias_Criticos' le pone el nombre directamente a la columna de conteo
    kpi_criticos = criticos.groupby(['City', 'Anio']).size().reset_index(name='Dias_Criticos')
    
    # Guardar
    kpi_criticos.to_gbq(f'{DATASET}.kpi_dias_criticos', project_id=PROJECT_ID, if_exists='replace')
    print("    ✅ kpi_dias_criticos CREADO.")
else:
    print("    ⚠️ No hay días críticos. Creando tabla dummy.")
    dummy = pd.DataFrame({'Ciudad': ['Sin Datos'], 'Anio': [2024], 'Dias_Criticos': [0]})
    dummy.to_gbq(f'{DATASET}.kpi_dias_criticos', project_id=PROJECT_ID, if_exists='replace')

# --- REPARACIÓN KPI 2: TENDENCIA ---
print("--> Generando KPI Tendencia Mensual...")
# Creamos columna de mes texto
df['Mes_Anio'] = df['Date'].dt.strftime('%Y-%m')

# Agrupamos
kpi_tendencia = df.groupby('Mes_Anio')['AQI'].mean().reset_index()
kpi_tendencia.columns = ['Mes_Anio', 'AQI_Promedio']

# Guardar
kpi_tendencia.to_gbq(f'{DATASET}.kpi_tendencia', project_id=PROJECT_ID, if_exists='replace')
print("    ✅ kpi_tendencia CREADO.")

print("🎉 REPARACIÓN FINALIZADA")
