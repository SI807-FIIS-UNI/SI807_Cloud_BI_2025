# 🌩️ Proyecto Cloud BI – Luz del Sur (Facturación Atípica)

Repositorio del proyecto de **Inteligencia de Negocios en la Nube** basado en datos de **Luz del Sur** sobre clientes, suministros y facturación eléctrica en **Lima Metropolitana**.

El objetivo es implementar un pipeline **RAW → BRONZE → SILVER → GOLD → Dashboard** en **AWS + Power BI** para detectar y visualizar **casos de facturación atípica**.

## Estructura del Proyecto
```text
grupo08_LuzdelSur/Luz_del_Sur
│
├── etl/                  # Scripts y procesos de integración cloud
│   ├── scripts/
│   └── logs/
│   └── raw/
│
├── dw/                   # Data warehouse cloud
│   ├── ddl/
│   └── consultas/
│
├── dashboard/            # Dashboards y visualizaciones
│   ├── evidencias/
│   └── publicacion/
│
├── docs/                 # Documentación técnica
│   ├── arquitectura_cloud.pdf
│   ├── bitacora_tecnica.md
│   ├── costos_cloud.xlsx
│   └── informe_final.pdf
│
└── README.md
```
---

## Requerimientos   
---
## ☁️ Cuenta AWS, costos y entorno

- **Cuenta AWS:** se utilizó una cuenta personal con créditos gratuitos y control de costos.
- **Región:** 'sa-east-1' (debe ser consistente entre S3, Glue y Athena).
- **Servicios usados:** S3, Glue (Data Catalog + Jobs), Athena, IAM.
- **Control de costos:**
  - Uso de datos reducidos (~82k filas en acumulado).
  - Formato Parquet en Bronze/Silver/Gold para minimizar bytes escaneados.
  - Creación de un *Workgroup* en Athena con límite de gasto recomendado.

## 🔌 Archivo ODBC (DSN) para Athena → Power BI

Se configuró un **Data Source Name (DSN)** en Windows usando el driver:

- **Driver:** *Simba Amazon Athena ODBC Driver 2.x (64-bit)*
- **Nombre DSN:** `athena_luzdelsur`

Parámetros principales:

- **AWS Region:** `[sa-east-1]`
- **S3 Output Location:**
```text
  s3://lds-s3-bucket-demo/athena_results/
```

## 🎯 Objetivos
- Diseñar y desplegar un **data lake** en S3 siguiendo la **arquitectura Medallion**.
- Automatizar la ingesta y limpieza con **AWS Glue (Data Catalog + Jobs)**.
- Modelar datos de consumo y facturación mensual en capas **Silver** y **Gold**.
- Detectar **facturación atípica** mediante reglas estadísticas (IQR).
- Exponer los datos a **Power BI** vía **Amazon Athena (ODBC)** y construir un dashboard analítico.

## 🏗️ Arquitectura AWS

Servicios principales:

- **Amazon S3**: almacenamiento por capas (`raw/`, `bronze/`, `silver/`, `gold/`, `athena_results/`).
- **AWS Glue Data Catalog**: bases `raw_db`, `bronze_db`, `silver_db`, `gold_db`.
- **AWS Glue Studio / Jobs**: transformación CSV → Parquet y limpieza de esquemas.
- **Amazon Athena**: consultas SQL, creación de tablas externas y *views*.
- **Power BI Desktop**: conexión vía **ODBC Athena** y construcción del dashboard.


Bucket principal:

    lds-s3-bucket-demo/
    ├── raw/
    │   ├── cliente/
    │   ├── suministro/
    │   ├── medidor/
    │   ├── sector/
    │   ├── tarifa/
    │   ├── tarifa_asignacion/
    │   └── acumulado/          # consumo mensual 2022–2025
    ├── bronze/
    │   ├── bronze_cliente/
    │   ├── bronze_suministro/
    │   ├── bronze_medidor/
    │   ├── bronze_sector/
    │   ├── bronze_tarifa/
    │   ├── bronze_tarifa_asignacion/
    │   └── bronze_acumulado/   
    ├── silver/
    |   ├── consumo_mensual/
    ├── gold/
    |   ├── facturacion_teorica_mes/
    └── athena_results/
 

