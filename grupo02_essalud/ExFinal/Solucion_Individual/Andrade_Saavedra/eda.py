import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. CONFIGURACIÓN DE ENTORNO ---
# Truco para que funcione sin importar desde dónde lo ejecutes
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
NOMBRE_ARCHIVO = os.path.join(DIRECTORIO_ACTUAL, "train.csv")
CARPETA_EVIDENCIAS = os.path.join(DIRECTORIO_ACTUAL, "Docs", "Media")

# Crear carpeta si no existe
if not os.path.exists(CARPETA_EVIDENCIAS):
    os.makedirs(CARPETA_EVIDENCIAS)

print("==========================================")
print("   INICIO EDA: CASO RETAIL SUPERSTORE")
print("==========================================")

# --- 2. CARGA DE DATOS (Manejo de errores de codificación) ---
try:
    print(f"📂 Leyendo archivo: {NOMBRE_ARCHIVO}...")
    try:
        df = pd.read_csv(NOMBRE_ARCHIVO, encoding="utf-8")
    except UnicodeDecodeError:
        print("⚠️ Encoding UTF-8 falló, intentando con Latin-1...")
        df = pd.read_csv(NOMBRE_ARCHIVO, encoding="latin1")

    print("✅ Archivo cargado exitosamente.")
except FileNotFoundError:
    print(f"❌ ERROR CRÍTICO: No se encuentra el archivo en: {NOMBRE_ARCHIVO}")
    print(
        "   -> Por favor, guarda el CSV del caso como 'superstore.csv' en esta misma carpeta."
    )
    exit()

# --- 3. LIMPIEZA INICIAL DE NOMBRES ---
df.columns = [c.lower().strip().replace(" ", "_").replace("-", "_") for c in df.columns]

# --- 4. CALIDAD DE DATOS (Lo que pide la rúbrica) ---

print(f"\n📊 [DIMENSIONES]: {df.shape[0]} filas, {df.shape[1]} columnas")

print("\n🔍 [DUPLICADOS]")
duplicados = df.duplicated().sum()
if duplicados > 0:
    print(f"⚠️ Se encontraron {duplicados} filas totalmente duplicadas.")
else:
    print("✅ No se encontraron filas duplicadas.")

print("\n🚫 [VALORES NULOS]")
nulos = df.isnull().sum()
nulos_existentes = nulos[nulos > 0]
if not nulos_existentes.empty:
    print(nulos_existentes)
else:
    print("✅ No se encontraron valores nulos en ninguna columna (Dataset limpio).")

print("\nℹ️ [TIPOS DE DATOS]")
print(df.dtypes)

# --- 5. ESTADÍSTICAS BÁSICAS ---
print("\n🧮 [RESUMEN ESTADÍSTICO (Numérico)]")
cols_clave = ["sales", "quantity", "discount", "profit"]
cols_existentes = [c for c in cols_clave if c in df.columns]
if cols_existentes:
    print(df[cols_existentes].describe().round(2))
else:
    print("⚠️ No se detectaron columnas numéricas estándar (Sales, Profit).")

# --- 6. GENERACIÓN DE EVIDENCIA GRÁFICA ---
print("\n🎨 [GENERANDO GRÁFICO...]")

try:
    if "sales" in df.columns and "category" in df.columns:
        if df["sales"].dtype == "object":
            df["sales"] = (
                df["sales"].astype(str).str.replace("$", "").str.replace(",", "")
            )
            df["sales"] = pd.to_numeric(df["sales"])

        ventas_cat = df.groupby("category")["sales"].sum().sort_values(ascending=True)

        plt.figure(figsize=(10, 6))
        ventas_cat.plot(kind="barh", color="#2E86C1")  # Azul corporativo
        plt.title("Total de Ventas por Categoría - Superstore", fontsize=14)
        plt.xlabel("Ventas ($)", fontsize=12)
        plt.ylabel("Categoría", fontsize=12)
        plt.grid(axis="x", linestyle="--", alpha=0.6)
        plt.tight_layout()

        ruta_grafico = os.path.join(CARPETA_EVIDENCIAS, "eda_ventas_superstore.png")
        plt.savefig(ruta_grafico)
        print(f"✅ Gráfico guardado en: {ruta_grafico}")
    else:
        print("❌ No se pudo generar el gráfico: Faltan columnas 'Category' o 'Sales'.")

except Exception as e:
    print(f"❌ Error al generar gráfico: {str(e)}")

print("\n==========================================")
print("       FIN DEL ANÁLISIS (EDA)")
print("==========================================")
