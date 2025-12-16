# Script de Análisis Exploratorio (EDA) - Caso Superstore
# Objetivo: Validación preliminar de KPIs (Top productos, Rentabilidad y Estacionalidad)

import pandas as pd

print("--- REPORTE INICIAL: SUPERSTORE SALES ---")
print("Cargando dataset...")

# 1. Carga y limpieza inicial
# Usamos encoding 'latin-1' por si hay tildes y parseamos fechas
df = pd.read_csv('train.csv', encoding='latin-1')

# Convertimos Order Date a datetime para analizar estacionalidad
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y', errors='coerce')

print(f"\n[INFO] Registros cargados: {df.shape[0]}")
print(f"[INFO] Columnas detectadas: {df.shape[1]}")

print("\n--- KPI 1: RENTABILIDAD POR REGIÓN ---")
# Agrupamos por región sumando Ganancia (Profit) y Ventas (Sales)
kpi_region = df.groupby('Region')[['Sales', 'Profit']].sum().sort_values(by='Profit', ascending=False)
print(kpi_region)

print("\n--- KPI 2: TOP 10 PRODUCTOS (Por Ventas) ---")
# Identificamos los productos estrella
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
print(top_products)

print("\n--- KPI 3: PATRONES DE ESTACIONALIDAD (Ventas por Año) ---")
# Extraemos el año para ver volumen general
df['Year'] = df['Order Date'].dt.year
print(df.groupby('Year')['Sales'].sum())

print("\n--- VALIDACIÓN DE CALIDAD DE DATOS ---")
# Chequeamos si hay nulos en campos críticos
nulos = df[['Sales', 'Profit', 'Region', 'Order Date']].isnull().sum()
print("Valores Nulos encontrados:")
print(nulos)

print("\n--- FIN DEL EDA ---")
