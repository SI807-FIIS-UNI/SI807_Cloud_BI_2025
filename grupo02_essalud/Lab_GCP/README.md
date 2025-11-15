# 🧪 Laboratorio Big Data en Google Cloud Platform  
### Hadoop + Spark + Kafka + Spark Streaming + HDFS + Parquet

Este laboratorio muestra el proceso completo para construir un flujo Big Data usando:
- **Google Cloud Dataproc**
- **Apache Hadoop (HDFS)**
- **Apache Spark**
- **Apache Kafka**
- **Spark Structured Streaming**
- **Google Cloud Storage**

El objetivo es subir datos a HDFS, procesarlos con Spark, generar un flujo en tiempo real con Kafka y almacenarlo en formato Parquet.

## 📂 1. Crear un Bucket en Google Cloud Storage

El bucket servirá como almacenamiento inicial para archivos y notebooks.

### Pasos:
1. Ir a **Cloud Storage**.
2. Clic en **Crear**.
3. Asignar un nombre único (p. ej. `g2-lab2`).
4. Subir el archivo `flights.csv`.
5. Subir los notebooks del laboratorio:
   - `ConsultaSparkDF_lab.ipynb`
   - `ConsutarParquet_lab.ipynb`
   - `ReadStream_lab.ipynb`

 ![Bucket](/grupo02_essalud/Lab_GCP/evidencias/01_Creacion_Bucket.png)

## 📁 2. Subir el csv flights

 Subimos el archivo .csv al bucket

  ![Bucket](/grupo02_essalud/Lab_GCP/evidencias/02_Subir_Flights.png)

## 🔐 3. Autenticación en Google Cloud

Desde la Cloud Shell colocamos:

`gcloud auth login`

Configuramos el nombre del proyecto

`gcloud config set project Labo2-G2`

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/03_Autenticacion.png)

## ☁️ 4. Creación del Clúster Dataproc

Comando utilizado:

```
  --enable-component-gateway \
  --bucket g2-lab2 \
  --region southamerica-west1 \
  --zone southamerica-west1-a \
  --master-machine-type n4-standard-2 \
  --master-boot-disk-size 32 \
  --num-workers 2 \
  --worker-machine-type n4-standard-2 \
  --worker-boot-disk-size 32 \
  --image-version 2.1-debian11 \
  --properties spark:spark.jars.packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3 \
  --optional-components JUPYTER,ZOOKEEPER \
  --max-age 14400s \
  --initialization-actions 'gs://goog-dataproc-initialization-actions-europe-west1/kafka/kafka.sh' \
  --project labo2-g2
```

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/04_CargaClusterDataProc.png)    

Podemos visualizar que se creo el Cluster

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/05_VisualizarCluster.png)

Ingresamos a JupyterLab

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/06_EntrandoJupyterLab.png)

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/07_JupyterLab.png)

## 📁 5. Preparación del HDFS en Dataproc

Obtener los permisos 
Colocamos los siguientes comandos en la terminal

`sudo -u hdfs bash`

Coloca `hadoop fs -ls /` para obtener todos los directorios que se encuentran en tu HDFS

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/08_Permisos.png)

Creamos directorio usamos el siguiente comando

`hadoop fs - mkdir /laboratorio2`

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/09_CrearDirectorio.png)

Copiar archivos del sistema hacia el sistema de archivos Hadoop, usamos el siguiente comando:

`hadoop fs -copyFromLocal /flights.csv /laboratorio2`

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/10_CopiarArchivo.png)

Subimos los notebooks

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/11_Notebooks.png)

## 📊 6. Validar lectura del CSV con Spark

donde su codigo es

v
![Bucket](/grupo02_essalud/Lab_GCP/evidencias/12_ValidarCargaDataFrame.png)

## 🔊 7. Kafka – Crear y validar Topic

Creando el topic llamado "retrasos". Para ello colocamos en la terminal 

`/usr/lib/kafka/bin/kafka-topics.sh --bootstrap-server micluster-w-0:9092 --create --replication-factor 1 --partitions 1 --topic retrasos`

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/13_TopicRetrasos.png)

Y lo verificamos con el comando 
`/usr/lib/kafka/bin/kafka-topics.sh --bootstrap-server micluster-w-0:9092 –list`

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/14_VerificarRetrasos.png)

Iniciamos el productor para las simulaciones

`/usr/lib/kafka/bin/kafka-console-producer.sh --broker-list micluster-w-0:9092 --topic retrasos`

## ⚡ 8. Spark Streaming – Lectura desde Kafka

Ejecutamos el archivo ReadStream_lab.ipynb

```python
# Leer el streaming desde Kafka

retrasosStreamingDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "micluster-w-0:9092,micluster-w-1:9092") \
    .option("subscribe", "retrasos") \
    .load()
#Leer la estructura de Streaming
retrasosStreamingDF.printSchema()

# Todos los campos son creadas automáticamente por Spark cuando leemos de Kafka. De ellas, la que nos interesa es `value` que contiene propiamente el mensaje de Kafka

#DAR FORMATO DE LECTURA AL VALOR VALUE

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,DoubleType

# Definir el esquema del JSON que estás esperando en el campo VALUE
json_schema = StructType([
    StructField("dest", StringType(), True),
    StructField("arr_delay", DoubleType(), True)
])

# Convertir el campo `value` a string y luego parsear el JSON
parsedDF = retrasosStreamingDF.selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json(col("json_value"), json_schema).alias("data")) \
    .select("data.*")

# Mostrar el resultado en la consola
# Modo Append para verificar los mensajes que llegan
parsedDF.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()
#Para Guardar se sobreescribirá en un archivo parquet dentro de HFDS
parsedDF.writeStream \
    .format("parquet") \
    .option("path", "/resultado/miparquet_stream") \
    .option("checkpointLocation", "/resultado/checkpoint") \
    .outputMode("append") \
    .start()

```

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/15_EjecutarReadStream.png)

## 📩 9. Enviar datos JSON desde el Producer

Simulamos el envio de información JSON en la terminal

```json
{"dest": "GRX", "arr_delay": 2.6}
{"dest": "MAD", "arr_delay": 5.4} 
{"dest": "GRX", "arr_delay": 1.5}
{"dest": "MAD", "arr_delay": 20.0}
```

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/16_SimulaciónEnvioInfo.png)

## 👀 10. Validar mensajes recibidos en Kafka

Para asegurarse de que los mensajes se han enviado correctamente, usamos el siguiente comando en la terminal

`/usr/lib/kafka/bin/kafka-console-consumer.sh --bootstrap-server micluster-w-0:9092 --topic retrasos --from-beginning`

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/17_MsjEnviados.png)

Vemos que hay un total de 12 mensages

## 📦 11. Validar Parquet generado

Podemos validar lo que se guardo en el ConsutarParquet_lab.ipynb.

![Bucket](/grupo02_essalud/Lab_GCP/evidencias/18_ValidarConsultarParquet.png)
