# Flujo de Implementación

## 1. Asignar los roles (IAM)

Antes de crear recursos en Azure, se definen claramente las responsabilidades de cada miembro del equipo y se asignan los **roles mínimos necesarios (principio de mínimo privilegio)** usando Azure RBAC.  
En este entorno se trabaja con tres personas ficticias: **Persona 1, Persona 2 y Persona 3**, cada una con un ámbito de administración bien delimitado.

---

### 1.1 Persona 1 – Propietario del despliegue de aplicaciones

**Responsabilidades principales**

Persona 1 se encarga de todo lo relacionado con el despliegue y operación de las aplicaciones:

- **Azure Container Registry**: `acrbbvadashboard`
- **Backend**: Container App `bbva-backend-api`
- **Frontend**: Static Web App `bbva-dashboard-frontend`
- **Container Apps Environment**: `managedEnvironment-vnet`
- **Log Analytics Workspace**: `law-bbva-dashboard`

**Objetivo**: poder construir, versionar y desplegar el backend y frontend, además de revisar la observabilidad básica de la solución.

#### Roles asignados a Persona 1

| Recurso                             | Rol                         |
|-------------------------------------|-----------------------------|
| Resource Group `rg-bbva-dashboard`  | Contributor (base)          |
| ACR `acrbbvadashboard`              | AcrPush, AcrPull            |
| Container App `bbva-backend-api`    | Contributor                 |
| Static Web App `bbva-dashboard-frontend` | Contributor           |
| Container Apps Environment `managedEnvironment-vnet` | Container Apps Contributor |
| Log Analytics `law-bbva-dashboard`  | Log Analytics Contributor   |

<img width="1865" height="908" alt="image" src="https://github.com/user-attachments/assets/c224d541-08e4-4748-871e-e295879adaeb" />

### 1.2 Persona 2 – Dueño de datos y analytics (Data & Security Engineer)

#### Responsabilidades principales

Persona 2 administra todo lo que tiene que ver con **datos, gobernanza y respaldo**:

- Databricks Workspace: `dbw-bbva-dashboard`
- Key Vault: `kv-bbva-dashboard`
- PostgreSQL Flexible Server: `pg-bbva-dashboard`
- Backup Vault: `rg-bbva-dashboard-backup`
- Storage Account / Data Lake: `stbbvadatalake` (incluye niveles **Bronze / Silver / Gold**)

**Objetivo:** garantizar que los datos estén seguros, respaldados, encriptados y disponibles para los procesos de ingeniería y analytics.

#### Roles asignados a Persona 2

| Recurso                         | Rol                           |
|---------------------------------|-------------------------------|
| Databricks Workspace            | Owner                         |
| Key Vault `kv-bbva-dashboard`   | Key Vault Secrets Officer     |
| PostgreSQL Flexible Server      | Contributor                   |
| Backup Vault                    | Backup Contributor            |
| Storage Account `stbbvadatalake`| Storage Account Contributor   |
| Blobs / Data Lake del Storage   | Storage Blob Data Contributor |

<img width="1280" height="800" alt="Captura de pantalla 2025-12-01 192626" src="https://github.com/user-attachments/assets/f8867f4d-4a6e-442a-a369-4c4406928386" />

---

### 1.3 Persona 3 – Seguridad, redes y conectividad (Network & Firewall Admin)

#### Responsabilidades principales

Persona 3 es responsable de toda la **capa de red y perímetro de seguridad**:

- Virtual Network: `vnet-bbva-dashboard`
- Network Security Groups (NSGs) de todas las subnets
- Private Endpoints
- Private DNS Zones
- Firewall: `fw-bbva-dashboard`
- Firewall Policy: `policy-bbva-firewall`
- Route Table: `rt-firewall`
- Public IPs asociadas al firewall y otros componentes de red

**Objetivo:** asegurar que toda la comunicación entre servicios sea **privada, controlada y trazable**, aplicando buenas prácticas de segmentación y filtrado.

#### Roles asignados a Persona 3

| Recurso          | Rol                          |
|------------------|------------------------------|
| VNet completa    | Network Contributor          |
| NSGs             | Network Contributor          |
| Private Endpoints| Network Contributor          |
| Private DNS Zones| Private DNS Zone Contributor |
| Public IPs       | Network Contributor          |
| Firewall         | Network Contributor          |
| Firewall Policy  | Network Contributor          |
| Route Table      | Network Contributor          |

