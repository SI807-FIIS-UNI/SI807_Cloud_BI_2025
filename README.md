
# SI807U - Cloud BI 2025
# 📊 Proyecto ETL Retail Analytics - Grupo 09

## 📋 Descripción

Migración de pipeline ETL de **Hadoop/Spark** a **Google Cloud Platform (GCP)** para análisis de datos de ventas retail con arquitectura de tres capas: RAW, CURATED y ANALYTICS.

---

## 🏗️ Arquitectura
```
CSV Files → Cloud Storage → BigQuery (RAW) → Dataproc PySpark → 
BigQuery (CURATED) → BigQuery (OLAP) → Looker Studio
```

---

## 📁 Estructura del Proyecto
```
grupo09_retail_analytics/
├── etl/
│   ├── scripts/
│   │   ├── etl_curated_job.py          # Script PySpark de transformación
│   │   └── cloud_function_trigger.py   # Automatización
│   └── logs/
├── dw/
│   ├── ddl/
│   │   ├── 01_create_dataset.sql
│   │   ├── 02_create_raw_tables.sql
│   │   ├── 03_create_curated_tables.sql
│   │   └── 04_create_analytics_tables.sql
│   └── consultas/
│       ├── 01_populate_cubo_olap.sql
│       ├── 02_validacion_olap_vs_fact.sql
│       └── 03_analisis_olap.sql
└── README.md
```

---

## 🚀 Implementación Rápida

### **1. Configuración Inicial**
```bash
# Crear proyecto y habilitar APIs
gcloud projects create etl-retail-analytics
gcloud services enable compute storage dataproc bigquery

# Crear bucket
gsutil mb -l us-central1 gs://mi-etl-proyecto-2025

# Subir CSVs
gsutil cp *.csv gs://mi-etl-proyecto-2025/raw/[tabla]/
```

### **2. BigQuery: Crear Tablas**
```bash
# Ejecutar DDLs en BigQuery Console en orden:
# 01_create_dataset.sql
# 02_create_raw_tables.sql
# 03_create_curated_tables.sql
# 04_create_analytics_tables.sql
```

### **3. Transformación con Dataproc**
```bash
# Subir script PySpark
gsutil cp etl/scripts/etl_curated_job.py gs://mi-etl-proyecto-2025/scripts/

# Ejecutar job
gcloud dataproc batches submit pyspark \
    --project=etl-retail-analytics \
    --region=us-central1 \
    --batch=etl-curated-job-g9-$(date +%Y%m%d-%H%M%S) \
    --jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.32.2.jar \
    gs://mi-etl-proyecto-2025/scripts/etl_curated_job.py
```

### **4. Poblar Cubo OLAP**
```sql
-- Ejecutar en BigQuery:
-- dw/consultas/01_populate_cubo_olap.sql
```

### **5. Dashboard en Looker Studio**

1. Ir a: https://lookerstudio.google.com
2. Conectar a BigQuery: `dataset_si807_g9.resumen_ventas_analytics`
3. Crear visualizaciones

---

## 📊 Modelo de Datos

### **Capas del Data Warehouse**

| Capa | Descripción | Tablas |
|------|-------------|--------|
| **RAW** | Tablas externas (CSV en GCS) | 6 tablas sin transformar |
| **CURATED** | Datos limpios y tipados | 5 dimensiones + 1 fact table |
| **ANALYTICS** | Cubo OLAP agregado | 1 tabla de resumen |

### **Dimensiones y Métricas**

**Dimensiones:** Año, Mes, Ciudad, Tienda, Categoría, Marca  
**Métricas:** Ventas Netas, Unidades, Tickets

---

## 🔧 Transformaciones Principales

- ✅ Conversión de fechas a tipo DATE
- ✅ Manejo de valores NULL (SKs y campos descriptivos)
- ✅ Estandarización a MAYÚSCULAS
- ✅ Corrección de encoding (AlmacÃ©n → Almacén)
- ✅ Integridad referencial (sk_promocion NULL → -1)

---

## ✅ Validación
```sql
-- Ejecutar validación completa:
-- dw/consultas/02_validacion_olap_vs_fact.sql

-- Resultado esperado: Diferencia = 0 entre Cubo OLAP y Fact Table
```

---

## 📈 Consultas Analíticas

Disponibles en `dw/consultas/03_analisis_olap.sql`:

