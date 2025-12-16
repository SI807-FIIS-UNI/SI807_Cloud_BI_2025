import pandas as pd

print("--- REPORTE DE VENTAS: SUPERSTORE ---")
print("Autor: Callupe Pardo")

# 1. Carga de datos
# Usamos on_bad_lines para saltar errores de formato si los hubiera
try:
    df = pd.read_csv('train.csv', encoding='latin-1', on_bad_lines='skip')
except:
    df = pd.read_csv('train.csv', encoding='latin-1')

# 2. Conversión de Fecha
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y', errors='coerce')

print(f"\n[INFO] Dataset Cargado. Filas: {df.shape[0]} | Columnas: {len(df.columns)}")

print("\n--- KPI 1: DESEMPEÑO POR REGIÓN (Ventas Totales) ---")
# Usamos Sales porque no tenemos Profit
print(df.groupby('Region')['Sales'].sum().sort_values(ascending=False))

print("\n--- KPI 2: TOP 5 PRODUCTOS (Más Vendidos) ---")
print(df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5))

print("\n--- KPI 3: TENDENCIA DE VENTAS (Por Año) ---")
df['Year'] = df['Order Date'].dt.year
print(df.groupby('Year')['Sales'].sum())

print("\n--- KPI 4: VENTAS POR CATEGORÍA ---")
print(df.groupby('Category')['Sales'].sum().sort_values(ascending=False))

print("\n--- CALIDAD DE DATOS (Nulos en Ventas) ---")
print(df['Sales'].isnull().sum())
print("--- FIN DEL REPORTE ---")
