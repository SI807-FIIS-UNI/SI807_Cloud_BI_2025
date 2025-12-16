import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
import io

# =========================
# CONFIGURACIÓN
# =========================
PROJECT_ID = "double-basis-481318-h5"
BUCKET_NAME = "dl-bi-examen-caruzo"
CURATED_PATH = "bronce/curated/appointments_curated.parquet"
DATASET_PLATA = "dw_plata"

storage_client = storage.Client()
bq_client = bigquery.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

# =========================
# LECTURA CURATED
# =========================
blob = bucket.blob(CURATED_PATH)
data = blob.download_as_bytes()
df = pd.read_parquet(io.BytesIO(data))

print(f"Filas leídas desde curated: {len(df)}")

# =========================
# DIM_PACIENTE
# =========================
dim_paciente = df[[
    "patientid", "gender", "age",
    "scholarship", "hipertension",
    "diabetes", "alcoholism", "handcap"
]].drop_duplicates().reset_index(drop=True)

dim_paciente["paciente_id"] = dim_paciente.index + 1

# =========================
# DIM_TIEMPO
# =========================
dim_tiempo = df[["appointmentday"]].drop_duplicates().reset_index(drop=True)
dim_tiempo["tiempo_id"] = dim_tiempo.index + 1

dim_tiempo["fecha"] = dim_tiempo["appointmentday"].dt.date
dim_tiempo["anio"] = dim_tiempo["appointmentday"].dt.year
dim_tiempo["mes"] = dim_tiempo["appointmentday"].dt.month
dim_tiempo["dia"] = dim_tiempo["appointmentday"].dt.day
dim_tiempo["dia_semana"] = dim_tiempo["appointmentday"].dt.day_name()
dim_tiempo["hora"] = dim_tiempo["appointmentday"].dt.hour

# =========================
# DIM_BARRIO
# =========================
dim_barrio = df[["neighbourhood"]].drop_duplicates().reset_index(drop=True)
dim_barrio["barrio_id"] = dim_barrio.index + 1

# =========================
# DIM_CANAL (NUEVA)
# =========================
dim_canal = df[["sms_received"]].drop_duplicates().reset_index(drop=True)

dim_canal["descripcion_canal"] = dim_canal["sms_received"].apply(
    lambda x: "Con SMS" if x > 0 else "Sin SMS"
)

dim_canal["canal_id"] = dim_canal.index + 1

# =========================
# FACT_CITAS
# =========================
fact = (
    df.merge(
        dim_paciente,
        on=["patientid", "gender", "age", "scholarship",
            "hipertension", "diabetes", "alcoholism", "handcap"],
        how="left"
    )
    .merge(
        dim_tiempo,
        on="appointmentday",
        how="left"
    )
    .merge(
        dim_barrio,
        on="neighbourhood",
        how="left"
    )
    .merge(
        dim_canal,
        on="sms_received",
        how="left"
    )
)

# Lead time (anticipación en días)
fact["lead_time"] = (
    fact["appointmentday"] - fact["scheduledday"]
).dt.days

fact_citas = fact[[
    "appointmentid",
    "paciente_id",
    "tiempo_id",
    "barrio_id",
    "canal_id",
    "lead_time",
    "no_show"
]]

# =========================
# CARGA A BIGQUERY (PLATA)
# =========================
dim_paciente.to_gbq(
    f"{DATASET_PLATA}.dim_paciente",
    project_id=PROJECT_ID,
    if_exists="replace"
)

dim_tiempo.to_gbq(
    f"{DATASET_PLATA}.dim_tiempo",
    project_id=PROJECT_ID,
    if_exists="replace"
)

dim_barrio.to_gbq(
    f"{DATASET_PLATA}.dim_barrio",
    project_id=PROJECT_ID,
    if_exists="replace"
)

dim_canal.to_gbq(
    f"{DATASET_PLATA}.dim_canal",
    project_id=PROJECT_ID,
    if_exists="replace"
)

fact_citas.to_gbq(
    f"{DATASET_PLATA}.fact_citas",
    project_id=PROJECT_ID,
    if_exists="replace"
)

print("✔ BRONCE / CURATED → PLATA (v2 con dim_canal) completado")
print("Tablas creadas:")
print("- dim_paciente")
print("- dim_tiempo")
print("- dim_barrio")
print("- dim_canal")
print("- fact_citas")
