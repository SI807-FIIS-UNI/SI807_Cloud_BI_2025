# ExFinal — AWS (Bronce → Plata → Oro) — Aymachoque_Aymachoque

## Datos y recursos
- Región: `us-east-1`
- Bucket: `exfinal-aymachoque-1765858502`
- Archivo fuente: `Sample_Superstore.csv`

---

# 3.1 — BRONCE (S3 + carga CSV + EDA)

## 3.1.1 Variables de trabajo (CloudShell)
```bash
REGION="us-east-1"
BUCKET="exfinal-aymachoque-1765858502"

echo "REGION=$REGION"
echo "BUCKET=$BUCKET"
```

## 3.1.2 Crear bucket (CLI)
```bash
aws s3 mb "s3://$BUCKET" --region "$REGION"
aws s3api head-bucket --bucket "$BUCKET" && echo "Bucket OK"
```

## 3.1.3 Crear estructura Bronce (CLI)
```bash
printf "" > .keep
aws s3 cp .keep "s3://$BUCKET/bronce/raw/.keep"
aws s3 cp .keep "s3://$BUCKET/bronce/processed/.keep"
aws s3 cp .keep "s3://$BUCKET/bronce/curated/.keep"

aws s3 ls "s3://$BUCKET/bronce/" --recursive
```
<img width="1694" height="515" alt="estructrua" src="https://github.com/user-attachments/assets/324eeea5-d35d-440a-a208-40f8aba4e2c8" />

## 3.1.4 Cargar CSV a Bronce/Raw (CLI)
(Archivo local en CloudShell: `Sample_Superstore.csv`)
```bash
aws s3 cp "Sample_Superstore.csv" "s3://$BUCKET/bronce/raw/Sample_Superstore.csv"
aws s3 ls "s3://$BUCKET/bronce/raw/"
```
<img width="1671" height="471" alt="Bronce raw" src="https://github.com/user-attachments/assets/500ec661-9e70-42f8-8b03-9a44e0a5b4af" />

## 3.1.5 Crear carpeta de evidencias `docs/` (CLI)
```bash
aws s3 cp .keep "s3://$BUCKET/docs/.keep"
aws s3 ls "s3://$BUCKET/docs/"
```

## 3.1.6 Script EDA (eda_bronce.py)
```python
import pandas as pd

CSV = "Sample_Superstore.csv"

def read_csv_with_fallback(path: str):
    for enc in ["utf-8", "utf-8-sig", "cp1252", "latin1"]:
        try:
            df = pd.read_csv(path, encoding=enc)
            print(f"OK: leído con encoding={enc}")
            return df, enc
        except Exception:
            pass
    raise RuntimeError("No se pudo leer el CSV con encodings comunes")

df, used = read_csv_with_fallback(CSV)

print("=== EDA BRONCE: Sample_Superstore ===")
print("Filas, Columnas:", df.shape)

print("\n--- Columnas ---")
print(list(df.columns))

print("\n--- Nulos por columna (top 20) ---")
print(df.isna().sum().sort_values(ascending=False).head(20))

for c in ["Sales", "Profit", "Discount", "Quantity"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

num_cols = [c for c in ["Sales", "Profit", "Quantity"] if c in df.columns]
if num_cols:
    print("\n--- Estadísticas numéricas (si aplica) ---")
    print(df[num_cols].describe())

if "Region" in df.columns and "Sales" in df.columns:
    print("\n--- Ventas por Región (top 15) ---")
    print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False).head(15))

if "Segment" in df.columns and "Sales" in df.columns:
    print("\n--- Ventas por Segmento ---")
    print(df.groupby("Segment")["Sales"].sum().sort_values(ascending=False))

if "Category" in df.columns and "Profit" in df.columns:
    print("\n--- Profit por Categoría ---")
    print(df.groupby("Category")["Profit"].sum().sort_values(ascending=False))

if "Product Name" in df.columns and "Profit" in df.columns:
    print("\n--- Ejemplos de registros con pérdida (Profit < 0) ---")
    cols = ["Product Name", "Profit"]
    print(df.loc[df["Profit"] < 0, cols].head(10))

if "Order Date" in df.columns and "Sales" in df.columns:
    d = df.copy()
    d["Order Date"] = pd.to_datetime(d["Order Date"], errors="coerce")
    d = d.dropna(subset=["Order Date"])
    d["YearMonth"] = d["Order Date"].dt.to_period("M").astype(str)
    serie = d.groupby("YearMonth")["Sales"].sum().sort_index()
    print("\n--- Tendencia mensual (últimos 12) ---")
    print(serie.tail(12))
```

## 3.1.7 Ejecutar EDA y guardar salida (CLI)
```bash
python3 eda_bronce.py | tee eda_output_31.txt
```