<img width="1708" height="845" alt="image" src="https://github.com/user-attachments/assets/1f6d285e-62f9-44e5-8f5f-3b9eddca8656" />



## 2. Crear los Resource Group
Como primer paso se definieron tres grupos de recursos para separar responsabilidades y facilitar la gobernanza:

### 1. `rg-bbva-alerts`
**Propósito:** Concentrar recursos de monitoreo y alertas.
**Recursos incluidos:**
- Log Analytics
- Azure Monitor
- Action Groups

### 2. `rg-bbva-dashboard`
**Propósito:** Agrupar servicios directamente relacionados al dashboard.
**Recursos incluidos:**
- Storage Account del Data Lake
- Servidor PostgreSQL flexible
- Workspace de Databricks
- Otros componentes de aplicación (ej. backend/frontend) ligados al proyecto

### 3. `rg-bbva-red`
**Propósito:** Reservado para componentes de red y seguridad.
**Recursos incluidos:**
- Virtual Network y subredes privadas
- Network Security Groups (NSG)
- Private Endpoints
- Azure Firewall
- Recursos de gobernanza (Private DNS Zone, Recovery Services Vault)

### Beneficios de esta estructura:
- **Separación por dominio** (alertas, carga de trabajo y red)
- Permite aplicar **políticas y permisos diferenciados** por equipo
- **Simplifica la administración** y gobernanza

<img width="1865" height="905" alt="image" src="https://github.com/user-attachments/assets/5662aada-ce67-423f-93b2-062aa1598f72" />

## 3. Crear key vault
Se creó el recurso **`kv-bbva-dashboard`** dentro del grupo de recursos **`rg-bbva-dashboard`**.

### Propósito
Centralizar todos los secretos sensibles utilizados por la solución.

### Secretos almacenados
- Cadenas de conexión hacia **PostgreSQL Flexible Server**
- Claves de acceso del **Storage Account**
- Credenciales de **service principal** o **identidades administradas** que consumen el Data Lake
- Cualquier otro secreto necesario para el **backend** o los **jobs de Databricks**

### Configuración destacada
- **SKU:** Standard (suficiente para escenarios internos y académicos)
- **Soft delete:** Habilitado (protege contra eliminaciones accidentales)
- **Control de acceso:** Integración con Access Policies / IAM

### Políticas de acceso
El acceso está limitado únicamente a:
- Identidades de **Databricks**
- Identidades del **backend** / scripts de administración
- Usuarios **administradores** del entorno

### Beneficio de seguridad
Evita almacenar credenciales en:
- Código fuente
- Archivos `.env`
- Variables de entorno sin protección

<img width="1864" height="905" alt="image" src="https://github.com/user-attachments/assets/413acc08-7d6b-4bec-a84c-e259d54a77b9" />

## 4. Crear el Storage Account
Para implementar el Data Lake se creó el Storage Account **stbbvadatalake** con las siguientes características:

- **Tipo:** StorageV2 (general purpose v2)
- **Hierarchical namespace:** Enabled, para habilitar Azure Data Lake Storage Gen2
- **Replicación:** LRS (Locally Redundant Storage), suficiente para el ámbito académico del proyecto
- **Access tier:** Hot, ya que los datos se leen y escriben en cada ciclo de carga mensual

**Acceso seguro mediante:**
- Require secure transfer for REST API operations = Enabled
- Integración con Private Endpoints (se observan conexiones privadas configuradas en el panel de Networking)

<img width="1864" height="909" alt="image" src="https://github.com/user-attachments/assets/62ac2d43-1154-4381-b2e3-619ca0ee8cf2" />

Dentro del Storage Account se definieron varios contenedores:

- **bronze:** capa de data sucia / raw, donde se almacenan los CSV tal como llegan
- **silver:** capa de data limpia / transformada, en formato parquet u otro formato optimizado tras el ETL
- **slogs** y **$blobchangefeed:** contenedores técnicos para logs/cambios de blobs (propios del servicio)

Esta estructura respeta la separación raw/trusted y facilita el control de acceso por capa.

<img width="1866" height="907" alt="image" src="https://github.com/user-attachments/assets/7bc23514-06a7-4739-98ee-eedb01cbb292" />

