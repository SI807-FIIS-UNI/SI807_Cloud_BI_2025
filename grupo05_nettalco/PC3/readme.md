# 🧪 Evidencias de despliegue
A continuación, se presentan las evidencias de la implementación y el procesamiento de datos realizado en Google Cloud Platform (GCP).

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

## 🗂️ 4. Dashboard en Looker
Los resultados del procesamiento se visualizaron en la siguiente herramienta:
![9](/grupo05_nettalco/PC3/evidencias_pc3/img_009.png)

**Link del Dashboard:** [Dashboard Looker Studio](https://lookerstudio.google.com/u/0/reporting/9139c4d1-2f52-4bd1-9e86-97b7554b2d58)
