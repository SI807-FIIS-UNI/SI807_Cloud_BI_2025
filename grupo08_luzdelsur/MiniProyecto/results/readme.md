# Directorio de Resultados del Análisis

Este directorio contiene todas las salidas generadas del pipeline de análisis, incluyendo visualizaciones, métricas e insights de negocio.

## Archivos Generados

### Visualizaciones (Imágenes PNG)

Todas las visualizaciones se guardan como archivos PNG de alta resolución (300 DPI) adecuados para reportes y presentaciones.

#### Del Notebook de EDA (02):

**`distributions_numerical.png`**
- Histogramas de variables numéricas clave
- Muestra: Cantidad Ordenada, Precio Unitario, Ventas, MSRP
- Incluye líneas de referencia de media y mediana

**`distributions_categorical.png`**
- Gráficos de barras de frecuencias de variables categóricas
- Muestra: Estado, Línea de Producto, Tamaño de Negociación, País, Territorio
- Top 10 valores mostrados para cada una

**`sales_by_productline.png`**
- Ventas totales y promedio por categoría de producto
- Identifica líneas de producto con mejor y peor desempeño

**`sales_by_country.png`**
- Gráfico de barras horizontales de los 15 principales países por ingresos
- Comparación de desempeño geográfico

**`sales_by_territory.png`**
- Gráfico circular mostrando distribución de ventas por territorio
- Porcentajes de contribución regional

**`monthly_sales_trend.png`**
- Gráfico de líneas de series temporales de ventas mensuales
- Análisis de tendencias sobre el periodo completo del dataset

**`annual_quarterly_sales.png`**
- Comparación de ventas anuales
- Tendencias de ventas trimestrales por año

**`dealsize_analysis.png`**
- Distribución de ventas por tamaño de negociación (boxplot)
- Proporción de tamaños de negociación (gráfico circular)

**`correlation_matrix.png`**
- Mapa de calor de correlaciones entre características numéricas
- Identifica relaciones entre variables

**`productline_territory_heatmap.png`**
- Tabulación cruzada de ventas por línea de producto y territorio
- Patrones de desempeño geográfico de productos

**`top_customers_analysis.png`**
- Top 20 clientes por ingresos
- Gráfico de dispersión de órdenes vs ventas de clientes

**`order_status_distribution.png`**
- Gráfico de barras de frecuencias de estados de órdenes
- Tasas de completitud y problemas

#### Del Notebook de Insights de Negocio (03):

**`customer_segmentation.png`**
- Distribución de segmentos de clientes (gráfico circular)
- Valor monetario por segmento (gráfico de barras)
- Basado en análisis RFM

**`kmeans_clustering.png`**
- Gráfico de dispersión 3D de clusters de clientes
- Distribución de tamaño de clusters
- Resultados de segmentación K-means

**`product_performance.png`**
- Top 20 productos por ingresos
- Dispersión de Órdenes vs Ventas (tamaño de burbuja = cantidad)
- Métricas de eficiencia de productos

**`seasonal_patterns.png`**
- Patrón de ventas mensuales (gráfico de líneas)
- Distribución de ventas por día de la semana
- Identifica periodos pico

### Exportaciones de Datos (Archivos CSV)

**`summary_statistics.csv`**
- Métricas resumen generales del dataset
- Ventas totales, órdenes, clientes
- Rangos de fechas y promedios

**`customer_rfm_analysis.csv`**
- Scores RFM para cada cliente
- Valores de Recencia, Frecuencia, Monetario
- Asignaciones de segmentos de clientes
- Usado para marketing dirigido

**`product_performance.csv`**
- Métricas completas de productos
- Ventas totales, conteo de órdenes, cantidades
- Cálculos de ingresos por orden
- Ranking de productos por desempeño

**`geographic_analysis.csv`**
- Desempeño por país y territorio
- Ventas por cliente por región
- Métricas de concentración de clientes

### Reportes de Texto

**`business_insights.txt`**
- Resumen de insights clave de negocio
- Segmentos con mejor desempeño identificados
- Recomendaciones estratégicas
- Próximos pasos accionables

## Uso

### Ver Resultados

**Visualizaciones:**
- Abrir archivos PNG con cualquier visor de imágenes
- Importar en presentaciones o reportes
- Todas las imágenes son de calidad para publicación

**Archivos de Datos:**
- Abrir archivos CSV con Excel, pandas o cualquier herramienta de hojas de cálculo
- Usar para análisis adicional o reportes
- Pueden importarse en herramientas de BI

**Reportes de Texto:**
- Abrir con cualquier editor de texto
- Contiene resumen ejecutivo
- Listo para compartir con stakeholders

### Regenerar Resultados

Para regenerar todas las salidas:

**Windows:**
```powershell
.\scripts\run_analysis.bat
```

**Linux/Mac:**
```bash
bash scripts/run_analysis.sh
```

O ejecutar notebooks 02 y 03 manualmente después de limpiar los datos.

## Organización de Archivos

Los resultados están organizados por tipo de análisis:
- **Visualizaciones descriptivas:** Gráficos de distribución y frecuencia
- **Visualizaciones analíticas:** Tendencias, correlaciones, comparaciones
- **Salidas de segmentación:** Agrupaciones de clientes y productos
- **Inteligencia de negocio:** Insights y recomendaciones

## Notas

- Todos los archivos se sobrescriben cuando los notebooks se re-ejecutan
- Guardar versiones importantes en otro lugar si es necesario
- Los archivos PNG pueden convertirse a otros formatos si se requiere
- Los archivos CSV mantienen precisión completa para valores numéricos
- Datasets grandes pueden producir tamaños de archivo mayores

## Mejores Prácticas

1. Revisar visualizaciones para calidad de datos antes de presentar
2. Cruzar referencias de insights con conocimiento de negocio
3. Actualizar análisis cuando nuevos datos estén disponibles
4. Archivar resultados por fecha para comparación histórica
5. Compartir insights con stakeholders relevantes

## Permisos de Archivos

- Todos los archivos son accesibles para lectura/escritura
- No se requieren permisos especiales
- Seguro de eliminar para regeneración