## Estructura Bronze – Data Sucia
En el contenedor **bronze** se creó una carpeta lógica **data_sucia** que separa los archivos según el dominio funcional:

- `data_sucia_practitioner`
- `data_sucia_continuous_integration`

En estas ubicaciones se cargan los archivos CSV exportados desde el Marco Playbook (o sus equivalentes de prueba en este entorno).

Cada subcarpeta representa el **“raw zone”** de su dominio, sin transformaciones ni limpieza aplicada.

<img width="1861" height="907" alt="image" src="https://github.com/user-attachments/assets/e9a9b3bd-9c9e-42a3-82ca-d05f1aff0f55" />

## Estructura Silver – Data Limpia
En el contenedor **silver** se creó la carpeta **data_limpia**, también separada por dominio:

- `data_limpia_practitioner`
- `data_limpia_continuous_integration`

Aquí Databricks escribe los resultados de las transformaciones: datos limpios, tipificados y listos para ser cargados en la capa Oro (PostgreSQL).

Esta separación permite trazar claramente qué dataset se encuentra en qué nivel de calidad.

<img width="1863" height="903" alt="image" src="https://github.com/user-attachments/assets/5016c728-5c23-40aa-a0f1-b0776e1dc504" />

## 5. Crear PostgreSQL Flexible Server

Para la capa de datos Oro se optó por **Azure Database for PostgreSQL – Flexible Server**, alineado con el motor usado en el entorno local.

**El servidor creado es:**

- **Nombre:** `pg-bbva-dashboard`
- **Ubicación:** Central US
- **Tipo:** General Purpose, tamaño D2ds v5 (2 vCores, 8 GB RAM, 128 GB storage)
- **Acceso restringido** mediante reglas de red y Private Endpoints (conectado a la VNet de rg-bbva-red)
- **Alta disponibilidad** deshabilitada en este entorno académico (pero documentada como recomendación para entornos productivos)

Este servidor se utiliza como **Data Warehouse relacional** donde se modela la capa Oro con esquemas en estrella para Practitioner y CI.

<img width="1865" height="907" alt="image" src="https://github.com/user-attachments/assets/822b9aae-9a3f-4817-a188-53a42340b894" />

## Creación de las bases de datos Oro

Dentro del servidor `pg-bbva-dashboard` se crearon las bases de datos de la capa Oro:

- `data_oro_practitioner`
- `data_oro_ci`

**Cada una contiene:**

- Tablas de hechos y dimensiones necesarias para los KPIs del dominio
- Índices y claves foráneas que soportan las consultas del dashboard
- Esquemas diseñados para facilitar las consultas analíticas desde el backend y, si se necesitara, desde herramientas externas de BI

Estas bases de datos son el **destino final** del ETL ejecutado en Databricks.

<img width="1861" height="906" alt="image" src="https://github.com/user-attachments/assets/dc6091d0-b359-40ac-804a-c82e41d8a783" />
<img width="1913" height="887" alt="image" src="https://github.com/user-attachments/assets/b37d6173-3c20-4ef7-92b3-0fb840165759" />
<img width="1915" height="979" alt="image" src="https://github.com/user-attachments/assets/67e0d65e-0790-4cf3-8029-1a669c0c31be" />

## 6. Crear Databricks
Para el procesamiento distribuido se aprovisionó un workspace de **Azure Databricks**:

- **Nombre:** `dbw-bbva-dashboard`
- **Resource group:** `rg-bbva-dashboard`
- **Tipo de workspace:** Hybrid
- **Enable No Public IP:** Yes, lo que obliga a consumir Databricks a través de la red privada y endpoints seguros, alineado con los requisitos de seguridad del proyecto

Este workspace es el **punto central** para desarrollar notebooks PySpark, ejecutar el ETL y orquestar los jobs.

<img width="1864" height="906" alt="image" src="https://github.com/user-attachments/assets/9a7f5036-5aa8-45bc-82d3-7c3a28471510" />

## Creación del clúster de Databricks

Dentro del workspace se configuró el clúster **cluster-bbva**, con las siguientes características:

- **Runtime:** Databricks 16.4 LTS (incluye Apache Spark 3.5.2)
- **Tipo de nodo:** Standard_D4as_v5 (16 GB Memory, 4 Cores)
- **Modo:** Single node (suficiente para los volúmenes actuales)
- **Auto-termination:** 20 minutos de inactividad, para evitar costos innecesarios
- **Access mode:** Custom, permitiendo ajustar permisos de acceso a datos según las necesidades del ETL

