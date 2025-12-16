# Examen Final SI807-U 
Loayza Segura Roger Salvador
USO DE GCP:



INICIAR EL CLI DE GCP:
Id del proyecto: ef-si807u-20220018k

USO DEL CLI PARA CONFIGURAR EL PROYECTO COMO PRINCIPAL:

CREACION DEL BUCKET:
BUCKET_NAME="bi-examen-final" 
gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1


VISTA EN GOOGLE CLOUD STORAGE:

CREACION DE LAS CARPETAS BRONCE:
*bronce/raw
*bronce/processed
*bronce/curated


VISUALIZACION EN GCS:



CARGA DEL CSV USANDO CLI:





CAMBIAMOS LA DIRECCION DEL ARCHIVO:
 
Pasamos el archivo de la dirección base /home/r_loayza_s/ al gcs


BUCKET_NAME="bi-examen-final" 
NUEVO_ARCHIVO="Flight_delay.csv"
gcloud storage cp $NUEVO_ARCHIVO gs://$BUCKET_NAME/bronce/raw/$NUEVO_ARCHIVO

CARGA COMPLETADA:


COMPROBAMOS QUE SE ENCUENTRA CARGADO EL CSV:



ABRIMOS EL EDITOR DE GOOGLE CLOUD:




CREAMOS LAS CARPETAS:



CREACION DEL EDA Y EL PROCESO ETL:
pip install pandas google-cloud-storage fsspec gcsfs #
python scripts/eda.py




SCRIPT DEL EDA EN PYTHON:



INSTALACION DE LA DEPENDENCIA PANDASY EJECUCION DEL SCRIPT:


MODELO ESTRELLA MINIMO:




