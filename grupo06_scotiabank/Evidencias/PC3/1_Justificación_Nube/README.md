# 🏦 1. Justificación del Uso de la Nube

### *Comparación técnica y financiera entre AWS, Azure y GCP*

## 1.1 Recordatorio

El proyecto planteado por el equipo, consiste en la construcción de un flujo completo de Inteligencia de Negocios: web scraping, ETL, arquitectura Medallion (Bronce-Plata-Oro), procesamiento PySpark, almacenamiento analítico y visualización final en Power BI.
Para migrar este proyecto a la nube, se evaluaron **AWS**, **Azure** y **Google Cloud Platform (GCP)** considerandolos algunas caracteristicas que tiene el proyecto:

* Dataset reducido (~1GB).
* Adopción de una arquitectura Medallion.
* Preferencia por servicios **serverless** para evitar mantenimiento.
* Curva de aprendizaje manejable.
* Seguridad para un entorno bancario.

---

## 1.2 Criterios de evaluación

Los criterios aplicados son:

1. **Seguridad y cumplimiento normativo**
2. **Escalabilidad y elasticidad operativa**
3. **Estructura de costos y modelos de pricing**
4. **Ecosistema de BI**
5. **Redundancia, resiliencia y continuidad operativa**
6. **Capacidades de red (latencia, ancho de banda)**
7. **Soporte para cargas batch**

---

## 1.3 Comparación técnica entre AWS, Azure y GCP

A continuación se compararan en profundidad cada uno de los criterios aplicados para la evaluación de AWS, Azure y Google Cloud Platform (GCP).

### 1.3.1 Seguridad y cumplimiento normativo

La seguridad en entornos cloud se analiza desde tres puntos: controles de identidad, capacidades de protección de datos y portafolio de cumplimiento normativo.
Para entornos bancarios, estos aspectos deben alinearse con normativas como PCI DSS, ISO 27001, SOC 2 para temas de seguridad.

| Aspecto | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Certificaciones de cumplimiento** | 143 estándares (ISO 27001, SOC 1/2/3, PCI DSS Level 1, HIPAA) | 116 estándares (ISO 27001, SOC 1/2/3, PCI DSS, ENS High) | 98 estándares (ISO 27001, SOC 1/2/3, PCI DSS Level 1) |
| **Cifrado por defecto** | Opcional (debe habilitarse manualmente en S3, RDS, etc.) | Opcional (debe configurarse en Storage, SQL Database) | **Automático en todos los servicios sin configuración** |
| **Modelo Zero Trust** | IAM + AWS Organizations + GuardDuty | Microsoft Entra ID + Conditional Access + Defender | **BeyondCorp (implementación nativa desde 2011)** |
| **Gestión de claves** | AWS KMS (control granular por región) | Azure Key Vault (integración con HSM) | Cloud KMS + **Cloud HSM certificado FIPS 140-2 Nivel 3** |
| **Auditoría y logging** | CloudTrail (registro de API calls) | Azure Monitor + Log Analytics | **Cloud Audit Logs (habilitado por defecto, inmutable)** |
| **DLP nativo** | Amazon Macie (ML para datos sensibles en S3) | Microsoft Purview (integrado con M365) | **Cloud DLP (detección de 150+ tipos de datos sensibles)** |

**Requisitos de seguridad para proyecto:**

| Requisito | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Cifrado automático | ❌ Manual | ❌ Manual | ✅ **Automático** |
| Auditoría por defecto | ⚠️ Debe configurarse | ⚠️ Debe configurarse | ✅ **Inmutable y automático** |
| Complejidad de configuración | ⚠️ Alta | ⚠️ Media-Alta | ✅ **Mínima** |


**GCP satisface todos los requisitos de seguridad bancaria con el menor overhead operativo**, permitiendo enfocarnos en la arquitectura de datos en lugar de configuración de controles de seguridad.


### 1.3.2 Escalabilidad y elasticidad

