# 1. Arquitectura avanzada en la nube (Azure)

## 1.1. Objetivo de la sección

La arquitectura en Azure despliega un **flujo completo de Business Intelligence** para medir los niveles de madurez *Practitioner* y *Continuous Integration (CI)* a partir de archivos CSV generados por el **Marco Playbook**.

La solución cloud mantiene la lógica funcional de la arquitectura on-premise (ETL en Spark + modelo estrella + dashboard web), pero la mejora en:

- Escalabilidad y elasticidad (autoscaling de cómputo y servicios gestionados).
- Alta disponibilidad y recuperación ante desastres.
- Seguridad, redes privadas y gobierno de datos.
- Observabilidad centralizada (métricas, logs y alertas).

---

## 1.2. Diagrama general de la arquitectura

<img width="7871" height="5438" alt="image" src="https://github.com/user-attachments/assets/f82f0dd9-aeed-430c-bd96-cbc458eba43b" />

El siguiente diagrama de arquitectura muestra lo siguiente:

- **Sources**: archivos CSV del Marco Playbook.
- **Process / Backend**: interfaz de carga, Databricks y base de datos PostgreSQL gestionada.
- **Store**: Data Lake con capas Bronze, Silver y Gold.
- **Serve**: backend en Azure App Service y frontend en Azure Static Web Apps.
- **Servicios transversales**: VNet, Private Endpoints, NSG, Azure Firewall, Key Vault, Azure Monitor, Log Analytics, Private DNS Zone, Recovery Services Vault y Audit Logs.

---

## 1.3. Capas funcionales de la solución

La arquitectura se organiza en capas lógicas, siguiendo el flujo de datos de extremo a extremo.

### 1.3.1. Fuentes de datos (Sources)

- **Origen principal**: archivos CSV exportados manualmente desde el **Marco Playbook**.
- Cada mes se cargan dos archivos:
  - CSV Practitioner.
  - CSV Continuous Integration.

<img width="1025" height="355" alt="image" src="https://github.com/user-attachments/assets/1e893de6-96be-4b71-8cd2-cbb40404a3bc" />

---

### 1.3.2. Capa de proceso (Backend)

Componentes principales:

- **Interfaz de carga**  
  Formulario web que permite al *Service Owner* subir los CSV al entorno cloud.

- **Azure Databricks**  
  Ejecuta los notebooks PySpark que realizan:
  - Limpieza y validación de datos.
  - Estandarización de tipos y formatos.
  - Cálculo de KPIs de Practitioner y CI.
  - Generación de las tablas finales para el modelo estrella.

- **PostgreSQL gestionado en Azure**  
  Base de datos analítica donde se implementa el **modelo dimensional tipo estrella** (tablas de hechos y dimensiones) que será consumido por el dashboard y por futuros casos de uso.

---

### 1.3.3. Capa de almacenamiento (Store)

La solución utiliza un **Data Lake en Azure** con una arquitectura tipo **Medallion**:

- **Capa Bronze (raw)**  
  Almacena los CSV tal como llegan desde el Marco Playbook, sin transformar.  
  Es la “fuente de la verdad” histórica.

- **Capa Silver (trusted)**  
  Contiene los datos limpios y tipificados en formato optimizado (por ejemplo, Parquet).  
  Aquí ya se han aplicado reglas de calidad (nulos, duplicados, tipos).

- **Capa Gold (refined)**  
  Concentra los datos agregados y listos para consumo analítico y carga al modelo estrella en PostgreSQL.

---

### 1.3.4. Capa de presentación (Serve)

- **Azure App Service (backend Flask)**  
  Expone una API REST que consulta el modelo estrella y sirve los KPIs y métricas necesarios para el dashboard.

- **Azure Static Web Apps (frontend React)**  
  Hospeda una Single Page Application (SPA) desarrollada en React que:
  - Consume las APIs del backend.
  - Muestra tablas, gráficos y KPIs de madurez Practitioner/CI.
  - Actúa como “visor BI” personalizado, en lugar de utilizar un servicio de BI cloud externo (Power BI, Looker, etc.).

<img width="1859" height="941" alt="image" src="https://github.com/user-attachments/assets/58be1ae5-45d8-46df-af34-dd24ff763961" />

---

## 1.4. Servicios Azure utilizados

La siguiente tabla resume los servicios clave de la arquitectura:

