# 🧪 Evidencias de despliegue
A continuación, se presentan las evidencias de la implementación y el procesamiento de datos realizado en Google Cloud Platform (GCP).

**LINK VIDEO EXPLICATIVO:**  [👉 VIDEO-PC3](./evidencias_pc3/Video-PC3.mp4)


Esta sección ilustra el resultado del trabajo, que involucró el procesamiento de los datasets de la empresa Nettalco para el proyecto del Parcial, utilizando la infraestructura de Big Data desplegada en GCP.

## 🗂️ 1. Google Cloud Storage 
## 💾 Configuración de Google Cloud Storage (GCS)

GCS actuará como nuestro sistema de archivos distribuido (donde almacenaremos los datos y los *scripts*).

### a. **Crear un *Bucket* de GCS**

Un *bucket* es el contenedor fundamental de almacenamiento de objetos en GCS.

1.  En la barra de búsqueda, escribimos y seleccionamos **"Cloud Storage"**.
2.  Hacemos clic en **"Crear bucket"**.
3.  Se asigna un nombre **único y global**
4.  Se selecciona la **Región** donde se desplegará el clúster de Dataproc.
5.  Configuramos las opciones de privacidad y protección .
6.  Hacemos clic en **"Crear"**.

![captura bucket](/grupo05_nettalco/PC3/evidencias_pc3/img_001.png)

### b. **Subir Archivos de Prueba (*Scripts* y *Datasets*)**

Una vez creado el *bucket*, subiremos los archivos que el clúster usará para el procesamiento.

1.  Dentro de tu *bucket*, haz clic en **"Subir archivos"** o arrastra los archivos al navegador de carpetas.
2.  Selecciona los *scripts* de Spark y los *datasets* de prueba desde tu máquina local.
3.  Haz clic en **"Abrir"** para iniciar la subida.

**Evidencia:** El *bucket* `nettalco-data-bd_grupo05` con los archivos CSV y los directorios de trabajo listos para ser utilizados por Dataproc.

![bucket GCS con CSV](/grupo05_nettalco/PC3/evidencias_pc3/img_002.png)

---

## 🗂️ 2. Cloud Shell
En este paso, utilizaremos la herramienta de línea de comandos `gcloud` a través de **Cloud Shell** para construir y lanzar el clúster.

### a. **Inicializar Cloud Shell y Desplegar el Clúster**

1.  Navega al servicio **Dataproc** en la Consola de GCP.
2.  Haz clic en el icono **Cloud Shell** (terminal en la web) en la esquina superior derecha de la Consola.
3.  Una vez en Cloud Shell, ejecuta el comando de creación del clúster (mostrado a continuación) para iniciar el despliegue de los recursos.

**Evidencia:** El Cloud Shell activo, mostrando los comandos de `gcloud dataproc clusters create` utilizados para configurar el entorno.

![3](/grupo05_nettalco/PC3/evidencias_pc3/img_003.png)

### b. **Comando de Despliegue**

Utilizaremos la herramienta de línea de comandos gcloud en Cloud Shell o en la  terminal local para desplegar el clúster.

```bash
gcloud dataproc clusters create nettalco-cluster \
    --region=us-east1 \
    --zone=us-east1-c \
    --master-machine-type=n1-standard-2 \
    --master-boot-disk-size=100 \
    --num-workers=2 \
    --worker-machine-type=n1-standard-2 \
    --worker-boot-disk-size=100 \
    --image-version=2.1-debian11 \
    --bucket=nettalco-data-bd_grupo05 \
    --optional-components=JUPYTER \
    --enable-component-gateway \
    --max-idle=336h \
    --project=nettalco-data-478503
```

![4](/grupo05_nettalco/PC3/evidencias_pc3/img_004.png)

## 🗂️ 3. Ejecución de Trabajos y Procesamiento de Datos(Dataproc) 

Una vez que el clúster `nettalco-cluster` está activo y los datos se encuentran en GCS, procedemos a ejecutar el *script* de Spark que realiza las transformaciones y la carga final de los datos. Utilizamos **JupyterLab** para la ejecución interactiva.

### a. **Ejecución del *Script* de Spark en JupyterLab**

El primer paso es ejecutar el *notebook* que contiene el código de **PySpark**. Este código lee los archivos CSV de Nettalco desde GCS, realiza las transformaciones y prepara los *datasets* para el análisis.

**Evidencia:** El entorno JupyterLab activo, mostrando el *notebook* `Procesamiento_nettalco.ipynb` con el código PySpark listo para la lectura y transformación de datos.

