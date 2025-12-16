import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import storage
import io

# =====================
# CONFIGURACIÓN
# =====================
BUCKET_NAME = "dl-bi-examen-caruzo"
CURATED_FILE = "bronce/curated/appointments_curated.parquet"

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

# =====================
# LECTURA CURATED
# =====================
blob = bucket.blob(CURATED_FILE)
data = blob.download_as_bytes()
df = pd.read_parquet(io.BytesIO(data))

# =====================
# EDA – NULOS
# =====================
nulls = df.isnull().sum()
nulls.to_csv("nulos.csv")

# =====================
# EDA – ESTADÍSTICAS
# =====================
stats = df.describe()
stats.to_csv("estadisticas.csv")

# =====================
# EDA – DISTRIBUCIONES
# =====================
plt.figure()
df["age"].hist(bins=30)
plt.title("Distribución de Edad")
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.savefig("distribucion_edad.png")

# =====================
# EDA – CORRELACIONES
# =====================
plt.figure(figsize=(10,6))
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Matriz de Correlación")
plt.savefig("correlaciones.png")

print("✔ EDA completado")
