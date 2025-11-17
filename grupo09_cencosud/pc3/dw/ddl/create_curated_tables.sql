-- ============================================================================
-- CREACIÓN DE TABLAS NATIVAS - CAPA CURATED
-- Proyecto: grupo09_retail_analytics
-- Dataset: dataset_si807_g9
-- Autor: Grupo 9
-- ============================================================================

-- 1. dim_cliente_curated
CREATE OR REPLACE TABLE `etl-retail-analytics.dataset_si807_g9.dim_cliente_curated` (
    sk_cliente INT64,
    cod_cliente STRING,
    cod_tipo_cliente STRING,
    desc_tipo_cliente STRING,
    estado_cliente STRING,
    numero_tarjeta_bonus STRING,
    fecha_alta_cliente_dt DATE,
    recencia INT64
);

-- 2. dim_periodo_curated
CREATE OR REPLACE TABLE `etl-retail-analytics.dataset_si807_g9.dim_periodo_curated` (
    sk_periodo INT64,
    anio INT64,
    mes INT64,
    nombre_mes STRING,
    trimestre INT64,
    es_mes_cerrado INT64,
    inicio_mes_dt DATE,
    fin_mes_dt DATE
);

-- 3. dim_producto_curated
CREATE OR REPLACE TABLE `etl-retail-analytics.dataset_si807_g9.dim_producto_curated` (
    sk_producto INT64,
    cod_material STRING,
    desc_material STRING,
    categoria STRING,
    subcategoria STRING,
    marca STRING,
    unidad_medida STRING,
    pack_size STRING
);

-- 4. dim_promocion_precio_curated
CREATE OR REPLACE TABLE `etl-retail-analytics.dataset_si807_g9.dim_promocion_precio_curated` (
    sk_promocion INT64,
    cod_promocion STRING,
    cod_tipo_precio STRING,
    desc_tipo_precio STRING,
    flag_ticket_con_promocion INT64,
    vigencia_inicio_dt DATE,
    vigencia_fin_dt DATE
);

-- 5. dim_tienda_canal_curated
CREATE OR REPLACE TABLE `etl-retail-analytics.dataset_si807_g9.dim_tienda_canal_curated` (
    sk_tienda INT64,
    cod_tienda STRING,
    nombre_tienda STRING,
    cadena STRING,
    cod_canal STRING,
    desc_canal STRING,
    ciudad STRING,
    formato STRING
);

-- 6. fact_hecho_venta_curated
CREATE OR REPLACE TABLE `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_curated` (
    cod_ticket STRING,
    sk_cliente INT64,
    sk_producto INT64,
    sk_tienda INT64,
    sk_periodo INT64,
    sk_promocion INT64,
    num_secuencia INT64,
    monto_venta_bruta FLOAT64,
    monto_venta_neta FLOAT64,
    monto_margen FLOAT64,
    monto_descuento FLOAT64
);