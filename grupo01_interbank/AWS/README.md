#  🧾 Bitácora Técnica del Pipeline AWS

### GRUPO 01
### INTEGRANTES:
### - AYMACHOQUE AYMACHOQUE, JAIRO
### - LAUREANO HIDALGO, JORDAN CESAR
### - GAMBOA CHECNES, JOEL FERNANDO

### 🪣 Paso 1 – Carga de datos en S3
<img width="1280" height="546" alt="image" src="https://github.com/user-attachments/assets/f4d915a6-2973-45a0-86bb-351c973443ae" />

<img width="1280" height="604" alt="image" src="https://github.com/user-attachments/assets/82cfb3f9-0d62-4de4-be49-e309be73a9c7" />

<img width="1280" height="573" alt="image" src="https://github.com/user-attachments/assets/50d1a7bc-598b-49b0-8573-dd03d583054a" />

![Imagen de WhatsApp 2025-11-14 a las 20 46 30_d7560bc1](https://github.com/user-attachments/assets/eae698e5-2642-4c90-a060-f47ceee04fed)

### ⚙️ Paso 2 – Glue Data Catalog

![Imagen de WhatsApp 2025-11-14 a las 20 46 30_7d34b66a](https://github.com/user-attachments/assets/0667f629-1af4-4282-93e8-9f0d93707d09)

<img width="1280" height="600" alt="image" src="https://github.com/user-attachments/assets/61902002-0960-42c6-bfce-ab21ab40dd91" />


### 🧠 Paso 3 – Glue Job PySpark
<img width="1280" height="528" alt="image" src="https://github.com/user-attachments/assets/f5d5839d-7eef-4ee9-bfd7-7fba0daf36cc" />

<img width="1280" height="535" alt="image" src="https://github.com/user-attachments/assets/f96565da-9697-4164-8076-7e3ceada1ca2" />

## Almacenamiento ETL en AWS

<img width="1280" height="536" alt="image" src="https://github.com/user-attachments/assets/9f7368c6-a273-4979-8dfe-e9c606309c5a" />

### Consumo de datos Athena

```sql
DROP TABLE IF EXISTS analytics_db.sales_curated;

CREATE EXTERNAL TABLE IF NOT EXISTS analytics_db.sales_curated (
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
LOCATION 's3://s3-grupo-1-vf/curated/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');

MSCK REPAIR TABLE analytics_db.sales_curated;
```
