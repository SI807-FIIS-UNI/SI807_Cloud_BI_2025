# 🧪 Evidencias de despliegue
A continuación, se presentan las evidencias de la implementación y el procesamiento de datos realizado en Google Cloud Platform (GCP).

Esta sección ilustra el resultado del trabajo, que involucró el procesamiento de los datasets de la empresa Nettalco para el proyecto del Parcial, utilizando la infraestructura de Big Data desplegada en GCP.

## 🗂️ 1. Google Cloud Storage 
El primer paso consistió en crear un bucket S3 que servirá como almacenamiento principal para los datos utilizados en el laboratorio.  
Este bucket será el origen desde el cual AWS Glue obtendrá los archivos para el proceso de catalogación y análisis.
El bucket de S3 funciona como data lake. Ahí almacenan tanto los datos crudos (raw) como los procesados (curated).

![1](/grupo05_nettalco/PC3/evidencias_pc3/img_001.png)


![2](/grupo05_nettalco/PC3/evidencias_pc3/img_002.png)

## 🗂️ 2. Cloud Shell

![3](/grupo05_nettalco/PC3/evidencias_pc3/img_003.png)

## 🗂️ 3. Dataproc - clubster
Utilizaremos la herramienta de línea de comandos gcloud en Cloud Shell o en la  terminal local para desplegar el clúster.
## Comando de Despliegue:
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

## 🗂️ 4. Dataproc - Clubster - Procesamiento

![6](/grupo05_nettalco/PC3/evidencias_pc3/img_006.png)

## 🗂️ 5. Dataproc - clubster - carga a bigquery

![7](/grupo05_nettalco/PC3/evidencias_pc3/img_007.png)

## 🗂️ 6. Bigquery

![8](/grupo05_nettalco/PC3/evidencias_pc3/img_008.png)

## 🗂️ 7. Dashboard en Looker
Los resultados del procesamiento se visualizaron en la siguiente herramienta:
![9](/grupo05_nettalco/PC3/evidencias_pc3/img_009.png)

**Link del Dashboard:** [Dashboard Looker Studio](https://lookerstudio.google.com/u/0/reporting/9139c4d1-2f52-4bd1-9e86-97b7554b2d58)