![Notebook_JupyterLab](/grupo05_nettalco/PC3/evidencias_pc3/img_006.png)

### b. **Carga de Datos Procesados a BigQuery**

Una vez transformados los datos con Spark, el *job* se encarga de cargarlos en BigQuery para su posterior consumo por herramientas de BI como Looker Studio. El clúster utiliza conectores Spark-BigQuery para realizar esta operación masiva.

**Evidencia:** La terminal de JupyterLab mostrando los comandos de `bq load` o los resultados de las operaciones de carga de Spark, confirmando el estado **DONE** (Completado) para múltiples tablas de Nettalco.

![Terminal de JupyterLab](/grupo05_nettalco/PC3/evidencias_pc3/img_007.png)

> **Nota:** La evidencia muestra la exitosa finalización de la carga de *datasets* clave como `ventas_volumen_ventas_por_cliente`, `eficiencia_operativa`, e `indice_ventas_cliente`.

---

# 🗂️ 4. BigQuery

Después del procesamiento en Dataproc, los resultados fueron cargados en
BigQuery dentro del dataset `ventas_nettalco`.\
Esta sección detalla las tablas finales creadas, su estructura y las
consultas SQL utilizadas para validar la consistencia de los datos
transformados.

------------------------------------------------------------------------

## 📌 4.1 Tablas creadas en BigQuery

Tras ejecutar los comandos `bq load`, el dataset `ventas_nettalco` quedó
conformado por **9 tablas finales**, cada una derivada de procesos
PySpark en Dataproc:

| Tabla                                   | Descripción Detallada                                                    |
|-----------------------------------------|--------------------------------------------------------------------------|
| **total_prendas_por_talla**             | Cantidad total de prendas producidas agrupadas según cada talla          |
| **volumen_ventas_por_cliente**          | Volumen acumulado de prendas entregadas por cada cliente                 |
| **fecha_ventas**                        | Registro diario de ventas procesadas por fecha                           |
| **tendencias_ventas_por_franja_horaria**| Análisis de ventas por franjas horarias (mañana, tarde, noche)           |
| **productos_mas_vendidos**              | Identificación y ranking de los estilos con mayor volumen de ventas       |
| **eficiencia_operativa**                | Proporción de eficiencia basada en fallas vs inspecciones realizadas      |
| **indice_ventas_cliente**               | Ventas por cliente, desglosadas por línea de producto                     |
| **prediccion_ventas**                   | Tendencias históricas con cálculo del promedio móvil de 7 periodos        |
| **comportamiento_clientes**             | Métricas de comportamiento: frecuencia de compra y promedio de prendas    |


![10](/grupo05_nettalco/PC3/evidencias_pc3/img_010.png)

------------------------------------------------------------------------

## 📥 4.2 Evidencia de la carga en BigQuery

A continuación se detallan los comandos utilizados para cargar cada una
de las tablas procesadas desde Google Cloud Storage hacia el dataset
`ventas_nettalco` en BigQuery.\
Cada comando utiliza `--autodetect` para permitir que BigQuery
identifique de manera automática los tipos de datos de cada columna.

------------------------------------------------------------------------

### 1. **Total prendas por talla**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.total_prendas_por_talla \
gs://nettalco-data-bd_grupo05/curated/total_prendas_por_talla/*.csv
```

### 2. **Volumen de ventas por cliente**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.volumen_ventas_por_cliente \
gs://nettalco-data-bd_grupo05/curated/volumen_ventas_por_cliente/*.csv
```

### 3. **Fecha ventas**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.fecha_ventas \
gs://nettalco-data-bd_grupo05/curated/fecha_ventas/*.csv
```

### 4. **Tendencias por franja horaria**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.tendencias_ventas_por_franja_horaria \
gs://nettalco-data-bd_grupo05/curated/tendencias_ventas_por_franja_horaria/*.csv
```

### 5. **Productos más vendidos**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.productos_mas_vendidos \
gs://nettalco-data-bd_grupo05/curated/productos_mas_vendidos/*.csv
```

### 6. **Eficiencia operativa**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.eficiencia_operativa \
gs://nettalco-data-bd_grupo05/curated/eficiencia_operativa/*.csv
```

### 7. **Índice de ventas por cliente y línea**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.indice_ventas_cliente \
gs://nettalco-data-bd_grupo05/curated/indice_ventas_cliente/*.csv
```

### 8. **Predicción de ventas**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.prediccion_ventas \
gs://nettalco-data-bd_grupo05/curated/prediccion_ventas/*.csv
```

