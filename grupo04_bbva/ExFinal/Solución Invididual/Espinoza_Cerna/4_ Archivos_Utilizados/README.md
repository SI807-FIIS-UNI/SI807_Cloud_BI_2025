# Proyecto de Análisis de Retrasos de Vuelos

Este proyecto implementa una plataforma de datos de extremo a extremo en Azure para analizar los retrasos de los vuelos. La solución permite a los usuarios cargar un conjunto de datos, procesarlo a través de un pipeline ETL moderno y visualizar los resultados y KPIs en un dashboard interactivo.

## ✈️ Arquitectura General

La aplicación sigue una arquitectura desacoplada y basada en eventos, utilizando tecnologías modernas de la nube para garantizar la escalabilidad, seguridad y eficiencia. El flujo de trabajo principal es el siguiente:

1. **Carga de Datos**: El usuario sube un archivo `flight_delay.csv` a través del **Frontend** (React).
2. **Recepción y Almacenamiento**: El **Backend** (Flask) recibe el archivo, valida sus encabezados y lo almacena en la capa **Bronce** (datos crudos) de un Azure Data Lake Storage (ADLS Gen2).
3. **Orquestación del Pipeline**: El Backend invoca la API de Databricks para ejecutar una secuencia de notebooks en un clúster de trabajo efímero (serverless), iniciando el proceso ETL.
4. **Procesamiento ETL (Arquitectura Medallion)**:
   - **Bronce a Plata**: Un notebook de Databricks (`Limpiar.py`) lee los datos crudos, los limpia, estandariza tipos de datos y los guarda en formato Delta en la capa **Plata**.
   - **Plata a Oro**: Otro notebook (`Transformar.py`) lee los datos limpios de la capa Plata, los modela en un esquema de estrella (hechos y dimensiones) y los carga en una base de datos **Azure PostgreSQL**, que actúa como la capa **Oro**.
   - **Capa Semántica**: Un último notebook (`Vista.py`) crea vistas SQL sobre las tablas de la capa Oro para pre-calcular KPIs y simplificar las consultas.
5. **Visualización de Datos**: El **Frontend** consulta los endpoints del **Backend** para obtener los datos. El Backend, a su vez, consulta las vistas en PostgreSQL y devuelve los KPIs y los datos detallados para ser mostrados en los dashboards.
6. **Infraestructura y Despliegue**: Toda la infraestructura de Azure se provisiona mediante **Terraform (IaC)**, y los despliegues de la aplicación se automatizan a través de **GitHub Actions (CI/CD)**.

---

## 📂 Estructura del Proyecto

El repositorio está organizado en carpetas que representan cada componente principal de la solución:
```plaintext
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml       # Build & push de imagen Docker y deploy del Backend a Azure Container Apps.
│       ├── deploy-frontend.yml      # Build y deploy del Frontend a Azure Static Web App.
│       ├── deploy-databricks.yml    # Ejecución / despliegue de notebooks y configuración en Databricks.
│       ├── deploy-postgres.yml      # Inicialización y/o migraciones del esquema en PostgreSQL.
│       ├── infra-deploy.yml         # Terraform init, plan y apply para el despliegue de infraestructura.
│       └── infra-destroy.yml        # Terraform destroy controlado para eliminación de infraestructura.
│
├── 1-infrastructure/
│   ├── modules/                     # Módulos reutilizables de Terraform.
│   │   ├── alerts/                  # Alertas de monitoreo (Azure Monitor).
│   │   ├── backup_vault/            # Backup Vault y políticas de respaldo.
│   │   ├── container_app/           # Azure Container Apps para el backend.
│   │   ├── container_registry/      # Azure Container Registry (ACR).
│   │   ├── databricks_config/       # Configuración adicional del workspace Databricks.
│   │   ├── databricks_workspace/    # Workspace de Azure Databricks.
│   │   ├── firewall/                # Azure Firewall y reglas asociadas.
│   │   ├── key_vault/               # Azure Key Vault para secretos y credenciales.
│   │   ├── log_analytics/           # Log Analytics Workspace.
│   │   ├── network/                 # VNet, subnets y endpoints privados.
│   │   ├── postgresql/              # Azure Database for PostgreSQL.
│   │   ├── resource_group/          # Resource Groups base del proyecto.
│   │   ├── route_table/             # Tablas de ruteo de red.
│   │   ├── static_web_app/          # Azure Static Web App para el frontend.
│   │   └── storage/                 # Azure Storage / Data Lake Gen2.
│   │
│   ├── main.tf                      # Orquestación principal de los módulos Terraform.
│   ├── variables.tf                 # Definición de variables.
│   ├── outputs.tf                   # Outputs expuestos para pipelines y otros módulos.
│   └── terraform.tfvars             # Valores de variables (sin secretos).
│
├── 2-database/
│   └── query.sql                    # Script DDL para creación del modelo (estrella) en PostgreSQL.
│
├── 3-databricks-notebooks/
│   ├── Limpiar.py                   # Proceso Bronce → Plata.
│   ├── Transformar.py               # Proceso Plata → Oro.
│   └── Vista.py                     # Creación de vistas semánticas en la capa Oro.
│
├── 4-backend/
│   ├── routes.py                    # Definición de endpoints de la API Flask.
│   ├── database.py                  # Conexión y consultas a PostgreSQL.
│   ├── databricks_client.py         # Cliente para interactuar con la API de Databricks.
│   ├── azure_storage.py             # Acceso a Azure Data Lake Storage.
│   ├── config.py                    # Gestión de configuración y variables de entorno.
│   ├── requirements.txt             # Dependencias del backend.
│   └── Dockerfile                   # Imagen del contenedor del backend.
│
├── 5-frontend/
│   ├── src/
│   │   ├── components/              # Componentes React.
│   │   │   ├── FileUpload.jsx
│   │   │   ├── KpiDashboard.jsx
│   │   │   └── FlightExplorer.jsx
│   │   ├── services/                # Lógica de consumo de la API backend.
│   │   └── App.jsx                  # Componente raíz y enrutador.
│   ├── index.html
│   ├── package.json
│   └── vite.config.js               # Configuración de Vite.
│
└── README.md                        # Descripción general del proyecto, arquitectura y pipelines.
```