## 3.1.8 Subir evidencias Bronce a S3 (CLI)
```bash
cat > docs_bronce_31.txt << 'TXT'
BRONCE (3.1)
- Bucket: exfinal-aymachoque-1765858502
- Archivo: bronce/raw/Sample_Superstore.csv
- EDA: eda_bronce.py
- Salida: eda_output_31.txt
TXT

aws s3 cp "docs_bronce_31.txt" "s3://$BUCKET/docs/docs_bronce_31.txt"
aws s3 cp "eda_bronce.py"      "s3://$BUCKET/docs/eda_bronce.py"
aws s3 cp "eda_output_31.txt"  "s3://$BUCKET/docs/eda_output_31.txt"

aws s3 ls "s3://$BUCKET/docs/"
```

---

# 3.2 — PLATA (limpieza + modelo simple dim/fact)

## 3.2.1 Crear estructura Plata en S3 (CLI)
```bash
aws s3 cp .keep "s3://$BUCKET/plata/dim/.keep"
aws s3 cp .keep "s3://$BUCKET/plata/fact/.keep"
aws s3 ls "s3://$BUCKET/plata/" --recursive
```

## 3.2.2 Preparar archivo de entrada local (CLI)
Se usa `input_bronce.csv` como entrada para el script de plata.
```bash
aws s3 cp "s3://$BUCKET/bronce/raw/Sample_Superstore.csv" "input_bronce.csv"
ls -lh input_bronce.csv
```

## 3.2.3 Script Plata (plata_build.py)
```python
import pandas as pd

INP = "input_bronce.csv"

df = None
used = None
for enc in ["utf-8", "utf-8-sig", "cp1252", "latin1"]:
    try:
        df = pd.read_csv(INP, encoding=enc)
        used = enc
        break
    except Exception:
        pass

if df is None:
    raise RuntimeError("No se pudo leer el CSV con encodings comunes")

print(f"OK leído con encoding={used}")
print("Shape inicial:", df.shape)

for c in df.select_dtypes(include=["object"]).columns:
    df[c] = df[c].astype(str).str.strip()

df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"], errors="coerce")

for c in ["Sales", "Profit", "Discount"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

before = len(df)
df = df.dropna(subset=["Order Date"])
print(f"Order Date inválidas removidas: {before - len(df)}")

before = len(df)
df = df.drop_duplicates(subset=["Row ID"]) if "Row ID" in df.columns else df.drop_duplicates(subset=["Order ID","Product ID","Customer ID"])
print(f"Duplicados removidos: {before - len(df)}")

before = len(df)
df = df[df["Sales"] >= 0]
print(f"Sales < 0 removidas: {before - len(df)}")

before = len(df)
df = df[df["Quantity"] > 0]
print(f"Quantity <= 0 removidas: {before - len(df)}")

before = len(df)
df = df[(df["Discount"] >= 0) & (df["Discount"] <= 1)]
print(f"Discount fuera [0,1] removidas: {before - len(df)}")

df["Quantity"] = df["Quantity"].astype("Int64")
print("Shape después de limpieza:", df.shape)

dim_tiempo = df[["Order Date"]].drop_duplicates().sort_values("Order Date").reset_index(drop=True)
dim_tiempo["time_key"] = dim_tiempo.index + 1
dim_tiempo["year"] = dim_tiempo["Order Date"].dt.year
dim_tiempo["month"] = dim_tiempo["Order Date"].dt.month
dim_tiempo["quarter"] = dim_tiempo["Order Date"].dt.quarter
dim_tiempo["day"] = dim_tiempo["Order Date"].dt.day

dim_producto = (
    df.sort_values(["Product ID", "Category", "Sub-Category", "Product Name"])
      .drop_duplicates(subset=["Product ID"], keep="first")
      [["Product ID", "Product Name", "Category", "Sub-Category"]]
      .reset_index(drop=True)
)
dim_producto["product_key"] = dim_producto.index + 1

dim_cliente = (
    df.sort_values(["Customer ID", "Segment", "Customer Name"])
      .drop_duplicates(subset=["Customer ID"], keep="first")
      [["Customer ID", "Customer Name", "Segment"]]
      .reset_index(drop=True)
)
dim_cliente["customer_key"] = dim_cliente.index + 1

reg_cols = ["Region", "State", "City", "Postal Code", "Country"]
reg_cols = [c for c in reg_cols if c in df.columns]
dim_region = df[reg_cols].drop_duplicates().sort_values(reg_cols).reset_index(drop=True)
dim_region["region_key"] = dim_region.index + 1

fact = df.copy()
fact = fact.merge(dim_tiempo[["Order Date","time_key"]], on="Order Date", how="left")
fact = fact.merge(dim_producto[["Product ID","product_key"]], on="Product ID", how="left")
fact = fact.merge(dim_cliente[["Customer ID","customer_key"]], on="Customer ID", how="left")
fact = fact.merge(dim_region[reg_cols + ["region_key"]], on=reg_cols, how="left")

fact_ventas = fact[[
    "Order ID","time_key","product_key","customer_key","region_key",
    "Sales","Profit","Quantity","Discount"
]].copy()

dim_tiempo.to_csv("dim_tiempo.csv", index=False, encoding="utf-8", date_format="%Y-%m-%d")
dim_producto.to_csv("dim_producto.csv", index=False, encoding="utf-8")
dim_cliente.to_csv("dim_cliente.csv", index=False, encoding="utf-8")
dim_region.to_csv("dim_region.csv", index=False, encoding="utf-8")
fact_ventas.to_csv("fact_ventas.csv", index=False, encoding="utf-8")

print("\n=== RESUMEN PLATA ===")
print("dim_tiempo:", len(dim_tiempo))
print("dim_producto:", len(dim_producto))
print("dim_cliente:", len(dim_cliente))
print("dim_region:", len(dim_region))
print("fact_ventas:", len(fact_ventas))
print("fact_ventas debería ser igual a filas limpias:", len(df))
```