La escalabilidad evalúa la capacidad de ajustar recursos automáticamente según la demanda, mientras que la elasticidad mide qué tan rápido y eficiente es ese ajuste. En función de nuestro proyecto, se requiere escalamiento horizontal automático sin intervención manual.

| Aspecto | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Procesamiento Spark** | EMR con Auto Scaling (escala por nodos, requiere configuración de métricas) | Synapse Spark Pools (escalamiento manual o automático con warmup) | **Dataproc Serverless (escala de 0 a N workers automáticamente)** |
| **Tiempo de escalamiento** | 5-10 minutos (provisionar nuevos nodos) | 3-8 minutos (activar pool + warmup) | **< 1 minuto (sin clústeres permanentes)** |
| **Modelo de escalamiento** | Basado en métricas de CloudWatch (CPU, memoria, custom) | Basado en carga de trabajo o programado | **Completamente automático basado en demanda** |
| **Almacenamiento analítico** | Redshift: escala mediante resize (minutos a horas de downtime) | Synapse SQL: escala DWUs (pausable manualmente) | **BigQuery: escalamiento transparente sin gestión** |
| **Escalamiento a cero** | EMR requiere al menos 1 nodo master activo | Synapse puede pausarse pero requiere acción manual | **Dataproc Serverless escala a 0 automáticamente** |
| **Orquestación batch** | Step Functions (escala automáticamente) | Azure Data Factory (escala por Integration Runtime) | **Cloud Composer (Airflow administrado, escala automáticamente)** |
| **Granularidad de escalamiento** | Por instancia completa (mínimo 1 EC2) | Por unidad de procesamiento (vCore, DWU) | **Por vCPU-segundo en Dataproc, por slot en BigQuery** |


**Requisitos de escalabilidad para el proyecto**

| Requisito | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Escalamiento sin gestión de clústeres | ❌ Requiere EMR | ❌ Requiere Spark Pools | ✅ **Dataproc Serverless** |
| Escala a cero entre ejecuciones batch | ❌ No (nodo master permanente) | ⚠️ Manual | ✅ **Automático** |
| Tiempo de inicio < 2 minutos | ❌ 5-10 min | ⚠️ 3-8 min | ✅ **< 1 min** |
| Almacenamiento analítico sin gestión | ⚠️ Redshift Serverless (limitado) | ⚠️ Synapse (requiere configuración) | ✅ **BigQuery (completamente automático)** |
| Facturación por uso real | ❌ Factura por hora de clúster | ⚠️ Factura por pool activo | ✅ **Por vCPU-segundo real** |


**Para el proyecto con ejecuciones batch y dataset reducido**, GCP ofrece la elasticidad más eficiente.



### 1.3.3 Costos y modelo de pricing

Se evalúa un aprocimado del costo total de operación (TCO) considerando procesamiento , almacenamiento, consultas analíticas y servicios de orquestación para **1-2 ejecuciones mensuales de ETL**.

| Componente | AWS | Azure | GCP |
|------------|-----|-------|-----|
| **Almacenamiento objeto (Bronce)** | S3 Standard: $0.023/GB-mes | ADLS Gen2: $0.0208/GB-mes | Cloud Storage Standard: **$0.020/GB-mes** |
| **Almacenamiento analítico (Oro)** | Redshift Serverless: $0.375/RPU-hora (mínimo 8 RPUs = **$3/hora**) | Synapse SQL: $1.20/DWU-hora (mínimo 100 DWUs = **$120/hora**) | BigQuery: **$5/TB consultado** (storage: $0.020/GB-mes) |
| **Orquestación ETL** | Step Functions: $0.025/1000 transiciones + Lambda ($0.20/millón requests) | Data Factory: **$1/1000 pipeline runs** | Cloud Scheduler: **$0.10/job-mes** (3 jobs gratis) |
| **Transferencia de datos** | $0.09/GB salida internet | $0.087/GB salida internet | **$0.12/GB salida internet** (primeros 1GB/mes gratis) |
| **Modelo de facturación** | Por tiempo de recurso activo | Por unidad de procesamiento-hora | **Por uso real (pay-per-query)** |


