-- ============================================================================
-- CREACIÓN DE TABLAS EXTERNAS - CAPA RAW
-- Proyecto: grupo09_retail_analytics
-- Dataset: dataset_si807_g9
-- Autor: Grupo 9
-- ============================================================================

-- 1. dim_cliente_raw
CREATE OR REPLACE EXTERNAL TABLE `etl-retail-analytics.dataset_si807_g9.dim_cliente_raw` (
    sk_cliente INT64,
    cod_cliente STRING,
    cod_tipo_cliente STRING,
    desc_tipo_cliente STRING,
    estado_cliente STRING,
    numero_tarjeta_bonus STRING,
    fecha_alta_cliente STRING,
    recencia INT64
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://mi-etl-proyecto-2025/raw/dim_cliente/*.csv'],
    skip_leading_rows = 1,
    field_delimiter = ',',
    allow_jagged_rows = true,
    max_bad_records = 10
);

-- 2. dim_periodo_raw
CREATE OR REPLACE EXTERNAL TABLE `etl-retail-analytics.dataset_si807_g9.dim_periodo_raw` (
    sk_periodo INT64,
    anio INT64,
    mes INT64,
    nombre_mes STRING,
    trimestre INT64,
    inicio_mes STRING,
    fin_mes STRING,
    es_mes_cerrado INT64
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://mi-etl-proyecto-2025/raw/dim_periodo/*.csv'],
    skip_leading_rows = 1,
    field_delimiter = ',',
    allow_jagged_rows = true,
    max_bad_records = 10
);

-- 3. dim_producto_raw
CREATE OR REPLACE EXTERNAL TABLE `etl-retail-analytics.dataset_si807_g9.dim_producto_raw` (
    sk_producto INT64,
    cod_material STRING,
    desc_material STRING,
    categoria STRING,
    subcategoria STRING,
    marca STRING,
    unidad_medida STRING,
    pack_size STRING
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://mi-etl-proyecto-2025/raw/dim_producto/*.csv'],
    skip_leading_rows = 1,
    field_delimiter = ',',
    allow_jagged_rows = true,
    max_bad_records = 10
);

-- 4. dim_promocion_precio_raw
CREATE OR REPLACE EXTERNAL TABLE `etl-retail-analytics.dataset_si807_g9.dim_promocion_precio_raw` (
    sk_promocion INT64,
    cod_promocion STRING,
    cod_tipo_precio STRING,
    desc_tipo_precio STRING,
    flag_ticket_con_promocion INT64,
    vigencia_inicio STRING,
    vigencia_fin STRING
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://mi-etl-proyecto-2025/raw/dim_promocion_precio/*.csv'],
    skip_leading_rows = 1,
    field_delimiter = ',',
    allow_jagged_rows = true,
    max_bad_records = 10
);

-- 5. dim_tienda_canal_raw
CREATE OR REPLACE EXTERNAL TABLE `etl-retail-analytics.dataset_si807_g9.dim_tienda_canal_raw` (
    sk_tienda INT64,
    cod_tienda STRING,
    nombre_tienda STRING,
    cadena STRING,
    cod_canal STRING,
    desc_canal STRING,
    ciudad STRING,
    formato STRING
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://mi-etl-proyecto-2025/raw/dim_tienda_canal/*.csv'],
    skip_leading_rows = 1,
    field_delimiter = ',',
    allow_jagged_rows = true,
    max_bad_records = 10
);

-- 6. fact_hecho_venta_raw
CREATE OR REPLACE EXTERNAL TABLE `etl-retail-analytics.dataset_si807_g9.fact_hecho_venta_raw` (
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
)
OPTIONS (
    format = 'CSV',
    uris = ['gs://mi-etl-proyecto-2025/raw/fact_hecho_venta/*.csv'],
    skip_leading_rows = 1,
    field_delimiter = ',',
    allow_jagged_rows = true,
    max_bad_records = 10
);