Este clúster es el que ejecuta los notebooks de limpieza y transformación que mueven la información desde:

1. **Bronze → Silver** en el Data Lake
2. **Silver → Oro** en PostgreSQL Flexible Server

<img width="1862" height="944" alt="image" src="https://github.com/user-attachments/assets/4ff71757-db17-4bbe-b51e-39c69513cf93" />

## Creación de Jobs de ETL

Sobre el clúster `cluster-bbva` se diseñaron dos Jobs principales (ilustrativos en este entorno académico):

### Job ETL Practitioner
- Lee los CSV crudos desde `bronze/data_sucia_practitioner`
- Aplica limpieza, tipificación y joins necesarios
- Escribe los datos limpios en `silver/data_limpia_practitioner`
- Finalmente carga la capa Oro en la base de datos `data_oro_practitioner` (tablas de hechos y dimensiones)

### Job ETL Continuous Integration (CI)
- Mismo patrón que el anterior, pero usando:
  - `bronze/data_sucia_continuous_integration`
  - `silver/data_limpia_continuous_integration`
  - Base de datos `data_oro_ci` como destino final

**Nota:** En un escenario productivo, ambos jobs se programarían para ejecutarse automáticamente 1 vez al mes, alineados con la frecuencia de exportación del Marco Playbook. En este proyecto se dejan configurados de forma ilustrativa, demostrando la lógica de orquestación y la trazabilidad del pipeline, aunque no estén conectados a un origen real productivo.

## Subir los notebooks a Databricks

Una vez creado el workspace y el clúster de Databricks, se suben los notebooks que implementan el ETL completo sobre las tablas de Practitioner y Continuous Integration.

En la siguiente captura se observa la carpeta de trabajo del usuario con los seis notebooks creados:

- `Limpiar Practitioner`
- `Limpiar Continuous Integration`
- `Transformar Practitioner`
- `Transformar Continuous Integration`
- `Vista Practitioner`
- `Vista Continuous Integration`

**Los notebooks siguen el patrón Medallion:**

- Los notebooks de **Limpieza** leen los CSV ubicados en la capa Bronze y escriben datos tipificados y depurados en la capa Silver
- Los notebooks de **Transformación** enriquecen la información Silver (joins, derivación de campos, normalización) y preparan las tablas de Gold que luego se cargan en PostgreSQL
- Los notebooks de **Vista** generan las vistas de negocio (KPIs) que se consultan desde el backend

**Nota:** Estos notebooks pueden ejecutarse manualmente durante el laboratorio o programarse como Jobs para que se disparen automáticamente (por ejemplo, una vez al mes cuando Marco Playbook publique nuevos archivos).

<img width="1865" height="944" alt="image" src="https://github.com/user-attachments/assets/4bd79a64-c027-419d-9c0e-343f2978bfbb" />

## 7. Crear Container Registry

Para empaquetar y versionar la API de backend en contenedores se crea un **Azure Container Registry (ACR)** dentro del resource group `rg-bbva-dashboard`.

En la captura se aprecia el registro privado con:

- **Pricing plan:** tipo Premium (útil para escenarios corporativos y mayor throughput)
- **Integración** con la suscripción y el grupo de recursos del proyecto
- **Soft delete** deshabilitado (para simplificar el laboratorio)

Este registro actúa como **repositorio central de imágenes Docker internas**, evitando exponer el backend en registries públicos y permitiendo controlar versiones, acceso y políticas de seguridad.

<img width="1863" height="907" alt="image" src="https://github.com/user-attachments/assets/4750e3a1-1e30-4874-82ae-39b33a8389f7" />

## Publicar la imagen del backend en el Registry

A partir del código del backend Flask se construye una imagen Docker y se publica en el ACR.

En la captura del repositorio `bbva-backend` se ve la etiqueta `v1`, que corresponde a la primera versión estable del servicio:

**La imagen incluye:**

- Código Flask de la API
- Dependencias Python (`requirements.txt`)
- Configuración de Gunicorn para servir la aplicación

**El tag `v1`** permite gestionar versiones posteriores (`v2`, `v3`, etc.) y facilitar rollbacks en caso de errores de despliegue.