### 9. **Comportamiento de clientes**

``` bash
bq load --source_format=CSV --autodetect ventas_nettalco.comportamiento_clientes \
gs://nettalco-data-bd_grupo05/curated/comportamiento_clientes/*.csv
```

------------------------------------------------------------------------

La carga fue realizada desde el nodo maestro vía `bq load`, confirmando
el estado **DONE** en todas las tablas:

    Current status: DONE

------------------------------------------------------------------------

## 🔎 4.3 Validación de datos en BigQuery

Se realizaron consultas para verificar:

-   Estructura
-   Tipos detectados
-   Calidad de datos
-   Integridad de agregaciones
-   Outliers

------------------------------------------------------------------------

# 🧪 4.4 Consultas SQL de validación

## ✅ A) Validar conteo de registros por tabla

``` sql
SELECT
  table_id,
  row_count,
  size_bytes,
  TIMESTAMP_MILLIS(creation_time) AS creation_time,
  TIMESTAMP_MILLIS(last_modified_time) AS last_modified
FROM `ventas_nettalco.__TABLES__`
ORDER BY row_count DESC;
```
![11](/grupo05_nettalco/PC3/evidencias_pc3/img_011.png)

## ✅ B) Revisar esquema

``` sql
SELECT 
  table_name,
  column_name,
  data_type
FROM `ventas_nettalco.INFORMATION_SCHEMA.COLUMNS`
ORDER BY table_name;
```
![12](/grupo05_nettalco/PC3/evidencias_pc3/img_012.png)

## ✅ C) Mostrar primeras filas

``` sql
SELECT *
FROM `ventas_nettalco.total_prendas_por_talla`
LIMIT 10;
```
![13](/grupo05_nettalco/PC3/evidencias_pc3/img_013.png)

------------------------------------------------------------------------

# 📊 4.5 Validaciones específicas por tabla

### **1️⃣ Total de prendas**

``` sql
SELECT SUM(TOTAL_PRENDAS) AS total_prendas_suma
FROM `ventas_nettalco.total_prendas_por_talla`;
```
![14](/grupo05_nettalco/PC3/evidencias_pc3/img_014.png)

### **2️⃣ Top clientes por volumen**

``` sql
SELECT 
  TCODICLIE,
  TOTAL_PRENDAS
FROM `ventas_nettalco.volumen_ventas_por_cliente`
ORDER BY TOTAL_PRENDAS DESC
LIMIT 10;
```
![15](/grupo05_nettalco/PC3/evidencias_pc3/img_015.png)

### **3️⃣ Validación por franja horaria**

``` sql
SELECT 
  FRANJA_HORARIA,
  COUNT(*) AS registros,
  SUM(TOTAL_PRENDAS) AS total
FROM `ventas_nettalco.tendencias_ventas_por_franja_horaria`
GROUP BY FRANJA_HORARIA;
```
![16](/grupo05_nettalco/PC3/evidencias_pc3/img_016.png)

### **4️⃣ Productos más vendidos**

``` sql
SELECT 
  ESTILO,
  TOTAL_PRENDAS
FROM `ventas_nettalco.productos_mas_vendidos`
ORDER BY TOTAL_PRENDAS DESC
LIMIT 15;
```
![17](/grupo05_nettalco/PC3/evidencias_pc3/img_017.png)

### **5️⃣ Eficiencia operativa**

``` sql
SELECT 
  MIN(EFICIENCIA_PORCENTUAL) AS min_ef,
  MAX(EFICIENCIA_PORCENTUAL) AS max_ef
FROM `ventas_nettalco.eficiencia_operativa`;
```

### **6️⃣ Tendencias con promedio móvil**

``` sql
SELECT 
  DATE(FECHA_TERMINO_TS) AS FECHA_TERMINO,
  ESTILO,
  TOTAL_PRENDAS,
  PROMEDIO_MOVIL
FROM `ventas_nettalco.prediccion_ventas`
ORDER BY FECHA_TERMINO DESC
LIMIT 20;
```
![18](/grupo05_nettalco/PC3/evidencias_pc3/img_018.png)

### **7️⃣ Comportamiento del cliente**

``` sql
SELECT
  TCODICLIE,
  FRECUENCIA_COMPRA,
  PROMEDIO_PRENDAS
FROM `ventas_nettalco.comportamiento_clientes`
ORDER BY FRECUENCIA_COMPRA DESC;
```
![19](/grupo05_nettalco/PC3/evidencias_pc3/img_019.png)

------------------------------------------------------------------------

# 🧩 4.6 Conclusión

