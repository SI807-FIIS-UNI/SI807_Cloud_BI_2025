
## 🧱 Arquitectura General

### 1. **Ingesta (Batch + Web Scraping)**

* **Cloud Run Jobs** ejecuta periódicamente un contenedor con el scraper.
* Recupera archivos CSV desde la web de la SBS.
* Guarda los archivos en **Cloud Storage (bucket Bronze)**.

### 2. **Procesamiento Medallion**

* **Bronze:** Archivos raw (sin procesar), almacenados tal cual vienen.
* **Silver:** Transformaciones estructurales y limpieza usando
  **Dataproc Serverless para Spark**.
* **Gold:** Tablas analíticas y agregaciones finales cargadas en **BigQuery**.

### 3. **Analytics & Visualización**

* El dashboard se construye sobre **BigQuery Standard Edition**, utilizando vistas y modelos optimizados para consulta.

---

## 🧬 Metodología Medallion: Justificación

| Capa       | Propósito                                           | Justificación                                                                                |
| ---------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Bronze** | Guardar datos crudos, íntegros y auditables.        | Mantiene trazabilidad del scraping, útil por si la SBS cambia estructura o aparecen errores. |
| **Silver** | Limpieza, tipificación, estandarización.            | Reduce errores, facilita queries y prepara el dataset para reporting.                        |
| **Gold**   | Métricas listas para negocio, agregaciones y joins. | Minimiza costo de BigQuery al optimizar estructuras para dashboards.                         |

---

## 🧰 Servicios Utilizados y Justificación Técnica

### 🟦 **Cloud Run Jobs**

**Rol:** ejecuta el scraper en modo batch, con CPU y memoria asignados bajo demanda.

**Por qué usarlo:**

* Serverless y escalamiento a 0 → costo mínimo.
* Ideal para workloads batch con contenedores.
* No requiere VMs ni mantenimiento.
* Permite scheduling con Cloud Scheduler.

**Costos del estimate:**

| Concepto    | Cantidad | Precio (USD) |
| ----------- | -------- | ------------ |
| Jobs CPU    | 1460     | **1.02**     |
| Jobs Memory | 730      | **0.056**    |

Total Cloud Run → **≈ 1.08 USD/mes**

---

### 🟩 **Dataproc Serverless for Spark**

**Rol:** realizar ETL/ELT sobre datos masivos del scraping.

**Por qué usarlo:**

* Solo se paga por uso (DCUs).
* No es necesario mantener clústeres.
* Compatible con PySpark para limpiar y transformar datos.

**Costo estimate:**

* DCU-hours (milli): **13.87 USD**

> Aunque se ejecuta en **us-central1**, se justifica por ser más económico para cargas batch no sensibles a latencia.

---

### 🟨 **Cloud Storage**

**Rol:** almacenamiento para las capas Bronze y Silver + staging.

**Por qué usarlo:**

* Económico.
* Integración nativa con Dataproc y BigQuery.
* Versionamiento y seguridad integradas.

**Costos del estimate:**

| Concepto                         | Precio (USD) |
| -------------------------------- | ------------ |
| Standard Storage US Multi-Region | 24.21        |
| Network Transfer (replicación)   | 0.04 + 0.04  |

Total Storage → **≈ 24.3 USD/mes**

---

### 🟥 **BigQuery Standard Edition**

**Rol:** servir como data warehouse y base del dashboard.

**Por qué usarlo:**

* Serverless, altamente escalable.
* Optimiza costos mediante storage logical/physical.
* Permite SQL estándar y vistas materializadas.

**Costos del estimate:**

| Concepto                   | Precio (USD) |
| -------------------------- | ------------ |
| Standard Edition           | 416.1        |
| Active Logical Storage     | 30.30        |
| Long-term Logical Storage  | 21.08        |
| Active Physical Storage    | 55.27        |
| Long-term Physical Storage | 27.63        |
| Storage API (read/write)   | 0            |

Total BigQuery → **≈ 550.4 USD/mes**

> BigQuery es el componente más costoso, pero es indispensable para consultas rápidas del dashboard y escalabilidad.

---

## 🧮 Costo Total Estimado

| Servicio             | Costo Mensual (USD)  |
| -------------------- | -------------------- |
| Cloud Run Jobs       | 1.08                 |
| Dataproc Serverless  | 13.87                |
| Cloud Storage        | 24.30                |
| **BigQuery**         | **550.4**            |
| **Total Aproximado** | **589.64 USD / mes** |

---

## 📊 Flujo Completo del Proceso

1. **Cloud Scheduler** activa un **Cloud Run Job**.
2. El job realiza **web scraping** a la SBS.
3. Archivos descargados se guardan en **GCS Bronze**.
4. Un Batch job de **Dataproc Serverless** transforma los datos → Silver.
5. Se genera tabla Gold procesada.
6. Los datos Gold se cargan a **BigQuery**.
7. Dashboard lee datos optimizados de BigQuery.

---

## ⭐ Beneficios de la Arquitectura

* **Serverless end-to-end:** cero mantenimiento de infraestructura.
* **Escalable:** soporta nuevos orígenes SBS sin reestructurar.
* **Bajo costo de ingesta:** menos de USD 2 por scraping mensual.
* **Procesamiento eficiente:** Dataproc cobra por segundo.
* **Analítica empresarial:** BigQuery garantiza performance para dashboards.

---

## 🔗 Enlace al Estimado de Costos

```
https://cloud.google.com/calculator?dl=CjhDaVF4T1RZd05HWTNPQzFpWW1FNExUUTVNRFF0WWpGaU9DMDBabVpoWmprMk5tSmxOekFRQVE9PRokNjYxNEVERTMtQTJGOC00RDk5LUJEMTktNDNERjA2MzdCQ0ZB
```
---

