import pandas as pd
from google.cloud import storage
import io

# =====================
# CONFIGURACIÓN
# =====================
BUCKET_NAME = "dl-bi-examen-caruzo"
RAW_FILE = "bronce/raw/KaggleV2-May-2016.csv"
PROCESSED_FILE = "bronce/processed/appointments.parquet"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

# =====================
# LECTURA CSV DESDE GCS
# =====================
blob = bucket.blob(RAW_FILE)
csv_data = blob.download_as_text()

df = pd.read_csv(io.StringIO(csv_data))

# =====================
# NORMALIZACIÓN BÁSICA
# =====================
df.columns = (
    df.columns
    .str.lower()
    .str.replace("-", "_")
    .str.replace(" ", "_")
)

# Conversión de fechas
df["scheduledday"] = pd.to_datetime(df["scheduledday"])
df["appointmentday"] = pd.to_datetime(df["appointmentday"])

# =====================
# GUARDAR PARQUET
# =====================
df.to_parquet("appointments.parquet", index=False)

bucket.blob(PROCESSED_FILE).upload_from_filename("appointments.parquet")

print("✔ RAW → PROCESSED completado")
print(f"Filas cargadas: {len(df)}")
