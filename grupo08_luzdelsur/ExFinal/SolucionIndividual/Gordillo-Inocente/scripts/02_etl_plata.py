"""
ETL Capa Plata - Modelo Dimensional
Objetivo: Construir modelo estrella para analizar ventas y margen por sucursal, 
producto y tipo de cliente
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import boto3
from io import BytesIO
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

S3_BUCKET = 'supermarket-sales-si807-2025'
s3 = boto3.client('s3')

print("="*80)
print("ETL CAPA PLATA - MODELO ESTRELLA")
print("Objetivo: Modelado dimensional para analisis de ventas y margen")
print("="*80)

def save_parquet(df, key):
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, compression='snappy')
    buffer.seek(0)
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buffer.getvalue())
    print(f"  Guardado: {key} ({len(df)} filas)")

print("\n[1/7] Cargando datos desde Bronze...")

response = s3.get_object(Bucket=S3_BUCKET, Key='bronce/raw/supermarket_sales.csv')
df = pd.read_csv(BytesIO(response['Body'].read()))

print(f"  Datos cargados: {len(df)} filas, {len(df.columns)} columnas")

df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

print("\n[2/7] Construyendo dim_tiempo...")

dim_tiempo = pd.DataFrame({
    'fecha': df['Date'].dt.strftime('%Y-%m-%d'),
    'ano': df['Date'].dt.year,
    'mes': df['Date'].dt.month,
    'dia': df['Date'].dt.day,
    'trimestre': df['Date'].dt.quarter,
    'dia_semana': df['Date'].dt.day_name()
}).drop_duplicates().reset_index(drop=True)

meses_dict = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}
dim_tiempo['nombre_mes'] = dim_tiempo['mes'].map(meses_dict)

dim_tiempo.insert(0, 'tiempo_key', range(1, len(dim_tiempo) + 1))

save_parquet(dim_tiempo, 'plata/dimensiones/dim_tiempo/dim_tiempo.parquet')

print("\n[3/7] Construyendo dim_sucursal...")

dim_sucursal = df[['Branch', 'City']].drop_duplicates().reset_index(drop=True)
dim_sucursal.columns = ['branch', 'city']
dim_sucursal.insert(0, 'sucursal_key', range(1, len(dim_sucursal) + 1))

save_parquet(dim_sucursal, 'plata/dimensiones/dim_sucursal/dim_sucursal.parquet')

print("\n[4/7] Construyendo dim_producto...")

dim_producto = df[['Product line']].drop_duplicates().reset_index(drop=True)
dim_producto.columns = ['product_line']
dim_producto.insert(0, 'producto_key', range(1, len(dim_producto) + 1))

save_parquet(dim_producto, 'plata/dimensiones/dim_producto/dim_producto.parquet')

print("\n[5/7] Construyendo dim_cliente...")

dim_cliente = df[['Customer type', 'Gender']].drop_duplicates().reset_index(drop=True)
dim_cliente.columns = ['customer_type', 'gender']
dim_cliente.insert(0, 'cliente_key', range(1, len(dim_cliente) + 1))

save_parquet(dim_cliente, 'plata/dimensiones/dim_cliente/dim_cliente.parquet')

print("\n[6/7] Construyendo dim_pago...")

dim_pago = df[['Payment']].drop_duplicates().reset_index(drop=True)
dim_pago.columns = ['payment_method']
dim_pago.insert(0, 'pago_key', range(1, len(dim_pago) + 1))

save_parquet(dim_pago, 'plata/dimensiones/dim_pago/dim_pago.parquet')

print("\n[7/7] Construyendo fact_ventas...")

df['fecha_str'] = df['Date'].dt.strftime('%Y-%m-%d')

fact = df.copy()

fact = fact.merge(
    dim_tiempo[['fecha', 'tiempo_key']],
    left_on='fecha_str',
    right_on='fecha',
    how='left'
).drop('fecha', axis=1)

fact = fact.merge(
    dim_sucursal[['branch', 'city', 'sucursal_key']],
    left_on=['Branch', 'City'],
    right_on=['branch', 'city'],
    how='left'
).drop(['branch', 'city'], axis=1)

fact = fact.merge(
    dim_producto[['product_line', 'producto_key']],
    left_on='Product line',
    right_on='product_line',
    how='left'
).drop('product_line', axis=1)

fact = fact.merge(
    dim_cliente[['customer_type', 'gender', 'cliente_key']],
    left_on=['Customer type', 'Gender'],
    right_on=['customer_type', 'gender'],
    how='left'
).drop(['customer_type', 'gender'], axis=1)

fact = fact.merge(
    dim_pago[['payment_method', 'pago_key']],
    left_on='Payment',
    right_on='payment_method',
    how='left'
).drop('payment_method', axis=1)

fact_final = fact[[
    'Invoice ID',
    'tiempo_key',
    'sucursal_key',
    'producto_key',
    'cliente_key',
    'pago_key',
    'Unit price',
    'Quantity',
    'Tax 5%',
    'Sales',
    'cogs',
    'gross margin percentage',
    'gross income',
    'Rating'
]]

fact_final.columns = [
    'invoice_id',
    'tiempo_key',
    'sucursal_key',
    'producto_key',
    'cliente_key',
    'pago_key',
    'unit_price',
    'quantity',
    'tax',
    'sales',
    'cogs',
    'gross_margin_percentage',
    'gross_income',
    'rating'
]

fact_final.insert(0, 'venta_id', range(1, len(fact_final) + 1))

fact_final['year'] = df['Date'].dt.year

for year in fact_final['year'].unique():
    fact_year = fact_final[fact_final['year'] == year].drop('year', axis=1)
    key = f'plata/hechos/year={year}/fact_ventas.parquet'
    save_parquet(fact_year, key)

print("\n" + "="*80)
print("RESUMEN ETL PLATA")
print("="*80)

print(f"""
DIMENSIONES CREADAS:
  1. dim_tiempo:       {len(dim_tiempo)} filas
  2. dim_sucursal:     {len(dim_sucursal)} filas
  3. dim_producto:     {len(dim_producto)} filas
  4. dim_cliente:      {len(dim_cliente)} filas
  5. dim_pago:         {len(dim_pago)} filas

TABLA DE HECHOS:
  - fact_ventas:       {len(fact_final)} filas
  - Particiones:       year=2019

MODELO ESTRELLA COMPLETADO
Enfoque: Analisis de ventas y margen por sucursal, producto y cliente
""")

print("="*80)
print("ETL PLATA COMPLETADO")
print("="*80)