| Capa / Dominio          | Servicio Azure                            | Rol principal en la solución                                         |
|-------------------------|-------------------------------------------|---------------------------------------------------------------------|
| Red y seguridad         | **Virtual Network (VNet)**                | Red privada que aísla los recursos de la solución.                  |
|                         | **Subredes + Network Security Groups**    | Segmentación de servicios (datos, backend, seguridad) y filtrado L4.|
|                         | **Private Endpoints**                     | Acceso privado a cuentas de almacenamiento y base de datos.         |
|                         | **Azure Firewall**                        | Firewall centralizado para tráfico saliente/entrante controlado.    |
|                         | **Private DNS Zone**                      | Resolución DNS interna para endpoints privados.                     |
|                         | **Audit Logs**                            | Auditoría de acciones administrativas y de seguridad.               |
| Procesamiento           | **Azure Databricks**                      | Ejecución de notebooks PySpark para el ETL completo.                |
| Almacenamiento          | **Azure Data Lake (Bronze/Silver/Gold)** | Data Lake estructurado con arquitectura Medallion.                  |
|                         | **Blob Storage**                          | Zona de aterrizaje inicial para los CSV del Marco Playbook.         |
| Datos relacionales      | **PostgreSQL gestionado en Azure**        | Data Warehouse con modelo estrella (hechos/dimensiones).            |
| Aplicación / API        | **Azure App Service**                     | Backend Flask que expone KPIs y métricas vía API.                   |
| Presentación            | **Azure Static Web Apps**                 | SPA React que actúa como visor BI en la nube.                       |
| Seguridad de secretos   | **Azure Key Vault**                       | Almacén seguro de cadenas de conexión y credenciales.               |
| Monitoreo y logging     | **Azure Monitor + Log Analytics**         | Métricas, logs centralizados y alertas.                             |
| Backup / DR             | **Recovery Services Vault**               | Copias de seguridad y recuperación ante desastres.                  |

<img width="1861" height="941" alt="image" src="https://github.com/user-attachments/assets/95c980f0-e790-416a-bddd-44e389f67e18" />

---

## 1.5. Flujo de datos end-to-end

1. **Carga de archivos**  
   El *Service Owner* descarga los CSV del Marco Playbook y los sube a través de la interfaz web.  
   La aplicación los envía a **Blob Storage** (zona de staging).

2. **Ingesta al Data Lake (Bronze)**  
   Un proceso controlado carga los CSV desde Blob a la **capa Bronze** del Data Lake, preservando la estructura original.

3. **Procesamiento en Databricks (Silver)**  
   Azure Databricks:
   - Lee los archivos de Bronze.
   - Aplica reglas de limpieza y tipificación.
   - Escribe los resultados limpios en la **capa Silver**.

4. **Enriquecimiento y agregación (Gold)**  
   Nuevos notebooks en Databricks:
   - Realizan joins, agregaciones y cálculo de KPIs.
   - Escriben las tablas refinadas en la **capa Gold**.

5. **Carga al Data Warehouse (PostgreSQL)**  
   Databricks inserta/actualiza las tablas de hechos y dimensiones en PostgreSQL utilizando los datos refinados de Gold.

6. **Exposición vía API (App Service)**  
   El backend Flask, desplegado en App Service, expone endpoints REST que consultan el modelo estrella.

7. **Visualización (Static Web Apps)**  
   La SPA React, hospedada en Azure Static Web Apps:
   - Consume las APIs del backend.
   - Presenta KPIs, gráficos y tablas al *Service Owner* y al resto de usuarios internos.

---

## 1.6. Escalabilidad, elasticidad y alta disponibilidad

### Escalabilidad y elasticidad

- **Azure Databricks**
  - Clústeres con **autoscaling** (por ejemplo, 2–8 workers).
  - Auto-termination tras la ventana de procesamiento mensual, evitando costo de recursos ociosos.

- **Azure App Service**
  - Plan Standard S1 con **escalado horizontal** basado en métricas (CPU/uso de memoria).
  - Capacidad de aumentar instancias del backend durante picos de uso del dashboard.

- **PostgreSQL en Azure**
  - Escalado **vertical** ajustando vCores y almacenamiento sin downtime significativo.

### Alta disponibilidad y DR

- Servicios gestionados (App Service, PostgreSQL, almacenamiento) con SLA elevado (hasta 99.95–99.99 % según configuración).
- **Recovery Services Vault**:
  - Almacena las copias de seguridad de recursos críticos.
  - Permite restauraciones ante fallos graves o desastres.
- Uso de almacenamiento con redundancia local y, opcionalmente, redundancia geográfica si se requiere un escenario multi-región.

---

## 1.7. Seguridad, redes y gobernanza (visión general)

> *El detalle técnico se documenta en la carpeta `2_Seguridad_IAM_Redes_y_Gobernanza`. Aquí se presenta un resumen a nivel de arquitectura.*

- **VNet + subredes privadas**  
  Todos los servicios de datos (Data Lake, PostgreSQL, Databricks) se ubican en subredes privadas, sin exposición directa a Internet.

- **Network Security Groups y Azure Firewall**  
  Controlan el tráfico entrante y saliente por puertos/protocolos, restringiendo el acceso sólo a los servicios y orígenes necesarios.

- **Private Endpoints + Private DNS Zone**  
  El acceso a cuentas de almacenamiento y bases de datos se realiza mediante **endpoints privados**, evitando uso de IPs públicas.

- **Azure Key Vault**  
  Las cadenas de conexión y secretos no se guardan en código ni variables de entorno sin protección; se leen de Key Vault.

- **Audit Logs**  
  Registra operaciones administrativas y de seguridad sobre los recursos, permitiendo auditoría y trazabilidad.

---

## 1.8. Monitoreo y observabilidad

- **Azure Monitor + Log Analytics Workspace**
  - Centralizan métricas de:
    - App Service (latencia, errores HTTP, CPU).
    - Databricks (estado de jobs y clústeres).
    - PostgreSQL (conexiones, tiempos de respuesta).
    - Storage y Static Web Apps (errores, tráfico).
  - Permiten definir **alertas** (por ejemplo, fallos de job, latencia alta, costo proyectado).


