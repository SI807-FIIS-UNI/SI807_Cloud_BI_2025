
CREATE EXTERNAL TABLE IF NOT EXISTS analytics_db.sales_curated (
  order_id string,
  order_date string,
  ship_date string,
  customer_id string,
  customer_name string,
  segment string,
  country string,
  city string,
  state string,
  product_id string,
  category string,
  sub_category string,
  product_name string,
  sales double,
  quantity int,
  discount double,
  profit double,
  margen double
)
PARTITIONED BY (anio string, mes string)
STORED AS PARQUET
LOCATION 's3://si807u-<grupo>-bi/curated/ecommerce/';
MSCK REPAIR TABLE analytics_db.sales_curated;
