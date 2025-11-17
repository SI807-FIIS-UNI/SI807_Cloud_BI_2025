# Laboratorio GCP_GRUPO 5: Levantar Cluster Hadoop utilizando Google Cloud Platform 

## 📖 1. **Introducción**

En esta guía, aprenderás a crear y configurar un clúster de procesamiento de datos en Google Cloud Platform (GCP). Utilizaremos Google Cloud Dataproc para desplegar de manera eficiente un entorno que soporte:

Hadoop y Apache Spark: Las herramientas esenciales para el procesamiento distribuido de grandes volúmenes de datos (Big Data).

Simulación de Streaming en Tiempo Real: Realizaremos un ejercicio práctico integrando Kafka y Spark Streaming para demostrar el procesamiento de datos en vivo.

## 🎯 Lo que Lograrás al Finalizar la Guía

Al completar este tutorial, habrás adquirido las siguientes habilidades y conocimientos prácticos:

* Entenderás el flujo de trabajo para el **despliegue y gestión de clústeres** de procesamiento de datos en Google Cloud Platform.
* Sabrás cómo configurar y utilizar **Google Cloud Storage (GCS)** como el sistema de archivos distribuido (*cloud-native*) para tu clúster.
* Serás capaz de **levantar un clúster de Hadoop y Spark** utilizando Google Cloud Dataproc de manera rápida y eficiente.
* Aprenderás a integrar **Apache Kafka y Spark Streaming** para configurar una simulación completa de **procesamiento de datos en tiempo real**.

---

## 2. 💡 **Conceptos Fundamentales**

Esta sección define los componentes clave de la infraestructura que utilizaremos para el despliegue del clúster.

### a. **¿Qué es Google Cloud Platform (GCP)?**

GCP es una *suite* de servicios de computación en la nube que ofrece Google. Permite a los usuarios almacenar, procesar y analizar grandes volúmenes de datos, así como desplegar aplicaciones con alta escalabilidad.

**Servicios clave en esta guía:**

* **Dataproc:** Servicio gestionado para el despliegue de clústeres Hadoop y Spark.
* **BigQuery:** Almacén de datos (*data warehouse*) sin servidor, altamente escalable.
* **Cloud Storage (GCS):** Servicio de almacenamiento de objetos unificado.

### b. **¿Qué es Google Cloud Dataproc?**

Dataproc es un servicio rápido, fácil de usar y gestionado por GCP que permite **desplegar y administrar clústeres de Big Data** (Hadoop, Spark, Flink, Presto, etc.) de forma eficiente. Reduce el tiempo de despliegue de minutos a segundos y automatiza las tareas de mantenimiento.

### c. **¿Qué es Google Cloud Storage (GCS)?**

GCS es un **servicio de almacenamiento de objetos** altamente duradero y escalable. En el contexto de Big Data, GCS se utiliza como el **sistema de archivos principal** (en lugar de HDFS) para almacenar los *datasets* que serán procesados por las aplicaciones de Hadoop y Spark.

---

## 3. 🛠️ **Herramientas Tecnológicas a Utilizar**

Para completar esta guía, nos apoyaremos en las siguientes plataformas y *frameworks*:

* **Google Cloud Console:** La interfaz principal para gestionar los recursos de GCP.
* **Google Dataproc:** Para el despliegue y orquestación del clúster.
* **Google Cloud Storage (GCS):** Para el almacenamiento persistente de datos.
* **Apache Hadoop:** El *framework* esencial para el procesamiento distribuido.
* **Apache Spark:** El motor de análisis de datos que permite un procesamiento rápido en memoria.
* **Apache Kafka:** Para la creación de *pipelines* de datos en tiempo real (utilizado en la simulación de *streaming*).

---

## 4. ⚙️ **Configuración Inicial en Google Cloud Platform (GCP)**

Antes de proceder con el despliegue del clúster, es necesario configurar el entorno de trabajo en GCP.

### a. **Crear una Cuenta en GCP**

Si aún no tienes una cuenta, regístrate a través del siguiente enlace. GCP ofrece una capa gratuita (Free Tier) y créditos para nuevos usuarios.