##### **Comparación de costos por componente clave**

**Procesamiento Spark (por job de 20 minutos)**

| Proveedor | Configuración | Costo por Job | Costo 2 Jobs/Mes |
|-----------|---------------|---------------|-------------------|
| **AWS EMR** | 2 nodos m5.xlarge | **$0.19** | **$0.38** |
| **Azure Synapse** | 4 vCores Spark Pool | **$0.58** | **$1.16** |
| **GCP Dataproc Serverless** | 4 vCPUs (escalamiento automático) | **$0.075** | **$0.15** |

GCP es 2.5x más barato que AWS y 7.7x más barato que Azure en procesamiento Spark.

**Almacenamiento y consultas analíticas (uso mensual real)**

| Proveedor | Modelo | Costo 25 Queries (150 MB promedio cada una) | Observaciones |
|-----------|--------|----------------------------------------------|---------------|
| **AWS Redshift** | Serverless (factura por RPU-hora) | **$6/mes** (estimado 2h uso esporádico) | Cobra por tiempo de endpoint activo aunque no se use |
| **Azure Synapse SQL** | Serverless Pool | **$0.02/mes** ($5/TB escaneado × 0.00375 TB) | Opción viable y económica |
| **GCP BigQuery** | Pay-per-query | **$0.02/mes** (3.75 GB escaneados) | **Dentro del free tier (1 TB/mes gratis)** = **$0** |

BigQuery es efectivamente GRATIS para este proyecto (3.75 GB << 1 TB límite), mientras AWS Redshift cuesta $6/mes por mantener endpoint.


**Ventaja clave: Frecuencia baja de ejecución**

Con solo **1-2 ejecuciones mensuales**, el impacto de costos es mínimo en las tres plataformas, pero GCP mantiene ventajas estructurales:

| Aspecto | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Costo por ejecución esporádica** | EMR cobra por clúster completo aunque se use 20 min | Synapse cobra por pool aunque se use poco | **Dataproc solo cobra por tiempo real de procesamiento** |
| **Penalización por uso infrecuente** | ⚠️ Redshift mantiene costos base | ✅ Synapse Serverless eficiente | ✅ **BigQuery sin costos fijos** |
| **Sostenibilidad a largo plazo** | ⚠️ Costos permanentes aunque uso sea mínimo | ✅ Modelo viable | ✅ **Gratis indefinidamente dentro de límites** |



### 1.3.4 Ecosistema de Business Intelligence

El ecosistema de BI evalúa la capacidad de cada proveedor para soportar el flujo completo: ingesta de datos, transformación ETL, arquitectura Medallion (Bronce-Plata-Oro), procesamiento PySpark y visualización final en Power BI. Se prioriza integración nativa, simplicidad operativa y compatibilidad con herramientas del proyecto.


| Componente | AWS | Azure | GCP |
|------------|-----|-------|-----|
| **Ingesta/Web Scraping** | Lambda + EventBridge | Azure Functions + Logic Apps | **Cloud Functions + Cloud Scheduler** |
| **Almacenamiento Bronce (raw data)** | S3 (object storage) | ADLS Gen2 (object storage) | **Cloud Storage (object storage)** |
| **Procesamiento ETL (Plata)** | AWS Glue o EMR (PySpark) | Azure Data Factory + Synapse Spark | **Dataproc Serverless (PySpark) + Dataflow** |
| **Almacenamiento analítico (Oro)** | Redshift / Redshift Spectrum | Synapse Analytics (SQL Pools) | **BigQuery (columnar, serverless)** |
| **Orquestación de pipelines** | Step Functions + MWAA (Airflow) | Data Factory + Synapse Pipelines | **Cloud Composer (Airflow administrado) / Cloud Scheduler** |
| **Integración con Power BI** | Conector genérico ODBC/JDBC (requiere configuración) |**Conector nativo certificado** (integración profunda) |*Conector oficial BigQuery y Power BI(DirectQuery) |
| **Notebooks interactivos** | EMR Notebooks / SageMaker | Synapse Notebooks (integrado) | **Vertex AI Workbench / Dataproc Notebooks** |
| **Transformación SQL** | Athena (query S3 directamente) | Synapse SQL Serverless | **BigQuery (SQL estándar, sin infraestructura)** |
| **Visualización nativa** | QuickSight (básica, adicional) | Power BI (ecosistema Microsoft) | Looker / Looker Studio (Data Studio) |


