-- 1. LIMPIEZA (Capa Plata)
CREATE OR REPLACE TABLE `superstore_bi.silver_ventas` AS
SELECT DISTINCT
  Order_ID,
  SAFE.PARSE_DATE('%d/%m/%Y', Order_Date) AS Order_Date,
  Customer_ID,
  Customer_Name,
  Segment,
  Country,
  City,
  State,
  Postal_Code,
  Region,
  Product_ID,
  Category,
  Sub_Category,
  Product_Name,
  Sales
FROM `superstore_bi.raw_ventas`
WHERE Order_ID IS NOT NULL;

-- 2. MODELO ESTRELLA (Capa Oro)
CREATE OR REPLACE TABLE `superstore_bi.dim_cliente` AS
SELECT DISTINCT Customer_ID, Customer_Name, Segment FROM `superstore_bi.silver_ventas`;

CREATE OR REPLACE TABLE `superstore_bi.dim_producto` AS
SELECT DISTINCT Product_ID, Category, Sub_Category, Product_Name FROM `superstore_bi.silver_ventas`;

CREATE OR REPLACE TABLE `superstore_bi.dim_ubicacion` AS
SELECT DISTINCT Postal_Code, Country, City, State, Region FROM `superstore_bi.silver_ventas`;

CREATE OR REPLACE TABLE `superstore_bi.fact_ventas` AS
SELECT Order_ID, Order_Date, Customer_ID, Product_ID, Postal_Code, Sales FROM `superstore_bi.silver_ventas`;