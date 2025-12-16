"""
ETL Capa Oro - Generacion de KPIs
Objetivo: KPIs enfocados en mejora de ventas y margen por sucursal, 
linea de producto y tipo de cliente
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import boto3
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

S3_BUCKET = 'supermarket-sales-si807-2025'
s3 = boto3.client('s3')

print("="*80)
print("ETL CAPA ORO - GENERACION DE KPIs")
print("Objetivo: Metricas clave para optimizacion de ventas y margen")
print("="*80)

def load_parquet(key):
    response = s3.get_object(Bucket=S3_BUCKET, Key=key)
    return pd.read_parquet(BytesIO(response['Body'].read()))

def load_partitioned(prefix):
    objs = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    if 'Contents' not in objs:
        print(f"  Advertencia: No se encontraron archivos en {prefix}")
        return pd.DataFrame()
    
    dfs = []
    for obj in objs['Contents']:
        if obj['Key'].endswith('.parquet'):
            dfs.append(load_parquet(obj['Key']))
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def save_parquet(df, key):
    buffer = BytesIO()
    df.to_parquet(buffer, index=False, compression='snappy')
    buffer.seek(0)
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=buffer.getvalue())
    print(f"  Guardado: {key} ({len(df)} filas)")

print("\n[1/6] Cargando datos desde Plata...")

dim_tiempo = load_parquet('plata/dimensiones/dim_tiempo/dim_tiempo.parquet')
dim_sucursal = load_parquet('plata/dimensiones/dim_sucursal/dim_sucursal.parquet')
dim_producto = load_parquet('plata/dimensiones/dim_producto/dim_producto.parquet')
dim_cliente = load_parquet('plata/dimensiones/dim_cliente/dim_cliente.parquet')
dim_pago = load_parquet('plata/dimensiones/dim_pago/dim_pago.parquet')
fact_ventas = load_partitioned('plata/hechos/')

print(f"  dim_tiempo:      {len(dim_tiempo)} filas")
print(f"  dim_sucursal:    {len(dim_sucursal)} filas")
print(f"  dim_producto:    {len(dim_producto)} filas")
print(f"  dim_cliente:     {len(dim_cliente)} filas")
print(f"  dim_pago:        {len(dim_pago)} filas")
print(f"  fact_ventas:     {len(fact_ventas)} filas")

print("\n[2/6] Generando KPI 1: Ventas y margen por sucursal...")

fact_sucursal = fact_ventas.merge(dim_tiempo, on='tiempo_key') \
                            .merge(dim_sucursal, on='sucursal_key')

kpi1 = fact_sucursal.groupby(['branch', 'city', 'ano', 'mes']).agg({
    'venta_id': 'count',
    'sales': 'sum',
    'gross_income': 'sum'
}).reset_index()

kpi1.columns = ['branch', 'city', 'ano', 'mes', 'total_transacciones', 'total_ventas', 'margen_bruto']
kpi1['ticket_promedio'] = kpi1['total_ventas'] / kpi1['total_transacciones']
kpi1['margen_porcentaje'] = (kpi1['margen_bruto'] / kpi1['total_ventas']) * 100

kpi1 = kpi1.sort_values('total_ventas', ascending=False)

save_parquet(kpi1, 'oro/kpis/kpi_ventas_sucursal/kpi_ventas_sucursal.parquet')

print("\n[3/6] Generando KPI 2: Top lineas de producto...")

fact_prod = fact_ventas.merge(dim_producto, on='producto_key')

kpi2 = fact_prod.groupby('product_line').agg({
    'venta_id': 'count',
    'sales': 'sum',
    'gross_income': 'sum',
    'rating': 'mean'
}).reset_index()

kpi2.columns = ['product_line', 'total_transacciones', 'total_ventas', 'margen_bruto', 'rating_promedio']
kpi2['margen_porcentaje'] = (kpi2['margen_bruto'] / kpi2['total_ventas']) * 100

kpi2 = kpi2.sort_values('total_ventas', ascending=False)

save_parquet(kpi2, 'oro/kpis/kpi_top_productos/kpi_top_productos.parquet')

print("\n[4/6] Generando KPI 3: Ventas por tipo de pago...")

fact_pago_suc = fact_ventas.merge(dim_sucursal, on='sucursal_key') \
                            .merge(dim_pago, on='pago_key')

kpi3 = fact_pago_suc.groupby(['city', 'payment_method']).agg({
    'venta_id': 'count',
    'sales': 'sum'
}).reset_index()

kpi3.columns = ['city', 'payment_method', 'total_transacciones', 'total_ventas']

kpi3['total_ciudad'] = kpi3.groupby('city')['total_transacciones'].transform('sum')
kpi3['porcentaje'] = (kpi3['total_transacciones'] / kpi3['total_ciudad']) * 100
kpi3 = kpi3.drop('total_ciudad', axis=1)

kpi3 = kpi3.sort_values(['city', 'total_transacciones'], ascending=[True, False])

save_parquet(kpi3, 'oro/kpis/kpi_ventas_pago/kpi_ventas_pago.parquet')

print("\n[5/6] Generando KPI 4: Ticket promedio por cliente...")

fact_cliente_suc = fact_ventas.merge(dim_cliente, on='cliente_key') \
                               .merge(dim_sucursal, on='sucursal_key')

kpi4 = fact_cliente_suc.groupby(['customer_type', 'gender', 'city']).agg({
    'venta_id': 'count',
    'sales': ['sum', 'mean'],
    'gross_income': 'sum'
}).reset_index()

kpi4.columns = ['customer_type', 'gender', 'city', 'total_transacciones', 'total_ventas', 'ticket_promedio', 'margen_bruto']

kpi4 = kpi4.sort_values('total_ventas', ascending=False)

save_parquet(kpi4, 'oro/kpis/kpi_ticket_cliente/kpi_ticket_cliente.parquet')

print("\n[6/6] Generando vista ejecutiva...")

vista = fact_ventas.merge(dim_tiempo, on='tiempo_key') \
                   .merge(dim_sucursal, on='sucursal_key') \
                   .merge(dim_producto, on='producto_key') \
                   .merge(dim_cliente, on='cliente_key') \
                   .merge(dim_pago, on='pago_key')

vista_final = vista[[
    'invoice_id',
    'fecha',
    'branch',
    'city',
    'customer_type',
    'gender',
    'product_line',
    'payment_method',
    'unit_price',
    'quantity',
    'sales',
    'gross_income',
    'rating',
    'ano'
]]

for year in vista_final['ano'].unique():
    vista_year = vista_final[vista_final['ano'] == year].drop('ano', axis=1)
    key = f'oro/kpis/vista_ejecutiva/year={year}/vista_ejecutiva.parquet'
    save_parquet(vista_year, key)

print("\n" + "="*80)
print("RESUMEN ETL ORO")
print("="*80)

print(f"""
KPIs GENERADOS (Enfoque: Mejora de ventas y margen):

1. kpi_ventas_sucursal ({len(kpi1)} filas)
   - Ventas, margen y ticket promedio por sucursal y mes
   - Top sucursal: {kpi1.iloc[0]['branch']} - {kpi1.iloc[0]['city']}

2. kpi_top_productos ({len(kpi2)} filas)
   - Ranking de lineas de producto por ventas y margen
   - Top producto: {kpi2.iloc[0]['product_line']}

3. kpi_ventas_pago ({len(kpi3)} filas)
   - Distribucion de ventas por metodo de pago
   - Analisis de preferencias por ciudad

4. kpi_ticket_cliente ({len(kpi4)} filas)
   - Ticket promedio por tipo de cliente
   - Segmentacion por genero y ciudad

5. vista_ejecutiva ({len(vista_final)} filas)
   - Vista completa para analisis ad-hoc

METRICAS CLAVE:
  Total ventas:    ${fact_ventas['sales'].sum():,.2f}
  Margen bruto:    ${fact_ventas['gross_income'].sum():,.2f}
  Ticket promedio: ${fact_ventas['sales'].mean():,.2f}
""")

print("="*80)
print("ETL ORO COMPLETADO")
print("="*80)
