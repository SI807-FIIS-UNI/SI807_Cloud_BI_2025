# 📘 Bitácora de Proyecto: Retail Analytics ETL Pipeline
**Curso:** Data Engineering on GCP  
**Proyecto:** PC4 - Arquitectura Lakehouse Retail  
**Grupo:** 09  
**Fecha:** Diciembre 2025  

---

## 1. Descripción del Proyecto
Implementación de un pipeline de datos *End-to-End* en Google Cloud Platform para una empresa de Retail. La arquitectura sigue el paradigma **Lakehouse** (Raw, Curated, Analytics) y utiliza procesamiento **Serverless**, orquestación con **Airflow** y seguridad avanzada (**VPC + KMS**).

## 2. Arquitectura Implementada
* **Ingesta:** Google Cloud Storage (Cifrado con CMEK).
* **Procesamiento:** Dataproc Serverless (PySpark) dentro de VPC Privada.
* **Almacenamiento:** BigQuery (Capas Raw, Curated, Analytics).
* **Orquestación:** Cloud Composer (Apache Airflow).
* **Automatización:** Cloud Functions (Gen 2) + Pub/Sub.
* **Observabilidad:** Cloud Monitoring + Alerting Policies.
* **Visualización:** Looker Studio.

---

## 3. Registro de Ejecución

### 📆 Fase 1: Configuración y Seguridad (Security First)
**Objetivo:** Preparar el entorno con los estándares de seguridad exigidos (Rúbrica: 20%).

* [x] Definición de variables de entorno (`PROJECT_ID`, `REGION`, etc.).
* [x] Habilitación masiva de APIs (Compute, Dataproc, Composer, KMS, etc.).

#### 🔐 Implementación de Seguridad Avanzada
Para cumplir con los requisitos de gobernanza, implementamos:
1.  **KMS (Key Management Service):** Creación del keyring `keyring-retail-g9` y la llave `key-retail-data`.
2.  **IAM Granular:** Asignación del rol `cryptoKeyEncrypterDecrypter` a las cuentas de servicio de Storage, BigQuery y Dataproc.
3.  **VPC Personalizada:** Creación de la red `vpc-retail-g9` y subred `sub-retail-us` con *Private Google Access* habilitado.
4.  **Firewall:** Reglas para permitir comunicación interna de nodos Dataproc.

> **Comando Clave:**
> ```bash
> gcloud compute networks subnets create sub-retail-us --enable-private-ip-google-access ...
> ```

---

### 📆 Fase 2: Data Lake (Cloud Storage)
**Objetivo:** Crear la capa de almacenamiento con estructura definida.

* [x] Creación del Bucket `gs://pc4-si807-g9-bucket` con encriptación KMS por defecto.
* [x] Creación de estructura de carpetas (`raw`, `curated`, `analytics`) usando objetos vacíos.
* [x] Carga de 6 archivos CSV maestros a la capa `raw`.

> **Nota Técnica:** GCS no tiene carpetas reales. Utilizamos el truco `gsutil cp /dev/null gs://.../` para simular la estructura requerida por la rúbrica.

---

### 📆 Fase 3: Data Warehouse (BigQuery - Capa RAW)
**Objetivo:** Exponer los archivos CSV como tablas externas.

* [x] Creación del Dataset `dataset_si807_g9`.
* [x] Ejecución de DDLs para crear 6 tablas externas (`_raw`).

---

### 📆 Fase 4: Transformación (Dataproc Serverless)
**Objetivo:** Limpieza y curación de datos usando PySpark.

* [x] Desarrollo del script `etl_curated_job.py`.
* [x] **Corrección de Errores:**
    * *Error:* `TypeError: 'Column' object is not callable`.
    * *Solución:* Se corrigió la sintaxis en `transform_dim_cliente`, agregando comas faltantes y usando `lower(col(...))` correctamente.
* [x] Ejecución del Job Batch en Dataproc.

> **Ejecución Segura (Evidence):**
> Se lanzó el job especificando la red y la llave de encriptación:
> ```bash
> gcloud dataproc batches submit pyspark ... --subnet=sub-retail-us --kms-key=$KMS_KEY
> ```

---

### 📆 Fase 5: Modelado y OLAP
**Objetivo:** Generar tablas de negocio y cubo analítico.

* [x] Validación de tablas `_curated` en BigQuery.
* [x] Creación de la tabla `resumen_ventas_analytics` (Cubo OLAP) mediante SQL.
* [x] **Validación de Calidad:** Se ejecutó query de integridad comparando `SUM(Ventas)` en Fact Table vs Cubo OLAP. Diferencia = 0.

---

### 📆 Fase 6: Automatización (Event-Driven)
**Objetivo:** Disparar el ETL automáticamente al subir archivos nuevos.

* [x] Creación de Topic Pub/Sub `etl-notifications`.
* [x] Despliegue de Cloud Function Gen 2 `trigger-etl-on-upload`.
* [x] **Resolución de Problema IAM:**
    * *Error:* `Permission denied ... Cloud Storage service account ... unable to publish`.
    * *Solución:* Se otorgó el rol `roles/pubsub.publisher` al Agente de Servicio de Google Storage.

---

### 📆 Fase 7: Observabilidad
**Objetivo:** Monitoreo proactivo de fallos.

* [x] Creación de Política de Alerta en Cloud Monitoring.
* [x] **Ajuste de Configuración:**
    * *Error:* `Unknown resource type: dataproc.googleapis.com/Batch`.
    * *Solución:* Se corrigió el filtro del YAML para usar `resource.type="dataproc_batch"`.

---

### 📆 Fase 8: Orquestación (Cloud Composer)
**Objetivo:** Pipeline programado y visual.

* [x] Creación de entorno Composer 2 (Airflow).
* [x] Despliegue del DAG `etl_retail_dag.py`.
* [x] Ejecución manual exitosa (Todos los nodos en verde).

---

### 📆 Fase 9: Optimización y BI
**Objetivo:** Mejora de rendimiento y entrega final.

* [x] Creación de **Vista Materializada** `mv_ventas_mensuales`.
    * *Resultado:* Reducción de tiempo de consulta de ~1.2s a ~0.3s.
* [x] Conexión de Looker Studio a BigQuery.
* [x] Creación de Dashboard con KPIs de ventas por ciudad y temporalidad.

---

## 4. Conclusiones y Lecciones Aprendidas
1.  **Seguridad:** Implementar VPC y KMS desde el inicio es fundamental para arquitecturas empresariales, aunque añade complejidad a los permisos IAM.
2.  **Serverless:** Dataproc Serverless simplifica la gestión de infraestructura, eliminando la necesidad de configurar clusters Hadoop manualmente.
3.  **Eventos:** El uso de Eventarc y Cloud Functions permite desacoplar la ingesta del procesamiento, modernizando el flujo de datos tradicional.

---
**Firmado:** Grupo 09
