# 3. MATRIZ DE COSTOS Y PROYECCIÓN DE USO  

## 3.1. Metodología de estimación  

**Herramienta utilizada:** Azure Pricing Calculator oficial (https://azure.microsoft.com/en-us/pricing/calculator/)

**Supuestos de uso y volumetría**

1. **Frecuencia de procesamiento**

- Mensual (12 ejecuciones/año).

2. **Volumen de datos**

- CSV Practitioner: 50 MB/mes (600 MB/año).  
- CSV Continuous Integration: 80 MB/mes (960 MB/año).  
- **Total ingesta:** 130 MB/mes ≈ 1.56 GB/año.

3. **Azure Data Lake Storage Gen2**

- Capa Bronze: 5 GB acumulado (CSV crudos históricos).  
- Capa Silver: 8 GB acumulado (archivos Parquet limpios).  
- Capa Gold: 3 GB acumulado (tablas Delta que soportan el modelo estrella).  
- **Total almacenamiento estimado:** 16 GB.

4. **Base de datos gestionada en Azure (PostgreSQL)**

- Servicio: *Azure Database for PostgreSQL* (configuración General Purpose equivalente a 4 vCores).  
- Tamaño de base de datos: 10 GB inicial → 25 GB proyectado a 12 meses.  
- Consultas del backend/dashboard: 50,000 queries/mes.  
- Conexiones concurrentes: ~10 usuarios simultáneos.

5. **Azure Databricks**

- Tipo de clúster: Standard_DS3_v2 (4 vCores, 14 GB RAM).  
- Autoscaling: 2–8 workers (promedio 4 workers en ejecución).  
- Horas de ejecución: 4 horas/mes (limpieza, transformaciones y carga al DW).

6. **Azure Container Apps (backend Flask)**

- Backend expuesto como contenedor (API Flask) desplegado en Azure Container Apps.  
- Consumo equivalente a 1 instancia base con 1–2 vCPU y ~2 GB RAM.  
- Autoscaling: 1–3 réplicas (promedio 1.5 réplicas activas).  
- Usuarios concurrentes en el backend: 20–30 (vía dashboard React).

7. **Azure Static Web Apps (frontend React)**

- Plan: Free.  
- Uso: despliegue del frontend React (SPA) sin costo adicional de infraestructura dentro de los límites del plan gratuito.

8. **Servicios de seguridad, monitoreo y gobierno**

- **Azure Key Vault:** almacén centralizado de secretos.  
- **Azure Monitor + Log Analytics Workspace:** observabilidad unificada (métricas, logs y alertas) de Databricks, Container Apps, base de datos, Static Web Apps, Firewall, etc.  
- **Componentes de red y seguridad:** Virtual Network, Network Security Groups, Private Endpoints, Private DNS Zone, Azure Firewall, Recovery Services Vault y Audit Logs.  
  - En esta estimación se modelan explícitamente los costos de *Log Analytics* y *Key Vault*; el resto de componentes introduce un costo marginal adicional frente a los servicios de cómputo y se considera dentro del margen de error de la proyección.

**Consideraciones especiales**

- **Región:** East US (referencia de precios; regiones con costos competitivos).  
- **Redundancia:** LRS (Locally Redundant Storage) en esta estimación (entorno académico / desarrollo).  
- **Reservas:** no se consideran Reserved Instances en el primer año (modelo pay-as-you-go para validar la volumetría real).  
- **Descuentos:** se asume un descuento corporativo efectivo de aproximadamente 40 % en la base de datos gestionada (similar al efecto de acuerdos de licenciamiento en entornos empresariales), solo con fines estimativos.

---

## 3.2. Costos por servicio  

### 3.2.1. Servicio 1: Azure Data Lake Storage Gen2  

| **Componente**                  | **SKU/Tier**    | **Volumen mensual** | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                              |
|---------------------------------|-----------------|----------------------|--------------------------|------------------------|-------------------------------------------------------------------------------|
| Almacenamiento Hot Tier         | Standard LRS    | 16 GB                | 0.37                     | 4.44                   | Capas Bronze/Silver/Gold con acceso mensual. Ref: ~0.0184 USD/GB/mes × 16 GB |
| Operaciones Lectura (Class 2)   | –               | 10,000 ops/mes       | 0.01                     | 0.12                   | Databricks lee datos en Bronze y Silver (CSV/Parquet).                        |
| Operaciones Escritura (Class 1) | –               | 5,000 ops/mes        | 0.10                     | 1.20                   | Proceso de ingesta y Databricks escriben en Bronze/Silver/Gold.              |
| **Total Data Lake Gen2**        |                 |                      | **0.48**                 | **5.76**               |                                                                               |

**Justificación de dimensionamiento**

- 16 GB son suficientes para almacenar ~12 meses históricos:  
  - Bronze: ~1.56 GB/año (CSV crudos).  
  - Silver: ~3 GB/año (Parquet comprimido).  
  - Gold: ~1 GB/año (Delta).  
- Hot Tier adecuado por el patrón de acceso (lecturas/escrituras mensuales para procesamiento).  
- Operaciones por ciclo de ETL (aprox.):  
  - 1 escritura principal de datos crudos a Bronze.  
  - Varias lecturas/escrituras de Databricks para capas Silver y Gold.

---

### 3.2.2. Servicio 2: Azure Databricks (Premium Tier)  

| **Componente**           | **SKU/Tier**      | **Volumen mensual**     | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                                |
|--------------------------|-------------------|--------------------------|--------------------------|------------------------|----------------------------------------------------------------------------------|
| Databricks Units         | Premium Jobs      | 16 DBU/mes               | 0.90                     | 10.80                  | 4 h de ejecución × 4 DBU/hora. Ref: ~0.15 USD/DBU × 4 DBU × 4 h                  |
| Compute VM (driver)      | Standard_DS3_v2   | 4 horas/mes             | 0.68                     | 8.16                   | Nodo driver activo durante las ejecuciones (∼0.17 USD/h × 4 h).                 |
| Compute VM (workers)     | Standard_DS3_v2   | 16 worker-hours/mes     | 2.72                     | 32.64                  | Autoscaling promedio 4 workers × 4 h (0.17 USD/h × 4 × 4).                      |
| **Total Databricks**     |                   |                          | **4.30**                 | **51.60**              |                                                                                  |

**Justificación de dimensionamiento**

- Standard_DS3_v2 (4 vCores, 14 GB RAM) es suficiente para procesar ~130 MB/mes + histórico sin clústeres grandes.  
- Premium Tier aporta:  
  - RBAC y auditoría avanzados.  
  - Integración con Delta Lake (ACID, optimizaciones de lectura/escritura).  
- 4 horas/mes como estimación conservadora para:  
  - Transformaciones Bronze → Silver.  
  - Transformaciones Silver → Gold.  
  - Preparación/carga hacia la base de datos PostgreSQL.  
- Autoscaling 2–8 workers (promedio 4) equilibra rendimiento y costo.

---

### 3.2.3. Servicio 3: Base de datos gestionada en Azure (Azure Database for PostgreSQL – General Purpose)  

| **Componente**                 | **SKU/Tier**                      | **Volumen mensual**          | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                                 |
|--------------------------------|-----------------------------------|------------------------------|--------------------------|------------------------|-----------------------------------------------------------------------------------|
| Compute (vCore)                | General Purpose, 4 vCores         | 730 horas/mes (24/7)         | 423.60                   | 5,083.20               | 4 vCores suficientes para ~50,000 queries/mes de backend/dashboard.              |
| Storage                        | Premium SSD                       | 25 GB                        | 6.25                     | 75.00                  | 10 GB inicial → 25 GB a 12 meses (modelo estrella + índices).                    |
| Backup Storage (LRS)           | Backups automatizados             | 25 GB                        | 2.50                     | 30.00                  | Retención típica 35 días.                                                         |
| **Subtotal antes de descuento**|                                   |                              | **432.35**               | **5,188.20**           |                                                                                   |
| Descuento corporativo (≈40 %)  | –                                 | –                            | **–172.94**              | **–2,075.28**          | Descuento efectivo similar a acuerdos de licenciamiento en entornos banca.       |
| **Total base de datos**        |                                   |                              | **259.41**               | **3,112.92**           |                                                                                   |

**Justificación de dimensionamiento**

- **4 vCores General Purpose:**  
  - Balance adecuado para una carga analítica moderada (≈50,000 consultas/mes ≈ 69 consultas/hora promedio).  
  - Permite cierto crecimiento sin cambiar de tier inmediatamente.  
- **25 GB de almacenamiento:**  
  - Incluye crecimiento del modelo dimensional (hechos, dimensiones, índices) a ~12 meses.  
- **Descuento corporativo ~40 %:**  
  - Representa un escenario realista de negociación de precios/licenciamiento en organizaciones grandes.  
- Servicios como Azure Synapse SQL Pool se descartan en esta fase por costo base más alto y por estar sobredimensionados para <100 GB y concurrencia limitada.

---

### 3.2.4. Servicio 4: Azure Container Apps (backend Flask)  

| **Componente**                      | **SKU/Tier**            | **Volumen mensual**           | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                                 |
|-------------------------------------|-------------------------|-------------------------------|--------------------------|------------------------|-----------------------------------------------------------------------------------|
| Cómputo base (réplica 1)            | Consumo equivalente     | 730 horas/mes (24/7)          | 69.35                    | 832.20                 | Consumo aproximado equivalente a 1 instancia pequeña (∼1–2 vCPU, 2 GB RAM).      |
| Autoscaling (réplicas extra)        | Consumo equivalente     | 365 horas/mes adicionales     | 34.68                    | 416.10                 | Promedio 1.5 réplicas (1 base + 0.5 extra en picos de uso).                      |
| HTTPS y gestión de certificados     | Incluido                | –                             | 0.00                     | 0.00                   | Certificados TLS gestionados por la plataforma.                                  |
| **Total Container Apps**            |                         |                               | **104.03**               | **1,248.30**           |                                                                                   |

**Justificación de dimensionamiento**

- Se aproxima el costo al de un plan Standard S1 de App Service para una carga similar (backend Flask de tamaño moderado).  
- Permite autoscaling horizontal sin gestionar VMs, alineado con la arquitectura de contenedores.  
- Los 20–30 usuarios concurrentes previstos se consideran una carga ligera-moderada.

---

### 3.2.5. Servicio 5: Azure Static Web Apps (frontend React)  

| **Componente**         | **SKU/Tier** | **Volumen mensual**        | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                            |
|------------------------|--------------|-----------------------------|--------------------------|------------------------|------------------------------------------------------------------------------|
| Static Web Apps Plan   | Free         | Dentro de límites del plan | 0.00                     | 0.00                   | Hosting de la SPA React dentro de los límites del plan gratuito.            |

**Justificación de dimensionamiento**

- Para un escenario académico/prototipo, el plan **Free** es suficiente:  
  - Soporta despliegue de la SPA React.  
  - Incluye HTTPS y CI/CD básico.  
- La carga principal recae en el backend (Container Apps) y la base de datos, no en Static Web Apps.

---

### 3.2.6. Servicio 6: Azure Key Vault  

| **Componente**        | **SKU/Tier**    | **Volumen mensual** | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                                  |
|-----------------------|-----------------|----------------------|--------------------------|------------------------|------------------------------------------------------------------------------------|
| Secret Operations     | Standard Tier   | 10,000 ops/mes       | 0.03                     | 0.36                   | Backend y Databricks leen secretos varias veces al día.                            |
| Secrets Storage       | Standard Tier   | 5 secretos           | 0.00                     | 0.00                   | Primeros 10,000 secretos sin costo adicional.                                      |
| **Total Key Vault**   |                 |                      | **0.03**                 | **0.36**               |                                                                                    |

**Justificación de dimensionamiento**

- 10,000 operaciones/mes:  
  - Estimación conservadora (~300 accesos/día × 30 días ≈ 9,000 ops).  
- 5 secretos (ejemplos):  
  - Cadena de conexión a PostgreSQL.  
  - Credenciales de Storage Account.  
  - Secretos de acceso a Databricks.  
  - Credenciales de Service Principal, etc.

---

### 3.2.7. Servicio 7: Azure Monitor + Log Analytics Workspace  

| **Componente**              | **SKU/Tier**     | **Volumen mensual** | **Costo mensual (USD)** | **Costo anual (USD)** | **Justificación**                                                                  |
|-----------------------------|------------------|----------------------|--------------------------|------------------------|------------------------------------------------------------------------------------|
| Log Analytics Ingestion     | Pay-as-you-go    | 5 GB logs/mes        | 11.50                    | 138.00                 | Logs de Databricks, Container Apps, DB, Static Web Apps, Firewall, etc.           |
| Log Analytics Retention     | 90 días          | 5 GB almacenados     | 0.50                     | 6.00                   | Días 1–31 gratis; días 32–90 con costo (~0.10 USD/GB).                             |
| Alertas (Action Groups)     | Standard Tier    | 10 alertas/mes       | 0.20                     | 2.40                   | Alertas por fallos, alta latencia o consumo anómalo.                               |
| **Total Azure Monitor**     |                  |                      | **12.20**                | **146.40**             |                                                                                    |

**Justificación de dimensionamiento**

- 5 GB de logs/mes estimados:  
  - Databricks: ~2 GB (logs de notebooks/jobs).  
  - Azure Container Apps: ~1.5 GB (requests, errores).  
  - Base de datos PostgreSQL gestionada: ~0.5 GB.  
  - Static Web Apps, Firewall y otros componentes: ~1 GB.  
- Retención 90 días:  
  - Compromiso entre requisitos de auditoría/diagnóstico y costo.  
- 10 alertas/mes:  
  - Fallos de ejecución críticos.  
  - Latencia elevada en la API.  
  - Uso de CPU/memoria anómalo.  
  - Costos acercándose a un presupuesto definido.

---

## 3.3. Costo total estimado  

### 3.3.1. Desglose por servicio  

| **Servicio Azure**                                      | **Costo mensual (USD)** | **Costo anual (USD)** | **% del total aprox.** |
|---------------------------------------------------------|--------------------------|------------------------|------------------------|
| Base de datos gestionada (Azure Database for PostgreSQL) | 259.41                   | 3,112.92               | 68.2 %                 |
| Azure Container Apps (backend Flask)                   | 104.03                   | 1,248.30               | 27.3 %                 |
| Azure Monitor + Log Analytics                          | 12.20                    | 146.40                 | 3.2 %                  |
| Azure Databricks                                       | 4.30                     | 51.60                  | 1.1 %                  |
| Azure Data Lake Storage Gen2                           | 0.48                     | 5.76                   | 0.1 %                  |
| Azure Key Vault                                        | 0.03                     | 0.36                   | <0.1 %                 |
| Azure Static Web Apps                                  | 0.00                     | 0.00                   | 0.0 %                  |
| **TOTAL MENSUAL**                                      | **380.45**               |                        | **100 %**              |
| **TOTAL ANUAL**                                        |                          | **4,565.40**           |                        |

---

### 3.3.2. Desglose por categoría  

> Separando el costo de la base de datos en cómputo y almacenamiento/backups tras aplicar el descuento.

| **Categoría**                                                     | **Costo mensual (USD)** | **Costo anual (USD)** | **% del total aprox.** |
|-------------------------------------------------------------------|--------------------------|------------------------|------------------------|
| **Cómputo** (Databricks + Azure Container Apps + cómputo DB)      | 362.49                   | 4,349.88               | 95.3 %                 |
| **Almacenamiento** (Data Lake + almacenamiento/backups de la DB)  | 5.73                     | 68.76                  | 1.5 %                  |
| **Servicios gestionados** (Key Vault + Azure Monitor/Log Analytics) | 12.23                   | 146.76                 | 3.2 %                  |
| **TOTAL**                                                         | **380.45**               | **4,565.40**           | **100 %**              |

> Nota: para simplificar, el costo total de la base de datos se ha desagregado internamente entre cómputo y almacenamiento/backups, aunque Azure lo factura como un único servicio gestionado.

---

### 3.3.3. Observaciones clave  

1. **La base de datos gestionada en Azure es el principal driver de costos**, representando alrededor del **68 %** del costo mensual total.  
   - Esto se justifica por:  
     - Alta disponibilidad (SLA gestionado).  
     - Backups automáticos y capacidad de restauración.  
     - Capacidad suficiente para manejar ~50,000 queries/mes del backend/dashboard.

2. **El descuento corporativo (~40 %) aporta un ahorro aproximado de 2,075 USD/año** sobre la base de datos gestionada.  
   - Sin este descuento, el costo anual de la base de datos pasaría de **3,112.92 USD** a ~**5,188.20 USD**, elevando el TCO del entorno en torno a un 45 %.

3. **El almacenamiento es extremadamente económico**, representando cerca del **1.5 %** del costo total anual (~**68.76 USD/año**):  
   - Incluye Data Lake Gen2 (capas Bronze, Silver, Gold).  
   - Incluye almacenamiento y backups de la base de datos PostgreSQL gestionada.

4. **Los servicios gestionados de seguridad y observabilidad (Key Vault + Azure Monitor/Log Analytics)** suponen alrededor del **3.2 %** del costo total:  
   - Aportan seguridad centralizada de secretos (Key Vault).  
   - Monitoreo, logging y alertas unificadas (Azure Monitor + Log Analytics).  
   - Permiten incorporar también logs de red y seguridad (Firewall, NSG, Private Endpoints, Audit Logs) en el mismo workspace.

5. **No se incurre en costos adicionales de BI cloud** (como Power BI Service):  
   - La visualización se realiza exclusivamente mediante el frontend React en Azure Static Web Apps (plan Free) consumiendo la API en Azure Container Apps.  
   - Esto mantiene el costo de BI cloud en **0 USD**, a cambio de concentrar la lógica de presentación y reporting dentro de la propia aplicación web.