## 🧱 Modelo de Datos (capas)
### BRONZE
BRONZE (datos limpios, 1:1 RAW)

Tablas principales (Parquet):
- bronze_cliente
- bronze_suministro
- bronze_medidor
- bronze_sector
- bronze_tarifa
- bronze_asignacion_tarifa
- bronze_acumulado (consumo mensual por medidor y suministro)
---
### SILVER
- consumo_mensual

```sql
    CREATE DATABASE IF NOT EXISTS silver_db;
    CREATE TABLE silver_db.silver_consumo_mensual
    WITH (
    external_location = 's3://lds-s3-bucket-demo/silver/consumo_mensual/',
    format = 'PARQUET',
    write_compression = 'SNAPPY'
    ) AS
    SELECT
    id_suministro,
    id_medidor,
    anio_mes,
    energia_total_kwh,
    demanda_max_kw,
    n_registros,
    n_registros_error,
    n_registros_error * 1.0 / NULLIF(n_registros, 0) AS pct_registros_error
    FROM bronze_db.bronze_acumulado;
```

Grano: (id_suministro, id_medidor, anio_mes)
Campos: energía mensual, demanda máxima, registros esperados, % de registros con error.

---

### GOLD
```sql
    CREATE DATABASE IF NOT EXISTS gold_db;
    DROP TABLE IF EXISTS gold_db.gold_facturacion_teorica_mes;
    CREATE TABLE gold_db.gold_facturacion_teorica_mes
    WITH (
    external_location = 's3://lds-s3-bucket-demo/gold/facturacion_teorica_mes/',
    format = 'PARQUET',
    write_compression = 'SNAPPY'
    ) AS
    WITH base AS (
    SELECT
        cm.id_suministro,
        cm.id_medidor,
        cm.anio_mes,
        cm.energia_total_kwh,
        cm.demanda_max_kw,
        cm.n_registros,
        cm.n_registros_error,
        cm.pct_registros_error,
        s.nivel_tension,
        s.distrito,
        c.tipo_cliente,
        atf.cod_tarifa,
        t.cargo_energia,
        t.cargo_fijo,
        (cm.energia_total_kwh * t.cargo_energia) + t.cargo_fijo AS facturacion_teorica
    FROM silver_db.silver_consumo_mensual cm
    JOIN bronze_db.bronze_suministro s
        ON cm.id_suministro = s.id_suministro
    JOIN bronze_db.bronze_cliente c
        ON s.id_cliente = c.id_cliente
    JOIN bronze_db.bronze_asignacion_tarifa atf
        ON atf.id_suministro = s.id_suministro
    AND atf.estado_asignacion = 'ACTIVO'
    JOIN bronze_db.bronze_tarifa t
        ON t.cod_tarifa = atf.cod_tarifa
    ),
    seg AS (
    SELECT
        *,
        COUNT(*) OVER (
        PARTITION BY tipo_cliente, nivel_tension, anio_mes
        ) AS n_segmento,
        approx_percentile(facturacion_teorica, 0.25) OVER (
        PARTITION BY tipo_cliente, nivel_tension, anio_mes
        ) AS q1,
        approx_percentile(facturacion_teorica, 0.75) OVER (
        PARTITION BY tipo_cliente, nivel_tension, anio_mes
        ) AS q3
    FROM base
    ),
    bounds AS (
    SELECT
        *,
        (q3 - q1) AS iqr,
        q3 + 1.5 * (q3 - q1) AS umbral_superior
    FROM seg
    )
    SELECT
    *,
    CASE
        WHEN n_segmento >= 30
        AND facturacion_teorica > umbral_superior
        THEN 1 ELSE 0
    END AS es_atipico
    FROM bounds;
```
- Integra Silver + cliente + suministro + tarifa.
- Calcula facturacion_teorica = energía × cargo_energía + cargo_fijo.
- Calcula métricas por segmento (tipo_cliente, nivel_tension, anio_mes) usando IQR: Q1, Q3, IQR, umbral superior.
- Bandera es_atipico para casos sobre Q3 + 1.5 × IQR en segmentos con n_segmento ≥ 30.

---

