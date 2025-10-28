import pandas as pd

# Cambia la ruta a tu archivo
ruta = "C:/Users/EL ADMIN/Documents/SI807_Cloud_BI_2025/grupo01_interbank/MiniProyecto/data/raw/netflix_titles.csv"

# Lee el CSV (detecta encabezados por defecto)
df = pd.read_csv(ruta, encoding="utf-8", sep=",")   # usa sep=";" si tu CSV está separado por punto y coma
print(df.head())  # primeras 5 filas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

df = pd.read_csv("C:/Users/EL ADMIN/Documents/SI807_Cloud_BI_2025/grupo01_interbank/MiniProyecto/data/raw/netflix_titles.csv")
df

print("# 1) Vista general: filas/columnas, nulos, tipos inferidos")
print(df.shape)
print(df.info())
print(df.head(3))

print("# 2) Porcentaje de nulos por columna")
null_pct = df.isna().mean().sort_values(ascending=False)
print(null_pct.head(10))

print("# 3) Duplicados de filas completas")
print("Filas duplicadas:", df.duplicated().sum())

print("# 4) Cardinalidad y muestra de categorías (para columnas tipo 'object')")
cat_cols = df.select_dtypes(include="object").columns
for c in cat_cols:
    print(f"\n[{c}] únicos:", df[c].nunique())
    print(df[c].dropna().astype(str).str.strip().str.lower().value_counts().head(5))

print("# 5) ¿Números guardados como texto?")
num_like = []
for c in df.columns:
    # prueba convertir a numérico
    coerced = pd.to_numeric(df[c].astype(str).str.replace(",", ".", regex=False), errors="coerce")
    ratio_numeric = coerced.notna().mean()
    if ratio_numeric > 0.7 and str(df[c].dtype) == "object":
        num_like.append((c, ratio_numeric))
print("Columnas que parecen numéricas pero son texto:", num_like)

print("# 6) Fechas como texto (intenta parseo rápido)")
date_candidates = [c for c in df.columns if "fecha" in c.lower() or "date" in c.lower()]
for c in date_candidates:
    parsed = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
    print(f"{c}: % parseable ->", parsed.notna().mean())

print("# 7) Outliers con IQR (para numéricas reales)")
num_cols = df.select_dtypes(include=["number"]).columns
for c in num_cols:
    q1, q3 = df[c].quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr > 0:
        outliers = ((df[c] < (q1 - 1.5*iqr)) | (df[c] > (q3 + 1.5*iqr))).mean()
        print(f"{c}: % outliers (IQR) -> {outliers:.2%}")

print("# 8) Espacios y mayúsculas inconsistentes (sample)")
for c in cat_cols[:5]:
    sample_rare = (
        df[c].dropna().astype(str)
        .value_counts()
        .tail(3)
    )
    print(f"\nValores raros en {c} (muestra):\n", sample_rare)

print("# 1) Normalizar strings básicos")
text_cols = ["type","title","director","cast","country","rating","duration","listed_in","description","date_added"]
for c in text_cols:
    df[c] = df[c].astype(str).str.strip()

print("# Opcional: una copia 'normalizada' para detectar duplicados lógicos")
df_norm = df.copy()
for c in ["type","title","country"]:
    df_norm[c] = (df_norm[c]
                  .str.normalize("NFKD")  # quita acentos si quieres
                  .str.encode("ascii","ignore").str.decode("utf-8")
                  .str.strip().str.lower())

print("# 2) Detectar títulos duplicados 'lógicos'")
dupes_titulo = df_norm.duplicated(subset=["title"], keep=False)
duplicados_logicos = df.loc[dupes_titulo, ["show_id","title"]].sort_values("title")
# -> revísalo: puede haber mismos títulos con distinta obra/país/año

print("# 3) Estandarizar 'type'")
map_type = {"tv show": "TV Show", "movie": "Movie"}
df["type"] = df["type"].str.strip().str.lower().map(map_type).fillna(df["type"])

print("# 4) Parsear fechas y aislar problemas")
df["date_added_dt"] = pd.to_datetime(df["date_added"], errors="coerce")
fechas_malas = df[df["date_added_dt"].isna() & df["date_added"].notna()][["show_id","date_added"]]

