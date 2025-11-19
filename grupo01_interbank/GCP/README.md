# LABORATORIO GOOGLE CLOUD PLATFORM
## 5. Configuración de GCS
### a. Creación de Bucket en GCS
![Imagen de WhatsApp 2025-11-10 a las 20 33 07_f3f07bf3](https://github.com/user-attachments/assets/0f294539-a191-45a9-9dbf-98eb4fed6fbf)
### b. Subida de archivos a GCS
![Imagen de WhatsApp 2025-11-10 a las 20 33 40_1c891af5](https://github.com/user-attachments/assets/b3024c93-3dbb-461c-af66-6ef08724f6f4)

## 6. Crear Cluster en Google Dataproc
### a. Utilización de terminal gcloud y Configuración del entorno
![Imagen de WhatsApp 2025-11-10 a las 20 40 53_170f1e8f](https://github.com/user-attachments/assets/f8ac727c-1bba-41dc-86c1-ca93ed7f3290)

### b. Cluster creado
![Imagen de WhatsApp 2025-11-10 a las 20 45 49_cfff8744](https://github.com/user-attachments/assets/661ac3cf-0d7e-438d-9af3-eb934cea6da3)

## 7. Acceder al cluster
## a. Usar la Terminal para Almacenar en HDFS

En este paso se trabajó dentro del clúster **Dataproc** creado en Google Cloud Platform, utilizando la terminal del entorno **JupyterLab** para interactuar directamente con el sistema de archivos distribuido **HDFS (Hadoop Distributed File System)**.

El objetivo fue crear un directorio en HDFS y cargar el archivo `flights.csv` previamente almacenado en el bucket de Google Cloud Storage (GCS), para luego validar su lectura en **Apache Spark**.

---

### Obtener permisos de usuario HDFS

Primero, se ingresó a la sesión del usuario `hdfs` utilizando el siguiente comando:

```bash
sudo -u hdfs bash
```

Esto otorga permisos administrativos sobre el sistema HDFS, necesarios para crear directorios y copiar archivos dentro del entorno distribuido.

 Ejecución del comando sudo -u hdfs bash y acceso a la terminal del usuario hdfs.

---

### Verificar los directorios existentes en HDFS

Para listar los directorios del sistema de archivos HDFS, se utilizó el comando:

```bash
hadoop fs -ls /
```

El resultado muestra los directorios principales creados por defecto: /tmp, /user, y /var.

Listado inicial de los directorios en la raíz de HDFS.

![Img1](https://github.com/user-attachments/assets/c913067a-5a12-45c9-91a5-43c54d96f648)


---

### Crear un nuevo directorio de trabajo

Luego, se creó un nuevo directorio llamado /laboratorio2, donde se almacenarán los archivos del ejercicio:

```bash
hadoop fs -mkdir /laboratorio2
```

Esto confirma la correcta operación del entorno HDFS dentro del clúster Dataproc.

Creación exitosa del directorio /laboratorio2 en HDFS.

![Img2](https://github.com/user-attachments/assets/843acefd-5287-4b85-929e-2472b453266d)



---

### Cargar el archivo flights.csv en Spark

Una vez creado el directorio, se abrió el entorno JupyterLab y se ejecutó el notebook ConsultaSparkDF_lab.ipynb.
El archivo flights.csv, ubicado en /laboratorio2, fue leído directamente desde HDFS utilizando PySpark:

```python
ruta_hdfs = "/laboratorio2/flights.csv"

flightsDF = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(ruta_hdfs)
```

El comando flightsDF.show(5) muestra las primeras filas del dataset, mientras que flightsDF.printSchema() confirma la estructura y los tipos de datos inferidos automáticamente.


Notebook ejecutado correctamente, mostrando las primeras filas del DataFrame y el esquema detectado por Spark.

![Img3](https://github.com/user-attachments/assets/6377f0a4-eafa-4f1f-91a2-fdbdeceae191)


### b. Uso de la terminal para el uso de Apache Kafka

- Crear un Topic llamado "retrasos"
<img width="1218" height="41" alt="image" src="https://github.com/user-attachments/assets/a4ff7d4d-9fb7-4c06-b496-0a3be0f8eeb8" />

- Iniciamos el productor y realizamos las simulaciones
<img width="943" height="97" alt="image" src="https://github.com/user-attachments/assets/514bced4-b6fb-40e1-b71a-d21ed8d663ab" />

- Muestra del Archivo RedStream_lab
<img width="1600" height="806" alt="image" src="https://github.com/user-attachments/assets/d4fcc9ff-567a-4b6b-b733-5a5f97ee12cb" />

- Aseguramiento de los mensajes enviados
<img width="1600" height="789" alt="image" src="https://github.com/user-attachments/assets/b462b51d-f834-4919-9d1e-59dca381aa03" />

- verificacion terminal
<img width="1600" height="827" alt="image" src="https://github.com/user-attachments/assets/60b1cb79-3126-49ce-8c0d-074c57c6519c" />

## 👥 Autores
> 
| Rol            | Integrante                                            |
| -------------- | ----------------------------------------------------- |
| Líder de grupo | Jordan Laureano                                       |
| Miembros       | Joel Gamboa, Luis Aymachoque                          |
| Curso          | Sistemas de Inteligencia de Negocio                   |
| Universidad    | UNI - Facultad de Ingeniería Industrial y de Sistemas |

