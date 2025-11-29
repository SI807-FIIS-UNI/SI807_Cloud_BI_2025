# Procesamiento de Datos Bronce → Plata con Dataproc (Spark)
Se resume el proceso completo de ingestión, estandarización y carga de datos en niveles Bronce y Plata, utilizando Google Cloud Platform, Dataproc (Spark), Google Cloud Storage (GCS) y BigQuery.

## 📌  1. Creación de la Base de Datos Bronce

Los datos originales de EsSalud se cargaron en el dataset: `essalud_bronce`
Donde se crearon las siguientes tablas:
•   Diabetes
•   Obesidad
•   Hipertension
•   Ubigeo

Cada tabla contiene los datos exactamente como fueron descargados, sin limpieza ni modificaciones.
Esto permite conservar una “copia fiel” del origen.

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata01.png)

# ⚙️ 2. Procesamiento Bronce → Plata usando Dataproc (Spark)

Se creó un clúster Dataproc:

Con los parámetros 
```
PROJECT=grupo2-essalud
REGION=us-central1
ZONE=us-central1-a
CLUSTER_NAME=cluster-spark-essalud
IMAGE_VERSION=2.1-debian11
BUCKET_TEMP=grupo2-essalud-datalake

gcloud config set project $PROJECT
```

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata02.png)

```
gcloud dataproc clusters create $CLUSTER_NAME \
  --region=$REGION \
  --zone=$ZONE \
  --image-version=$IMAGE_VERSION \
  --enable-component-gateway \
  --optional-components=JUPYTER \
  --master-machine-type=n1-standard-2 \
  --master-boot-disk-size=100GB \
  --num-workers=2 \
  --worker-machine-type=n1-standard-2 \
  --worker-boot-disk-size=100GB \
  --bucket=$BUCKET_TEMP \
  --project=$PROJECT
```

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata03.png)

Este clúster ejecuta el código PySpark encargado de:
•   Leer tablas Bronce desde BigQuery
•   Unificarlas en un solo DF (df_all)
•   Estandarizar valores
•   Generar tablas Plata limpias
•   Guardarlas en GCS y en BigQuery automáticamente
Se creó el cluster 

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata04.png)

Donde nos dirigimos a Intefaces web --> JupyterLab

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata05.png)

Luego seleccionamos el notebook --> Python 3, donde realizaremos el procesamiento 

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata06.png)

Colocamos el siguiente el codigo 

- [Limpieza y data a plata](../Scripts/Limpieza_y_data_plata.ipynb)

Lo cual veremos en la imagen

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata07.png)

## 🧼 3. Limpieza de Datos y Cálculo de Métricas

Para cada tabla Plata se realizó:
✔️ 1. Conteo de registros iniciales
✔️ 2. Identificación y eliminación de registros con valores nulos en claves
✔️ 3. Eliminación de duplicados
✔️ 4. Conteo de registros finales
✔️ 5. Registro de métricas de calidad

Una función central (limpiar_y_contar) procesó:

•   total_inicial
•   nulos_eliminados
•   duplicados_eliminados
•   total_final

Las métricas se guardan en:
`gs://grupo2-essalud-datalake/plata/metricas_calidad`

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata08.png)

Podemos ver los resultados de total_inicial, nulos_eliminados, duplicados_eliminados, total_final

## 🗂️ 4. Creación de la Base de Datos Plata

Luego de procesar se crea automáticamente el dataset: `essalud_plata`

Y se cargaron automáticamente las tablas procesadas:
•   paciente
•   medico
•   cie10
•   ubigeo
•   diagnostico
•   procedimiento
•   resultado_procedimiento

Cada tabla fue generada con:
•   Datos limpios
•   Estructura optimizada
•   Identificadores generados cuando fue necesario

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata09.png)

# Explicación de lo que hace el codigo

## 📁 5. Guardado de Datos Plata en Google Cloud Storage (CSV)

Cada tabla procesada se consolidó en un único archivo CSV usando:
`df.coalesce(1).write.mode("overwrite").option("header", "true").csv(...)`

Las tablas se guardaron en:
`gs://grupo2-essalud-datalake/plata/`

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata10.png)

## 🗄️ 6. Carga Automática a BigQuery (Plata)

Se configuró el bucket temporal para el conector BigQuery:

```python
spark.conf.set("temporaryGcsBucket", "grupo2-essalud-datalake")
```

Y cada tabla Plata fue exportada automáticamente con:

```python
df.write.format("bigquery") \
  .option("table", "grupo2-essalud.essalud_plata.paciente") \
  .mode("overwrite") \
  .save()
```

Esto creó las tablas del dataset:
essalud_plata
 ├── paciente
 ├── medico
 ├── cie10
 ├── ubigeo
 ├── diagnostico
 ├── procedimiento
 └── resultado_procedimiento

![Bucket](/grupo02_essalud/4PC/Media/Fotos/Pruebas/BroncePlata09.png) 