- Top 10 ciudades, tiendas, categorías, marcas
- Evolución mensual y crecimiento
- Análisis de concentración (Pareto)
- Ticket promedio
- Estacionalidad

---

## 🛠️ Stack Tecnológico

- **Almacenamiento:** Google Cloud Storage
- **Data Warehouse:** Google BigQuery
- **Procesamiento:** Dataproc Serverless (PySpark)
- **Visualización:** Looker Studio
- **Lenguajes:** Python, SQL

---

## 👥 Equipo - Grupo 09

- **Curso:** Inteligencia de Negocios (SI807)
- **Año:** 2025

---

## 📝 Configuración Importante

| Parámetro | Valor |
|-----------|-------|
| **Proyecto GCP** | etl-retail-analytics |
| **Dataset BigQuery** | dataset_si807_g9 |
| **Bucket GCS** | mi-etl-proyecto-2025 |
| **Región** | us-central1 |
| **Encoding CSV** | UTF-8 |
| **Delimitador** | coma (,) |

# 🧠 SI807U – Sistemas de Inteligencia de Negocios (Fase Cloud) – 2025-II

Este repositorio centralizado es el entorno oficial del curso **SI807U – Sistemas de Inteligencia de Negocios** de la Universidad Nacional de Ingeniería, correspondiente al semestre **2025-II**.  
Aquí se desarrollará la **segunda parte del proyecto integrador**, enfocada en el **despliegue de soluciones de Business Intelligence en la nube** utilizando **Google Cloud Platform (GCP)**, **Azure** o **AWS**.

---

## 🎯 Fines del Repositorio

El objetivo principal de este repositorio es **centralizar y estandarizar** el trabajo de todos los grupos del curso en un entorno controlado, reproducible y colaborativo, simulando las prácticas profesionales de un equipo de datos corporativo.

**En este repositorio los estudiantes:**
- Migrarán su sistema BI local a un entorno **Cloud**.  
- Implementarán procesos **ETL automatizados** en servicios nativos de nube (Dataproc, Synapse, Glue, etc.).  
- Desplegarán **Data Warehouses** y modelos multidimensionales.  
- Publicarán **Dashboards analíticos** conectados en tiempo real (Power BI Service, Looker Studio o QuickSight).  
- Documentarán su arquitectura, scripts y bitácora técnica bajo control de versiones.  

---

## 🏗️ Estructura General del Proyecto

```
SI807U_Cloud_BI_2025/
│
├── grupo01_interbank/
├── grupo02_essalud/
├── grupo03_credicorp/
├── grupo04_bbva/
├── grupo05_nettalco/
├── grupo06_scotiabank/
├── grupo07_claro/
├── grupo08_luzdelsur/
├── grupo09_cencosud/
├── grupo10_sutran/
│
├── docs/
│   ├── guia_docente.md
│   ├── rubrica_evaluacion.xlsx
│   ├── plan_cloud.pdf
│
├── CONTRIBUTING.md
└── README.md
```

Cada carpeta de grupo contiene el proyecto completo del equipo (scripts ETL, consultas SQL, dashboards y documentación).

---

## 🧩 Metodología y Flujo de Trabajo

El desarrollo sigue el flujo **GitFlow**, con ramas protegidas para mantener la trazabilidad y control docente.

| Rama | Propósito |
|------|------------|
| `main` | Rama principal, aprobada y mantenida por el docente. |
| `develop` | Integración de cambios validados por los líderes de grupo. |
| `feature/grupoXX-init` | Ramas independientes por grupo de estudiantes. |

Cada grupo trabajará exclusivamente en su rama asignada y generará *Pull Requests* hacia `develop`, que serán revisadas y aprobadas por el docente.

---

## ☁️ Entornos Cloud Soportados

Cada grupo deberá elegir **uno de los tres entornos cloud oficiales**:

| Plataforma | Servicios Clave |
|-------------|----------------|
| **Google Cloud Platform (GCP)** | Cloud Storage, Dataproc, BigQuery, Composer, Looker Studio |
| **Microsoft Azure** | Azure Blob Storage, Data Factory, Synapse Analytics, Power BI Service |
| **Amazon Web Services (AWS)** | S3, Glue, Redshift, Step Functions, QuickSight |

---

## 🧰 Requerimientos Técnicos Mínimos

