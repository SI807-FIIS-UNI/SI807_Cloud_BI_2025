# 2. SELECCIÓN DE SERVICIOS CLOUD

## 2.1. Visión general de servicios Azure seleccionados

La siguiente tabla resume la correspondencia entre la arquitectura local y los servicios de Azure utilizados en la migración, organizada por capas del flujo BI.

**Tabla 2.1 – Mapeo de componentes locales a servicios Azure**

| Capa funcional                         | Componente local                                   | Servicio Azure seleccionado                                      | Rol dentro del flujo BI                                                                                 |
|----------------------------------------|----------------------------------------------------|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| Ingesta / almacenamiento bruto         | Sistema de archivos local (uploads de CSV)         | **Azure Data Lake Storage Gen2 – Capa Bronze**                    | Punto de entrada de los archivos CSV del Marco Playbook; almacena los datos crudos tal como llegan.    |
| Data Lake                              | HDFS (Hortonworks)                                 | **Azure Data Lake Storage Gen2 – Capas Bronze, Silver y Gold**    | Almacenamiento distribuido para datos crudos, limpios y curados bajo el modelo Medallion.              |
| Procesamiento ETL                      | Apache Zeppelin + Apache Spark                     | **Azure Databricks**                                              | Ejecución de notebooks PySpark para limpieza, transformación y cálculo de KPIs.                        |
| Data Warehouse (DW)                    | PostgreSQL en contenedor Docker                    | **Azure Database for PostgreSQL (servicio PaaS)**                 | Almacenamiento relacional del modelo dimensional tipo estrella.                                        |
| Backend API                            | Flask en contenedor Docker                         | **Azure Container Apps**                                          | Hosting del backend (API Flask) que expone KPIs y métricas hacia el frontend y otros consumidores.     |
| Frontend web                           | React servido desde el mismo contenedor            | **Azure Static Web Apps**                                         | Hosting del frontend React como SPA, que consume la API de Container Apps.                             |
| Gestión de secretos                    | Variables de entorno / archivos de configuración   | **Azure Key Vault**                                               | Almacenamiento seguro de secretos y cadenas de conexión utilizados por los distintos componentes.      |
| Monitoreo y logging                    | Logs en stdout de contenedores / archivos sueltos  | **Azure Monitor + Log Analytics Workspace + Audit Logs**          | Monitoreo unificado de rendimiento, disponibilidad y auditoría de acciones sobre los recursos.         |
| Red y seguridad perimetral             | Red local, firewall físico, VLANs                  | **Virtual Network, Network Security Groups, Azure Firewall**      | Segmentación de red, control de tráfico entrante/saliente y protección de la superficie de ataque.     |
| Acceso privado a servicios PaaS        | Conexiones directas en la red interna              | **Private Endpoints + Private DNS Zone**                          | Exposición privada de servicios PaaS (Data Lake, PostgreSQL, etc.) sólo dentro de la VNet.             |
| Respaldo y recuperación ante desastres | Scripts y discos externos                          | **Recovery Services Vault**                                       | Gestión centralizada de backups y estrategias de recuperación de los componentes críticos.             |

> Nota: en esta arquitectura no se utiliza Power BI ni servicios adicionales de BI cloud.  
> Toda la visualización se realiza mediante el **dashboard React** desplegado en Azure Static Web Apps y consumiendo la API Flask en Azure Container Apps.

---

## 2.2. Servicios Azure por capa funcional

### 2.2.1. Almacenamiento y Data Lake

#### Azure Data Lake Storage Gen2

**Función**

Actúa como almacenamiento distribuido jerárquico que implementa la arquitectura **Medallion** (capas Bronze, Silver y Gold), permitiendo organizar los datos según su grado de procesamiento:

- **Bronze:** datos crudos (raw) tal como llegan desde los archivos CSV del Marco Playbook.  
- **Silver:** datos limpios y estandarizados luego de las primeras transformaciones.  
- **Gold:** datos curados y agregados, listos para el consumo por el Data Warehouse y la API.

**Justificación**

- Reemplaza el **HDFS** del entorno Hortonworks por un servicio totalmente gestionado, eliminando la necesidad de administrar nodos y discos físicos.  
- Proporciona **jerarquía de directorios y ACLs granulares**, lo que facilita separar dominios (Practitioner vs CI) y controlar permisos a nivel de archivo/carpeta.  
- Ofrece **alto rendimiento** de lectura/escritura e integración nativa con Spark mediante el driver **ABFS**, simplificando la configuración en Azure Databricks.  
- En combinación con **Delta Lake**, permite disponer de:
  - Transacciones **ACID** sobre archivos.  
  - Manejo de históricos y **time travel**.  
  - Soporte para actualizaciones incrementales y corrección de datos.  
- Permite recibir directamente los archivos CSV desde la interfaz de carga, por lo que **no se requiere un Blob Storage intermedio**: la capa Bronze del Data Lake asume el rol de zona de aterrizaje inicial.

**Equivalente local**

- **Hadoop HDFS** dentro del contenedor Hortonworks y sistema de archivos local usado para almacenar los CSV.

---

### 2.2.2. Procesamiento y transformación

