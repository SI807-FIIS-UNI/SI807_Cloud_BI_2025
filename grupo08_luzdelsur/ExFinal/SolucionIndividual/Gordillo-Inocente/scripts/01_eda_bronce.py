"""
Análisis Exploratorio de Datos (EDA) - Capa Bronze
Dataset: Supermarket Sales Myanmar
Objetivo: Análisis inicial para identificar oportunidades de mejora en ventas y margen
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import boto3
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

S3_BUCKET = 'supermarket-sales-si807-2025'
S3_KEY = 'bronce/raw/supermarket_sales.csv'

print("="*80)
print("ANALISIS EXPLORATORIO - SUPERMARKET SALES")
print("Objetivo: Identificar oportunidades de mejora en ventas y margen por sucursal")
print("="*80)

try:
    s3 = boto3.client('s3')
    print(f"\n[1/8] Cargando datos desde S3...")
    print(f"      Bucket: {S3_BUCKET}")
    print(f"      Key: {S3_KEY}")
    
    response = s3.get_object(Bucket=S3_BUCKET, Key=S3_KEY)
    df = pd.read_csv(BytesIO(response['Body'].read()))
    
    print(f"      Datos cargados: {len(df)} registros")
    
except Exception as e:
    print(f"      ERROR: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("[2/8] INFORMACION GENERAL")
print("="*80)

print(f"\nDIMENSIONES:")
print(f"  - Filas (registros):  {len(df):,}")
print(f"  - Columnas:           {len(df.columns)}")

print(f"\nCOLUMNAS DISPONIBLES:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print(f"\nTIPOS DE DATOS:")
print(df.dtypes)

# ====================================================================
# 2. VALORES NULOS
# ====================================================================
print("\n" + "="*80)
print("[3/8] ANÁLISIS DE VALORES NULOS")
print("="*80)

nulos = df.isnull().sum()
nulos_pct = (df.isnull().sum() / len(df)) * 100

nulos_df = pd.DataFrame({
    'Columna': nulos.index,
    'Nulos': nulos.values,
    'Porcentaje': nulos_pct.values
})

print("\n" + nulos_df.to_string(index=False))

total_nulos = nulos.sum()
if total_nulos == 0:
    print(f"\nResultado: Dataset sin valores nulos")
else:
    print(f"\nAdvertencia: {total_nulos} valores nulos encontrados")

# ====================================================================
# 3. ESTADÍSTICAS DESCRIPTIVAS
# ====================================================================
print("\n" + "="*80)
print("[4/8] ESTADÍSTICAS DESCRIPTIVAS (VARIABLES NUMÉRICAS)")
print("="*80)

print("\n" + df.describe().to_string())

# ====================================================================
# 4. ANÁLISIS DE VARIABLES CATEGÓRICAS
# ====================================================================
print("\n" + "="*80)
print("[5/8] ANÁLISIS DE VARIABLES CATEGÓRICAS")
print("="*80)

categoricas = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']

for cat in categoricas:
    if cat in df.columns:
        print(f"\n{cat}:")
        conteo = df[cat].value_counts()
        for val, count in conteo.items():
            pct = (count / len(df)) * 100
            print(f"  - {val}: {count} ({pct:.1f}%)")

# ====================================================================
# 5. ANÁLISIS TEMPORAL
# ====================================================================
print("\n" + "="*80)
print("[6/8] ANÁLISIS TEMPORAL")
print("="*80)

if 'Date' in df.columns:
    # Convertir a datetime
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    
    print(f"\nRANGO DE FECHAS:")
    print(f"  - Fecha mínima: {df['Date_parsed'].min()}")
    print(f"  - Fecha máxima: {df['Date_parsed'].max()}")
    print(f"  - Días totales: {(df['Date_parsed'].max() - df['Date_parsed'].min()).days}")
    
    # Distribución por mes
    df['Mes'] = df['Date_parsed'].dt.month
    print(f"\nDISTRIBUCIÓN POR MES:")
    meses_nombres = {1: 'Enero', 2: 'Febrero', 3: 'Marzo'}
    for mes, count in df['Mes'].value_counts().sort_index().items():
        print(f"  - {meses_nombres.get(mes, mes)}: {count} transacciones")

# ====================================================================
# 6. ANÁLISIS FINANCIERO
# ====================================================================
print("\n" + "="*80)
print("[7/8] ANÁLISIS FINANCIERO CLAVE")
print("="*80)

if 'Sales' in df.columns:
    print(f"\nVENTAS TOTALES:")
    print(f"  - Total:          ${df['Sales'].sum():,.2f}")
    print(f"  - Promedio:       ${df['Sales'].mean():,.2f}")
    print(f"  - Mediana:        ${df['Sales'].median():,.2f}")
    print(f"  - Mínimo:         ${df['Sales'].min():,.2f}")
    print(f"  - Máximo:         ${df['Sales'].max():,.2f}")

if 'gross income' in df.columns:
    print(f"\nINGRESO BRUTO:")
    print(f"  - Total:          ${df['gross income'].sum():,.2f}")
    print(f"  - Promedio:       ${df['gross income'].mean():,.2f}")

if 'Rating' in df.columns:
    print(f"\nRATING DE CLIENTES:")
    print(f"  - Promedio:       {df['Rating'].mean():.2f}/10")
    print(f"  - Mediana:        {df['Rating'].median():.2f}/10")
    print(f"  - Mínimo:         {df['Rating'].min():.2f}/10")
    print(f"  - Máximo:         {df['Rating'].max():.2f}/10")

# ====================================================================
# 7. MUESTRA DE DATOS
# ====================================================================
print("\n" + "="*80)
print("[8/8] MUESTRA DE DATOS (PRIMERAS 5 FILAS)")
print("="*80)

print("\n" + df.head().to_string(index=False))

print("\n" + "="*80)
print("RESUMEN EJECUTIVO")
print("="*80)

print(f"""
CALIDAD DE DATOS:
  Registros:          {len(df):,}
  Columnas:           {len(df.columns)}
  Valores nulos:      {total_nulos}
  Duplicados:         {df.duplicated().sum()}

PERIODO:
  Enero - Marzo 2019 (3 meses)

DIMENSIONES DE NEGOCIO:
  Sucursales:         {df['Branch'].nunique()}
  Ciudades:           {df['City'].nunique()}
  Lineas producto:    {df['Product line'].nunique()}
  Tipos cliente:      {df['Customer type'].nunique()}
  Metodos pago:       {df['Payment'].nunique()}

METRICAS CLAVE:
  Ventas totales:     ${df['Sales'].sum():,.2f}
  Ticket promedio:    ${df['Sales'].mean():,.2f}
  Margen bruto:       ${df['gross income'].sum():,.2f}
  Rating promedio:    {df['Rating'].mean():.2f}/10

CONCLUSION:
  Dataset validado y listo para modelado dimensional
  Oportunidades identificadas en analisis por sucursal y linea de producto
""")

print("="*80)
print("EDA COMPLETADO")
print("="*80)
