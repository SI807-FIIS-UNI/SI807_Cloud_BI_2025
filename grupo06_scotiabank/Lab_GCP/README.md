# 🚀 Laboratorio: Levantar un Clúster Hadoop + Spark + Kafka en Google Cloud Platform (GCP)

En este laboratorio implementamos un clúster Dataproc en Google Cloud Platform (GCP), configuramos almacenamiento en Google Cloud Storage (GCS), procesamos datos utilizando Hadoop y Spark, y realizamos una simulación de transmisión en tiempo real con Apache Kafka y Spark Streaming.

---

## 🧰 Herramientas utilizadas

* **Google Cloud Platform (GCP)**
* **Google Dataproc (Hadoop + Spark)**
* **Google Cloud Storage (GCS)**
* **Apache Kafka**
* **JupyterLab**
* **Spark Streaming**

---

## 🏁 1. Configuración Inicial en GCP

### 1.1 Creación de la cuenta en GCP

Ingresamos a [cloud.google.com](https://cloud.google.com) y activamos la cuenta con créditos gratuitos para nuevos usuarios.

<p align="center">
    <img width="60%" src="./evidences/procesos.jpeg">
</p>

### 1.2 Creación del proyecto

Dentro de la consola:

1. Accedimos al panel de **Proyectos**.
2. Creamos el proyecto llamado: **Lab GCP Grupo 6**.
3. Registramos el **ID del proyecto:** `lab-gcp-grupo-6`.

### 1.3 Habilitación de APIs necesarias

Desde **APIs & Services**, habilitamos:

* **Cloud Dataproc API**

### 1.4 Configuración de permisos IAM

Validamos que nuestra cuenta contaba con permisos de **Editor**, necesario para operar Dataproc.

---

## 🗄️ 2. Creación del Bucket en Google Cloud Storage (GCS)

En **Cloud Storage**:

1. Creamos un bucket exclusivo para el laboratorio con el nombre `sin-grupo6-bucket-1`.
2. Seleccionamos la región correspondiente a Chile `southamerica-west1 (Santiago)`.
3. Mantenemos la política de privacidad por defecto.
4. Subimos el archivo de datos `flights.csv` que posteriormente utilizaremos en HDFS y Spark.

---

## 🧩 3. Creación del Clúster en Dataproc

Abrimos **Cloud Shell** para ejecutar los comandos.

### 3.1 Autenticación

Nos autenticamos correctamente en GCP:

```bash
gcloud auth login
```

Seleccionamos el proyecto:

```bash
gcloud config set project lab-gcp-grupo-6
```

### 3.2 Creación del clúster

Ejecutamos el despliegue del clúster Dataproc:

```bash
gcloud dataproc clusters create cluster-grupo-6 \
  --enable-component-gateway \
  --bucket sin-grupo6-bucket-1 \
  --region southamerica-west1 \
  --subnet default \
  --no-address \
  --master-machine-type n4-standard-2 \
  --master-boot-disk-type hyperdisk-balanced \
  --master-boot-disk-size 30 \
  --num-workers 2 \
  --worker-machine-type n4-standard-2 \
  --worker-boot-disk-type hyperdisk-balanced \
  --worker-boot-disk-size 30 \
  --image-version 2.2-debian12 \
  --optional-components JUPYTER,ZOOKEEPER \
  --max-idle 3600s \
  --max-age 10800s \
  --scopes "https://www.googleapis.com/auth/cloud-platform" \
  --project lab-gcp-grupo-6
```

Una vez aprovisionado, ingresamos al entorno de JupyerLab siguiento la ruta:

**Dataproc → Clúster → Interfaces Web → JupyterLab**

---

## 📂 4. Gestión de archivos con HDFS

En JupyterLab abrimos una terminal y realizamos las siguientes operaciones:

### 4.1 Cambio al usuario HDFS

```bash
sudo -u hdfs bash
```

### 4.2 Listado de directorios raíz

Confirmamos la estructura inicial de HDFS:

```bash
hadoop fs -ls /
```

### 4.3 Creación del directorio de trabajo

Creamos el directorio para almacenar los archivos del laboratorio:

```bash
hadoop fs -mkdir /laboratorio2
```

### 4.4 Carga del archivo CSV a HDFS

Copiamos el archivo `flights.csv` desde el sistema local:

```bash
hadoop fs -copyFromLocal /flights.csv /laboratorio2
```

Con esto dejamos los datos listos para ser usados por Spark.

---

## 📘 5. Ejecución de Notebooks en Spark

Subimos al bucket los notebooks:

* **ConsultaSparkDF_lab.ipynb**
* **ConsutarParquet_lab.ipynb**
* **ReadStream_lab.ipynb**

Luego los abrimos en JupyterLab y ejecutamos:

✔ Carga del CSV en un DataFrame Spark
✔ Conversión y validación en formato Parquet
✔ Configuración del Streaming conectado a Kafka

---

## 📡 6. Kafka en el clúster

Desde la terminal del clúster configuramos el entorno de Kafka.

### 6.1 Creación del topic “retrasos”

```bash
/usr/lib/kafka/bin/kafka-topics.sh --bootstrap-server micluster-w-0:9092 \
--create --replication-factor 1 --partitions 1 --topic retrasos
```

### 6.2 Verificación del topic

```bash
/usr/lib/kafka/bin/kafka-topics.sh --bootstrap-server micluster-w-0:9092 --list
```

Confirmamos que **retrasos** fue creado correctamente.

### 6.3 Inicio del productor

```bash
/usr/lib/kafka/bin/kafka-console-producer.sh --broker-list micluster-w-0:9092 --topic retrasos
```

Enviamos varios mensajes de prueba en formato JSON:

```json
{"dest": "GRX", "arr_delay": 2.6}
{"dest": "MAD", "arr_delay": 5.4}
{"dest": "GRX", "arr_delay": 1.5}
{"dest": "MAD", "arr_delay": 20.0}
```

### 6.4 Inicio del consumidor

```bash
/usr/lib/kafka/bin/kafka-console-consumer.sh --bootstrap-server micluster-w-0:9092 --topic retrasos --from-beginning
```

Verificamos que todos los mensajes enviados desde el productor fueran recibidos correctamente.

---

## 📊 7. Validación del procesamiento en Spark Streaming

Ejecutamos el notebook **ReadStream_lab.ipynb**, donde observamos la llegada en tiempo real de los mensajes publicados en Kafka.

En **ConsutarParquet_lab.ipynb** revisamos que los resultados procesados fueron almacenados satisfactoriamente en formato Parquet dentro del bucket asignado.

---

## 🧹 8. Apagado del clúster

Finalmente, para evitar costos adicionales, eliminamos el clúster:

```bash
gcloud dataproc clusters delete micluster --region us-east1
```

---

## ✅ Conclusiones

Completamos exitosamente la implementación de un entorno Big Data en GCP, utilizando Hadoop, Spark y Kafka sobre un clúster Dataproc. Procesamos datos estáticos y flujos en tiempo real, validando tanto la infraestructura como la correcta integración de cada componente.

---

Si quieres, también puedo preparar:

📌 Una versión aún más narrativa ("bitácora del laboratorio")
📌 Un README con capturas de pantalla incluidas
📌 Una versión académica estilo informe o monografía

¿Deseas alguna de estas opciones?
