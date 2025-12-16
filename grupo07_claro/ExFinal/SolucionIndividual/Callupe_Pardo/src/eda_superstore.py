# Script de Análisis Exploratorio de Datos (EDA) - Caso Superstore
# Autor: Callupe Pardo
# Ejecutado en: Google Cloud Shell

import pandas as pd

print("--- INICIO REPORTE: SUPERSTORE SALES ---")
# Carga del dataset desde el entorno local de Cloud Shell
# Encoding latin-1 para soportar caracteres especiales
df = pd.read_csv('train.csv', encoding='latin-1')

print("\n1. VISTA PREVIA DE DATOS (HEAD):")
print(df.head(5))

print("\n2. DIMENSIONES DEL DATASET:")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

print("\n3. ESTADÍSTICAS DESCRIPTIVAS (Ventas):")
print(df['Sales'].describe())

print("\n4. TOP 5 REGIONES POR VENTAS:")
print(df.groupby('Region')['Sales'].sum().sort_values(ascending=False).head(5))

print("\n5. VALIDACIÓN DE CALIDAD (Nulos):")
print(df.isnull().sum())

print("--- FIN DEL REPORTE ---")