**Enlace de registro:**
[https://cloud.google.com/](https://cloud.google.com/)


Una vez registrado, accederás a la **Consola de Google Cloud** para comenzar a gestionar tus recursos.

![consola](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/imagen002_consola.png)


### b. **Crear un Proyecto**

Todos los recursos en GCP deben estar contenidos dentro de un proyecto.

1. Navega al selector de proyectos en la barra superior (junto al logo de Google Cloud).
   ![captura de proyecto](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/imagen003_capturaProyecto.png)
   
2. Haz clic en **"Proyecto nuevo"** o **"Crear proyecto"**.

![captura de proyecto](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/imagen004_capturaProyecto2.png)

3. Asigna un nombre descriptivo al proyecto.
4. **Guarda el ID del proyecto** (es único y lo necesitarás más adelante).

![captura de proyecto](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/id_proyecto.png)

### c. **Habilitar APIs Necesarias**

Debemos asegurar que el servicio Dataproc esté habilitado para poder crear el clúster.

1. En la barra de búsqueda superior, escribe y selecciona **"APIs & Servicios"**.
2. Haz clic en **"Habilitar APIs y servicios"**.
3. Busca y habilita la API: **Google Cloud Dataproc**.

![captura habilitar API](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/imagen006_APIS.png)

### d. **Configurar Permisos de IAM**

Verifica que tu cuenta de usuario tenga los permisos necesarios para crear y gestionar clústeres.

1. Ve a **IAM & Admin** (Identidad y Acceso Gestionado).
2. Confirma que tienes asignado alguno de los siguientes roles en el proyecto:
    * **Editor** (cubre la mayoría de las operaciones)
    * **Dataproc Editor** (rol específico para el servicio)

![captura IAM](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/IAM_imagen00.png)

---

## 5. 💾 **Configuración de Google Cloud Storage (GCS)**

GCS actuará como nuestro sistema de archivos distribuido (donde almacenaremos los datos y los *scripts*).

### a. **Crear un *Bucket* de GCS**

Un *bucket* es el contenedor fundamental de almacenamiento de objetos en GCS.

1. En la barra de búsqueda, escribe y selecciona **"Cloud Storage"**.
2. Haz clic en **"Crear bucket"**.
3. **Asigna un nombre único y global** (esto es crucial).
4. **Selecciona la Región** donde se desplegará tu clúster de Dataproc.
5. Configura las opciones de privacidad y protección (generalmente, las opciones por defecto son suficientes para este tutorial).
6. Haz clic en **"Crear"**.

![captura bucket](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/buckets_imagen00.png)

### b. **Subir Archivos de Prueba (*Scripts* y *Datasets*)**

Una vez creado el *bucket*, subiremos los archivos que el clúster usará para el procesamiento.

1. Dentro de tu *bucket*, haz clic en **"Subir archivos"**.
2. Selecciona los *scripts* de Spark y los *datasets* de prueba desde tu máquina local.
3. Haz clic en **"Abrir"** para iniciar la subida.

[!subir archivo](/imagen_07.jpg)

---

## 6. 🛠️ Crear y Desplegar el Clúster con Google Dataproc

En este paso, utilizaremos la herramienta de línea de comandos `gcloud` a través de Cloud Shell para construir y lanzar el clúster.

### a. **Inicializar Cloud Shell**

1.  Navega al servicio **Dataproc** en la Consola de GCP.
2.  Haz clic en el icono **Cloud Shell** (terminal en la web) en la esquina superior de la Consola.

![abrir shell](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/ShellCluster_imagen00.png)


### b. **Configurar el Entorno en Cloud Shell**

Antes de ejecutar el comando de creación, asegúrate de que el entorno de Cloud Shell esté apuntando al proyecto correcto.

**Autenticación (si es la primera vez):**
```bash
gcloud auth login
```

Seleccionar proyecto: Reemplaza [ID_DEL_PROYECTO] con el ID que guardaste en el paso 4.b.

```bash
gcloud config set project [ID_DEL_PROYECTO]
```
![abrir shell](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/verificacionShell_imagen00.png)

### c. Comando de Creación del Clúster
Comando base:

Ejecuta el siguiente comando para crear el clúster, el cual incluye soporte para Spark Streaming (Kafka), Jupyter y la acción de inicialización para Kafka.

**IMPORTANTE:**

- Reemplaza `bucket-prueba-mia` con el nombre de tu bucket de GCS.  
- Ajusta la `--region` y `--zone` si trabajas en otra ubicación.  
- Asegúrate de cambiar la propiedad `--project` si tu proyecto no es `hadoop-spark-lab2`.

```bash
gcloud beta dataproc clusters create micluster \
 --enable-component-gateway \
 --bucket bucket-prueba-mia \
 --region us-east1 \
 --zone us-east1-c \
 --master-machine-type n1-standard-2 \
 --master-boot-disk-size 500 \
 --num-workers 2 \
 --worker-machine-type n1-standard-2 \
 --worker-boot-disk-size 500 \
 --image-version 2.1-debian11 \
 --properties spark:spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 \
 --optional-components JUPYTER,ZOOKEEPER \
 --max-age 14400s \
 --initialization-actions 'gs://goog-dataproc-initialization-actions-europe-west1/kafka/kafka.sh' \
 --project hadoop-spark-lab2
```

Nota:
Si encuentras errores de sintaxis, considera ejecutar el comando por partes o verificar las versiones de la imagen y los packages de Spark.

* Cambiar `--bucket` por tu bucket.
* Cambiar `--project` por tu ID.
* Si falla, pegar línea por línea.

![captura creación cluster](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/creacionCluster_imagen00.png)

---

### 7. 💻 Acceso y Operaciones Iniciales del Clúster

Una vez que el clúster esté en estado **RUNNING (Activo)**, puedes acceder a sus componentes.

---

### a. Acceder a la Terminal de HDFS (Vía JupyterLab)

Utilizaremos la terminal de **JupyterLab**, que se ejecuta directamente en el nodo maestro del clúster, para interactuar con el **Hadoop Distributed File System (HDFS)**.

### • En la consola de **Dataproc**, haz clic en el botón **"Web Interfaces"**  
   (o **"Puerta de enlace de componentes"** si lo habilitaste).

### • Selecciona **JupyterLab**.

### • Una vez dentro de JupyterLab, abre una **Terminal**.

1. Abrir **JupyterLab** → **Terminal**.

![abrir jupyter](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/jupyterLab_imagen00.png)

Obtener Permisos de Superusuario (para HDFS)::

```bash
sudo -u hdfs bash
```

Listar Directorios Raíz de HDFS:

```bash
hadoop fs -ls /
```

Subir un Archivo de Datos Local a HDFS: 
Este comando copia un archivo desde el sistema de archivos local del master (donde se ejecuta la terminal) a HDFS.

```bash
hadoop fs -mkdir/laboratorio2
```

Subir archivo:

```bash
hadoop fs -copyFromLocal/flights.csv/laboratorio2
```

Preparación de Notebooks:
Asegúrate de que los siguientes notebooks estén subidos a tu bucket de GCS (no a HDFS, ya que Spark leerá desde GCS):

* ConsultaSparkDF_lab.ipynb
* ConsultarParquet_lab.ipynb
* ReadStream_lab.ipynb
  
Abrir el archivo ConsultaSparkDF y validar cargar el cvs al un dataframe de Spark


![spark](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/hdfs2_iamgen.jpg)
---

### b. Configuración y Uso de Apache Kafka
El clúster ya incluye Kafka gracias a la acción de inicialización. Ejecutaremos los siguientes comandos desde la misma terminal de JupyterLab.

Crear un Tópico (Topic): 
Creamos el topic "retrasos2" para simular datos de streaming.:

```bash
/usr/lib/kafka/bin/kafka-topics.sh --bootstrap-server micluster-w-0:9092 --create --replication-factor 1 --partitions 1 --topic retrasos
```

Listar Tópicos Existentes:

```bash
/usr/lib/kafka/bin/kafka-topics.sh --bootstrap-server micluster-w-0:9092 --list
```

Iniciar el Productor de Mensajes:
Abre una nueva terminal en JupyterLab para que esta se mantenga activa y puedas escribir mensajes.

```bash
/usr/lib/kafka/bin/kafka-console-producer.sh --broker-list micluster-w-0:9092 --topic retrasos
```
![topic](/grupo05_nettalco/LABORATORIO_GCP/evidencias_gcp/evidenciaHDFS.png)

Ejemplos de mensajes JSON:
Ingresa estos mensajes en la terminal del productor, uno por línea:

```json
{"dest": "GRX", "arr_delay": 2.6}
{"dest": "MAD", "arr_delay": 5.4}
{"dest": "GRX", "arr_delay": 1.5}
{"dest": "MAD", "arr_delay": 20.0}
```

Iniciar el Consumidor de Mensajes (Opcional para Verificación):
Abre una tercera terminal para ver los mensajes siendo recibidos.

```bash
/usr/lib/kafka/bin/kafka-console-consumer.sh --bootstrap-server micluster-w-0:9092 --topic retrasos --from-beginning
```

---
