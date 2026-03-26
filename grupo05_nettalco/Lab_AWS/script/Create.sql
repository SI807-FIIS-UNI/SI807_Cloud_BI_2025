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
LOCATION 's3://s3-grupo-6-vf/curated/'
TBLPROPERTIES ('parquet.compression'='SNAPPY');