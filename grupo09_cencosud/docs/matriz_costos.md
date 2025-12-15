# 💰 Estimación de Costos Mensuales - Arquitectura GCP

Este documento detalla la estimación de costos operativos mensuales para la arquitectura de **Data Lakehouse en Google Cloud Platform**. El cálculo se basa en un escenario de carga de trabajo típica para el procesamiento de datos retail.

| **Costo Total Estimado** | **$487.94 USD / Mes** |
|:-------------------------|:---------------------:|

---

## 📊 Desglose por Componente

### 1. Ingesta y Almacenamiento (Data Lake)
Servicios encargados de recibir los archivos crudos, disparar eventos y almacenar los datos históricos.

| Servicio | Detalle de Uso | Costo Estimado |
| :--- | :--- | :--- |
| **Cloud Storage** | **Almacenamiento:** 50 GB Standard (`$1.15`) <br> **Operaciones:** Clase A (`$2.50`) y Clase B (`$0.20`) | **$3.85** |
| **Cloud Functions** | **Invocaciones:** 2 millones/mes (Trigger por archivo) <br> **Config:** 256MB RAM, 200ms duración | **$3.00** |
| **Pub/Sub** | **Volumen:** 100 GB de tráfico de mensajes | **$4.00** |
| | **Subtotal Ingesta** | **$10.85** |

### 2. Procesamiento y Transformación (ETL)
Capa de cómputo para la limpieza, transformación y enriquecimiento de datos utilizando Spark.

| Servicio | Detalle de Uso | Costo Estimado |
| :--- | :--- | :--- |
| **Dataproc** | **Recursos:** 4 vCPUs, 16GB RAM (2 Instancias) <br> **Uso:** 4 horas diarias (ventanas de carga) durante 30 días | **$120.00** |
| | **Subtotal Procesamiento** | **$120.00** |

### 3. Data Warehouse & Analítica
Almacenamiento estructurado y consultas SQL para Business Intelligence.

| Servicio | Detalle de Uso | Costo Estimado |
| :--- | :--- | :--- |
| **BigQuery** | **Almacenamiento Activo:** 100 GB (`$2.00`) <br> **Análisis:** 1 TB de consultas procesadas (`$5.00`) | **$7.00** |
| | **Subtotal Analítica** | **$7.00** |

### 4. Orquestación y Gobierno
Gestión del flujo de trabajo (DAGs) y seguridad de los datos.

| Servicio | Detalle de Uso | Costo Estimado |
| :--- | :--- | :--- |
| **Cloud Composer** | **Entorno:** Small (gestión de Airflow 24/7 - 730 horas) | **$350.00** |
| **Cloud KMS** | **Llaves:** 1 Versión de clave + 100k operaciones criptográficas | **$0.09** |
| **Cloud Monitoring**| **Logs & API:** 50 MB ingestión + 1000 llamadas (Capa gratuita) | **$0.00** |
| | **Subtotal Gobierno** | **$350.09** |
