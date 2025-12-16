import pandas as pd
import sys
from google.cloud import bigquery
from google.cloud import storage
import io

# Argumentos
BUCKET_NAME = sys.argv[1]
PROJECT_ID = sys.argv[2]

def run_etl_gold():
    print("--- INICIO ETL GOLD (Cálculo de KPIs) ---")
    bq_client = bigquery.Client()
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    # 1. LEER DATOS DESDE BIGQUERY (Capa Plata)
    # Usamos SQL para agregar los datos directamente (más eficiente)
    query = f"""
    SELECT 
        f.Neighbourhood,
        p.Gender,
        -- Agrupamos edades en rangos para mejor análisis
        CASE 
            WHEN p.Age < 18 THEN '0-17 Menor'
            WHEN p.Age BETWEEN 18 AND 35 THEN '18-35 Joven'
            WHEN p.Age BETWEEN 36 AND 60 THEN '36-60 Adulto'
            ELSE '60+ Senior'
        END as Rango_Edad,
        COUNT(f.AppointmentID) as Total_Citas,
        SUM(f.is_NoShow) as Cantidad_Faltas,
        AVG(f.LeadTimeDays) as Promedio_Espera_Dias
    FROM `{PROJECT_ID}.silver_layer.fact_citas` f
    JOIN `{PROJECT_ID}.silver_layer.dim_paciente` p ON f.PatientId = p.PatientId
    GROUP BY 1, 2, 3
    ORDER BY Total_Citas DESC
    """
    
    print("Ejecutando consulta analítica en BigQuery...")
    df_gold = bq_client.query(query).to_dataframe()
    
    # 2. CALCULAR KPI PRINCIPAL (Tasa de No-Show)
    df_gold['Tasa_NoShow_Porc'] = (df_gold['Cantidad_Faltas'] / df_gold['Total_Citas']) * 100
    df_gold['Tasa_NoShow_Porc'] = df_gold['Tasa_NoShow_Porc'].round(2)
    
    # Mostrar un adelanto en consola
    print("\n--- Top 5 Barrios con más citas ---")
    print(df_gold.head().to_string())

    # 3. GUARDAR EN GCS (Capa Oro - Curated)
    # Esto sirve para descargarlo fácil si PowerBI lo pide como CSV
    blob = bucket.blob("bronce/curated/kpi_resumen_noshow.csv")
    blob.upload_from_string(df_gold.to_csv(index=False), 'text/csv')
    print(f"\n-> KPI guardado en GCS: bronce/curated/kpi_resumen_noshow.csv")

    # 4. GUARDAR EN BIGQUERY (Tabla Final para Dashboard)
    dataset_id = f"{PROJECT_ID}.gold_layer"
    try:
        bq_client.create_dataset(bigquery.Dataset(dataset_id), exists_ok=True)
    except:
        pass
    
    table_id = f"{dataset_id}.kpi_resumen"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = bq_client.load_table_from_dataframe(df_gold, table_id, job_config=job_config)
    job.result()
    
    print(f"-> KPI disponible en BigQuery: {table_id}")
    
    # Guardar evidencia
    with open("docs/log_etl_gold.txt", "w") as f:
        f.write("ETL Gold completado.\n")
        f.write(df_gold.head().to_string())

if __name__ == "__main__":
    run_etl_gold()
    