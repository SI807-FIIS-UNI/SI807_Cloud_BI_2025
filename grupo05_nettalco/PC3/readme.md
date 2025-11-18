# 🧪 Evidencias de despliegue
En este laboratorio enseñan a implementar un pipeline de datos usando S3, Glue, IAM y Athena sobre AWS. 
Paso a paso, se desarrollara desde la configuración segura del almacenamiento, hasta la automatización del catálogo,
la transformación eficiente y el análisis con consultas SQL.

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

![9](/grupo05_nettalco/PC3/evidencias_pc3/img_009.png)


```
├── data/
│   └── raw/
├── evidencias/
├── script/
└── README.md
```
![1](/grupo05_nettalco/PC3/evidencias_pc3/img_001.png)


```json
{
    "Version": "2012-10-17",
    "statement": [
        {
            "Effect": "Allow",
            "Action": [
              "s3:GetObject",
              "s3:Putobject",
              "s3:ListBucket",
              "s3:Deleteobject"
            ],
            "Resource": [
                "arn:aws:s3:::s3-grupo-5-vf/*"
            ],
            "Condition": {
                "StringEquals": {
                    "aws: ResourceAccount": "581983650106"
                }
            }
        }
    ]
}
```

```sql
DROP TABLE IF EXISTS base_prueba.orders_parquet

CREATE EXTERNAL TABLE IF NOT EXISTS base_prueba.orders_parquet (
    index_id               int,
    order_id               string,
    order_date             date,
    order_status           string,
    fulfilment_type        string,
    sales_channel          string,
    ship_service_level     string,
    style                  string,
    sku                    string,
    category               string,
    size                   string,
    asin                   string,
    courier_status         string,
    quantity               int,
    currency_code          string,
    amount                 double,
    ship_city              string,
    ship_state             string,
    ship_postal_code       double,
    ship_country           string,
    promotion_ids          string,
    is_b2b                 boolean,
    fulfilled_by           string,
    amount_numeric         double
)
PARTITIONED BY (
    anio                   int,
    mes                    string
)
STORED AS PARQUET
LOCATION 's3://s3-grupo-5-vf/curated/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');


MSCK REPAIR TABLE base_prueba.orders_parquet;

SELECT *
FROM base_prueba.orders_parquet
LIMIT 100;
```