**Requisitos del ecosistema BI para el proyecto**

| Requisito | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Soporte PySpark sin gestión clústeres | ❌ EMR requiere clústeres | ❌ Synapse requiere pools | ✅ **Dataproc Serverless** |
| Arquitectura Medallion | ✅ S3 + EMR/Glue + Redshift/Athena | ✅ ADLS + Synapse Spark + Synapse SQL | ✅ **Cloud Storage + Dataproc + BigQuery** |
| SQL estándar (ANSI compatible) | ⚠️ PostgreSQL-like | ⚠️ T-SQL (Microsoft) | ✅ **ANSI SQL:2011 completo** |
| Notebooks interactivos para desarrollo | ✅ EMR Notebooks / SageMaker | ✅ Synapse Notebooks integrados | ✅ **Vertex AI Workbench / Dataproc Notebooks** |
| Orquestación programada (cron-like) | ⚠️ EventBridge + Step Functions | ⚠️ Data Factory triggers | ✅ **Cloud Scheduler (sintaxis cron nativa)** |
| Costo de infraestructura BI | 🔴 Alto (clústeres + warehouse) | 🟡 Medio (pools + SQL) | ✅ **Bajo (serverless completo)** |

**GCP ofrece el ecosistema BI más eficiente para este proyecto**: combina procesamiento serverless (Dataproc), almacenamiento analítico de alto rendimiento (BigQuery) e integración directa con Power BI, todo con complejidad operativa mínima y costo cero dentro del free tier.



### 1.3.5 Redundancia, resiliencia y continuidad operativa

La redundancia evalúa la capacidad de recuperación ante fallos de hardware o zonas completas, mientras que la resiliencia mide la disponibilidad continua del servicio. Para un proyecto BI bancario, se requiere alta disponibilidad de datos y recuperación ante desastres, aunque con tolerancia a interrupciones breves dado el carácter batch del procesamiento.


**Comparación de arquitectura de disponibilidad**

| Aspecto | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Regiones globales** | **33 regiones** (diciembre 2024) | 60+ regiones | 40+ regiones |
| **Zonas de disponibilidad (AZs)** |**105 AZs** (3+ por región) | 3+ por región (menor cantidad total) | **3+ por región** (Google Global Network) |
| **Regiones en Sudamérica** | 1 (São Paulo, Brasil) | 1 (Brazil South) | **2 (São Paulo + Santiago de Chile)** |
| **Distancia desde Lima** | São Paulo: ~3,150 km | Brazil South: ~3,150 km | **Santiago: ~2,200 km** (30% más cerca) |
| **SLA de almacenamiento** | S3 Standard: 99.99% disponibilidad | ADLS Gen2: 99.9% disponibilidad | Cloud Storage: **99.95% disponibilidad** |
| **SLA de data warehouse** | Redshift: 99.9% (Multi-AZ) | Synapse: 99.9% | BigQuery: **99.99% (automático)** |
| **Replicación entre regiones** | S3 Cross-Region Replication (manual) | ADLS Geo-Redundant Storage (manual) | Cloud Storage Dual/Multi-region (automático) |
| **Backup automático** | Debe configurarse (S3 Versioning) | Debe configurarse (Soft delete) | **Versionamiento automático opcional** |

