#!/bin/bash

# 1. Total prendas por talla
bq load --source_format=CSV --autodetect ventas_nettalco.total_prendas_por_talla \
gs://nettalco-data-bd_grupo05/curated/total_prendas_por_talla/*.csv

# 2. Volumen de ventas por cliente
bq load --source_format=CSV --autodetect ventas_nettalco.volumen_ventas_por_cliente \
gs://nettalco-data-bd_grupo05/curated/volumen_ventas_por_cliente/*.csv

# 3. Fecha ventas
bq load --source_format=CSV --autodetect ventas_nettalco.fecha_ventas \
gs://nettalco-data-bd_grupo05/curated/fecha_ventas/*.csv

# 4. Tendencias por franja horaria
bq load --source_format=CSV --autodetect ventas_nettalco.tendencias_ventas_por_franja_horaria \
gs://nettalco-data-bd_grupo05/curated/tendencias_ventas_por_franja_horaria/*.csv

# 5. Productos más vendidos
bq load --source_format=CSV --autodetect ventas_nettalco.productos_mas_vendidos \
gs://nettalco-data-bd_grupo05/curated/productos_mas_vendidos/*.csv

# 6. Eficiencia operativa
bq load --source_format=CSV --autodetect ventas_nettalco.eficiencia_operativa \
gs://nettalco-data-bd_grupo05/curated/eficiencia_operativa/*.csv

# 7. Índice de ventas por cliente y línea
bq load --source_format=CSV --autodetect ventas_nettalco.indice_ventas_cliente \
gs://nettalco-data-bd_grupo05/curated/indice_ventas_cliente/*.csv

# 8. Predicción de ventas
bq load --source_format=CSV --autodetect ventas_nettalco.prediccion_ventas \
gs://nettalco-data-bd_grupo05/curated/prediccion_ventas/*.csv

# 9. Comportamiento de clientes
bq load --source_format=CSV --autodetect ventas_nettalco.comportamiento_clientes \
gs://nettalco-data-bd_grupo05/curated/comportamiento_clientes/*.csv