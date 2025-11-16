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

Dentro del bucket, se creó la siguiente estructura de carpetas:

```
├── data/
│   └── raw/
├── evidencias/
├── script/
└── README.md
```
![Bucket](/grupo05_nettalco/Lab_AWS/evidencias/S3_archive_subidos.jpg)

# 🤖 2. Configuración del Crawler en AWS Glue
A continuación, se utiliza un crawler de Glue para explorar automáticamente la estructura de los datos y alimentar el Glue Data Catalog con los metadatos.
## ⚙️ Campos configurados al crear el Crawler

Se completaron los siguientes campos requeridos:
- **Name**: crawler_grupo5

- **Data source**: S3

- **S3 path**: s3://s3-grupo-5-vf/archive/

- **IAM role**: AWSGlueServiceRole-grupo5 (rol creado con permisos específicos para acceder al bucket)

- **Schedule**: Ejecutar bajo demanda (no programado automáticamente)

- **Database**: base_prueba (base de datos creada en Glue para almacenar los metadatos)

- **Output**: Sobrescribir tablas existentes en caso de cambios detectados


Una vez se completa la configuración del crawler, lo ejecutan manualmente para que explore el bucket, detecte el archivo 'Amazon Sale Report.csv' y genere automáticamente en el Glue Data Catalog una tabla con la estructura de columnas y tipos de datos correspondiente. De esta manera, establecen un 
esquema organizado que facilita futuras etapas de procesamiento y análisis.

![Crawler](/grupo05_nettalco/Lab_AWS/evidencias/Creacion_crawler.jpg)