print("# 5) Separar duration -> minutos / temporadas")
def parse_duration(x):
    x = str(x).strip().lower()
    if "min" in x:
        try:
            return int(x.split()[0]), np.nan
        except:
            return np.nan, np.nan
    if "season" in x:
        try:
            return np.nan, int(x.split()[0])
        except:
            return np.nan, np.nan
    return np.nan, np.nan

df[["duration_minutes","seasons"]] = df["duration"].apply(lambda x: pd.Series(parse_duration(x)))

print("# 6) Validar release_year en rango razonable")
MIN_Y, MAX_Y = 1900, 2025
fuera_rango = df[(df["release_year"] < MIN_Y) | (df["release_year"] > MAX_Y)]
# Si quieres corregir:
df.loc[(df["release_year"] < MIN_Y) | (df["release_year"] > MAX_Y), "release_year"] = np.nan

print("# 7) Explode opcional para análisis por país / género")
def split_clean(s):
    return [t.strip() for t in str(s).split(",") if t.strip()]

df_countries = df.dropna(subset=["country"]).assign(country_list=df["country"].apply(split_clean)).explode("country_list")
df_genres    = df.assign(listed_list=df["listed_in"].apply(split_clean)).explode("listed_list")

import numpy as np

pd.set_option("display.max_colwidth", 140)
pd.set_option("display.width", 140)

# ---- Utilidades ----
def norm_txt(s: pd.Series):
    return (s.astype(str)
              .str.normalize("NFKD")
              .str.encode("ascii","ignore").str.decode("utf-8")
              .str.strip().str.lower())

def split_clean(s):
    return [t.strip() for t in str(s).split(",") if t and t.strip()]

# Campos texto útiles
text_cols = ["type","title","director","cast","country","rating","duration","listed_in","description","date_added"]
for c in text_cols:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip()

# Normalizados para detectar duplicados lógicos / casing
dfn = df.copy()
for c in ["type","title","country","rating"]:
    if c in dfn.columns:
        dfn[c + "_norm"] = norm_txt(dfn[c])

# Parseos auxiliares
dfn["date_added_dt"] = pd.to_datetime(dfn["date_added"], errors="coerce", dayfirst=False)

def parse_duration(x):
    x = str(x).strip().lower()
    if "min" in x:
        try: return int(x.split()[0]), np.nan
        except: return np.nan, np.nan
    if "season" in x:
        try: return np.nan, int(x.split()[0])
        except: return np.nan, np.nan
    return np.nan, np.nan

if "duration" in dfn.columns:
    dfn[["duration_minutes","seasons"]] = dfn["duration"].apply(lambda x: pd.Series(parse_duration(x)))

# ==========================================================
# 1) TÍTULOS DUPLICADOS “LÓGICOS”
#    (mismo title normalizado; inspecciona si son obras distintas o duplicados reales)
# ==========================================================
dupes_mask = dfn.duplicated(subset=["title_norm"], keep=False)
dupes_title = (dfn.loc[dupes_mask, ["show_id","title","title_norm","release_year","country","type","rating"]]
                   .sort_values(["title_norm","release_year","country"]))
print("\n>>> MUESTRA de títulos duplicados lógicos (primeros 20):")
print(dupes_title.head(20))

# Resumen por título normalizado
print("\n>>> Top títulos (normalizados) con más repeticiones:")
print(dupes_title["title_norm"].value_counts().head(10))

# ==========================================================
# 2) FECHAS NO PARSEABLES
# ==========================================================
bad_dates = dfn[dfn["date_added"].notna() & dfn["date_added_dt"].isna()][["show_id","date_added","title","type","release_year"]]
print("\n>>> FECHAS NO PARSEABLES (muestra):")
print(bad_dates.head(15))

print("\n>>> Formatos de fecha problemáticos (value_counts):")
print(bad_dates["date_added"].value_counts().head(20))

# ==========================================================
# 3) AÑOS FUERA DE RANGO (outliers)
# ==========================================================
MIN_Y, MAX_Y = 1900, 2025
yr_out = dfn[(dfn["release_year"] < MIN_Y) | (dfn["release_year"] > MAX_Y)][["show_id","title","release_year","type","country"]]
print("\n>>> AÑOS fuera de rango (muestra):")
print(yr_out.head(20))
print("\nRango observado:", int(dfn["release_year"].min()), "→", int(dfn["release_year"].max()))

