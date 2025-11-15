# 📘 README -- Pipeline de Introducción a AWS (Grupo 8)

## 🎯 Objetivo

Implementar un flujo inicial de procesamiento de datos en **AWS**, desde
la carga del dataset hasta la catalogación y preparación para análisis,
utilizando **S3 y Glue** como principales servicios.

El flujo esperado del laboratorio es:

    S3 (raw) → Glue Crawler → Glue Data Catalog → S3 (curated)

## 🧱 1. Estructura creada en S3

    s3://si807u-grupo8-bi/
    ├── raw/
    │   └── ecommerce/
    ├── curated/
    │   └── ecommerce/
    ├── analytics/
    │   └── results/
    └── athena_results/

## 2. Proceso ejecutado

### 1️⃣ Preparación del dataset

-   Dataset original: Amazon Sale Report.csv
-   Resultado del EDA: ecommerce_clean.csv

### 2️⃣ Carga de datos en S3

Archivo cargado en:

    s3://si807u-grupo8-bi/raw/ecommerce/ecommerce_clean.csv

### 3️⃣ Glue Data Catalog

-   Base creada: raw_db
-   Crawler configurado con la ruta raw/ecommerce/
-   ❗ El crawler no logró crear la tabla por un error no identificado

## 🚧 Trabajo Pendiente

-   Resolver el error del Crawler
-   Job PySpark
-   Athena
-   QuickSight

## ✔️ Conclusión

Se configuró correctamente S3 y Glue, pero el pipeline se detuvo por el
error del Crawler.