## 3.2.4 Ejecutar Plata y guardar log (CLI)
```bash
python3 plata_build.py | tee plata_build_log.txt
```

## 3.2.5 Subir outputs Plata a S3 (CLI)
```bash
aws s3 cp "dim_tiempo.csv"   "s3://$BUCKET/plata/dim/dim_tiempo.csv"
aws s3 cp "dim_producto.csv" "s3://$BUCKET/plata/dim/dim_producto.csv"
aws s3 cp "dim_cliente.csv"  "s3://$BUCKET/plata/dim/dim_cliente.csv"
aws s3 cp "dim_region.csv"   "s3://$BUCKET/plata/dim/dim_region.csv"
aws s3 cp "fact_ventas.csv"  "s3://$BUCKET/plata/fact/fact_ventas.csv"

aws s3 ls "s3://$BUCKET/plata/dim/"
aws s3 ls "s3://$BUCKET/plata/fact/"
```
<img width="1701" height="542" alt="plata" src="https://github.com/user-attachments/assets/bafff5dd-a3f4-4ce7-9713-8d0139d017f8" />

## 3.2.6 Subir evidencias Plata a S3 (CLI)
```bash
aws s3 cp "plata_build.py"      "s3://$BUCKET/docs/plata_build.py"
aws s3 cp "plata_build_log.txt" "s3://$BUCKET/docs/plata_build_log.txt"

aws s3 ls "s3://$BUCKET/docs/" | grep -E "plata_build"
```

---

# 3.2 — ORO (KPIs en CSV)

## 3.2.1 Crear estructura Oro en S3 (CLI)
```bash
aws s3 cp .keep "s3://$BUCKET/oro/kpis/.keep"
aws s3 ls "s3://$BUCKET/oro/kpis/"
```

## 3.2.2 Descargar Plata local para cálculo de KPIs (CLI)
```bash
aws s3 cp "s3://$BUCKET/plata/fact/fact_ventas.csv" "fact_ventas.csv"
aws s3 cp "s3://$BUCKET/plata/dim/dim_tiempo.csv"   "dim_tiempo.csv"
aws s3 cp "s3://$BUCKET/plata/dim/dim_producto.csv" "dim_producto.csv"
aws s3 cp "s3://$BUCKET/plata/dim/dim_cliente.csv"  "dim_cliente.csv"
aws s3 cp "s3://$BUCKET/plata/dim/dim_region.csv"   "dim_region.csv"
```

