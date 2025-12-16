import pandas as pd
print("--- REPORTE DE KPIS (Capa Oro) ---")

try:
    df = pd.read_csv('train.csv', encoding='latin-1', on_bad_lines='skip')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y', errors='coerce')
    print("Datos cargados correctamente.")
except:
    print("Error cargando datos.")

print("\n[KPI 1] Ventas Totales por Mes:")
df['Mes'] = df['Order Date'].dt.to_period('M')
print(df.groupby('Mes')['Sales'].sum().head(5))

print("\n[KPI 2] Top 5 Productos más vendidos:")
print(df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(5))