- Procesamiento ETL con Spark, Glue o Dataflow.  
- Almacenamiento estructurado en DW (BigQuery, Synapse, Redshift).  
- Dashboard analítico conectado al DW.  
- Documentación técnica reproducible (README, bitácora, scripts).  
- Uso correcto de control de versiones Git y buenas prácticas DevOps.

---

## 🧑‍💻 Roles dentro del Proyecto

| Rol | Responsabilidad |
|------|----------------|
| **Docente / Maintainer** | Administra el repositorio, revisa PRs, valida entregas. |
| **Líder de Grupo (Est. 01)** | Gestiona los merges hacia `develop`, coordina el trabajo. |
| **Miembros (Est. 02 y 03)** | Desarrollan tareas ETL, modelado y dashboards en sus ramas. |

---

## 🔒 Estructura de Permisos

- Cada grupo cuenta con un **equipo (Team)** propio dentro del repositorio GitHub `webconceptos/SI807_Cloud_BI_2025`.  
- Cada rama `feature/grupoXX-init` está protegida y solo su equipo puede realizar *push*.  
- Los merges a `main` requieren revisión docente.  

---

## 🧾 Evaluaciones Principales – Fase Cloud

| Hito Académico | Objetivo Principal | Entregables Clave |
|:--|:--|:--|
| **Práctica 3 – Migración y Automatización ETL en la Nube** | Implementar y documentar la migración del proceso ETL al entorno Cloud seleccionado (GCP, Azure o AWS). El grupo deberá demostrar la capacidad de orquestar, transformar y cargar datos en servicios gestionados de nube. | - Scripts PySpark / Dataflow / Glue funcionales<br>- Diagrama de flujo de datos actualizado<br>- Bitácora técnica de ejecución<br>- Documentación del proceso ETL en README.md |
| **Práctica 4 – Implementación del Data Warehouse Cloud** | Diseñar e implementar el **Data Warehouse** completo en la nube con modelo dimensional (Star o Snowflake), garantizando integridad, escalabilidad y seguridad. | - Scripts SQL / DDL de creación de DW<br>- Consultas OLAP y particionamiento<br>- Validación de integración con ETL<br>- Documento técnico: *“Diseño y despliegue del DW Cloud”* |
| **Examen Final – Despliegue Analítico e Integración Total** | Integrar todos los componentes del sistema de inteligencia de negocios en la nube. Presentar dashboards analíticos conectados al DW, demostrando la trazabilidad del flujo de datos desde la ingestión hasta la visualización final. | - Dashboard publicado (Power BI Service / Looker Studio / QuickSight)<br>- Video demostrativo del funcionamiento<br>- Informe técnico final con costos y arquitectura desplegada<br>- Repositorio actualizado y reproducible |

---

### 🧭 Notas Generales

- Cada grupo trabajará exclusivamente en su **rama asignada (`feature/grupoXX-init`)**.  
- Todos los entregables deberán cargarse en carpetas claramente estructuradas dentro del repositorio GitHub.  
- La evaluación prioriza **reproducibilidad, documentación y evidencia de ejecución real**.  
- El **Examen Final** representa la consolidación completa del sistema BI en la nube y su presentación ante el jurado académico.

---

## 🧠 Buenas Prácticas

- Mantener los datos sensibles fuera del repositorio (`.env`, `.gitignore`).  
- Seguir las reglas de contribución descritas en `CONTRIBUTING.md`.  
- Nombrar correctamente las ramas y commits (`feat:`, `fix:`, `docs:`).  
- Generar Pull Requests con descripción clara y evidencia de pruebas.  

---

## 🏁 Créditos

Curso: **SI807U – Sistemas de Inteligencia de Negocios**  
Docente: **Ing. Fernando García** (`@webconceptos`)  
Universidad Nacional de Ingeniería – Facultad de Ingeniería Industrial y de Sistemas  
Semestre: **2025-II**

---

## 🔗 Enlaces Útiles

- 🌐 Repositorio GitHub: [https://github.com/webconceptos/SI807_Cloud_BI_2025](https://github.com/webconceptos/SI807_Cloud_BI_2025)  
- 🧩 Guía de contribución: [CONTRIBUTING.md](./CONTRIBUTING.md)  
- 📊 Evaluación: [`docs/rubrica_evaluacion.xlsx`](./docs/rubrica_evaluacion.xlsx)

