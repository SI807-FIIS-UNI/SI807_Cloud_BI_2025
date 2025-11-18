# 🧱 Arquitectura BI – Servicios Utilizados y Flujo ETL/DW/Visualización (Versión Actualizada)

## 🔧 Servicios Utilizados y Función en el Flujo BI

### **1. Cloud Scheduler (Orquestación)**

* Programa la ejecución automática del pipeline (por ejemplo, diario o cada hora).
* Dispara Cloud Run Jobs mediante HTTP o Pub/Sub.

### **2. Secret Manager (Gestión de credenciales)**

* Almacena secretos necesarios para scraping (tokens, URLs, claves internas).
* Asegura que Cloud Run y Dataproc accedan a credenciales sin exponerlas en código.

### **3. IAM (Identity and Access Management)**

* Controla qué servicios pueden acceder a Storage, BigQuery y Secrets.
* Aplica el principio de mínimo privilegio para seguridad del pipeline.

---

## 🔵 ETL – Ingesta

### **4. Cloud Run Jobs**

* Ejecuta contenedores serverless encargados del scraping desde:

  * **SBS**
  * **BCRP**
  * **Scotiabank** (nuevo)
* Extrae datos en batch y los guarda en Cloud Storage.

### **5. Cloud Storage (Capa Bronze)**

* Almacena archivos crudos provenientes de las distintas fuentes.
* Define la **capa Bronze** dentro del modelo Medallion.

---

## ⚙️ ETL – Transformación

### **6. Dataproc Serverless (Capa Silver)**

* Procesa y limpia los datos almacenados en la capa Bronze.
* Estandariza formatos, genera tablas estructuradas Silver.
* Corre sin necesidad de clústeres permanentes.

---

## 🟡 DW – Modelado y Capa Gold

### **7. BigQuery**

* Almacena las tablas finales Gold listas para analítica.
* Permite agregar, enriquecer y modelar KPIs.
* Se optimiza mediante particionamiento, clustering y control de costos.

---

## 🟢 Visualización

### **8. Looker / Looker Studio**

* Conectado directamente a BigQuery.
* Construcción de dashboards con métricas clave de SBS, BCRP y Scotiabank.
* Permite compartir insights de manera segura.

---

## 📌 Resumen Final Actualizado

| Fase                        | Servicio             | Función                                          |
| --------------------------- | -------------------- | ------------------------------------------------ |
| **Orquestación**            | Cloud Scheduler      | Ejecuta el pipeline de forma programada          |
| **Seguridad**               | Secret Manager / IAM | Manejo seguro de credenciales + permisos mínimos |
| **Extracción**              | Cloud Run Jobs       | Scraping desde SBS, BCRP y Scotiabank            |
| **Raw (Bronze)**            | Cloud Storage        | Almacena datos crudos                            |
| **Transformación (Silver)** | Dataproc Serverless  | Limpieza y procesamiento Spark                   |
| **Data Warehouse (Gold)**   | BigQuery             | Modelo analítico final                           |
| **Visualización**           | Looker               | Dashboards interactivos                          |

---