#### Azure Databricks

**Función**

Plataforma basada en **Apache Spark** que ejecuta los notebooks PySpark de:

- Limpieza y validación de los datos provenientes de la capa Bronze.  
- Transformación y enriquecimiento hacia la capa Silver.  
- Agregación y cálculo de KPIs para la capa Gold y el Data Warehouse PostgreSQL.

**Justificación**

- Reemplaza directamente el stack **Apache Zeppelin + Apache Spark** del entorno local.  
- Proporciona **clusters gestionados** con:
  - Escalado automático (autoscaling) según la carga.  
  - Auto-terminación tras periodos de inactividad, lo que ayuda a controlar costos.  
- Ofrece **notebooks colaborativos** con integración a sistemas de control de versiones (por ejemplo, GitHub), facilitando el trabajo en equipo y la trazabilidad del código ETL.  
- Se integra de forma nativa con **Azure Data Lake Storage Gen2**, leyendo y escribiendo sobre rutas ABFS en las capas Bronze, Silver y Gold.  
- El uso de **Delta Lake** mejora la calidad y confiabilidad del Data Lake (upserts, manejo de históricos, corrección de registros).  

**Equivalente local**

- Conjunto **Apache Zeppelin + Apache Spark** ejecutándose sobre Hortonworks.

---

### 2.2.3. Base de datos analítica

#### Azure Database for PostgreSQL

**Función**

Actúa como **Data Warehouse relacional**, almacenando el **modelo dimensional tipo estrella** (tablas de hechos y dimensiones) que consolida la información de Practitioner y Continuous Integration tras las transformaciones de Databricks.

**Justificación**

- Reemplaza el **PostgreSQL local en contenedor Docker** por un servicio PaaS totalmente administrado.  
- Permite mantener prácticamente el **mismo modelo lógico** ya diseñado (esquema, tablas, tipos de datos y consultas SQL).  
- Ofrece ventajas gestionadas:
  - **Backups automáticos** y restauración dentro de una ventana de retención configurable.  
  - **Alta disponibilidad** mediante réplicas y SLA garantizado por la plataforma.  
  - Escalado vertical (vCores, memoria y almacenamiento) sin necesidad de reinstalar ni migrar manualmente.  
- Es consumido directamente por la **API Flask** desplegada en Azure Container Apps para responder las consultas del dashboard React.  

**Equivalente local**

- **PostgreSQL** desplegado dentro de un contenedor Docker en la infraestructura on-premise.

---

### 2.2.4. Visualización y capa de aplicación

#### Backend – Azure Container Apps

**Función**

Servicio gestionado para ejecutar el **backend Flask** dentro de contenedores, expuesto mediante endpoints HTTP/HTTPS que consumen los datos del Data Warehouse PostgreSQL y del Data Lake según sea necesario.

**Justificación**

- Reemplaza el **contenedor local** que ejecutaba Flask en la infraestructura on-premise.  
- Permite desplegar la aplicación directamente desde una imagen de contenedor (por ejemplo, desde un registro de contenedores) sin administrar máquinas virtuales.  
- Soporta **escalabilidad automática** basada en métricas (por ejemplo, número de peticiones o CPU), lo que permite acompañar el crecimiento de usuarios del dashboard.  
- Se integra con la **Virtual Network**, lo que posibilita que el backend acceda al Data Lake y a PostgreSQL a través de **Private Endpoints**, manteniendo el tráfico dentro de la red privada.  
- Envía logs y métricas a **Azure Monitor** y al **Log Analytics Workspace**, lo que simplifica la observabilidad del backend.

**Equivalente local**

- Contenedor Docker con la aplicación **Flask** ejecutándose en servidores on-premise.

---

#### Frontend – Azure Static Web Apps

**Función**

Servicio diseñado para hospedar el **frontend React** como **Single Page Application (SPA)** estática. La aplicación consume las APIs expuestas por el backend Flask en Azure Container Apps.

**Justificación**

- Se ajusta perfectamente al patrón SPA utilizado en el dashboard actual.  
- Integra de forma nativa flujos de **CI/CD con GitHub** (build + deploy automático), simplificando los despliegues del frontend.  
- Incluye CDN y cacheo en el edge, reduciendo la latencia de carga del dashboard para los usuarios.  
- Gestiona automáticamente **HTTPS** y las rutas de SPA (por ejemplo, `/dashboard`, `/detalle`), sin necesidad de configurar servidores adicionales.  
- Permite desacoplar claramente la capa de presentación del backend, facilitando la evolución independiente de ambas.

**Equivalente local**

- Parte frontend del contenedor que servía la aplicación **React** junto con Flask.

---

### 2.2.5. Red, seguridad y gobernanza

En la arquitectura local, la seguridad y operación dependían de:

- Un servidor físico, firewall y configuración de red manual.  
- Scripts de backup y discos externos.  
- Logs dispersos por contenedores y servidores sin un punto central de monitoreo.

En Azure, estas responsabilidades se distribuyen en varios servicios especializados.

**Tabla 2.2 – Servicios de red, seguridad y gobernanza**

