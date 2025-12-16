import pandas as pd
from google.cloud import storage
import io

# =====================
# CONFIGURACIÓN
# =====================
BUCKET_NAME = "dl-bi-examen-caruzo"
PROCESSED_FILE = "bronce/processed/appointments.parquet"
CURATED_FILE = "bronce/curated/appointments_curated.parquet"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

# =====================
# LECTURA PARQUET
# =====================
blob = bucket.blob(PROCESSED_FILE)
data = blob.download_as_bytes()

df = pd.read_parquet(io.BytesIO(data))

initial_rows = len(df)

# =====================
# VALIDACIONES BÁSICAS
# =====================

# Eliminar duplicados por AppointmentID
df = df.drop_duplicates(subset=["appointmentid"])

# Edades inválidas
df = df[df["age"] >= 0]

# Normalizar variable objetivo
df["no_show"] = df["no_show"].map({"Yes": 1, "No": 0})

# Convertir binarios a int
binary_cols = [
    "scholarship", "hipertension", "diabetes",
    "alcoholism", "handcap", "sms_received"
]

df[binary_cols] = df[binary_cols].astype(int)

final_rows = len(df)

# =====================
# GUARDAR CURATED
# =====================
df.to_parquet("appointments_curated.parquet", index=False)
bucket.blob(CURATED_FILE).upload_from_filename("appointments_curated.parquet")

print("✔ PROCESSED → CURATED completado")
print(f"Filas iniciales: {initial_rows}")
print(f"Filas finales: {final_rows}")
