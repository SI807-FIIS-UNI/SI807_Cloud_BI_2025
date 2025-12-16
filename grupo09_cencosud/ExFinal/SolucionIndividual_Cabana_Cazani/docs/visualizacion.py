import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración
project_id = os.popen("gcloud config get-value project").read().strip()
dataset_id = "bi_examen_db"

print("--- GENERANDO GRÁFICOS (VISUALIZACIÓN) ---")

# --- GRÁFICO 1: Ventas por Categoría ---
query1 = f"SELECT * FROM `{dataset_id}.kpi_ventas_categoria`"
df1 = pd.read_gbq(query1, project_id=project_id)

plt.figure(figsize=(10,6))
plt.bar(df1['categoria'], df1['monto'], color='skyblue')
plt.title('Ventas Totales por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Monto (S/)')
plt.savefig('docs/grafico_ventas_categoria.png') # Guardar imagen
print("✅ Gráfico 1 guardado en docs/grafico_ventas_categoria.png")

# --- GRÁFICO 2: Top Clientes ---
query2 = f"SELECT * FROM `{dataset_id}.kpi_top_clientes` LIMIT 5"
df2 = pd.read_gbq(query2, project_id=project_id)

plt.figure(figsize=(10,6))
plt.barh(df2['nombre_cliente'], df2['monto'], color='salmon')
plt.title('Top 5 Clientes VIP')
plt.xlabel('Monto Compra')
plt.savefig('docs/grafico_top_clientes.png') # Guardar imagen
print("✅ Gráfico 2 guardado en docs/grafico_top_clientes.png")

print("--- FIN DE VISUALIZACIÓN ---")