---

## 🧩 Componentes Detallados

### 1. Infraestructura como Código (`1-infrastructure`)

Utiliza **Terraform** para definir y provisionar todos los recursos de Azure de manera declarativa y reproducible. El código está modularizado para facilitar su mantenimiento.

**Recursos Clave:**
- **Red**: Una VNet con subredes dedicadas y endpoints privados para asegurar la comunicación interna.
- **Almacenamiento**: Azure Data Lake Storage Gen2 con contenedores para las capas `bronze` y `silver`.
- **Base de Datos**: Azure Database for PostgreSQL (Flexible Server) para la capa `gold`.
- **Procesamiento**: Azure Databricks Workspace con SKU `premium` para soportar trabajos serverless.
- **Aplicaciones**: Azure Container App para el backend y Azure Static Web App para el frontend.
- **Seguridad**: Azure Key Vault para la gestión centralizada de secretos.
- **CI/CD**: Azure Container Registry para almacenar la imagen Docker del backend.

### 2. Base de Datos (`2-database`)

Contiene el script `query.sql` que define el **modelo en estrella** en la base de datos PostgreSQL. Este modelo es ideal para consultas analíticas y de BI.

- **Tablas de Dimensiones**: `dim_date`, `dim_airline`, `dim_airport`, `dim_aircraft`.
- **Tabla de Hechos**: `fact_flight_delays`, que contiene las métricas y las claves foráneas a las dimensiones.
- **Vistas Analíticas**:
  - `vw_flight_analytics`: Para exploración detallada de vuelos.
  - `vw_flight_kpis`: Para KPIs agregados que alimentan el dashboard principal.

### 3. Notebooks de Databricks (`3-databricks-notebooks`)

Implementan el pipeline ETL siguiendo la **Arquitectura Medallion**.

- **`Limpiar.py` (Bronce → Plata)**: Lee el CSV crudo, corrige tipos de datos, maneja nulos y guarda los datos limpios en formato Delta.
- **`Transformar.py` (Plata → Oro)**: Carga los datos limpios de la capa Plata, crea las tablas de hechos y dimensiones y las puebla en PostgreSQL.
- **`Vista.py` (Capa Semántica)**: Se ejecuta al final para actualizar las vistas SQL en PostgreSQL, asegurando que los dashboards siempre tengan acceso a los datos más recientes de forma optimizada.

### 4. Backend (`4-backend`)

Desarrollado en **Flask**, actúa como el cerebro de la aplicación.

**Endpoints de API:**
- `/api/upload`: Recibe el archivo CSV, lo valida y lo sube a ADLS.
- `/api/flights/kpis`: Proporciona los datos agregados para el dashboard de KPIs.
- `/api/flights/explore`: Proporciona datos detallados para el explorador de vuelos.
- `/api/flights/filters`: Devuelve las opciones disponibles para los filtros del UI.

**Características:**
- **Orquestación**: Se comunica con la API de Databricks para lanzar los trabajos de procesamiento de forma asíncrona.
- **Contenerización**: Está diseñado para ser empaquetado en una imagen Docker y desplegado en Azure Container Apps.

### 5. Frontend (`5-frontend`)

Una interfaz de usuario moderna construida con **React** y **Tailwind CSS**.

