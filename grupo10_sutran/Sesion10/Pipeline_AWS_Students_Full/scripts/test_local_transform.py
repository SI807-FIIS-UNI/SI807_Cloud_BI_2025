
# Script para probar la transformación localmente (sin Glue)
import pandas as pd
import numpy as np

print("Leyendo dataset local...")

# Ruta absoluta o relativa a tu archivo limpio
path = r"C:\Users\jairo\Documents\Proyectos\aradiel_25-2\taller_2\archive\ecommerce_clean.csv"
df = pd.read_csv(path, encoding='latin1', low_memory=False)

# Limpieza de columnas
df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]

# Revisar que tengas columna de fecha
if "date" not in df.columns:
    raise ValueError("❌ La columna 'date' no existe en el dataset.")

df["order_date"] = pd.to_datetime(df["date"], errors="coerce")
df["anio"] = df["order_date"].dt.year
df["mes"] = df["order_date"].dt.month

# Validar columnas para calcular margen
if "amount" not in df.columns or "qty" not in df.columns:
    raise ValueError("❌ Faltan columnas necesarias para calcular el margen.")

# Calcular margen (mismo concepto que profit/sales)
df["margen"] = np.where(df["amount"] > 0, df["qty"] / df["amount"], 0)

# Exportar como parquet
output_path = r"C:\Users\jairo\Documents\Proyectos\aradiel_25-2\taller_2\archive\sales_curated.parquet"
df.to_parquet(output_path, index=False)
print(f"✅ Transformación local completada. Archivo guardado en: {output_path}")