| Servicio                       | Función principal                                                                                     | Problema que resuelve frente al entorno local                                              |
|--------------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| **Virtual Network (VNet)**     | Define la red privada lógica donde se ubican Container Apps, PostgreSQL y demás recursos.            | Sustituye la red local física, permitiendo aislar la solución del resto de internet.      |
| **Network Security Groups**    | Reglas de seguridad a nivel de subred e interfaz para permitir o denegar tráfico.                    | Reemplaza reglas manuales en firewall/servidor; facilita segmentar tráfico por capas.     |
| **Azure Firewall**             | Firewall administrado y centralizado para controlar tráfico entrante/saliente hacia/desde la VNet.   | Aporta un punto único de inspección y registro, sin necesidad de hardware dedicado.       |
| **Private Endpoints**          | Publican servicios PaaS (Data Lake, PostgreSQL, etc.) como direcciones privadas dentro de la VNet.   | Evitan exponer endpoints públicos; el acceso a datos pasa por la red privada.             |
| **Private DNS Zone**           | Resuelve los nombres de los servicios PaaS a sus direcciones privadas asociadas a Private Endpoints. | Permite que las aplicaciones usen nombres de host “normales” pero con resolución privada. |
| **Azure Key Vault**            | Almacén seguro de secretos, claves y certificados.                                                    | Elimina credenciales hardcodeadas en código o variables de entorno sin protección.        |
| **Azure Monitor**              | Plataforma de monitoreo de métricas de los servicios.                                                 | Proporciona una vista centralizada de rendimiento y disponibilidad.                       |
| **Log Analytics Workspace**    | Repositorio y motor de consulta para logs de aplicaciones e infraestructura.                          | Centraliza los logs antes dispersos en stdout y archivos de cada contenedor/servicio.     |
| **Audit Logs / Activity Logs** | Registro de operaciones administrativas sobre los recursos de Azure.                                  | Aporta trazabilidad y auditoría, inexistente en la solución on-premise.                   |
| **Recovery Services Vault**    | Servicio para gestionar backups y restauraciones de recursos críticos.                                | Sustituye soluciones de backup manuales basadas en scripts y discos externos.             |

A continuación se describen brevemente los más relevantes.

---

#### Azure Key Vault

**Función**

Almacena de forma segura secretos (connection strings, claves de acceso, credenciales de servicio) utilizados por:

- Azure Databricks.  
- Azure Container Apps.  
- Otros componentes que requieran credenciales para conectarse a Data Lake o PostgreSQL.

**Justificación**

- Evita guardar secretos en código o archivos de configuración sin cifrar.  
- Permite **rotar claves** sin necesidad de cambiar el código de las aplicaciones.  
- Ofrece **auditoría** sobre el acceso a secretos.  
- Se integra con identidades administradas (Managed Identities), reduciendo el uso de contraseñas explícitas.

**Equivalente local**

- Variables de entorno y archivos de configuración sin mecanismos formales de auditoría ni rotación centralizada.

---

#### Azure Monitor + Log Analytics Workspace + Audit Logs

**Función**

- Recopilar métricas de rendimiento (CPU, memoria, latencia, uso de almacenamiento, etc.) de los servicios de la solución.  
- Centralizar los logs de aplicación (Container Apps, Static Web Apps, Databricks) y de infraestructura.  
- Registrar las operaciones administrativas realizadas sobre los recursos (creación, borrado, cambios de configuración).

**Justificación**

- Proporciona una **visión unificada** del estado de los componentes de la arquitectura.  
- Permite definir **alertas** (por ejemplo, ante fallos, timeouts, saturación de CPU o uso excesivo de almacenamiento).  
- Log Analytics ofrece consultas avanzadas mediante KQL para análisis de errores y patrones de uso.  
- Los **Audit Logs** facilitan demostrar quién hizo qué cambio y cuándo, algo clave en contextos regulados.

**Equivalente local**

- Logs dispersos por contenedores y servidores sin panel unificado ni mecanismos formales de alertas ni auditoría.

---

#### Virtual Network, Network Security Groups, Private Endpoints, Private DNS Zone y Azure Firewall

**Función conjunta**

- Definir una **red privada** donde residen los componentes de la solución.  
- Controlar qué tráfico entra, sale y se mueve entre subredes mediante **NSG** y **Azure Firewall**.  
- Exponer el Data Lake, PostgreSQL y otros servicios PaaS sólo mediante **Private Endpoints**, con nombres resueltos por **Private DNS Zone**.

**Justificación**

- Aísla la solución del tráfico público por defecto; sólo se publica lo estrictamente necesario (por ejemplo, el acceso al dashboard).  
- Reduce la superficie de ataque al evitar endpoints públicos en servicios de datos.  
- Permite aplicar políticas de segmentación por capas (ingesta, procesamiento, datos, exposición) similares o superiores a las que se tenían en la red local.

---

#### Recovery Services Vault

**Función**

Administrador central de **backups** y restauraciones de los recursos más críticos de la solución.

**Justificación**

- Sustituye scripts manuales y copias en discos externos.  
- Permite definir políticas de respaldo y retención consistentes en el tiempo.  
- Facilita la recuperación ante desastres con tiempos de restauración más predecibles.