- **Subida de Archivos**: Un componente intuitivo para que el usuario cargue el archivo `flight_delay.csv`. Muestra el estado del procesamiento en tiempo real.
- **Dashboard de KPIs**: Una vista que presenta los indicadores clave de rendimiento (KPIs) de forma agregada, con filtros interactivos y paginación.
- **Explorador de Vuelos**: Una tabla que permite explorar los datos de cada vuelo de forma detallada, también con filtros y paginación.

---

## 🚀 Configuración de GitHub Actions

### Requisitos Previos

Antes de configurar los pipelines de CI/CD, necesitas tener lo siguiente:

1. **Una cuenta de Azure** con permisos para crear recursos y Service Principals.
2. **Un repositorio de GitHub** donde alojarás este proyecto.
3. **Azure CLI** instalado en tu máquina local para crear el Service Principal.

### Paso 1: Crear un Service Principal en Azure

El Service Principal es una identidad que GitHub Actions utilizará para autenticarse con Azure y desplegar recursos.

Ejecuta los siguientes comandos en tu terminal:
```bash
# Inicia sesión en Azure
az login

# Crea un Service Principal con rol Contributor en tu suscripción
az ad sp create-for-rbac --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/{SUBSCRIPTION_ID} \
  --sdk-auth
```

**Nota**: Reemplaza `{SUBSCRIPTION_ID}` con tu ID de suscripción de Azure. Puedes obtenerlo ejecutando `az account show --query id -o tsv`.

Este comando generará un JSON similar a este:
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**Guarda estos valores de forma segura**, los necesitarás para configurar los secretos en GitHub.

### Paso 2: Configurar Secretos del Repositorio

Los secretos son valores sensibles que no deben ser expuestos en el código. Configúralos en tu repositorio de GitHub:

1. Ve a tu repositorio en GitHub.
2. Navega a **Settings** → **Secrets and variables** → **Actions** → **Secrets**.
3. Haz clic en **New repository secret** y agrega los siguientes secretos:

| Nombre del Secreto | Descripción | Valor |
|-------------------|-------------|-------|
| `ARM_CLIENT_ID` | ID del Service Principal (clientId del JSON) | El valor de `clientId` del JSON generado |
| `ARM_CLIENT_SECRET` | Secreto del Service Principal (clientSecret del JSON) | El valor de `clientSecret` del JSON generado |
| `ARM_SUBSCRIPTION_ID` | ID de tu suscripción de Azure | El valor de `subscriptionId` del JSON generado |
| `ARM_TENANT_ID` | ID del tenant de Azure Active Directory | El valor de `tenantId` del JSON generado |

### Paso 3: Estructura de Archivos en el Repositorio

Para que GitHub Actions funcione correctamente, asegúrate de que todos los archivos estén ubicados en la raíz de tu repositorio de GitHub con la estructura mencionada anteriormente.

**Estructura completa del repositorio:**
```
tu-repositorio/
├── .github/
│   └── workflows/
│       ├── infra-deploy.yml
│       ├── infra-destroy.yml
│       ├── deploy-backend.yml
│       ├── deploy-frontend.yml
│       ├── deploy-databricks.yml
│       └── deploy-postgres.yml
├── 1-infrastructure/
├── 2-database/
├── 3-databricks-notebooks/
├── 4-backend/
├── 5-frontend/
└── README.md
```

### Paso 4: Descripción de los Pipelines

#### 4.1 `infra-deploy.yml` - Despliegue de Infraestructura

**Propósito**: Aprovisionar todos los recursos de Azure utilizando Terraform.

**Cuándo se ejecuta**: 
- Manualmente desde la pestaña "Actions" de GitHub.
- Automáticamente cuando se hacen cambios en la carpeta `1-infrastructure/` y se hace push a la rama `main`.

**Qué hace**:
1. Configura Terraform en el runner de GitHub Actions.
2. Inicializa el backend de Terraform (state file en Azure Storage).
3. Ejecuta `terraform plan` para mostrar los cambios que se aplicarán.
4. Ejecuta `terraform apply` para crear o actualizar los recursos en Azure.

**Variables que utiliza**: `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID`.

**Resultado**: Infraestructura de Azure completamente desplegada y lista para ser utilizada.

#### 4.2 `infra-destroy.yml` - Eliminación de Infraestructura

**Propósito**: Eliminar todos los recursos de Azure de forma controlada.

**Cuándo se ejecuta**: Manualmente desde la pestaña "Actions" de GitHub (requiere confirmación).

**Qué hace**:
1. Ejecuta `terraform destroy` para eliminar todos los recursos aprovisionados.
2. Útil para entornos de desarrollo/pruebas o cuando deseas limpiar completamente el proyecto.