**Requisitos de continuidad para el proyecto**

| Requisito | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Disponibilidad del warehouse > 99.9% | ✅ Redshift 99.9% | ✅ Synapse 99.9% | ✅ **BigQuery 99.99%** |
| Recuperación de datos históricos (7 días) | ⚠️ Requiere snapshots programados | ⚠️ Requiere backups programados | ✅ **Time Travel incluido (7 días gratis)** |
| Tolerancia a fallos de AZ | ✅ Multi-AZ (configuración) | ✅ Zone-redundant (configuración) | ✅ **Automático en servicios serverless** |
| Backup automático sin configuración | ❌ Requiere configuración | ❌ Requiere configuración | ✅ **BigQuery snapshots automáticos** |
| Re-ejecución automática de jobs fallidos | ⚠️ Configurar en Step Functions | ⚠️ Configurar en Data Factory | ✅ **Retry policy nativo en Dataproc** |

Las tres plataformas ofrecen resiliencia adecuada para el proyecto. **GCP destaca por redundancia automática sin configuración**



### 1.3.6 Capacidades de red y latencia

La latencia de red impacta directamente la velocidad de carga de datos (web scraping → cloud), ejecución de jobs distribuidos (PySpark) y consultas interactivas desde Power BI. Para un proyecto operado desde Lima, Perú, la proximidad geográfica de la región es crítica.

| Aspecto | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Backbone de red** | Internet público + AWS Direct Connect (privado) | Internet público + Azure ExpressRoute (privado) | **Google Global Network privado (100% propio)** |
| **Distancia física desde Lima** | São Paulo: ~3,150 km | Brazil South: ~3,150 km | **Santiago: ~2,200 km** (30% más cerca) |
| **Latencia promedio desde Lima** | us-east-1: ~170 ms<br>sa-east-1: **~85 ms** | eastus: ~175 ms<br>brazilsouth: **~90 ms** | us-central1: ~180 ms<br>**southamerica-west1: ~45 ms** |
| **Ancho de banda entre regiones** | Hasta 100 Gbps (inter-region) | Hasta 100 Gbps (inter-region) | **Petabits/segundo (Google Global Network)** |
| **Peering con ISPs locales** | Peering extenso en Sudamérica | Peering con carriers principales | **Peering directo con > 10,000 ISPs globalmente** |
| **CDN integrado** | Amazon CloudFront | Azure CDN / Front Door | **Google Cloud CDN** (integrado con Global Network) |


**Requisitos de red para el proyecto**

| Requisito | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Latencia < 100 ms desde Lima | ✅ São Paulo ~85 ms | ✅ Brazil South ~90 ms | ✅ **Santiago ~45 ms** |
| Upload rápido de datos scraping | ✅ Aceptable (~15 seg) | ✅ Aceptable (~15 seg) | ✅ **Rápido (~10 seg)** |
| Consultas Power BI responsivas | ✅ ~1.5-2 seg | ✅ ~1.6-2.2 seg | ✅ **~0.8-1.2 seg** |
| Sin costos de ancho de banda inesperados | ✅ Predecible | ✅ Predecible | ✅ **Predecible (menor costo inter-región)** |
| Redundancia de rutas de red | ✅ Múltiples carriers | ✅ Múltiples carriers | ✅ **Google Global Network (más resiliente)** |


**AWS y Azure ofrecen capacidades de red robustas**, pero **la ventaja geográfica de GCP es resaltante**, da más rápida sin costos adicionales.

---

## 1.4 Decisión final

> **“Se seleccionó Google Cloud Platform porque  satisface simultáneamente los requerimientos técnicos, financieros y operativos del proyecto BI Scotiabank. GCP permite mantener la arquitectura Medallion, ejecutar en modo serverless y operar desde la región más cercana al Perú. Además, su free tier facilita el desarrollo académico sin costos.”**

