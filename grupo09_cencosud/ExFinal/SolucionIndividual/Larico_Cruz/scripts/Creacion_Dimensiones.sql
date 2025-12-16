CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_sucursal\` AS
SELECT DISTINCT ABS(FARM_FINGERPRINT(Branch)) as id_sucursal, Branch, City FROM \`$PROJECT_ID.$DATASET_NAME.tbl_supermarket_curated\`;
CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_producto\` AS
SELECT DISTINCT ABS(FARM_FINGERPRINT(product_line)) as id_producto, product_line FROM \`$PROJECT_ID.$DATASET_NAME.tbl_supermarket_curated\`;
CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_cliente\` AS
SELECT DISTINCT ABS(FARM_FINGERPRINT(CONCAT(customer_type, Gender))) as id_cliente, customer_type, Gender FROM \`$PROJECT_ID.$DATASET_NAME.tbl_supermarket_curated\`;
CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_pago\` AS
SELECT DISTINCT ABS(FARM_FINGERPRINT(Payment)) as id_pago, Payment FROM \`$PROJECT_ID.$DATASET_NAME.tbl_supermarket_curated\`;
CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.dim_tiempo\` AS
SELECT DISTINCT ABS(FARM_FINGERPRINT(CAST(Date AS STRING))) as id_tiempo, CAST(Date AS DATE) as fecha, EXTRACT(MONTH FROM CAST(Date AS DATE)) as mes FROM \`$PROJECT_ID.$DATASET_NAME.tbl_supermarket_curated\`;