**⚠️ Advertencia**: Este pipeline eliminará permanentemente todos los recursos. Úsalo con precaución.

#### 4.3 `deploy-backend.yml` - Despliegue del Backend

**Propósito**: Construir la imagen Docker del backend, subirla a Azure Container Registry y desplegarla en Azure Container Apps.

**Cuándo se ejecuta**:
- Automáticamente cuando se hacen cambios en la carpeta `4-backend/` y se hace push a la rama `main`.
- Manualmente desde la pestaña "Actions".

**Qué hace**:
1. Construye la imagen Docker del backend utilizando el `Dockerfile` en `4-backend/`.
2. Autentica con Azure Container Registry (ACR).
3. Etiqueta y sube la imagen a ACR.
4. Actualiza Azure Container Apps para usar la nueva versión de la imagen.

**Variables que utiliza**: `ARM_CLIENT_ID`, `ARM_CLIENT_SECRET`, `CONTAINER_REGISTRY_NAME`, `CONTAINER_APP_NAME`.

**Resultado**: Backend actualizado y ejecutándose en Azure Container Apps.

#### 4.4 `deploy-frontend.yml` - Despliegue del Frontend

**Propósito**: Construir la aplicación React del frontend y desplegarla en Azure Static Web Apps.

**Cuándo se ejecuta**:
- Automáticamente cuando se hacen cambios en la carpeta `5-frontend/` y se hace push a la rama `main`.
- Manualmente desde la pestaña "Actions".

**Qué hace**:
1. Instala las dependencias de Node.js (`npm install`).
2. Ejecuta el build de producción de Vite (`npm run build`).
3. Despliega los archivos estáticos generados en Azure Static Web Apps.

**Variables que utiliza**: Token de despliegue de Azure Static Web Apps (generado automáticamente por Azure).

**Resultado**: Frontend actualizado y disponible en la URL de tu Static Web App.

#### 4.5 `deploy-databricks.yml` - Despliegue de Notebooks de Databricks

**Propósito**: Subir y actualizar los notebooks de Databricks en el workspace.

**Cuándo se ejecuta**:
- Automáticamente cuando se hacen cambios en la carpeta `3-databricks-notebooks/` y se hace push a la rama `main`.
- Manualmente desde la pestaña "Actions".

**Qué hace**:
1. Autentica con Databricks usando el token de acceso.
2. Sube los notebooks (`Limpiar.py`, `Transformar.py`, `Vista.py`) al workspace de Databricks.
3. Opcionalmente, puede ejecutar los notebooks para validar que funcionan correctamente.

**Variables que utiliza**: `DATABRICKS_HOST`, `DATABRICKS_TOKEN`.

**Resultado**: Notebooks actualizados en Databricks y listos para ser ejecutados por el backend.

#### 4.6 `deploy-postgres.yml` - Inicialización de Base de Datos

**Propósito**: Ejecutar scripts SQL para crear o actualizar el esquema de la base de datos PostgreSQL.

**Cuándo se ejecuta**:
- Automáticamente cuando se hacen cambios en la carpeta `2-database/` y se hace push a la rama `main`.
- Manualmente desde la pestaña "Actions".

**Qué hace**:
1. Se conecta a Azure Database for PostgreSQL.
2. Ejecuta el script `query.sql` que contiene las definiciones de tablas, vistas y esquema en estrella.

**Variables que utiliza**: `POSTGRES_CONNECTION_STRING`.

**Resultado**: Base de datos con el esquema actualizado y lista para recibir datos del pipeline ETL.

### Paso 5: Orden de Ejecución Recomendado

Para un despliegue desde cero, sigue este orden:

1. **`infra-deploy.yml`**: Despliega toda la infraestructura de Azure.
2. **`deploy-postgres.yml`**: Inicializa el esquema de la base de datos.
3. **`deploy-databricks.yml`**: Sube los notebooks al workspace de Databricks.
4. **`deploy-backend.yml`**: Despliega el backend.
5. **`deploy-frontend.yml`**: Despliega el frontend.

Una vez completados estos pasos, la aplicación estará completamente funcional.

### Paso 6: Verificación del Despliegue

Después de ejecutar todos los pipelines:

1. **Verifica la infraestructura**: Accede al portal de Azure y confirma que todos los recursos se hayan creado correctamente en tu Resource Group.
2. **Prueba el backend**: Accede a la URL de tu Azure Container App y verifica que los endpoints de la API respondan correctamente.
3. **Prueba el frontend**: Navega a la URL de tu Azure Static Web App y verifica que la interfaz se cargue correctamente.
4. **Prueba el flujo completo**: Sube un archivo `flight_delay.csv` a través del frontend y verifica que el pipeline ETL se ejecute y los datos aparezcan en los dashboards.

---

