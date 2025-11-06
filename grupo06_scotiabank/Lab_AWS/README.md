# 🧪 Laboratorio AWS – Configuración Inicial (S3, Glue y IAM)

## 🗂️ 1. Creación del Bucket S3

El primer paso consistió en crear un **bucket S3** que servirá como almacenamiento principal para los datos utilizados en el laboratorio.  
Este bucket será el origen desde el cual **AWS Glue** obtendrá los archivos para el proceso de catalogación y análisis.

### 🔧 Detalles de configuración
Durante la creación del bucket, se completaron los siguientes campos solicitados por AWS:

- **Bucket name:** `s3-grupo-6-vf`  
- **AWS Region:** `us-east-1` (N. Virginia)  
- **Block Public Access:** Habilitado  
- **Bucket versioning:** Deshabilitado  
- **Default encryption:** Deshabilitado  


Dentro del bucket, se creó la siguiente estructura de carpetas:

```json
s3-grupo-6-vf/
 └── archive/
      └── Amazon Sale Report.csv
```


# 🤖 2. Configuración del Crawler en AWS Glue

El siguiente paso fue configurar un AWS Glue Crawler, encargado de escanear el bucket S3 y generar automáticamente una tabla de metadatos en el Glue Data Catalog.

## ⚙️ Campos configurados al crear el Crawler

Durante la creación del Crawler, se completaron los siguientes campos requeridos:

- **Name**: crawler-grupo-6

- **Data source**: S3

- **S3 path**: s3://s3-grupo-6-vf/archive/

- **IAM role**: AWSGlueServiceRole-grupo6 (rol creado con permisos específicos para acceder al bucket)

- **Schedule**: Ejecutar bajo demanda (no programado automáticamente)

- **Database**: grupo6_db (base de datos creada en Glue para almacenar los metadatos)

- **Output**: Sobrescribir tablas existentes en caso de cambios detectados

Una vez configurado, el crawler fue ejecutado manualmente para detectar el archivo Amazon Sale Report.csv dentro del bucket, generando automáticamente la estructura de columnas y tipos de datos en Glue Catalog.

# 🔐 3. Configuración de IAM Policy

Como parte del uso del Crawler, fue necesario definir una política de permisos IAM que permita al rol de Glue acceder correctamente al bucket S3.
Esta política garantiza que el servicio tenga los permisos mínimos necesarios para listar, leer, escribir y eliminar objetos dentro del bucket.

```json
# 📜 Política IAM utilizada
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-grupo-6-vf",
                "arn:aws:s3:::s3-grupo-6-vf/*",
                "arn:aws:s3:::s3-grupo-6-vf/archive/Amazon Sale Report.csv/*",
                "arn:aws:s3:::s3-grupo-6-vf/archive/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "877617909831"
                }
            }
        }
    ]
}
```
# 🔎 Aspectos destacados

Action: Define las operaciones permitidas sobre los recursos de S3:

- **GetObject**: Leer objetos del bucket

- **PutObject**: Escribir nuevos objetos

- **ListBucket**: Listar el contenido del bucket

- **DeleteObject**: Eliminar objetos existentes

- **Resource**: Especifica los recursos de S3 a los cuales el rol tiene acceso.
Incluye el bucket principal (s3-grupo-6-vf) y sus subrutas dentro de archive/.

## Script python



## SQL tabla test

```sql

```