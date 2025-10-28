# Directorio de Datos Procesados

Este directorio contiene datasets limpios y procesados listos para análisis.

## Archivos

### `sales_data_clean.csv`

**Descripción:** Datos de transacciones de ventas limpios y validados

**Origen:** Generado desde `data/raw/sales_data_sample.csv` por `01_data_cleaning_improved.ipynb`

**Proceso de Limpieza:**
1. Tratamiento de valores faltantes (STATE, POSTALCODE rellenados, campos críticos validados)
2. Conversiones de tipos de datos (ORDERDATE a datetime, IDs a enteros)
3. Detección y análisis de outliers (usando método IQR)
4. Eliminación de duplicados
5. Validación de datos (valores positivos para cantidades, precios, ventas)
6. Ingeniería de características (componentes de fecha, métricas de ingresos)

**Columnas:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| ORDERNUMBER | int | Identificador único de orden |
| QUANTITYORDERED | int | Número de unidades ordenadas |
| PRICEEACH | float | Precio por unidad |
| ORDERLINENUMBER | int | Número de línea dentro de la orden |
| SALES | float | Monto total de ventas para la línea |
| ORDERDATE | datetime | Fecha en que se realizó la orden |
| STATUS | string | Estado de la orden (Enviado, Cancelado, etc.) |
| QTR_ID | int | Trimestre (1-4) |
| MONTH_ID | int | Mes (1-12) |
| YEAR_ID | int | Año |
| PRODUCTLINE | string | Categoría de producto |
| MSRP | float | Precio de venta sugerido por el fabricante |
| PRODUCTCODE | string | Identificador de producto |
| CUSTOMERNAME | string | Nombre del cliente |
| PHONE | string | Teléfono del cliente |
| ADDRESSLINE1 | string | Dirección del cliente línea 1 |
| ADDRESSLINE2 | string | Dirección del cliente línea 2 |
| CITY | string | Ciudad del cliente |
| STATE | string | Estado/provincia del cliente |
| POSTALCODE | string | Código postal del cliente |
| COUNTRY | string | País del cliente |
| TERRITORY | string | Territorio de ventas |
| CONTACTLASTNAME | string | Apellido del contacto |
| CONTACTFIRSTNAME | string | Nombre del contacto |
| DEALSIZE | string | Categoría de tamaño de negociación (Small, Medium, Large) |

**Características Adicionales Creadas:**
- ORDER_YEAR: Año extraído de ORDERDATE
- ORDER_MONTH: Mes extraído de ORDERDATE
- ORDER_DAY: Día extraído de ORDERDATE
- ORDER_DAYOFWEEK: Día de la semana (0=Lunes, 6=Domingo)
- ORDER_QUARTER: Trimestre extraído de ORDERDATE
- REVENUE_PER_UNIT: Ventas divididas por cantidad ordenada

**Calidad de Datos:**
- Sin valores críticos faltantes
- Todos los valores numéricos validados (positivos)
- Fechas correctamente formateadas
- Duplicados eliminados
- Outliers identificados pero retenidos (casos de negocio legítimos)

**Estadísticas:**
- Registros originales: ~2,800
- Registros finales: Verificar salida del notebook para conteo exacto
- Tasa de retención: >95% (pérdida mínima de datos)
- Rango de fechas: 2003-2005
- Países: Múltiples (USA, Francia, España, Australia, etc.)
- Líneas de productos: 7 categorías

**Uso:**
- Cargar directamente en notebooks de análisis
- Usado por notebooks 02 y 03
- Puede cargarse con: `pd.read_csv('data/processed/sales_data_clean.csv')`

**Frecuencia de Actualización:**
- Regenerado cada vez que se ejecuta el notebook 01
- Actualizaciones manuales no recomendadas (usar flujo de notebooks)

**Formato de Archivo:**
- CSV (Valores Separados por Comas)
- Codificación: UTF-8
- Fila de encabezado incluida
- Sin columna de índice

**Notas:**
- Esta es la fuente única de verdad para todos los análisis posteriores
- No editar manualmente
- Para reprocesar, ejecutar notebook 01 con datos raw actualizados
- Tamaño de archivo: Aproximadamente 200-400 KB dependiendo del conteo final de registros
