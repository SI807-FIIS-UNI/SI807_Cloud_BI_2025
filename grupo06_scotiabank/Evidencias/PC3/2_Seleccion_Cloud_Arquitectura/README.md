

# 🧱 Arquitectura BI – Servicios Utilizados y Flujo ETL/DW/Visualización

Este documento detalla los servicios cloud utilizados en el pipeline BI para extraer información desde la **SBS**, procesarla mediante un flujo **ETL batch**, almacenarla en un **Data Warehouse** y finalmente visualizarla en un dashboard analítico.

---

## 🔧 Servicios Utilizados y Función en el Flujo BI

### **1. Cloud Run Jobs (ETL – Extracción / Ingesta)**

* Se utiliza para ejecutar periódicamente un contenedor encargado del **web scraping** desde la página de la SBS.
* Corre en modo *serverless*, con escalamiento a cero → ideal para cargas batch.
* Resultado: Archivos HTML/CSV/TXT o datos transformados mínimamente.

### **2. Cloud Storage (ETL – Ingesta / Capa Bronze)**

* Almacena los archivos **raw** provenientes del scraping.
* Representa la **capa Bronze** dentro de la arquitectura Medallion.
* Proporciona versionamiento, bajo costo y disponibilidad.

### **3. Dataproc Serverless (ETL – Transformación / Silver)**

* Ejecuta los procesos de transformación mediante PySpark/Spark.
* Limpia, estandariza y valida la data → **capa Silver**.
* Crea datasets consolidados para análisis.

### **4. BigQuery (Data Warehouse – Capa Gold)**

* Sirve como repositorio analítico y columna vertebral del DW.
* Crea tablas Gold optimizadas para dashboards.
* Ejecuta SQL altamente eficiente con escalamiento automático.

### **5. Looker Studio / Looker (Visualización)**

* Conecta directamente con BigQuery.
* Construye dashboards interactivos con KPIs, tendencias e indicadores finales.
* Utiliza tablas Gold para minimizar costos y latencia de consulta.

---

## 🧬 Fases del Proceso BI (ETL → DW → Visualización)

### **ETL**

* *Extracción*: Cloud Run Jobs obtiene datos de la SBS.
* *Carga RAW*: Cloud Storage almacena los datos iniciales.
* *Transformación*: Dataproc Serverless ejecuta limpieza y enriquecimiento.

### **DW**

* BigQuery almacena y organiza las tablas analíticas Gold.
* Se aplican modelos lógicos, agregaciones y particiones según el caso.

### **Visualización**

* Looker crea dashboards y reportes conectados directamente a BigQuery.

---

## 📌 Resumen Final

| Fase                        | Servicio            | Función                                     |
| --------------------------- | ------------------- | ------------------------------------------- |
| **Extracción**              | Cloud Run Jobs      | Scraping automático desde SBS               |
| **Raw Storage (Bronze)**    | Cloud Storage       | Almacenamiento de datos crudos              |
| **Transformación (Silver)** | Dataproc Serverless | Limpieza, enriquecimiento y estandarización |
| **Data Warehouse (Gold)**   | BigQuery            | Tablas finales optimizadas para BI          |
| **Visualización**           | Looker              | Dashboards para usuarios finales            |

---