**El flujo típico es:**

1. `docker build` de la imagen del backend
2. `docker tag` apuntando al login server del ACR
3. `docker push` para publicar la versión en el registro

<img width="1859" height="909" alt="image" src="https://github.com/user-attachments/assets/1596ede8-be5a-4fae-a962-f9ef951f4c4a" />

## 8. Crear Container Apps Environment

Como capa de ejecución para el backend se despliega un **Azure Container Apps Environment** asociado a una VNet (`managedEnvironment-vnet`).

En la captura se observa:

- El entorno ejecutándose en la región **East US**
- La integración con la red virtual y la subred de infraestructura, lo que permite:
  - Exponer el backend de forma controlada
  - Conectarlo de manera segura a PostgreSQL y al Storage Account
- Un contador de aplicaciones donde, para este laboratorio, se despliega una sola API: `bbva-backend-api`

Este entorno funcionará como **“cluster lógico”** para todas las Container Apps relacionadas con el dashboard.

<img width="1860" height="906" alt="image" src="https://github.com/user-attachments/assets/996ee684-5190-44c2-b102-b5084a5d0327" />

## 9. Crear el Conteiner App

Sobre el environment anterior se crea la Container App **bbva-backend-api**, que ejecuta la imagen `bbva-backend:v1` alojada en el ACR.

La captura muestra:

- Estado **Running** y URL pública de la aplicación
- Asociación al environment `managedEnvironment-vnet`
- Suscripción y resource group `rg-bbva-dashboard`

**En esta Container App se configuran:**

- Recursos (CPU/RAM) apropiados para una API ligera
- Variables de entorno con las cadenas de conexión a PostgreSQL y Storage, obtenidas desde Azure Key Vault
- Escalamiento automático basado en métricas (por ejemplo, número de requests o porcentaje de CPU), cumpliendo con los criterios de escalabilidad de la rúbrica

Esta API es el **punto de entrada** para el frontend React y otros posibles consumidores internos.

<img width="1861" height="906" alt="image" src="https://github.com/user-attachments/assets/997c73da-11f5-4413-81c7-6a3aae64ecda" />

## 10. Crear el Static Web App

Para la capa de presentación se utiliza **Azure Static Web Apps**, donde se despliega el dashboard web desarrollado en React.

En la primera captura se ve el recurso **bbva-dashboard-frontend**:

- Plan **Free**, suficiente para el laboratorio
- Dominio generado por Azure (URL de acceso público)
- Estado **Ready**, indicando que el último despliegue fue exitoso

<img width="1863" height="942" alt="image" src="https://github.com/user-attachments/assets/2e8b26d2-057f-487a-94ad-9b0fb33ffbeb" />

En la segunda captura (sección **Environments**) se observa:

- Un entorno de producción activo al **100 %** del tráfico
- La posibilidad de usar entornos **preview** vinculados a ramas o Pull Requests (útil para futuras mejoras de CI/CD)

**El flujo de despliegue es:**

1. Clonar el repositorio del frontend
2. Ejecutar `npm install` y `npm run build` para generar la carpeta de salida (`dist` o `build`)
3. Configurar Static Web Apps para que tome esa carpeta como origen del contenido estático
4. Cada **push a la rama principal** dispara un nuevo build y despliegue

<img width="1862" height="907" alt="image" src="https://github.com/user-attachments/assets/b27fb2ca-ddf8-4453-a52f-290f0237a7b7" />

## 11. Crear el Log Analytics workspace

Para centralizar métricas y logs de toda la solución se crea un **Log Analytics workspace** denominado `law-bbva-dashboard`.
Se puede observar:
- Workspace en la región **East US**
- Modelo de facturación **Pay-as-you-go**
- Integración con la suscripción y el resource group del proyecto

Este workspace es el **backend de observabilidad** sobre el que se apoyan:

- Azure Monitor
- Las métricas y logs de:
  - Storage Account (Data Lake)
  - Container Apps (backend)
  - Azure Database for PostgreSQL
  - Otros recursos que se deseen monitorear

<img width="1865" height="911" alt="image" src="https://github.com/user-attachments/assets/32697055-066a-4fb3-8cff-e08862932665" />

