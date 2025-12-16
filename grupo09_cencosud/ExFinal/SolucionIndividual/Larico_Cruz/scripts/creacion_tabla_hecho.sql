CREATE OR REPLACE TABLE \`$PROJECT_ID.$DATASET_NAME.fact_ventas\` AS
SELECT
    ABS(FARM_FINGERPRINT(Branch)) as id_sucursal,
    ABS(FARM_FINGERPRINT(product_line)) as id_producto,
    ABS(FARM_FINGERPRINT(CONCAT(customer_type, Gender))) as id_cliente,
    ABS(FARM_FINGERPRINT(Payment)) as id_pago,
    ABS(FARM_FINGERPRINT(CAST(Date AS STRING))) as id_tiempo,
    invoice_id, Sales as total, tax_5_percent as tax, gross_income, Quantity as quantity
FROM \`$PROJECT_ID.$DATASET_NAME.tbl_supermarket_curated\`;
