# Examen Final SI807-U 
Loayza Segura Roger Salvador
USO DE GCP:

![1](/grupo05_nettalco/EVIDENCIAS/1.png)

JUSTIFICACION:
Simplicidad y Escalabilidad: 
Google Cloud Storage (GCS) ofrece un almacenamiento de objetos altamente duradero y escalable, perfecto para la capa Bronce (Lakehouse).

Capacidades de BI/DW: 
BigQuery es un Data Warehouse (DW) sin servidor y de alto rendimiento, ideal para las capas Plata y Oro. Su integración nativa con GCS y la herramienta de transformación Dataproc/Dataprep o Cloud Functions/Cloud Run simplifica la arquitectura ETL/ELT.

Visualización: 
Looker Studio (anteriormente Google Data Studio) ofrece una integración gratuita y nativa con BigQuery.


INICIAR EL CLI DE GCP:

Id del proyecto: ef-si807u-20220018k

![1](/grupo05_nettalco/EVIDENCIAS/2.png)

USO DEL CLI PARA CONFIGURAR EL PROYECTO COMO PRINCIPAL:

![1](/grupo05_nettalco/EVIDENCIAS/3.png)

CREACION DEL BUCKET:

```bash
BUCKET_NAME="bi-examen-final"

gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1

```


![1](/grupo05_nettalco/EVIDENCIAS/4.png)

VISTA EN GOOGLE CLOUD STORAGE:

![1](/grupo05_nettalco/EVIDENCIAS/5.png)

CREACION DE LAS CARPETAS BRONCE:

*bronce/raw

*bronce/processed

*bronce/curated

![1](/grupo05_nettalco/EVIDENCIAS/6.png)

VISUALIZACION EN GCS:

![1](/grupo05_nettalco/EVIDENCIAS/7.png)

CARGA DEL CSV USANDO CLI:

![1](/grupo05_nettalco/EVIDENCIAS/8.png)



CAMBIAMOS LA DIRECCION DEL ARCHIVO:

Pasamos el archivo de la dirección base /home/r_loayza_s/ al gcs


```bash
BUCKET_NAME="bi-examen-final" 
NUEVO_ARCHIVO="Flight_delay.csv"
gcloud storage cp $NUEVO_ARCHIVO gs://$BUCKET_NAME/bronce/raw/$NUEVO_ARCHIVO

```

![1](/grupo05_nettalco/EVIDENCIAS/Imagen10.png)

CARGA COMPLETADA:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen11.png)

COMPROBAMOS QUE SE ENCUENTRA CARGADO EL CSV:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen12.png)

![1](/grupo05_nettalco/EVIDENCIAS/Imagen13.png)

ABRIMOS EL EDITOR DE GOOGLE CLOUD:



![1](/grupo05_nettalco/EVIDENCIAS/Imagen14.png)
![1](/grupo05_nettalco/EVIDENCIAS/Imagen15.png)

CREAMOS LAS CARPETAS:


![1](/grupo05_nettalco/EVIDENCIAS/Imagen16.png)
![1](/grupo05_nettalco/EVIDENCIAS/Imagen17.png)

CREACION DEL EDA Y EL PROCESO ETL:

```bash
BUCKET_NAME="bi-examen-final"
gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1
pip install pandas google-cloud-storage fsspec gcsfs
python scripts/eda.py
```


![1](/grupo05_nettalco/EVIDENCIAS/Imagen18.png)


SCRIPT DEL EDA EN PYTHON:

- [🐍 Scripts EDA](./grupo05_nettalco/scripts) - Código Python para la EDA minima


SUBIDA DEL ARCHIVO A GCS:

Comando para copiar el archivo procesado de Cloud Shell a GCS

```bash
BUCKET_NAME="bi-examen-final"
PROCESSED_FILE="processed_Flight_delay.csv"
gcloud storage cp $PROCESSED_FILE gs://$BUCKET_NAME/bronce/processed/$PROCESSED_FILE
```

SCRIPT DEL EDA EN PYTHON:

- [🐍 Scripts ETL](./grupo05_nettalco/scripts) - Código Python para la Transformacion y Carga


VISUALIZACION DE LA CAPA ORO Y PLATA EN BIGQUERY:

![1](/grupo05_nettalco/EVIDENCIAS/31.png)

![1](/grupo05_nettalco/EVIDENCIAS/32.png)


MODELO ESTRELLA MINIMO:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen19.png)