Una vez configurado el envío de diagnósticos al workspace, es posible ejecutar consultas **Kusto Query Language (KQL)** para analizar el comportamiento del entorno.
En la imagen se muestra un ejemplo de consulta sobre la tabla **StorageBlobLogs**.

<img width="1861" height="910" alt="image" src="https://github.com/user-attachments/assets/cdc8a632-7460-452d-bc43-c7b62b049ddc" />

Esta consulta permite:
- Ver las últimas operaciones de lectura/escritura realizadas sobre la capa **Bronze** del Data Lake
- Identificar errores (códigos `4xx`/`5xx`) y patrones de acceso durante la ejecución del ETL

## 12. Crear las Alertas

Se configuran reglas de alerta en Azure Monitor para reaccionar ante problemas de rendimiento, disponibilidad o capacidad.
En la captura de **Alert rules** se visualizan, entre otras, las siguientes reglas:

- **`alert-backend-5xx`**: se dispara cuando el backend devuelve más de 5 respuestas `5xx`, indicando errores en la API
- **`alert-backend-cpu-high`**: alerta cuando el CPU de la Container App supera el `70 %` durante un periodo sostenido
- **`alert-backend-no-requests`**: detecta ausencia de requests (posible caída de tráfico o problemas de conectividad)
- **`alert-postgres-connections-high`**: monitorea conexiones activas al servidor PostgreSQL, evitando saturar el límite configurado
- **`alert-postgres-cpu-high`** y **`alert-postgres-storage-low`**: vigilan el uso de CPU y el porcentaje de almacenamiento consumido
- **`alert-storage-egress`**, **`alert-storage-errors`** y **`alert-storage-latency`**: verifican volumen de tráfico, número de errores y latencia en el Data Lake

**Cada regla define:**
- Condición (métrica, umbral y ventana de tiempo)
- Severidad (Error, Warning o Informational)
- Action Group asociado (por ejemplo, envío de correo al equipo o notificación a Teams)

Con este set de alertas la solución cumple con los requisitos de monitoreo y gobernanza, permitiendo detectar incidentes con anticipación y tomar acciones correctivas.

<img width="1862" height="905" alt="image" src="https://github.com/user-attachments/assets/4310359f-e5ba-41b5-bff6-afffee35b244" />

## 13. Audit Logs
Para cumplir con la parte de auditoría y gobernanza se habilitó el uso de **Audit Logs en Microsoft Entra ID (Azure AD)**.

Estos logs permiten rastrear:

- Creación y eliminación de service principals usados por Databricks y Container Apps
- Cambios en asignaciones de roles y permisos
- Acciones de administración realizadas en el tenant

**Nota:** En un escenario corporativo, estos registros se enviarían también a Log Analytics o a un SIEM para retención a largo plazo y análisis avanzado.
<img width="1863" height="906" alt="image" src="https://github.com/user-attachments/assets/8068a347-cfe8-43a4-a169-51a06a82a044" />

## 14. Crear el Backup Vault

Para la estrategia de respaldo y recuperación ante desastres (DR) se configuró un **Azure Backup Vault** dedicado al proyecto.
En este vault se centraliza la política de backup de:

- Azure Database for PostgreSQL flexible server
- (Opcional) Máquinas virtuales o recursos adicionales si el entorno creciera
<img width="1862" height="908" alt="image" src="https://github.com/user-attachments/assets/6183d41a-fedb-4034-892a-ea510fa02d35" />

En la propiedades del vault se puede apreciar:
<img width="1862" height="909" alt="image" src="https://github.com/user-attachments/assets/0b15618e-007c-4860-a96a-37e2b977e825" />

**Aspectos relevantes:**
- **Redundancia:** Geo-redundant (GRS) para disponer de copias en una región secundaria
- **Soft delete habilitado** para proteger contra eliminaciones accidentales
- **Cross Region Restore habilitado**, lo que permite restaurar backups en otra región en caso de caída total de la principal

## 15  . Crear la Red

La conectividad interna del entorno se organiza alrededor de la VNet **`vnet-bbva-dashboard`**.

**Características principales:**

- **Address space:** `10.0.0.0/16`
- **Región:** East US
- **Integración con:**
  - Azure Firewall para inspección y filtrado de tráfico saliente
  - Private Endpoints de Storage, PostgreSQL, ACR y Key Vault
  - Subnets específicas por servicio (según se detalla a continuación)