BigQuery permitió validar que:

✔ Las tablas se cargaron exitosamente\
✔ Los tipos fueron detectados correctamente\
✔ Los cálculos de PySpark coinciden\
✔ Los datos están listos para visualización en Looker Studio

Esta fase asegura un flujo de Big Data estable y validado en GCP.

---

## 🗂️ 5. Dashboard en Looker
Los resultados del procesamiento se visualizaron en la siguiente herramienta:
![9](/grupo05_nettalco/PC3/evidencias_pc3/img_009.png)

**Link del Dashboard:** [Dashboard Looker Studio](https://lookerstudio.google.com/u/0/reporting/9139c4d1-2f52-4bd1-9e86-97b7554b2d58)

## 💰 6. Matriz de Costos y Optimización Financiera

Un componente crucial de cualquier despliegue en la nube es la gestión y optimización de costes. En esta sección, presentamos la matriz de costos actual del stack de Big Data, su desglose y las estrategias propuestas para lograr un ahorro significativo.

### a. Proyección de Costos (Matriz Resumen)

La siguiente matriz resume la situación financiera actual del proyecto y el potencial de ahorro estimado al implementar las políticas de optimización.

*Evidencia:* Matriz de Costos y Proyección de Uso (Cifras expresadas en Soles Peruanos: S/).

![20](/grupo05_nettalco/PC3/evidencias_pc3/img_020.png)

| Indicador | Valor Mensual | Valor Anual Estimado |
| :--- | :--- | :--- |
| *Costo Mensual Actual* | S/ 1,625.63 | - |
| *Costo Anual Estimado* | - | S/ 19,507.56 |
| *Ahorro Potencial* | S/ 956.07/mes | - |
| *Costo Optimizado (Estimado)* | S/ 669.56/mes | - |

### b. Desglose de Costos por Servicio

El análisis inicial revela que el *Procesamiento* (Dataproc) es el componente que representa la mayor parte del gasto (85.4%), seguido por la *Transferencia* de datos.

*Evidencia:* Desglose detallado de Costos por Servicio (Almacenamiento, Procesamiento y Transferencia).

![21](/grupo05_nettalco/PC3/evidencias_pc3/img_021.png)

| Servicio | Almacenamiento (S/) | Procesamiento (S/) | Transferencia (S/) | Total Mensual (S/) |
| :--- | :--- | :--- | :--- | :--- |
| *BigQuery* | S/ 88.13 | S/ 468.75 | S/ 56.25 | S/ 613.13 |
| *Cloud Storage* | S/ 43.13 | S/ 0.00 | S/ 31.88 | S/ 75.00 |
| *Dataproc (Spark)* | S/ 0.00 | S/ 918.75 | S/ 18.75 | S/ 937.50 |
| *Looker Studio* | S/ 0.00 | S/ 0.00 | S/ 0.00 | S/ 0.00 |
| *TOTAL* | *S/ 131.26 (8.1%)* | *S/ 1,387.50 (85.4%)* | *S/ 106.88 (6.6%)* | *S/ 1,625.63* |

### c. Propuesta de Optimización de Costos

Dado que el procesamiento (Dataproc) es el principal impulsor de costos, las siguientes estrategias se enfocan en la eficiencia del cómputo y el ciclo de vida de los datos, con un potencial de ahorro total de *S/ 956.07 mensuales*.

*Evidencia:* Propuesta de Optimización de Costos detallando las estrategias, el ahorro estimado y el porcentaje de descuento.

![22](/grupo05_nettalco/PC3/evidencias_pc3/img_022.png)

| Estrategia de Optimización | Implementación | Ahorro Mensual Estimado | % Ahorro |
| :--- | :--- | :--- | :--- |
| *Instancias Preemptibles en Dataproc* | Configurar workers como VMs preemptibles para trabajos tolerantes a fallos. | S/ 551.25 | -60% |
| *Clúster con *Autoscaling** | Escalar automáticamente según demanda y programar el apagado en horarios inactivos. | S/ 229.69 | -25% |
| *Lifecycle Policies en Cloud Storage* | Mover datos antiguos a clases de almacenamiento frías (Nearline/Coldline) después de 90 días. | S/ 21.56 | -50% |
| *Particionamiento en BigQuery* | Particionar tablas por fecha para reducir la cantidad de datos escaneados en consultas. | S/ 140.63 | -30% |
| *Compresión de Archivos CSV* | Convertir los archivos CSV a un formato columnar comprimido (Parquet o Avro). | S/ 12.94 | -30% |

---
