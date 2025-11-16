# 🧪 Laboratorio GRPO 05 AWS – Configuración Inicial 
En este laboratorio enseñan a implementar un pipeline de datos usando S3, Glue, IAM y Athena sobre AWS. 
Paso a paso, se desarrollara desde la configuración segura del almacenamiento, hasta la automatización del catálogo,
la transformación eficiente y el análisis con consultas SQL.

## 🗂️ 1. Creación del Bucket S3
El primer paso consistió en crear un bucket S3 que servirá como almacenamiento principal para los datos utilizados en el laboratorio.  
Este bucket será el origen desde el cual AWS Glue obtendrá los archivos para el proceso de catalogación y análisis.
El bucket de S3 funciona como data lake. Ahí almacenan tanto los datos crudos (raw) como los procesados (curated).

### 🔧Completamos los campos solicitados por AWS
- **Bucket name:** `s3-grupo-5-vf`  
- **AWS Region:** `sa-east-1` (Sudamérica – São Paulo)  
- **Block Public Access:** Habilitado  
- **Bucket versioning:** Deshabilitado  
- **Default encryption:** Deshabilitado  
