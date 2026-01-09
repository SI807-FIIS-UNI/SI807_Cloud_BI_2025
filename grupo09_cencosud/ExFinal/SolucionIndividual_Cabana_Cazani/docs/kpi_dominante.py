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

print(f"🚀 CALCULANDO CONTAMINANTE DOMINANTE (Bucket: {BUCKET})")

# Leer
ruta_raw = f"gs://{BUCKET}/bronce/raw/city_day.csv"
df = pd.read_csv(ruta_raw)

# Limpieza rápida de nombres y nulos
df.columns = [c.replace('.', '_').replace(' ', '_') for c in df.columns]

# Lista de contaminantes posibles
posibles = ['PM2_5', 'PM10', 'NO2', 'CO', 'SO2', 'O3', 'NH3']
cols_existentes = [c for c in posibles if c in df.columns]

# Llenar nulos con 0
for c in cols_existentes:
    df[c] = df[c].fillna(0)

# ---------------------------------------------------------
# LÓGICA CORREGIDA (Evitar error float vs str)
# ---------------------------------------------------------
print("--> Comparando químicos por ciudad...")
# 1. Obtenemos solo los promedios numéricos primero
df_promedios = df.groupby('City')[cols_existentes].mean()

# 2. Calculamos las series POR SEPARADO antes de modificar el DataFrame
serie_dominante = df_promedios.idxmax(axis=1) # El nombre de la columna mayor
serie_valor = df_promedios.max(axis=1)        # El valor numérico mayor

# 3. Construimos el reporte final limpio
kpi_dominante = pd.DataFrame({
    'City': df_promedios.index,
    'Contaminante_Principal': serie_dominante,
    'Concentracion_Promedio': serie_valor
}).reset_index(drop=True)

# Guardar en BigQuery
kpi_dominante.to_gbq(f'{DATASET}.kpi_contaminante_dominante', project_id=PROJECT_ID, if_exists='replace')

print("✅ KPI CONTAMINANTE DOMINANTE CREADO")
print(kpi_dominante.head())