# ==========================================================
# 4) DURATIONS RARAS (ni minutos ni seasons) o ambiguas
# ==========================================================
if "duration_minutes" in dfn and "seasons" in dfn:
    dur_bad = dfn[dfn["duration"].notna() & dfn["duration_minutes"].isna() & dfn["seasons"].isna()][["show_id","title","duration","type"]]
    print("\n>>> DURATIONS no reconocidas (muestra):")
    print(dur_bad.head(20))

    dur_both = dfn[dfn["duration_minutes"].notna() & dfn["seasons"].notna()][["show_id","title","duration","duration_minutes","seasons","type"]]
    print("\n>>> DURATIONS ambiguas (minutos y seasons simultáneamente) (muestra):")
    print(dur_both.head(10))

# ==========================================================
# 5) DIRECTORES NULOS (muestra al azar para revisar si conviene imputar)
# ==========================================================
if "director" in dfn.columns:
    dir_null = dfn[dfn["director"].isna() | (dfn["director"].astype(str).str.lower().isin(["nan","none","unknown"]))]
    print("\n>>> DIRECTOR nulo/unknown (muestra):")
    print(dir_null[["show_id","title","type","country","release_year","director"]].sample(min(10, len(dir_null)), random_state=42))

# ==========================================================
# 6) CASING INCONSISTENTE en TYPE / COUNTRY / RATING
#    (compara original vs normalizado para ver si hay variaciones)
# ==========================================================
def show_inconsist(c):
    raw = dfn[c].value_counts().head(10)
    norm = dfn[c + "_norm"].value_counts().head(10)
    print(f"\n>>> Muestras {c} (raw):\n{raw}")
    print(f"\n>>> Muestras {c}_norm:\n{norm}")

for c in ["type","country","rating"]:
    if c + "_norm" in dfn.columns:
        show_inconsist(c)

# ==========================================================
# 7) CAMPOS MULTIVALOR (country / listed_in) – inspección rápida
# ==========================================================
if "country" in dfn.columns:
    countries_exploded = (dfn.dropna(subset=["country"])
                             .assign(country_list=dfn["country"].apply(split_clean))
                             .explode("country_list"))
    print("\n>>> Top países (tras split):")
    print(norm_txt(countries_exploded["country_list"]).value_counts().head(15))

if "listed_in" in dfn.columns:
    genres_exploded = dfn.assign(listed_list=dfn["listed_in"].apply(split_clean)).explode("listed_list")
    print("\n>>> Top géneros/categorías (tras split):")
    print(norm_txt(genres_exploded["listed_list"]).value_counts().head(15))

# ==========================================================
# 8) EXPORTAR A EXCEL (para revisión manual cómoda)
#    Crea 'revision_datos.xlsx' con varias hojas: duplicados, fechas malas, años fuera, durations raras, etc.
# ==========================================================
with pd.ExcelWriter("revision_datos.xlsx", engine="xlsxwriter") as xw:
    dupes_title.to_excel(xw, sheet_name="duplicados_titulo", index=False)
    bad_dates.to_excel(xw, sheet_name="fechas_malas", index=False)
    yr_out.to_excel(xw, sheet_name="release_year_outliers", index=False)
    if "duration" in dfn.columns:
        dur_bad.to_excel(xw, sheet_name="duration_no_parse", index=False)
        dur_both.to_excel(xw, sheet_name="duration_ambigua", index=False)
    if "director" in dfn.columns:
        dir_null[["show_id","title","type","country","release_year","director"]].to_excel(xw, sheet_name="director_nulo", index=False)

print("\nArchivo generado: revision_datos.xlsx  (abre y revisa hoja por hoja)")

# fechas malas detectadas
print(fechas_malas.head(10))

# release_year fuera de rango antes de corregir (si guardaste 'fuera_rango')
print(fuera_rango.head(10))

df.to_csv("datos_limpios.csv", index=False, encoding="utf-8-sig")