Esta VNet también se enlaza con otras capacidades de red que se crean más adelante (Private DNS Zones, Private Endpoints, etc.), de forma que los servicios PaaS se consumen por rutas privadas.

<img width="1861" height="909" alt="image" src="https://github.com/user-attachments/assets/383aba16-1dff-4fdb-93b4-aaf248e8b6ef" />

Dentro de `vnet-bbva-dashboard` se definieron subredes dedicadas por tipo de servicio:

**Subnets más relevantes:**

- **`AzureFirewallSubnet`** – Reservada para el servicio de Azure Firewall
- **`snet-postgresql`** – Aloja el Private Endpoint hacia el servidor PostgreSQL
- **`snet-keyvault`** – Aloja el Private Endpoint de Key Vault
- **`snet-containerapp`** y **`snet-containerapp-infra`** – Dedicadas al entorno de Container Apps y su infraestructura
- **`snet-storage`** – Donde residen los Private Endpoints de Blob y DFS para el Data Lake
- **`snet-databricks-public`** y **`snet-databricks-private`** – Redes usadas por el workspace de Databricks (nodos de cluster y conectividad interna)

El objetivo es **segmentar el tráfico por tipo de servicio**, aplicar reglas de seguridad específicas y evitar que recursos con diferentes perfiles de riesgo compartan la misma subnet.

<img width="1863" height="909" alt="image" src="https://github.com/user-attachments/assets/ea4017ea-d9e7-4e0f-a366-b6a63117fe0f" />

## Crear los Network Security Groups (NSG)

Para controlar el tráfico a nivel de capa 4 se crearon Network Security Groups por tipo de servicio.
**Ejemplos de reglas:**

- **En `nsg-postgresql`:**
  - Permitir tráfico entrante desde `snet-containerapp` y `snet-databricks-private` al puerto `5432`
  - Denegar tráfico desde Internet

- **En `nsg-storage`:**
  - Permitir acceso desde subnets de Databricks y Container Apps a los endpoints de Storage
  - Restringir otros orígenes

- **En `nsg-databricks`:**
  - Controlar el tráfico saliente de los clusters hacia servicios internos y externos

Con esto se consigue un **modelo zero-trust** donde solo se permiten las comunicaciones necesarias entre componentes.

<img width="1860" height="907" alt="image" src="https://github.com/user-attachments/assets/5e65a7c0-dcbd-4e51-8a99-a15fe8b99ca9" />

## Crear las Private DNS Zones

Para que los servicios PaaS sean accesibles por nombres privados se crearon varias Private DNS Zones:
<img width="1863" height="905" alt="image" src="https://github.com/user-attachments/assets/cce7f449-1831-42a4-9479-3f4d9aaacb19" />
Estas zonas se agregaron a la VNet `vnet-bbva-dashboard`:
<img width="1863" height="907" alt="image" src="https://github.com/user-attachments/assets/cdd38702-d2f2-4914-9157-efad43dd9766" />
De esta forma:

- Cuando el backend o Databricks resuelven, por ejemplo, `stbbvadatalake.dfs.core.windows.net`, obtienen una IP privada en la VNet
- Todo el tráfico hacia ACR, Storage, Key Vault y PostgreSQL fluye por la red privada de Azure, sin exponer endpoints públicos

## Crear los Private Endpoints

Finalmente, se definieron Private Endpoints para los servicios críticos, mapeándolos a las subnets correspondientes.

<img width="1863" height="908" alt="image" src="https://github.com/user-attachments/assets/7585e9f2-fec8-41b6-b9f4-b28c64f2676d" />
<img width="1863" height="906" alt="image" src="https://github.com/user-attachments/assets/86599cfb-94c0-4fbc-9117-cbc35608a899" />
**Private Endpoints configurados:**

- **`pe-acr`** → Azure Container Registry (`acrbbvadashboard`) en `snet-storage` o subnet específica
- **`pe-keyvault`** → Key Vault del proyecto en `snet-keyvault`
- **`pe-postgresql`** → Servidor PostgreSQL flexible `pg-bbva-dashboard` en `snet-postgresql`
- **`pe-storage-blob`** y **`pe-storage-dfs`** → Cuenta de Storage `stbbvadatalake` (Blob y Data Lake Gen2) en `snet-storage`

