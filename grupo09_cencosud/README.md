# grupo09_cencosud - Parte individual
Proyecto Cloud BI 2025-II

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

---

## 🐛 Troubleshooting

### Error: "Permission denied"
```bash
PROJECT_NUMBER=$(gcloud projects describe etl-retail-analytics --format="value(projectNumber)")
gsutil iam ch serviceAccount:service-${PROJECT_NUMBER}@dataproc-accounts.iam.gserviceaccount.com:objectAdmin gs://mi-etl-proyecto-2025
```

### Error: "Totales no coinciden"
```sql
-- Verificar duplicados:
SELECT COUNT(*) - COUNT(DISTINCT CONCAT(anio, nombre_mes, ciudad, nombre_tienda, categoria, marca)) 
FROM dataset_si807_g9.resumen_ventas_analytics;
-- Si > 0, ejecutar: TRUNCATE TABLE y volver a poblar
```

---

## 📚 Recursos

- [Documentación BigQuery](https://cloud.google.com/bigquery/docs)
- [Documentación Dataproc](https://cloud.google.com/dataproc/docs)
- [Documentación Looker Studio](https://support.google.com/looker-studio)

---

## ✅ Checklist de Implementación
```
□ Proyecto GCP creado y configurado
□ CSVs subidos a Cloud Storage
□ Dataset y tablas creadas en BigQuery
□ Job de Dataproc ejecutado exitosamente
□ Cubo OLAP poblado
□ Validación: totales coinciden (diferencia = 0)
□ Dashboard en Looker Studio conectado
```

---

**🎯 Status:** Proyecto completado | **📅 Última actualización:** 2025
