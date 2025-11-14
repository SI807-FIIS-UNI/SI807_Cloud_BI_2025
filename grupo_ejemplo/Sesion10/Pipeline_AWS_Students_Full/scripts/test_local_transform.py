
# Script para probar la transformación localmente (sin Glue)
import pandas as pd
import numpy as np

print("📦 Leyendo dataset local...")
df = pd.read_csv("Ecommerce_Sales.csv", encoding='latin1')

df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
df["order_date"] = pd.to_datetime(df["order_date"])
df["anio"] = df["order_date"].dt.year
df["mes"] = df["order_date"].dt.month
df["margen"] = np.where(df["sales"]>0, df["profit"]/df["sales"], 0)

print("✅ Transformación local completada.")
df.to_parquet("sales_curated.parquet", index=False)
print("📂 Archivo guardado: sales_curated.parquet")