### Vistas KPI:  
- vw_facturacion_atipica_detalle
```sql
    CREATE OR REPLACE VIEW gold_db.vw_facturacion_atipica_detalle AS
    SELECT
    g.id_suministro,
    g.id_medidor,
    g.anio_mes,
    SUBSTR(g.anio_mes, 1, 4) AS anio,
    SUBSTR(g.anio_mes, 6, 2) AS mes,
    s.zona,           -- zona (cono) derivada del distrito
    g.distrito,
    g.tipo_cliente,
    g.nivel_tension,
    g.cod_tarifa,
    g.energia_total_kwh,
    g.demanda_max_kw,
    g.n_registros,
    g.n_registros_error,
    g.pct_registros_error,
    g.facturacion_teorica,
    g.n_segmento,
    g.q1,
    g.q3,
    g.iqr,
    g.umbral_superior,
    g.es_atipico
    FROM gold_db.gold_facturacion_teorica_mes g
    JOIN bronze_db.bronze_suministro s
    ON g.id_suministro = s.id_suministro;
```
- vw_kpi_atipicos_mes
```sql
    CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_mes AS
    SELECT
    anio_mes,
    SUBSTR(anio_mes, 1, 4) AS anio,
    SUBSTR(anio_mes, 6, 2) AS mes,
    COUNT(*) AS total_registros,
    COUNT_IF(es_atipico = 1) AS total_atipicos,
    COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
    FROM gold_db.gold_facturacion_teorica_mes
    GROUP BY anio_mes;
```
- vw_kpi_atipicos_zona_mes
```sql
    CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_zona_mes AS
    SELECT
    anio_mes,
    anio,
    mes,
    zona,
    COUNT(*) AS total_registros,
    COUNT_IF(es_atipico = 1) AS total_atipicos,
    COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
    FROM gold_db.vw_facturacion_atipica_detalle
    GROUP BY anio_mes, anio, mes, zona;
```
- vw_kpi_atipicos_distrito_mes
```sql
    CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_distrito_mes AS
    SELECT
    anio_mes,
    anio,
    mes,
    distrito,
    COUNT(*) AS total_registros,
    COUNT_IF(es_atipico = 1) AS total_atipicos,
    COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
    FROM gold_db.vw_facturacion_atipica_detalle
    GROUP BY anio_mes, anio, mes, distrito;
```
- vw_kpi_atipicos_zona_anual
```sql
    CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_zona_anual AS
    SELECT
    anio,
    zona,
    COUNT(*) AS total_registros,
    COUNT_IF(es_atipico = 1) AS total_atipicos,
    COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
    FROM gold_db.vw_facturacion_atipica_detalle
    GROUP BY anio, zona;
```

- vw_kpi_atipicos_distrito_anual
```sql
    CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_distrito_anual AS
    SELECT
    anio,
    distrito,
    COUNT(*) AS total_registros,
    COUNT_IF(es_atipico = 1) AS total_atipicos,
    COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
    FROM gold_db.vw_facturacion_atipica_detalle
    GROUP BY anio, distrito;
```
---

## 📊 KPI principal
Definición:
Proporción de suministros cuya facturación teórica mensual es significativamente mayor que la de clientes similares, de acuerdo con la regla:

facturacion_teorica > Q3 + 1.5 × IQR
(segmentando por tipo_cliente, nivel_tension y anio_mes).

Métricas clave:
- % de atípicos por mes
- Número de atípicos por distrito y zona (cono)
- Facturación total y promedio por segmento
- Ranking de distritos / zonas más críticos

## 🔄 Exportar datos de Athena a Power BI

### Exportar a Power BI

Conexión directa vía ODBC 
- Instalar driver ODBC Athena 2.x.
- Crear DSN athena_luzdelsur.

En Power BI:
- Obtener datos → ODBC → athena_luzdelsur.
- Seleccionar vistas de gold_db (ej. vw_facturacion_atipica_detalle).
- Modo de conexión: Import (dataset se almacena dentro del .pbix).




## 🧑‍💻 Autores
Proyecto: Luz del Sur – Facturación Atípica  
Curso: Sistema de Inteligencia de Negocios - SI807
Integrantes: 
```texto 
Hernández Jahir, Gordillo Mikhael y Enciso Frey
```
