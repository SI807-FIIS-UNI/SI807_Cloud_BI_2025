# 🏗️ ARQUITECTURA AWS DATA LAKE - ANÁLISIS DETALLADO

---

## 📋 TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Vista General de la Arquitectura](#vista-general)
3. [Servicios AWS Utilizados](#servicios-aws)
4. [Capa de Almacenamiento (S3 Data Lake)](#capa-almacenamiento)
5. [Capa de Procesamiento (AWS Glue)](#capa-procesamiento)
6. [Capa de Datos y Catálogo](#capa-catalogo)
7. [Capa de Análitica (DW/DataMart)](#capa-analitica)
8. [Capa de Visualización (BI)](#capa-visualizacion)
9. [Capa de Operación y Monitoreo](#capa-operacion)
10. [Flujo de Datos Completo](#flujo-datos)
11. [Dependencias entre Servicios](#dependencias)
12. [Traslado de Información](#traslado-informacion)
13. [Arquitectura Medallion (Bronze, Silver, Gold)](#arquitectura-medallion)
14. [Seguridad y Permisos](#seguridad)
15. [Conclusiones](#conclusiones)

---

## <a name="resumen-ejecutivo"></a>1. RESUMEN EJECUTIVO

La arquitectura analizada representa un **Data Lake moderno** implementado en AWS que sigue el patrón **Medallion Architecture** (Bronze → Silver → Gold) para transformar datos crudos en información analítica procesable.

### Características Principales:

✅ **Arquitectura Serverless:** Uso de servicios gestionados (S3, Glue, Redshift Serverless, Athena)  
✅ **Escalabilidad Automática:** Capacidad de procesar desde KB hasta TB de datos  
✅ **Costo Optimizado:** Pago por uso, sin infraestructura permanente  
✅ **Automatización:** Programación batch con EventBridge  
✅ **Observabilidad:** Monitoreo completo con CloudWatch  
✅ **Flexibilidad:** Múltiples opciones de consumo (Power BI, QuickSight, SQL)

---

## <a name="vista-general"></a>2. VISTA GENERAL DE LA ARQUITECTURA

La arquitectura se organiza en **4 capas lógicas principales**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DATA LAKE AWS                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OPERACIÓN     │    │   PROCESAMIENTO │    │  ALMACENAMIENTO │
│                 │    │                 │    │                 │
│ • EventBridge   │───▶│ • AWS Glue      │───▶│ • Amazon S3     │
│ • CloudWatch    │    │ • Glue Catalog  │    │ • Capas:        │
│ • AWS Lambda    │    │ • Athena        │    │   - Bronze      │
│ • IAM           │    │                 │    │   - Silver      │
└─────────────────┘    └─────────────────┘    │   - Gold        │
                                               └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐                          ┌─────────────────┐
│  VISUALIZACIÓN  │                          │   DATA WAREHOUSE│
│                 │◀─────────────────────────│                 │
│ • Power BI      │                          │ • Redshift      │
│ • QuickSight    │                          │ • Esquema STAR  │
└─────────────────┘                          └─────────────────┘
```

---

## <a name="servicios-aws"></a>3. SERVICIOS AWS UTILIZADOS

### 3.1 Resumen de Servicios por Categoría

| **Categoría** | **Servicio AWS** | **Propósito** | **Tipo de Uso** |
|---------------|------------------|---------------|-----------------|
| **Almacenamiento** | Amazon S3 | Data Lake principal | Core |
| **Procesamiento ETL** | AWS Glue (Jobs) | Transformación de datos PySpark | Core |
| **Catálogo de Datos** | AWS Glue (Data Catalog) | Metadatos de tablas | Core |
| **Crawling** | AWS Glue (Crawlers) | Descubrimiento automático de esquemas | Core |
| **Consultas Ad-hoc** | Amazon Athena | SQL sobre S3 sin servidor | Secundario |
| **Data Warehouse** | Amazon Redshift Serverless | DW para BI | Core |
| **Orquestación** | Amazon EventBridge | Programación de jobs batch | Core |
| **Monitoreo** | Amazon CloudWatch | Logs, métricas y alarmas | Core |
| **Validaciones Ligeras** | AWS Lambda | Triggers y validaciones | Secundario |
| **Seguridad** | AWS IAM | Autenticación y autorización | Core |
| **Visualización** | Power BI + QuickSight | Dashboards y reportes | Consumo |

### 3.2 Bucket S3 Principal

**Nombre:** `si807-cloud-bi-grupo08`

**Estructura:**
```
s3://si807-cloud-bi-grupo08/
├── bronze/        # Datos crudos particionados por periodo_yyyymm
├── silver/        # Datos limpios en Parquet tipado + validaciones (VEE)
└── gold/          # Datos listos para DW/BI en Parquet optimizado
```

---

## <a name="capa-almacenamiento"></a>4. CAPA DE ALMACENAMIENTO (S3 DATA LAKE)

### 4.1 Amazon S3 como Data Lake

Amazon S3 actúa como el **repositorio central** de todos los datos en sus diferentes estados de transformación.

#### 4.1.1 Capa BRONZE (Raw Data)

**Ubicación:** `s3://si807-cloud-bi-grupo08/bronze/`

**Características:**
- **Formato:** CSV particionado
- **Particionamiento:** Por `periodo_yyyymm` (ej. `periodo_yyyymm=202501/`)
- **Estado:** Datos crudos, mínimo procesamiento
- **Esquema:** Sin validación estricta
- **Propósito:** Conservar datos originales para auditoría y reprocesamiento

**Ejemplo de ruta:**
```
s3://si807-cloud-bi-grupo08/bronze/
├── cliente/
│   ├── periodo_yyyymm=202401/
│   │   └── data.csv
│   └── periodo_yyyymm=202402/
│       └── data.csv
├── suministro/
├── medidor/
├── tarifa/
├── asignacion_tarifa/
└── consolidado_mensual/
```

**Crawler asociado:** `Glue crawler (raw)`

#### 4.1.2 Capa SILVER (Clean Data)

**Ubicación:** `s3://si807-cloud-bi-grupo08/silver/`

**Características:**
- **Formato:** Parquet tipado
- **Validación:** VEE (Validation, Enrichment, Enhancement)
  - ✅ Tipos de datos correctos
  - ✅ Valores nulos controlados
  - ✅ Datos enriquecidos con transformaciones
- **Compresión:** Snappy (balance velocidad/tamaño)
- **Propósito:** Datos limpios y confiables para análisis

**Transformaciones aplicadas (Bronze → Silver):**

1. **Tipado de datos:**
   ```python
   # Ejemplo de transformación
   STRING → DATE
   STRING → DECIMAL
   STRING → INTEGER
   ```

2. **Limpieza de valores:**
   - Eliminación de espacios en blanco
   - Reemplazo de valores vacíos por NULL
   - Normalización de formatos de fecha

3. **Validación de calidad:**
   ```python
   # AWS Glue Data Quality
   Rules = [
       ColumnCount > 0,
       IsComplete "id_cliente",
       IsUnique "id_cliente"
   ]
   ```

**Crawler asociado:** `Glue crawler (silver)`

#### 4.1.3 Capa GOLD (Analytics-Ready Data)

**Ubicación:** `s3://si807-cloud-bi-grupo08/gold/`

**Características:**
- **Formato:** Parquet optimizado para BI
- **Esquema:** Desnormalizado (modelo dimensional)
- **Particionamiento:** Optimizado para consultas frecuentes
- **Propósito:** Datos listos para carga en Data Warehouse

**Ejemplo de transformaciones (Silver → Gold):**

```python
# Agregaciones
consumo_mensual = df.groupBy("id_cliente", "mes").agg(
    sum("consumo_kwh").alias("total_consumo"),
    avg("tarifa").alias("tarifa_promedio")
)

# Joins para desnormalizar
fact_consumo = (
    consumo
    .join(cliente, "id_cliente")
    .join(tarifa, "id_tarifa")
    .join(suministro, "id_suministro")
)
```

**Crawler asociado:** `Glue crawler (gold)`

---

## <a name="capa-procesamiento"></a>5. CAPA DE PROCESAMIENTO (AWS GLUE)

### 5.1 AWS Glue Jobs (PySpark)

AWS Glue ejecuta las transformaciones ETL usando **Apache Spark** gestionado.

#### 5.1.1 Glue Job 1 (Bronze → Silver)

**Nombre (ejemplo):** `bronze_cliente`

**Función:**
- Lee CSV desde capa Bronze
- Aplica transformaciones de limpieza
- Escribe Parquet en capa Silver
- Actualiza Glue Data Catalog

**Código (fragmento):**
```python
# Leer desde Bronze
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="lds_raw",
    table_name="cliente"
)

# Transformar
mapped = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("id_cliente", "string", "id_cliente", "int"),
        ("nombre", "string", "nombre", "string"),
        ("fecha_registro", "string", "fecha_registro", "date")
    ]
)

# Validar calidad
quality_rules = """
    Rules = [
        ColumnCount > 0,
        IsComplete "id_cliente"
    ]
"""

# Escribir a Silver
glueContext.write_dynamic_frame.from_options(
    frame=mapped,
    connection_type="s3",
    connection_options={"path": "s3://bucket/silver/cliente/"},
    format="parquet"
)
```

**Configuración típica:**
- **Worker type:** G.1X (4 vCPU, 16 GB RAM)
- **Number of workers:** 2-3
- **Glue version:** 4.0
- **Timeout:** 60 minutos

#### 5.1.2 Glue Job 2 (Silver → Gold)

**Nombre (ejemplo):** `gold_fact_consumo`

**Función:**
- Lee Parquet desde Silver
- Aplica agregaciones y joins
- Crea modelo dimensional
- Escribe Parquet en Gold

**Transformaciones complejas:**
```python
# Ejemplo: Job bronze_consolidado con función custom
class MyTransform(GlueTransform):
    def __call__(self, frame):
        # Limpieza de valores numéricos vacíos
        df = frame.toDF()
        numeric_cols = ["consumo_kwh", "monto", "tarifa"]
        
        for col in numeric_cols:
            df = df.withColumn(
                col,
                when(trim(col(col)) == "", None)
                .otherwise(col(col).cast("decimal"))
            )
        
        return DynamicFrame.fromDF(df, glueContext, "transformed")
```

### 5.2 AWS Glue Crawlers

Los crawlers **descubren automáticamente** el esquema de los datos en S3 y crean/actualizan tablas en Glue Data Catalog.

#### 5.2.1 Crawler Configuration

| **Crawler** | **Ruta S3** | **Base de Datos** | **Frecuencia** | **Particionamiento** |
|-------------|-------------|-------------------|----------------|----------------------|
| `Glue crawler (raw)` | `s3://.../bronze/` | `lds_raw` | On-demand / Scheduled | Por `periodo_yyyymm` |
| `Glue crawler (silver)` | `s3://.../silver/` | `lds_bronze` | Post-job | Ninguno |
| `Glue crawler (gold)` | `s3://.../gold/` | `lds_gold` | Post-job | Ninguno |

**Configuración típica:**
```json
{
  "Name": "lds_craw_final",
  "Role": "AWSGlueServiceRole",
  "DatabaseName": "lds_raw",
  "Targets": {
    "S3Targets": [
      {"Path": "s3://si807-cloud-bi-grupo08/bronze/"}
    ]
  },
  "SchemaChangePolicy": {
    "UpdateBehavior": "UPDATE_IN_DATABASE",
    "DeleteBehavior": "LOG"
  }
}
```

---

## <a name="capa-catalogo"></a>6. CAPA DE DATOS Y CATÁLOGO

### 6.1 AWS Glue Data Catalog

El **Data Catalog** es el **metastore centralizado** que almacena información sobre tablas, columnas, tipos de datos y particiones.

#### 6.1.1 Bases de Datos en el Catálogo

| **Base de Datos** | **Capa** | **Número de Tablas** | **Propósito** |
|-------------------|----------|----------------------|---------------|
| `lds_raw` | Bronze | ~7 | Tablas de datos crudos |
| `lds_bronze` | Silver | ~7 | Tablas limpias (nombre confuso, debería ser `lds_silver`) |
| `lds_gold` | Gold | ~5 | Tablas analíticas (facts + dims) |

#### 6.1.2 Ejemplo de Tabla en el Catálogo

**Tabla:** `lds_raw.cliente`

```json
{
  "Name": "cliente",
  "DatabaseName": "lds_raw",
  "StorageDescriptor": {
    "Columns": [
      {"Name": "id_cliente", "Type": "string"},
      {"Name": "nombre", "Type": "string"},
      {"Name": "direccion", "Type": "string"},
      {"Name": "fecha_registro", "Type": "string"}
    ],
    "Location": "s3://si807-cloud-bi-grupo08/bronze/cliente/",
    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
    "SerdeInfo": {
      "SerializationLibrary": "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
      "Parameters": {"field.delim": ","}
    }
  },
  "PartitionKeys": [
    {"Name": "periodo_yyyymm", "Type": "string"}
  ]
}
```

### 6.2 Amazon Athena

**Propósito:** SQL ad-hoc / QA sobre S3

Amazon Athena permite ejecutar consultas SQL directamente sobre los datos en S3 **sin necesidad de cargarlos** en una base de datos.

#### 6.2.1 Casos de Uso

1. **Exploración de datos:**
   ```sql
   SELECT * FROM lds_raw.cliente
   WHERE periodo_yyyymm = '202501'
   LIMIT 10;
   ```

2. **Validación de calidad:**
   ```sql
   SELECT 
       periodo_yyyymm,
       COUNT(*) as total_registros,
       COUNT(DISTINCT id_cliente) as clientes_unicos,
       SUM(CASE WHEN id_cliente IS NULL THEN 1 ELSE 0 END) as nulls
   FROM lds_raw.cliente
   GROUP BY periodo_yyyymm;
   ```

3. **Análisis rápido:**
   ```sql
   SELECT 
       t.nombre_tarifa,
       SUM(c.consumo_kwh) as total_consumo
   FROM lds_bronze.consolidado_mensual c
   JOIN lds_bronze.tarifa t ON c.id_tarifa = t.id_tarifa
   GROUP BY t.nombre_tarifa;
   ```

#### 6.2.2 Integración con Glue Catalog

Athena lee las definiciones de tablas desde **Glue Data Catalog**:

```
User Query → Athena → Glue Data Catalog (metadatos) → S3 (datos)
```

**Ventajas:**
- ✅ Sin infraestructura que gestionar
- ✅ Pago solo por datos escaneados
- ✅ Consultas en segundos
- ✅ Compatible con formatos: CSV, Parquet, ORC, JSON

**Desventajas:**
- ❌ No optimizado para consultas frecuentes (usar Redshift para eso)
- ❌ Puede ser costoso si se escanean muchos datos repetidamente

---

## <a name="capa-analitica"></a>7. CAPA DE ANALÍTICA (DW/DATAMART)

### 7.1 Amazon Redshift Serverless

**Propósito:** Data Warehouse / DataMart

Redshift es el **motor de datos estructurados** para análisis de BI de alto rendimiento.

#### 7.1.1 Características del Redshift Serverless

| **Aspecto** | **Detalle** |
|-------------|-------------|
| **Modelo de facturación** | Pago por segundo de uso (RPU - Redshift Processing Units) |
| **Capacidad** | Auto-escalado según carga |
| **Concurrencia** | Soporta múltiples usuarios simultáneos |
| **Optimizaciones** | Columnar storage, compresión, zone maps |
| **Integración S3** | Comando `COPY` para carga masiva desde S3 |

#### 7.1.2 Carga de Datos desde S3 (Gold → Redshift)

**Proceso:**

```sql
-- Comando COPY para cargar desde Gold
COPY public.fact_consumo
FROM 's3://si807-cloud-bi-grupo08/gold/fact_consumo/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3ReadRole'
FORMAT AS PARQUET;
```

**Flujo:**
```
S3 Gold Layer → COPY command → Redshift Table
```

**Características del COPY:**
- ✅ Carga paralela (múltiples workers)
- ✅ Compresión automática
- ✅ Manejo de errores con logs
- ✅ Upsert (MERGE) disponible

#### 7.1.3 Esquema STAR en Redshift

La arquitectura implementa un **esquema dimensional tipo STAR**:

```
                  ┌─────────────────┐
                  │  dim_cliente    │
                  │  - id_cliente   │
                  │  - nombre       │
                  │  - direccion    │
                  └────────┬────────┘
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼────────┐   ┌──────▼────────┐   ┌──────▼────────┐
│ dim_tarifa    │   │ FACT_CONSUMO  │   │ dim_periodo   │
│ - id_tarifa   │◀──│ - id_cliente  │──▶│ - id_periodo  │
│ - nombre      │   │ - id_tarifa   │   │ - mes         │
│ - precio      │   │ - id_periodo  │   │ - anio        │
└───────────────┘   │ - consumo_kwh │   └───────────────┘
                    │ - monto       │
                    └───────────────┘
```

**Ejemplo de tablas:**

```sql
-- Tabla de hechos
CREATE TABLE fact_consumo (
    id_consumo BIGINT IDENTITY(1,1),
    id_cliente INT,
    id_tarifa INT,
    id_periodo INT,
    consumo_kwh DECIMAL(10,2),
    monto DECIMAL(10,2),
    fecha_consumo DATE,
    PRIMARY KEY (id_consumo)
)
DISTKEY (id_cliente)
SORTKEY (fecha_consumo);

-- Dimensión cliente
CREATE TABLE dim_cliente (
    id_cliente INT,
    nombre VARCHAR(200),
    direccion VARCHAR(500),
    tipo_cliente VARCHAR(50),
    PRIMARY KEY (id_cliente)
)
DISTSTYLE ALL;
```

**Optimizaciones aplicadas:**
- **DISTKEY:** Distribuye datos por `id_cliente` para optimizar JOINs
- **SORTKEY:** Ordena por `fecha_consumo` para filtros temporales rápidos
- **DISTSTYLE ALL:** Replica dimensiones pequeñas en todos los nodos

---

## <a name="capa-visualizacion"></a>8. CAPA DE VISUALIZACIÓN (BI)

### 8.1 Power BI (Principal)

**Conector:** Power BI Redshift Connector

Power BI se conecta directamente a Redshift Serverless para consultas en tiempo real.

#### 8.1.1 Configuración de Conexión

```
Power BI Desktop
    ↓ [Redshift ODBC Driver]
Redshift Serverless Endpoint
    ↓ [SQL Queries]
Esquema STAR (fact_consumo + dims)
```

**Ventajas de Power BI:**
- ✅ Conexión DirectQuery (datos siempre actualizados)
- ✅ Modo Import para dashboards estáticos (más rápido)
- ✅ Transformaciones adicionales en Power Query
- ✅ Compartir dashboards en Power BI Service

#### 8.1.2 Ejemplo de Consulta desde Power BI

```sql
SELECT 
    dc.nombre as cliente,
    dp.mes,
    dp.anio,
    SUM(fc.consumo_kwh) as total_consumo,
    SUM(fc.monto) as total_facturado
FROM fact_consumo fc
JOIN dim_cliente dc ON fc.id_cliente = dc.id_cliente
JOIN dim_periodo dp ON fc.id_periodo = dp.id_periodo
WHERE dp.anio = 2025
GROUP BY dc.nombre, dp.mes, dp.anio;
```

### 8.2 Amazon QuickSight (Opcional)

**Propósito:** Alternativa nativa de AWS para BI

QuickSight puede conectarse a:
- ✅ Redshift Serverless
- ✅ Athena (para consultas ad-hoc sobre S3)
- ✅ S3 directamente (modo SPICE)

**Ventajas de QuickSight:**
- ✅ Integración nativa con servicios AWS
- ✅ Sin infraestructura (100% cloud)
- ✅ Pago por sesión de usuario
- ✅ ML Insights automáticos

**Desventajas:**
- ❌ Menos flexible que Power BI
- ❌ Menos conocido por usuarios de negocio

---

## <a name="capa-operacion"></a>9. CAPA DE OPERACIÓN Y MONITOREO

### 9.1 Amazon EventBridge

**Propósito:** Programación batch / Orquestación

EventBridge **dispara automáticamente** los jobs de Glue según un horario definido.

#### 9.1.1 Configuración de Regla

```json
{
  "Name": "daily-bronze-jobs",
  "ScheduleExpression": "cron(0 2 * * ? *)",
  "State": "ENABLED",
  "Targets": [
    {
      "Arn": "arn:aws:glue:sa-east-1:123456789012:job/bronze_cliente",
      "RoleArn": "arn:aws:iam::123456789012:role/EventBridgeGlueRole",
      "Id": "1"
    },
    {
      "Arn": "arn:aws:glue:sa-east-1:123456789012:job/bronze_suministro",
      "RoleArn": "arn:aws:iam::123456789012:role/EventBridgeGlueRole",
      "Id": "2"
    }
  ]
}
```

**Flujo:**
```
EventBridge Rule (2 AM diario)
    ↓
Dispara Glue Job (bronze_cliente)
    ↓
Job procesa datos Bronze → Silver
    ↓
Crawler actualiza catálogo
    ↓
EventBridge dispara siguiente job (silver → gold)
```

### 9.2 Amazon CloudWatch

**Propósito:** Logs / Métricas / Alarmas

CloudWatch monitorea **todos los servicios** de la arquitectura.

#### 9.2.1 Log Groups

| **Log Group** | **Fuente** | **Contenido** |
|---------------|------------|---------------|
| `/aws-glue/jobs/logs-v2` | Glue Jobs | Stdout de ejecuciones |
| `/aws-glue/jobs/error` | Glue Jobs | Errores y stacktraces |
| `/aws-glue/jobs/output` | Glue Jobs | Salida de print statements |
| `/aws/lambda/validation-function` | Lambda | Logs de validaciones |

#### 9.2.2 Métricas de Glue Observability

CloudWatch recibe **548+ métricas** automáticamente:

| **Categoría** | **Métricas Clave** | **Propósito** |
|---------------|-------------------|---------------|
| **error** | `glue.error.ALL`, `glue.succeed.ALL` | Detectar fallos |
| **job_performance** | `glue.driver.skewness.job` | Optimizar balanceo |
| **resource_utilization** | `glue.driver.memory.heap.used.percentage` | Prevenir OOM |

#### 9.2.3 Alarmas Configuradas

**Ejemplo: Alarma de errores**

```json
{
  "AlarmName": "CRITICAL-GlueJobErrors-AllJobs",
  "MetricName": "glue.error.ALL",
  "Namespace": "AWS/Glue",
  "Statistic": "Sum",
  "Period": 300,
  "EvaluationPeriods": 1,
  "Threshold": 1,
  "ComparisonOperator": "GreaterThanOrEqualToThreshold",
  "TreatMissingData": "notBreaching"
}
```

**Acciones cuando se dispara:**
1. Enviar notificación a SNS (email/SMS)
2. Disparar Lambda para remediation automática
3. Log en CloudWatch para auditoría

### 9.3 AWS Lambda

**Propósito:** Triggers / Validaciones ligeras

Lambda ejecuta **funciones ligeras** en respuesta a eventos.

#### 9.3.1 Casos de Uso

1. **Validación pre-procesamiento:**
   ```python
   def lambda_handler(event, context):
       # Validar que archivo S3 tenga tamaño mínimo
       bucket = event['Records'][0]['s3']['bucket']['name']
       key = event['Records'][0]['s3']['object']['key']
       
       size = get_object_size(bucket, key)
       if size < 100:  # Menos de 100 bytes
           raise ValueError("Archivo muy pequeño")
       
       # Disparar Glue Job
       glue.start_job_run(JobName='bronze_cliente')
   ```

2. **Notificación de completitud:**
   ```python
   def lambda_handler(event, context):
       # Al completar job, notificar por SNS
       job_name = event['detail']['jobName']
       status = event['detail']['state']
       
       sns.publish(
           TopicArn='arn:aws:sns:sa-east-1:123456789012:glue-jobs',
           Subject=f'Job {job_name} - {status}',
           Message=f'El job {job_name} terminó con estado: {status}'
       )
   ```

### 9.4 AWS IAM

**Propósito:** Usuarios / Grupos / Roles

IAM controla **quién puede hacer qué** en toda la arquitectura.

#### 9.4.1 Roles Principales

| **Rol** | **Servicio** | **Permisos** |
|---------|--------------|--------------|
| `AWSGlueServiceRole` | Glue Jobs | S3, Glue Catalog, CloudWatch Logs |
| `RedshiftS3ReadRole` | Redshift | S3 (read-only en bucket específico) |
| `LambdaExecutionRole` | Lambda | CloudWatch Logs, Glue (start_job_run), SNS |
| `EventBridgeGlueRole` | EventBridge | Glue (start_job_run) |

#### 9.4.2 Ejemplo de Política IAM para Glue

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::si807-cloud-bi-grupo08/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:CreateTable",
        "glue:UpdateTable"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

## <a name="flujo-datos"></a>10. FLUJO DE DATOS COMPLETO

### 10.1 Flujo End-to-End

```
┌──────────────────────────────────────────────────────────────────┐
│                    FLUJO DE DATOS COMPLETO                        │
└──────────────────────────────────────────────────────────────────┘

1. INGESTA
   ┌─────────────────┐
   │ Datos Crudos    │ (CSV, JSON, etc.)
   │ (origen externo)│
   └────────┬────────┘
            │ Upload manual o automatizado
            ▼
   ┌─────────────────┐
   │ S3 Bronze       │ CSV particionado por periodo_yyyymm
   └────────┬────────┘
            │
            ▼
2. DESCUBRIMIENTO
   ┌─────────────────┐
   │ Glue Crawler    │ Escanea S3, infiere esquema
   │ (raw)           │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Glue Data       │ Tabla: lds_raw.cliente
   │ Catalog         │
   └────────┬────────┘
            │
            ▼
3. TRANSFORMACIÓN (Bronze → Silver)
   ┌─────────────────┐
   │ EventBridge     │ Dispara job a las 2 AM
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Glue Job 1      │ Lee: lds_raw.cliente
   │ (PySpark)       │ Transforma: Tipado, limpieza, VEE
   │ bronze_cliente  │ Escribe: s3://.../silver/cliente/
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ S3 Silver       │ Parquet tipado + validado
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Glue Crawler    │ Actualiza esquema
   │ (silver)        │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Glue Data       │ Tabla: lds_bronze.bronze_cliente
   │ Catalog         │
   └────────┬────────┘
            │
            ▼
4. AGREGACIÓN (Silver → Gold)
   ┌─────────────────┐
   │ Glue Job 2      │ Lee múltiples tablas de Silver
   │ (PySpark)       │ Aplica: JOINs, agregaciones, modelo STAR
   │ gold_fact       │ Escribe: s3://.../gold/fact_consumo/
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ S3 Gold         │ Parquet desnormalizado, optimizado para BI
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Glue Crawler    │ Actualiza esquema
   │ (gold)          │
   └────────┬────────┘
            │
            ▼
5. CARGA AL DW
   ┌─────────────────┐
   │ Redshift COPY   │ COPY FROM s3://.../gold/...
   │ Command         │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Redshift        │ Tablas: fact_consumo, dim_cliente, etc.
   │ Serverless      │ Esquema: STAR
   └────────┬────────┘
            │
            ▼
6. VISUALIZACIÓN
   ┌─────────────────┐
   │ Power BI        │ SELECT ... FROM fact_consumo ...
   │ / QuickSight    │ Dashboard → Usuarios de negocio
   └─────────────────┘

MONITOREO CONTINUO (en paralelo):
   ┌─────────────────┐
   │ CloudWatch      │ Logs, métricas, alarmas
   │ + Lambda        │ Validaciones y notificaciones
   └─────────────────┘
```

### 10.2 Cronología de Ejecución Típica

**Ejemplo: Procesamiento diario a las 2 AM**

| **Hora** | **Acción** | **Servicio** | **Duración** |
|----------|------------|--------------|--------------|
| 02:00 | EventBridge dispara jobs | EventBridge | Instantáneo |
| 02:00 | Inicio de `bronze_cliente` | Glue Job | ~3 min |
| 02:00 | Inicio de `bronze_suministro` (paralelo) | Glue Job | ~4 min |
| 02:03 | Fin de `bronze_cliente`, escribe a Silver | S3 | Instantáneo |
| 02:03 | Crawler silver ejecuta | Glue Crawler | ~1 min |
| 02:04 | Catálogo actualizado | Glue Catalog | Instantáneo |
| 02:04 | Inicio de `gold_fact_consumo` | Glue Job | ~5 min |
| 02:09 | Fin de `gold_fact_consumo`, escribe a Gold | S3 | Instantáneo |
| 02:09 | Crawler gold ejecuta | Glue Crawler | ~1 min |
| 02:10 | Inicio de COPY a Redshift | Redshift | ~2 min |
| 02:12 | Datos disponibles en Redshift | Redshift | - |
| 02:12 | Actualización automática de dashboard Power BI | Power BI | Instantáneo |

**Duración total:** ~12 minutos

---

## <a name="dependencias"></a>11. DEPENDENCIAS ENTRE SERVICIOS

### 11.1 Grafo de Dependencias

```
                    ┌──────────────┐
                    │ Amazon S3    │
                    │ (Data Lake)  │
                    └──────┬───────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼─────┐  ┌──────▼──────┐ ┌─────▼────────┐
    │ Glue       │  │ Glue        │ │ Athena       │
    │ Crawler    │  │ Jobs        │ │ (lectura)    │
    └──────┬─────┘  └──────┬──────┘ └──────────────┘
           │               │
           └───────┬───────┘
                   │
            ┌──────▼──────┐
            │ Glue Data   │
            │ Catalog     │
            └──────┬──────┘
                   │
           ┌───────┼───────┐
           │               │
    ┌──────▼─────┐  ┌──────▼──────┐
    │ Athena     │  │ Redshift    │
    │ (consulta) │  │ (COPY)      │
    └────────────┘  └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Power BI /  │
                    │ QuickSight  │
                    └─────────────┘

ORQUESTACIÓN Y MONITOREO:
    ┌────────────┐      ┌────────────┐
    │EventBridge │─────▶│ Glue Jobs  │
    └────────────┘      └──────┬─────┘
                               │
                        ┌──────▼──────┐
                        │ CloudWatch  │
                        │ (logs/      │
                        │  metrics)   │
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │ Lambda      │
                        │ (triggers)  │
                        └─────────────┘

SEGURIDAD (todo depende de):
    ┌────────────┐
    │ AWS IAM    │
    │ (permisos) │
    └────────────┘
```

### 11.2 Matriz de Dependencias

| **Servicio** | **Depende de** | **Tipo de Dependencia** |
|--------------|----------------|-------------------------|
| S3 | Ninguno | Capa base |
| Glue Crawler | S3, IAM | Lee S3, escribe a Catalog |
| Glue Data Catalog | Glue Crawler | Recibe metadatos |
| Glue Jobs | S3, Glue Catalog, IAM, CloudWatch | Lee/escribe S3, consulta Catalog |
| Athena | S3, Glue Catalog, IAM | Lee metadatos + datos |
| Redshift | S3, Glue Catalog, IAM | COPY desde S3 |
| EventBridge | Glue Jobs, IAM | Dispara jobs |
| CloudWatch | Glue Jobs, Lambda | Recibe logs y métricas |
| Lambda | S3 (events), Glue, SNS, IAM | Responde a eventos |
| Power BI | Redshift | Consulta SQL |
| QuickSight | Redshift, Athena, S3 | Consulta múltiples fuentes |

---

## <a name="traslado-informacion"></a>12. TRASLADO DE INFORMACIÓN

### 12.1 Protocolos y Mecanismos de Transferencia

#### 12.1.1 S3 ↔ Glue Jobs

**Protocolo:** S3 API (HTTPS)

**Mecanismo:**
```python
# Lectura desde S3
datasource = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://bucket/bronze/cliente/"]},
    format="csv"
)

# Escritura a S3
glueContext.write_dynamic_frame.from_options(
    frame=transformed,
    connection_type="s3",
    connection_options={"path": "s3://bucket/silver/cliente/"},
    format="parquet"
)
```

**Características:**
- ✅ Transferencia paralela (múltiples workers)
- ✅ Compresión automática
- ✅ Cifrado en tránsito (TLS) y en reposo (S3-SSE)

#### 12.1.2 S3 → Redshift (COPY)

**Protocolo:** S3 API + Redshift COPY

**Mecanismo:**
```sql
COPY public.fact_consumo
FROM 's3://bucket/gold/fact_consumo/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftS3ReadRole'
FORMAT AS PARQUET
COMPUPDATE ON
STATUPDATE ON;
```

**Optimizaciones:**
- **Paralelización:** Redshift divide archivos entre nodos
- **Compresión:** Lee Parquet comprimido directamente
- **Cifrado:** Usa KMS para datos sensibles

#### 12.1.3 Redshift ↔ Power BI

**Protocolo:** JDBC/ODBC sobre TLS

**Mecanismo:**
```
Power BI → ODBC Driver → Redshift Endpoint (puerto 5439) → Query → Result Set
```

**Modos de conexión:**
1. **DirectQuery:** Cada visual ejecuta query en Redshift
2. **Import:** Carga snapshot de datos en memoria de Power BI

#### 12.1.4 EventBridge → Glue

**Protocolo:** AWS SDK (boto3) / API Gateway

**Mecanismo:**
```json
{
  "Target": {
    "Arn": "arn:aws:glue:sa-east-1:123456789012:job/bronze_cliente",
    "RoleArn": "arn:aws:iam::123456789012:role/EventBridgeGlueRole",
    "Input": "{\"Arguments\": {\"--periodo\": \"202501\"}}"
  }
}
```

**Flujo:**
```
EventBridge Rule → AWS API (start_job_run) → Glue Control Plane → Spark Cluster Launch
```

#### 12.1.5 Glue → CloudWatch

**Protocolo:** CloudWatch Logs API

**Mecanismo:**
```python
# Logging desde Glue Job
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Iniciando procesamiento...")
logger.error("Error al leer archivo: %s", error_msg)
```

**Envío automático:**
- Glue captura stdout/stderr
- Envía logs en batch a CloudWatch Logs
- Publica métricas cada 1 minuto

### 12.2 Volúmenes de Datos Estimados

| **Transferencia** | **Frecuencia** | **Volumen Típico** | **Tiempo Estimado** |
|-------------------|----------------|-------------------|---------------------|
| Ingesta → S3 Bronze | Diaria | 100 MB - 1 GB | Segundos - Minutos |
| S3 Bronze → Glue → S3 Silver | Diaria | 100 MB → 50 MB (Parquet) | 2-5 minutos |
| S3 Silver → Glue → S3 Gold | Diaria | 50 MB → 30 MB (agregado) | 3-7 minutos |
| S3 Gold → Redshift | Diaria | 30 MB | 1-2 minutos |
| Redshift → Power BI | On-demand | 1-10 MB (result set) | Segundos |

---

## <a name="arquitectura-medallion"></a>13. ARQUITECTURA MEDALLION (BRONZE, SILVER, GOLD)

### 13.1 Principios de la Arquitectura Medallion

La arquitectura **Medallion** (o **Multi-Hop**) organiza el Data Lake en capas de **calidad creciente**:

```
RAW DATA → BRONZE (crudo) → SILVER (limpio) → GOLD (analítico)
```

**Beneficios:**
- ✅ **Auditoría:** Bronze preserva datos originales
- ✅ **Reprocesamiento:** Puedes regenerar Silver/Gold desde Bronze
- ✅ **Separación de responsabilidades:** Ingeniería (Silver) vs Analítica (Gold)
- ✅ **Optimización progresiva:** Cada capa está más optimizada

### 13.2 Comparación Detallada de Capas

| **Aspecto** | **BRONZE** | **SILVER** | **GOLD** |
|-------------|------------|------------|----------|
| **Formato** | CSV (original) | Parquet tipado | Parquet optimizado |
| **Esquema** | Sin validar | Validado y tipado | Desnormalizado (STAR) |
| **Calidad** | Sin garantías | VEE aplicado | Business-ready |
| **Particionamiento** | Por periodo | Por entidad | Por dimensión analítica |
| **Compresión** | Ninguna | Snappy | Snappy + columnas optimizadas |
| **Tamaño relativo** | 100% | ~50% (por Parquet) | ~30% (por agregación) |
| **Usuarios** | Ingenieros (reproceso) | Científicos de datos | Analistas de negocio |
| **Latencia de consulta** | Alta (CSV) | Media (Parquet) | Baja (DW-ready) |

### 13.3 Transformaciones por Capa

#### 13.3.1 Bronze → Silver

**Transformaciones:**
1. **Conversión de formato:** CSV → Parquet
2. **Tipado de datos:** STRING → INT/DATE/DECIMAL
3. **Limpieza de valores:**
   - Trim de espacios
   - Reemplazo de blancos por NULL
   - Normalización de fechas
4. **Validación de calidad (VEE):**
   - Columnas requeridas presentes
   - Sin duplicados en claves primarias
   - Valores dentro de rangos esperados

**Código ejemplo:**
```python
# Mapeo de tipos
mapped = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("id_cliente", "string", "id_cliente", "int"),
        ("consumo_kwh", "string", "consumo_kwh", "decimal(10,2)"),
        ("fecha", "string", "fecha", "date")
    ]
)

# Validación
rules = """
    Rules = [
        ColumnCount > 0,
        IsComplete "id_cliente",
        IsUnique "id_cliente",
        ColumnValues "consumo_kwh" >= 0
    ]
"""
```

#### 13.3.2 Silver → Gold

**Transformaciones:**
1. **Joins entre entidades:**
   ```python
   fact_consumo = (
       consumo_silver
       .join(cliente_silver, "id_cliente")
       .join(tarifa_silver, "id_tarifa")
       .join(medidor_silver, "id_medidor")
   )
   ```

2. **Agregaciones:**
   ```python
   consumo_mensual = fact_consumo.groupBy(
       "id_cliente", "anio", "mes"
   ).agg(
       sum("consumo_kwh").alias("total_consumo"),
       avg("monto").alias("monto_promedio"),
       count("*").alias("numero_mediciones")
   )
   ```

3. **Desnormalización (STAR schema):**
   - Crear tabla de hechos con FK a dimensiones
   - Duplicar atributos dimensionales en hechos cuando mejora rendimiento

4. **Cálculos de negocio:**
   ```python
   df = df.withColumn(
       "tarifa_efectiva",
       col("monto") / col("consumo_kwh")
   )
   ```

---

## <a name="seguridad"></a>14. SEGURIDAD Y PERMISOS

### 14.1 Principios de Seguridad

La arquitectura implementa **seguridad en profundidad** (defense in depth):

```
Usuario/Servicio
    ↓ [IAM Authentication]
IAM Role/User
    ↓ [IAM Authorization]
Servicio AWS
    ↓ [Resource Policy]
Recurso (S3 bucket, Redshift table)
    ↓ [Encryption]
Datos (en tránsito y en reposo)
```

### 14.2 IAM Roles y Políticas

#### 14.2.1 Rol: AWSGlueServiceRole

**Usado por:** Glue Jobs

**Permisos:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::si807-cloud-bi-grupo08",
        "arn:aws:s3:::si807-cloud-bi-grupo08/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetPartitions",
        "glue:CreateTable",
        "glue:UpdateTable",
        "glue:CreatePartition"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:sa-east-1:*:log-group:/aws-glue/*"
    }
  ]
}
```

#### 14.2.2 Rol: RedshiftS3ReadRole

**Usado por:** Redshift Serverless

**Permisos:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::si807-cloud-bi-grupo08/gold/*"
      ]
    }
  ]
}
```

**Nota:** Este rol tiene acceso **solo a la capa Gold**, no a Bronze ni Silver (principio de mínimo privilegio).

### 14.3 Cifrado de Datos

#### 14.3.1 Cifrado en Reposo

| **Servicio** | **Mecanismo** | **Clave** |
|--------------|---------------|-----------|
| S3 | SSE-S3 o SSE-KMS | AWS-managed o KMS Customer Key |
| Glue Data Catalog | Cifrado automático | AWS-managed |
| Redshift | Cifrado de cluster | AWS-managed o KMS Customer Key |
| CloudWatch Logs | Cifrado automático | AWS-managed |

#### 14.3.2 Cifrado en Tránsito

**Todos los servicios usan TLS 1.2+:**
- S3 API: HTTPS obligatorio
- Redshift: SSL/TLS para conexiones JDBC/ODBC
- Glue: Comunicación interna cifrada
- EventBridge/Lambda: AWS PrivateLink (no sale de red AWS)

### 14.4 Segregación de Acceso

#### 14.4.1 Usuarios IAM

| **Usuario/Grupo** | **Acceso** | **Propósito** |
|-------------------|------------|---------------|
| `DataEngineers` | S3 (Bronze, Silver, Gold), Glue, Athena | Desarrollo de pipelines |
| `DataAnalysts` | Athena (read-only), QuickSight | Análisis ad-hoc |
| `BIUsers` | Redshift (read-only via Power BI) | Consumo de dashboards |
| `Administrators` | Todos los servicios | Gestión de infraestructura |

#### 14.4.2 Redshift Database Roles

```sql
-- Rol de solo lectura para usuarios de BI
CREATE ROLE bi_readonly;
GRANT USAGE ON SCHEMA public TO bi_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi_readonly;

-- Usuario de Power BI
CREATE USER powerbi_user PASSWORD 'secure_password';
GRANT bi_readonly TO powerbi_user;
```

---

## <a name="conclusiones"></a>15. CONCLUSIONES

### 15.1 Fortalezas de la Arquitectura

✅ **Escalabilidad:** Arquitectura serverless escala automáticamente desde GB hasta PB  
✅ **Costo-eficiencia:** Pago por uso, sin infraestructura ociosa  
✅ **Resiliencia:** Arquitectura Medallion permite reprocesamiento sin pérdida de datos  
✅ **Observabilidad:** Monitoreo completo con CloudWatch (548+ métricas)  
✅ **Separación de responsabilidades:** Cada capa tiene propósito y usuarios definidos  
✅ **Flexibilidad de consumo:** Múltiples opciones (Athena, Redshift, Power BI, QuickSight)  
✅ **Automatización:** EventBridge orquesta jobs sin intervención manual  
✅ **Seguridad:** IAM, cifrado, segregación de acceso

### 15.2 Áreas de Mejora Potenciales

⚠️ **Gestión de errores:** Implementar retry logic y dead letter queues  
⚠️ **Versionado de datos:** Agregar versionado en S3 para auditoría histórica  
⚠️ **Data Quality:** Expandir reglas de DQ más allá de validaciones básicas  
⚠️ **Linaje de datos:** Implementar herramienta como AWS Data Catalog Lineage  
⚠️ **CI/CD:** Automatizar despliegue de jobs con CloudFormation/Terraform  
⚠️ **Gobernanza:** Implementar AWS Lake Formation para permisos granulares  
⚠️ **Costos:** Implementar alertas de presupuesto y optimización de consultas

### 15.3 Recomendaciones

1. **Implementar SNS:** Conectar alarmas de CloudWatch a SNS para notificaciones por email
2. **Dashboard de monitoreo:** Crear dashboard centralizado en CloudWatch
3. **Optimizar particionamiento:** Revisar estrategia de particiones en capas Silver/Gold
4. **Políticas de retención:** Definir lifecycle policies para eliminar datos antiguos de Bronze
5. **Disaster Recovery:** Implementar S3 Cross-Region Replication para capa Gold
6. **Testing:** Agregar Glue Job unit tests con moto/localstack

### 15.4 Métricas de Éxito

| **Métrica** | **Objetivo** | **Estado Actual** |
|-------------|------------|-------------------|
| **Disponibilidad del pipeline** | >99% | Pendiente medir |
| **Latencia de datos** | <1 hora desde ingesta | ~15 minutos |
| **Costo mensual** | <$200 | ~$150 estimado |
| **Errores en jobs** | <1% | 0% (solo alarmas) |
| **Usuarios activos en dashboards** | >50 | Pendiente medir |
| **Cobertura de monitoreo** | 100% de jobs críticos | 100% (11 alarmas) |

### 15.5 Reflexión Final

Esta arquitectura representa un **Data Lake moderno y bien diseñado** que balancea:
- **Simplicidad:** Servicios gestionados eliminan complejidad operacional
- **Flexibilidad:** Múltiples opciones de consumo según necesidades
- **Costo:** Arquitectura serverless optimiza gastos
- **Calidad:** Arquitectura Medallion garantiza datos confiables

El proyecto está listo para escalar desde el entorno actual (desarrollo/prueba) hacia **producción enterprise** con ajustes menores en gobernanza y monitoreo.