**Gracias a estos endpoints:**

- Container Apps, Databricks y otros servicios acceden a los recursos PaaS sin salir a Internet
- Se reduce la superficie de ataque al deshabilitar (o minimizar) el acceso público
- Se facilita el cumplimiento de políticas de seguridad y gobernanza de red

## Network Interfaces

Las **Network Interfaces (NIC)** son los recursos que vinculan la red virtual con los servicios privados como Storage, PostgreSQL, Key Vault y el propio Azure Container Apps. Cada private endpoint crea de manera automática una NIC dentro del grupo de recursos de red, lo que permite controlar en detalle el tráfico que entra y sale de cada servicio.

<img width="1860" height="907" alt="image" src="https://github.com/user-attachments/assets/668a8173-f1d6-4672-af56-277e9de27ae4" />
En la figura se puede apreciar que se han creado cinco interfaces de red, cada una asociada a un private endpoint específico:

- **`pe-acr-nic`** – interfaz asociada al private endpoint del Azure Container Registry
- **`pe-keyvault-nic`** – interfaz asociada al private endpoint del Key Vault
- **`pe-postgresql-nic`** – interfaz asociada al private endpoint de la base de datos PostgreSQL flexible
- **`pe-storage-blob-nic`** y **`pe-storage-dfs-nic`** – interfaces asociadas a los private endpoints de Blob Storage y Data Lake (DFS)

**Tener estas NIC dedicadas permite:**

- Aislar el tráfico de cada servicio dentro de la VNet
- Aplicar reglas de seguridad por subnet y por Network Security Group (NSG)
- Auditar de forma más precisa los accesos a nivel de red

## Creación del Firewall y tabla de ruteo

Para centralizar el control del tráfico saliente y proteger el entorno frente a accesos no deseados desde Internet, se implementa un **Azure Firewall** dedicado, ubicado en el mismo grupo de recursos de red.

<img width="1860" height="903" alt="image" src="https://github.com/user-attachments/assets/de923a3a-510a-4f36-a042-ef8163fc31a5" />

En la captura se observan los recursos principales relacionados con el firewall:

- **`fw-bbva-dashboard`** – instancia de Azure Firewall que inspecciona el tráfico
- **`pip-firewall`** – IP pública asociada al firewall, necesaria para el tráfico de salida controlado
- **`policy-bbva-firewall`** – Firewall Policy donde se definen las reglas de:
  - Acceso a servicios de Azure (Storage, PostgreSQL, ACR, etc.)
  - Restricciones por FQDN o rangos de IP
- **`rt-firewall`** – tabla de ruteo que fuerza el tráfico de determinadas subnets (por ejemplo, Databricks, Container Apps, Storage) a pasar por el firewall

De esta manera, cualquier salida hacia Internet o hacia servicios PaaS expuestos por IP pública se canaliza a través del firewall, donde se pueden aplicar reglas de filtrado, logging y futuras políticas de inspección más avanzadas.

## Visualización general de la topología de red

Para validar la configuración y evidenciar la conectividad entre los distintos componentes, se utiliza la funcionalidad de **Resource Visualizer** sobre la red virtual principal. Esta vista permite mostrar de forma gráfica la relación entre:

- La VNet **`vnet-bbva-dashboard`**
- Las subnets especializadas (storage, key vault, PostgreSQL, container app, Databricks)
- Los Network Security Groups (NSG) que protegen cada subnet
- Los Private Endpoints que conectan los servicios PaaS a la VNet
- El firewall y su tabla de ruteo

<img width="1863" height="905" alt="image" src="https://github.com/user-attachments/assets/eb53dac9-abb5-467b-a33b-4f344e534ae9" />

En el diagrama se observa cómo:

- La VNet actúa como **nodo central** desde el cual se conectan los NSG, el firewall y los private endpoints
- El firewall se posiciona como **punto de salida controlada**, recibiendo tráfico desde las subnets de aplicación y redirigiéndolo hacia Internet o servicios externos
- Los private endpoints **garantizan** que PostgreSQL, Storage, Key Vault y el ACR sean consumidos de forma privada, sin exponer endpoints públicos

Esta visualización se incluye para que se tenga una comprensión rápida de la topología de red, apoyando la explicación previa de subnets, NSG, Private DNS Zones, Private Endpoints, Network Interfaces y Firewall.




