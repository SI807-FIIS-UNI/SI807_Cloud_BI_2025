import pandas as pd
import sys
from google.cloud import storage
from google.cloud import bigquery
import io

# Recibimos argumentos de la consola
BUCKET_NAME = sys.argv[1]
PROJECT_ID = sys.argv[2]

def run_etl_silver():
    print("--- INICIO ETL SILVER (Transformación a Modelo Estrella) ---")
    
    # 1. CONEXIÓN Y LECTURA
    storage_client = storage.Client()
    bq_client = bigquery.Client()
    
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob("bronce/raw/dataset_citas.csv")
    print(f"Descargando datos crudos desde: gs://{BUCKET_NAME}/bronce/raw/dataset_citas.csv")
    df = pd.read_csv(io.BytesIO(blob.download_as_string()))

    # 2. LIMPIEZA DE DATOS (Calidad)
    # Corregir nombres de columnas mal escritos en el origen
    df.rename(columns={'Hipertension': 'Hypertension', 'Handcap': 'Handicap'}, inplace=True)
    
    # Convertir fechas a formato datetime (normalizar quita las horas/minutos)
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay']).dt.normalize()
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay']).dt.normalize()
    
    # Limpieza: Eliminar registros con Edad negativa (Visto en el EDA)
    df = df[df['Age'] >= 0]

    # Feature Engineering: Calcular días de espera (Lead Time)
    df['LeadTimeDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
    # Corregir inconsistencias si la cita se agendó para el pasado (ponemos 0)
    df['LeadTimeDays'] = df['LeadTimeDays'].apply(lambda x: 0 if x < 0 else x)

    # 3. MODELADO DIMENSIONAL (Esquema Estrella)
    
    # --- TABLA DIMENSIÓN: PACIENTE ---
    # Un paciente puede tener muchas citas, nos quedamos con su última info registrada
    dim_paciente = df[['PatientId', 'Gender', 'Age', 'Scholarship', 'Hypertension', 
                       'Diabetes', 'Alcoholism', 'Handicap']].drop_duplicates(subset=['PatientId'], keep='last')
    
    # --- TABLA HECHOS: CITAS ---
    # Convertimos No-show a numero (1=Faltó, 0=Asistió) para poder sumar después
    df['is_NoShow'] = df['No-show'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    fact_citas = df[['AppointmentID', 'PatientId', 'ScheduledDay', 'AppointmentDay', 
                     'Neighbourhood', 'SMS_received', 'LeadTimeDays', 'is_NoShow']]

    # 4. CARGA A GCS (Capa Plata - Archivos CSV)
    save_to_gcs(dim_paciente, "bronce/processed/dim_paciente.csv", bucket)
    save_to_gcs(fact_citas, "bronce/processed/fact_citas.csv", bucket)
    
    # 5. CARGA A BIGQUERY (Data Warehouse)
    upload_to_bq(dim_paciente, "dim_paciente", bq_client)
    upload_to_bq(fact_citas, "fact_citas", bq_client)
    
    # Guardar log de evidencia
    with open("docs/log_etl_silver.txt", "w") as f:
        f.write("ETL Silver ejecutado correctamente.\n")
        f.write(f"Dimension Pacientes: {dim_paciente.shape[0]} filas.\n")
        f.write(f"Hechos Citas: {fact_citas.shape[0]} filas.\n")

def save_to_gcs(df, path, bucket):
    blob = bucket.blob(path)
    blob.upload_from_string(df.to_csv(index=False), 'text/csv')
    print(f" -> Guardado en GCS: {path}")

def upload_to_bq(df, table_name, client):
    dataset_id = f"{PROJECT_ID}.silver_layer"
    # Crear dataset si no existe
    try:
        client.create_dataset(bigquery.Dataset(dataset_id), exists_ok=True)
    except:
        pass
        
    table_id = f"{dataset_id}.{table_name}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result() # Esperar a que termine
    print(f" -> Cargado en BigQuery: {table_id}")

if __name__ == "__main__":
    run_etl_silver()

    