## 3.2.3 Script Oro (oro_kpis.py)
```python
import pandas as pd

fact = pd.read_csv("fact_ventas.csv", encoding="utf-8")
dim_tiempo = pd.read_csv("dim_tiempo.csv", encoding="utf-8")
dim_producto = pd.read_csv("dim_producto.csv", encoding="utf-8")
dim_cliente = pd.read_csv("dim_cliente.csv", encoding="utf-8")
dim_region = pd.read_csv("dim_region.csv", encoding="utf-8")

for c in ["Sales", "Profit", "Discount"]:
    fact[c] = pd.to_numeric(fact[c], errors="coerce")
fact["Quantity"] = pd.to_numeric(fact["Quantity"], errors="coerce")

ventas_total = float(fact["Sales"].sum())
profit_total = float(fact["Profit"].sum())
margen_pct = (profit_total / ventas_total * 100.0) if ventas_total else 0.0

kpi_resumen = pd.DataFrame([{
    "ventas_total": ventas_total,
    "profit_total": profit_total,
    "margen_pct": margen_pct
}])

fact_reg = fact.merge(dim_region[["region_key", "Region"]], on="region_key", how="left")
kpi_region = (fact_reg.groupby("Region", dropna=False)[["Sales","Profit"]]
              .sum()
              .reset_index())
kpi_region["margen_pct"] = kpi_region.apply(lambda r: (r["Profit"]/r["Sales"]*100.0) if r["Sales"] else 0.0, axis=1)
kpi_region = kpi_region.sort_values("Sales", ascending=False)

fact_seg = fact.merge(dim_cliente[["customer_key", "Segment"]], on="customer_key", how="left")
kpi_segmento = (fact_seg.groupby("Segment", dropna=False)[["Sales","Profit"]]
                .sum()
                .reset_index())
kpi_segmento["margen_pct"] = kpi_segmento.apply(lambda r: (r["Profit"]/r["Sales"]*100.0) if r["Sales"] else 0.0, axis=1)
kpi_segmento = kpi_segmento.sort_values("Sales", ascending=False)

dim_tiempo2 = dim_tiempo.copy()
dim_tiempo2["Order Date"] = pd.to_datetime(dim_tiempo2["Order Date"], errors="coerce")
dim_tiempo2["year_month"] = dim_tiempo2["Order Date"].dt.to_period("M").astype(str)

fact_time = fact.merge(dim_tiempo2[["time_key", "year_month"]], on="time_key", how="left")
kpi_tendencia = (fact_time.groupby("year_month", dropna=False)[["Sales","Profit"]]
                 .sum()
                 .reset_index()
                 .sort_values("year_month"))
kpi_tendencia["margen_pct"] = kpi_tendencia.apply(lambda r: (r["Profit"]/r["Sales"]*100.0) if r["Sales"] else 0.0, axis=1)

fact_prod = fact.merge(dim_producto[["product_key", "Product Name", "Category", "Sub-Category"]],
                       on="product_key", how="left")
kpi_top_prod = (fact_prod.groupby(["Product Name","Category","Sub-Category"], dropna=False)[["Sales","Profit","Quantity"]]
                .sum()
                .reset_index()
                .sort_values("Profit", ascending=False)
                .head(15))

kpi_resumen.to_csv("kpi_resumen.csv", index=False, encoding="utf-8")
kpi_region.to_csv("kpi_region.csv", index=False, encoding="utf-8")
kpi_segmento.to_csv("kpi_segmento.csv", index=False, encoding="utf-8")
kpi_tendencia.to_csv("kpi_tendencia_mensual.csv", index=False, encoding="utf-8")
kpi_top_prod.to_csv("kpi_top_productos_profit.csv", index=False, encoding="utf-8")

print("OK: KPIs generados")
print("kpi_resumen:", kpi_resumen.shape)
print("kpi_region:", kpi_region.shape)
print("kpi_segmento:", kpi_segmento.shape)
print("kpi_tendencia_mensual:", kpi_tendencia.shape)
print("kpi_top_productos_profit:", kpi_top_prod.shape)
```

## 3.2.4 Ejecutar Oro y guardar log (CLI)
```bash
python3 oro_kpis.py | tee oro_kpis_log.txt
```

## 3.2.5 Subir KPIs Oro a S3 (CLI)
```bash
aws s3 cp "kpi_resumen.csv"              "s3://$BUCKET/oro/kpis/kpi_resumen.csv"
aws s3 cp "kpi_region.csv"               "s3://$BUCKET/oro/kpis/kpi_region.csv"
aws s3 cp "kpi_segmento.csv"             "s3://$BUCKET/oro/kpis/kpi_segmento.csv"
aws s3 cp "kpi_tendencia_mensual.csv"    "s3://$BUCKET/oro/kpis/kpi_tendencia_mensual.csv"
aws s3 cp "kpi_top_productos_profit.csv" "s3://$BUCKET/oro/kpis/kpi_top_productos_profit.csv"

aws s3 ls "s3://$BUCKET/oro/kpis/"
```
<img width="1689" height="649" alt="Oro" src="https://github.com/user-attachments/assets/1efc5720-4b57-4608-9133-f9c02000618d" />

## 3.2.6 Subir evidencias Oro a S3 (CLI)
```bash
aws s3 cp "oro_kpis.py"      "s3://$BUCKET/docs/oro_kpis.py"
aws s3 cp "oro_kpis_log.txt" "s3://$BUCKET/docs/oro_kpis_log.txt"

aws s3 ls "s3://$BUCKET/docs/" | grep -E "oro_kpis"
```

---

# Verificaciones (S3)
```bash
echo "=== CHECK BRONCE ==="
aws s3 ls "s3://$BUCKET/bronce/" --recursive

echo "=== CHECK PLATA ==="
aws s3 ls "s3://$BUCKET/plata/" --recursive

echo "=== CHECK ORO ==="
aws s3 ls "s3://$BUCKET/oro/" --recursive

echo "=== CHECK DOCS ==="
aws s3 ls "s3://$BUCKET/docs/"
```


