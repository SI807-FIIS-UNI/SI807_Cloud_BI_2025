"""
Generacion de Dashboards - Capa Oro
Visualizaciones: Analisis de ventas, margen y comportamiento por sucursal
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import boto3
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

S3_BUCKET = 'supermarket-sales-si807-2025'
s3 = boto3.client('s3')

print("="*80)
print("GENERACION DE DASHBOARDS")
print("="*80)

def load_kpi(key):
    response = s3.get_object(Bucket=S3_BUCKET, Key=key)
    df = pd.read_parquet(BytesIO(response['Body'].read()))
    print(f"  Cargado: {key} ({len(df)} filas)")
    return df

print("\n[1/4] Cargando KPIs desde S3...")

kpi_ventas = load_kpi('oro/kpis/kpi_ventas_sucursal/kpi_ventas_sucursal.parquet')
kpi_productos = load_kpi('oro/kpis/kpi_top_productos/kpi_top_productos.parquet')
kpi_pagos = load_kpi('oro/kpis/kpi_ventas_pago/kpi_ventas_pago.parquet')
kpi_clientes = load_kpi('oro/kpis/kpi_ticket_cliente/kpi_ticket_cliente.parquet')

print("\n[2/4] Generando dashboard_1_ventas.png...")

fig, axes = plt.subplots(2, 2, figsize=(20, 14))
fig.suptitle('DASHBOARD 1: ANÁLISIS DE VENTAS POR CIUDAD Y PERÍODO', 
             fontsize=20, fontweight='bold', y=0.995)

ax1 = axes[0, 0]
city_total = kpi_ventas.groupby('city')['total_ventas'].sum().sort_values(ascending=False)
sns.barplot(x=city_total.index, y=city_total.values, palette='Set2', ax=ax1)
ax1.set_title('Ventas Totales por Ciudad', fontsize=14, fontweight='bold')
ax1.set_xlabel('Ciudad', fontsize=12)
ax1.set_ylabel('Ventas ($)', fontsize=12)
for i, v in enumerate(city_total.values):
    ax1.text(i, v + 1000, f'${v:,.0f}', ha='center', fontweight='bold')

ax2 = axes[0, 1]
for city in kpi_ventas['city'].unique():
    city_data = kpi_ventas[kpi_ventas['city'] == city].sort_values('mes')
    ax2.plot(city_data['mes'], city_data['total_ventas'], 
             marker='o', linewidth=2, label=city, markersize=8)
ax2.set_title('Evolución Mensual de Ventas', fontsize=14, fontweight='bold')
ax2.set_xlabel('Mes (2019)', fontsize=12)
ax2.set_ylabel('Ventas ($)', fontsize=12)
ax2.set_xticks([1, 2, 3])
ax2.set_xticklabels(['Enero', 'Febrero', 'Marzo'])
ax2.legend(loc='best', fontsize=10)
ax2.grid(True, alpha=0.3)

ax3 = axes[1, 0]
trans_ciudad = kpi_ventas.groupby('city')['total_transacciones'].sum()
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
wedges, texts, autotexts = ax3.pie(trans_ciudad, labels=trans_ciudad.index, 
                                     autopct='%1.1f%%', startangle=90,
                                     colors=colors_pie, textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax3.set_title('Distribución de Transacciones por Ciudad', fontsize=14, fontweight='bold')

ax4 = axes[1, 1]
pivot_ticket = kpi_ventas.pivot_table(values='ticket_promedio', index='city', columns='mes')
sns.heatmap(pivot_ticket, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax4, 
            cbar_kws={'label': 'Ticket Promedio ($)'})
ax4.set_title('Ticket Promedio: Ciudad vs Mes', fontsize=14, fontweight='bold')
ax4.set_xlabel('Mes', fontsize=12)
ax4.set_ylabel('Ciudad', fontsize=12)
ax4.set_xticklabels(['Enero', 'Febrero', 'Marzo'])

plt.tight_layout()
plt.savefig('C:/Users/User/Desktop/parte_final/docs/dashboard_1_ventas.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Guardado: docs/dashboard_1_ventas.png")

print("\n[3/4] Generando dashboard_2_productos.png...")

fig, axes = plt.subplots(2, 2, figsize=(20, 14))
fig.suptitle('DASHBOARD 2: ANÁLISIS DE PRODUCTOS Y RATINGS', 
             fontsize=20, fontweight='bold', y=0.995)

ax1 = axes[0, 0]
top6_productos = kpi_productos.nlargest(6, 'total_ventas')
sns.barplot(data=top6_productos, y='product_line', x='total_ventas', 
            palette='viridis', ax=ax1)
ax1.set_title('Top 6 Productos por Ventas', fontsize=14, fontweight='bold')
ax1.set_xlabel('Ventas Totales ($)', fontsize=12)
ax1.set_ylabel('Línea de Producto', fontsize=12)
for i, v in enumerate(top6_productos['total_ventas']):
    ax1.text(v + 500, i, f'${v:,.0f}', va='center', fontweight='bold')

ax2 = axes[0, 1]
productos_sorted = kpi_productos.sort_values('margen_bruto', ascending=False)
sns.barplot(data=productos_sorted, x='margen_bruto', y='product_line', 
            palette='coolwarm', ax=ax2)
ax2.set_title('Margen Bruto por Producto', fontsize=14, fontweight='bold')
ax2.set_xlabel('Margen Bruto ($)', fontsize=12)
ax2.set_ylabel('Línea de Producto', fontsize=12)

ax3 = axes[1, 0]
scatter = ax3.scatter(kpi_productos['rating_promedio'], 
                      kpi_productos['total_ventas'],
                      s=kpi_productos['total_transacciones']*5,
                      alpha=0.6, c=range(len(kpi_productos)), 
                      cmap='plasma', edgecolors='black', linewidth=1.5)
ax3.set_title('Rating vs Ventas (tamaño = transacciones)', fontsize=14, fontweight='bold')
ax3.set_xlabel('Rating Promedio', fontsize=12)
ax3.set_ylabel('Ventas Totales ($)', fontsize=12)
ax3.grid(True, alpha=0.3)
for idx, row in kpi_productos.iterrows():
    ax3.annotate(row['product_line'].split()[0], 
                 (row['rating_promedio'], row['total_ventas']),
                 fontsize=8, alpha=0.7)

ax4 = axes[1, 1]
margen_data = kpi_productos.sort_values('margen_porcentaje', ascending=False)
sns.barplot(data=margen_data, x='margen_porcentaje', y='product_line', 
            palette='RdYlGn', ax=ax4)
ax4.set_title('Margen % por Línea de Producto', fontsize=14, fontweight='bold')
ax4.set_xlabel('Margen Porcentaje (%)', fontsize=12)
ax4.set_ylabel('Línea de Producto', fontsize=12)
for i, v in enumerate(margen_data['margen_porcentaje']):
    ax4.text(v + 0.2, i, f'{v:.1f}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('C:/Users/User/Desktop/parte_final/docs/dashboard_2_productos.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Guardado: docs/dashboard_2_productos.png")

print("\n[4/4] Generando dashboard_3_clientes.png...")

fig, axes = plt.subplots(2, 2, figsize=(20, 14))
fig.suptitle('DASHBOARD 3: ANÁLISIS DE CLIENTES Y MÉTODOS DE PAGO', 
             fontsize=20, fontweight='bold', y=0.995)

ax1 = axes[0, 0]
pivot_pagos = kpi_pagos.pivot_table(values='total_transacciones', 
                                     index='city', columns='payment_method')
pivot_pagos.plot(kind='bar', ax=ax1, width=0.8)
ax1.set_title('Métodos de Pago por Ciudad', fontsize=14, fontweight='bold')
ax1.set_xlabel('Ciudad', fontsize=12)
ax1.set_ylabel('Total Transacciones', fontsize=12)
ax1.legend(title='Método de Pago', loc='upper right', fontsize=10)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)

ax2 = axes[0, 1]
pivot_pct = kpi_pagos.pivot_table(values='porcentaje', 
                                   index='city', columns='payment_method')
pivot_pct.plot(kind='bar', stacked=True, ax=ax2, colormap='Set3')
ax2.set_title('Distribución % Métodos de Pago por Ciudad', fontsize=14, fontweight='bold')
ax2.set_xlabel('Ciudad', fontsize=12)
ax2.set_ylabel('Porcentaje (%)', fontsize=12)
ax2.legend(title='Método', loc='upper right', fontsize=10)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.set_ylim(0, 100)

ax3 = axes[1, 0]
ticket_cliente = kpi_clientes.groupby('customer_type').agg({
    'ticket_promedio': 'mean',
    'total_transacciones': 'sum'
}).reset_index()
sns.barplot(data=ticket_cliente, x='customer_type', y='ticket_promedio', 
            palette='pastel', ax=ax3)
ax3.set_title('Ticket Promedio por Tipo de Cliente', fontsize=14, fontweight='bold')
ax3.set_xlabel('Tipo de Cliente', fontsize=12)
ax3.set_ylabel('Ticket Promedio ($)', fontsize=12)
for i, v in enumerate(ticket_cliente['ticket_promedio']):
    ax3.text(i, v + 5, f'${v:.2f}', ha='center', fontweight='bold')

ax4 = axes[1, 1]
pivot_ventas_pago = kpi_pagos.pivot_table(values='total_ventas', 
                                          index='payment_method', 
                                          columns='city')
sns.heatmap(pivot_ventas_pago, annot=True, fmt='.0f', cmap='Blues', ax=ax4,
            cbar_kws={'label': 'Ventas ($)'})
ax4.set_title('Ventas por Método de Pago y Ciudad', fontsize=14, fontweight='bold')
ax4.set_xlabel('Ciudad', fontsize=12)
ax4.set_ylabel('Método de Pago', fontsize=12)

plt.tight_layout()
plt.savefig('C:/Users/User/Desktop/parte_final/docs/dashboard_3_clientes.png', dpi=300, bbox_inches='tight')
plt.close()

print("  Guardado: docs/dashboard_3_clientes.png")

print("\n" + "="*80)
print("DASHBOARDS COMPLETADOS")
print("="*80)

print(f"""
ARCHIVOS GENERADOS:
  - dashboard_1_ventas.png (4 graficos)
  - dashboard_2_productos.png (4 graficos)
  - dashboard_3_clientes.png (4 graficos)

INSIGHTS:
  - Ciudad top ventas: {kpi_ventas.groupby('city')['total_ventas'].sum().idxmax()}
  - Producto top: {kpi_productos.iloc[0]['product_line']}
  - Ticket promedio: ${kpi_clientes['ticket_promedio'].mean():.2f}
  - Pago mas usado: {kpi_pagos.groupby('payment_method')['total_transacciones'].sum().idxmax()}
""")

print("="*80)
print("PROCESO COMPLETADO")
print("="*80)
