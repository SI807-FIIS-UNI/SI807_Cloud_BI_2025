# Examen Final SI807-U 
Loayza Segura Roger Salvador
USO DE GCP:

![1](/grupo05_nettalco/EVIDENCIAS/1.png)

INICIAR EL CLI DE GCP:
Id del proyecto: ef-si807u-20220018k
![1](/grupo05_nettalco/EVIDENCIAS/2.png)

USO DEL CLI PARA CONFIGURAR EL PROYECTO COMO PRINCIPAL:

![1](/grupo05_nettalco/EVIDENCIAS/3.png)

CREACION DEL BUCKET:

BUCKET_NAME="bi-examen-final"

gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1

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


BUCKET_NAME="bi-examen-final" 
NUEVO_ARCHIVO="Flight_delay.csv"
gcloud storage cp $NUEVO_ARCHIVO gs://$BUCKET_NAME/bronce/raw/$NUEVO_ARCHIVO
![1](/grupo05_nettalco/EVIDENCIAS/Imagen10.png)
CARGA COMPLETADA:
![1](/grupo05_nettalco/EVIDENCIAS/Imagen11.png)

COMPROBAMOS QUE SE ENCUENTRA CARGADO EL CSV:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen12.png)

ABRIMOS EL EDITOR DE GOOGLE CLOUD:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen13.png)


CREAMOS LAS CARPETAS:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen14.png)

CREACION DEL EDA Y EL PROCESO ETL:
pip install pandas google-cloud-storage fsspec gcsfs #
python scripts/eda.py

![1](/grupo05_nettalco/EVIDENCIAS/Imagen15.png)


SCRIPT DEL EDA EN PYTHON:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen16.png)

INSTALACION DE LA DEPENDENCIA PANDASY EJECUCION DEL SCRIPT:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen17.png)
SUBIDA DEL ARCHIVO A GCS:

Comando para copiar el archivo procesado de Cloud Shell a GCS

BUCKET_NAME="bi-examen-final"
PROCESSED_FILE="processed_Flight_delay.csv"
gcloud storage cp $PROCESSED_FILE gs://$BUCKET_NAME/bronce/processed/$PROCESSED_FILE

![1](/grupo05_nettalco/EVIDENCIAS/Imagen17.png)
MODELO ESTRELLA MINIMO:
![1](/grupo05_nettalco/EVIDENCIAS/Imagen18.png)



