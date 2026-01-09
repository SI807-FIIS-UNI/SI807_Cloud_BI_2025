import pandas as pd
import os

# --- CONFIGURACIÓN ---
# Obtiene tu ID de proyecto automáticamente
project_id = os.popen("gcloud config get-value project").read().strip()
bucket_name = "examen-bi-practica-1765740324"
dataset_id = "bi_examen_db"

print(f"🚀 INICIANDO ETL EN PROYECTO: {project_id}")

try:
    # ---------------------------------------------------------
    # 1. EXTRACCIÓN (Desde Capa BRONZE - Storage)
    # ---------------------------------------------------------
    print("--> [1] Leyendo CSV desde Cloud Storage...")
    ruta = f"gs://{bucket_name}/bronce/raw/ventas_examen.csv"
    df = pd.read_csv(ruta)
    
    # Limpieza básica de fechas
    df['fecha'] = pd.to_datetime(df['fecha'])

    # ---------------------------------------------------------
    # 2. TRANSFORMACIÓN (Hacia Capa SILVER - BigQuery)
    # ---------------------------------------------------------
    print("--> [2] Generando Modelo Estrella (Silver)...")

    # A. Dimensión Cliente
    dim_cliente = df[['id_cliente', 'nombre_cliente']].drop_duplicates()
    
    # B. Dimensión Producto
    dim_producto = df[['categoria', 'canal']].drop_duplicates().reset_index(drop=True)
    dim_producto['id_producto'] = dim_producto.index + 1

    # C. Tabla de Hechos
    fact_ventas = df[['id_transaccion', 'fecha', 'id_cliente', 'categoria', 'monto']]

    # Cargar a BigQuery
    print("    ... Guardando tablas Silver en BigQuery")
    dim_cliente.to_gbq(f'{dataset_id}.dim_cliente', project_id, if_exists='replace')
    dim_producto.to_gbq(f'{dataset_id}.dim_producto', project_id, if_exists='replace')
    fact_ventas.to_gbq(f'{dataset_id}.fact_ventas', project_id, if_exists='replace')

    # ---------------------------------------------------------
    # 3. GENERACIÓN DE KPIs (Hacia Capa GOLD - BigQuery)
    # ---------------------------------------------------------
    print("--> [3] Calculando KPIs (Gold)...")

    # KPI 1: Ventas por Categoría
    kpi_categoria = df.groupby('categoria')['monto'].sum().reset_index()
    kpi_categoria.to_gbq(f'{dataset_id}.kpi_ventas_categoria', project_id, if_exists='replace')

    # KPI 2: Top Clientes
    kpi_clientes = df.groupby('nombre_cliente')['monto'].sum().reset_index().sort_values('monto', ascending=False)
    kpi_clientes.to_gbq(f'{dataset_id}.kpi_top_clientes', project_id, if_exists='replace')

    print("\n✅ ¡ETL COMPLETADO! Tablas creadas exitosamente.")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
