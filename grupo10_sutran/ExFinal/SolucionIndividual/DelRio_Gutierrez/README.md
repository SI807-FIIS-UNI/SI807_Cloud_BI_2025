# ELABORACIÓN EXAMEN FINAL 25-2

## 3.1. Ingestión y Estructuración

### CREACIÓN DE ESTRUCTURA DE CARPETA EN BUCKET

Se crea en el bucket retail-transactions-final
![image2](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image2.png)

### CARGA DE ARCHIVO CSV
Se realizo desde el powershell de mi máquina local:
```
gsutil cp "C:\Users\jairo\Documents\Proyectos\aradiel_25-2\SI807_Cloud_BI_2025\grupo10_sutran\ExFinal\SolucionIndividual\DelRio_Gutierrez\bronce\Retail_Transactions_Dataset.csv" gs://retail-transactions-final/raw/
```
Auntenticacion

![image1](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image1.png)

Carga de archivos exitosa
![image3](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image3.png)

### CRACION DEL CLUSTER

[VER AQUI EL SCRIPT UTIALIZADO](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/scripts/crear_cluster.sh)

### Análisis exploratorio (EDA)

Se ejecutó un análisis exploratorio inicial del dataset original ubicado en la carpeta `/raw` del bucket `retail-transactions-final`. El objetivo fue revisar estructura, tipos de datos, valores únicos y campos faltantes, sin realizar transformaciones.

**Notebook usado:** `01_eda_raw_dataset.ipynb`
[VER AQUI EL SCRIPT UTIALIZADO](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/scripts/01_eda_raw_dataset.ipynb)

![image5](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image5.png)

## 3.2. Limpieza y estructuración – trusted

Se construyó la capa `trusted` utilizando PySpark sobre Dataproc, realizando:
- Conversión de tipos: fecha, enteros, decimales
- Limpieza de valores nulos en la columna `Promotion`
- Formato final: `.parquet` para optimizar futuras lecturas y transformaciones

**Ruta del archivo limpio:**  
`gs://retail-transactions-final/trusted/retail_trusted.parquet`
[VER AQUI EL SCRIPT UTIALIZADO](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/scripts/02_trusted_dataset.ipynb)

**Notebook:** `02_trusted_dataset.ipynb`

LIMPIEZA DE DATOS

![image6](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image6.png)

DATA LIMPIA ALMACENADA CORRECTAMENTE

![image7](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image7.png)

### LOGGING
Durante el proceso ETL tuve unos problemas con el kernel lo que se ve reflejado en el explorador de registros

![image8](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image8.png)


### CREACIÓN DEL ESQUEMA ALMACENADO ES REFINED

| Tabla                  | Columnas sugeridas                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| **fact_transacciones** | Transaction_ID, Date, Customer_ID, Store_ID, monto (`Total_Cost`), unidades (`Total_Items`), Ticket promedio |
| **dim_tiempo**         | fecha, año, mes, día, hora, temporada                                                                        |
| **dim_producto**       | Product_ID (derivado), nombre del producto                                                                   |
| **dim_tienda**         | City, Store_Type                                                                                             |
| **dim_cliente**        | Customer_Name, Customer_Category                                                                             |

[VER AQUI EL SCRIPT UTIALIZADO](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/scripts/03_refined_modelo_estrella.ipynb)

![image9](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image9.png)

### CARGA DE TABLAS ESQUEMA ESTRELLA A BIGQUERY

![image10](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image10.png)


### KPIS
| KPI                      | Descripción                                                     |
| ------------------------ | --------------------------------------------------------------- |
|  Ticket promedio      | Promedio de `Total_Cost` por transacción                        |
|  Top 10 productos      | Aún no explotamos productos (opcional más adelante)             |
|  Frecuencia de compra  | Número de compras por cliente (si decides usar `Customer_Name`) |
|  Horas pico             | Horas con mayor cantidad de transacciones                       |
|  Promociones efectivas | Comparación entre transacciones con y sin promoción             |

![image11](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/evidencias/image11.png)

[VER AQUI EL SCRIPT UTIALIZADO](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/scripts/05_kpis.ipynb)

ACA SUBIMOS LOS KPIS A BIGQUERY PARA VISUALIZARLOS LUEGO EN EL LOOKER STUDIO

**Notebook usado:** `06_kpis_to_bigquery.ipynb`
[VER AQUI EL SCRIPT UTIALIZADO](/grupo10_sutran/ExFinal/SolucionIndividual/DelRio_Gutierrez/scripts/06_kpis_to_bigquery.ipynb)


### VISUALIZACIÓN DASHBOARD LOOKERSTUDIO

Los KPIs generados en la capa oro fueron cargados a BigQuery y visualizados en dashboards interactivos usando Looker Studio.

**Tablas utilizadas en BigQuery:**
- kpi_ticket_promedio
- kpi_horas_pico
- kpi_frecuencia_compras
- kpi_promociones



**Dashboard:** [[inserta aquí el enlace de tu dashboard una vez creado]](https://lookerstudio.google.com/reporting/7057ae85-e6c4-4cf0-8721-d51c63501a43)
