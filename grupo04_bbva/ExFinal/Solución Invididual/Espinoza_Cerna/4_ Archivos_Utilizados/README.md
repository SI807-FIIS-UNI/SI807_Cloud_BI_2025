# Proyecto de Análisis de Retrasos de Vuelos

Este proyecto implementa una plataforma de datos de extremo a extremo en Azure para analizar los retrasos de los vuelos. La solución permite a los usuarios cargar un conjunto de datos, procesarlo a través de un pipeline ETL moderno y visualizar los resultados y KPIs en un dashboard interactivo.

## ✈️ Arquitectura General

La aplicación sigue una arquitectura desacoplada y basada en eventos, utilizando tecnologías modernas de la nube para garantizar la escalabilidad, seguridad y eficiencia.

El flujo de trabajo principal es el siguiente:

1.  **Carga de Datos**: El usuario sube un archivo `flight_delay.csv` a través del **Frontend** (React).
2.  **Recepción y Almacenamiento**: El **Backend** (Flask) recibe el archivo, valida sus encabezados y lo almacena en la capa **Bronce** (datos crudos) de un Azure Data Lake Storage (ADLS Gen2).
3.  **Orquestación del Pipeline**: El Backend invoca la API de Databricks para ejecutar una secuencia de notebooks en un clúster de trabajo efímero (serverless), iniciando el proceso ETL.
4.  **Procesamiento ETL (Arquitectura Medallion)**:
   *   **Bronce a Plata**: Un notebook de Databricks (`Limpiar.py`) lee los datos crudos, los limpia, estandariza tipos de datos y los guarda en formato Delta en la capa **Plata**.
   *   **Plata a Oro**: Otro notebook (`Transformar.py`) lee los datos limpios de la capa Plata, los modela en un esquema de estrella (hechos y dimensiones) y los carga en una base de datos **Azure PostgreSQL**, que actúa como la capa **Oro**.
   *   **Capa Semántica**: Un último notebook (`Vista.py`) crea vistas SQL sobre las tablas de la capa Oro para pre-calcular KPIs y simplificar las consultas.
5.  **Visualización de Datos**: El **Frontend** consulta los endpoints del **Backend** para obtener los datos. El Backend, a su vez, consulta las vistas en PostgreSQL y devuelve los KPIs y los datos detallados para ser mostrados en los dashboards.
6.  **Infraestructura y Despliegue**: Toda la infraestructura de Azure se provisiona mediante **Terraform (IaC)**, y los despliegues de la aplicación se automatizan a través de **GitHub Actions (CI/CD)**.

---

## 📂 Estructura del Proyecto

El repositorio está organizado en carpetas que representan cada componente principal de la solución:

```plaintext
├── .github/
│   └── workflows/
│       ├── deploy-backend.yml     # Build & push de imagen Docker y deploy del Backend a Azure Container Apps.
│       ├── deploy-frontend.yml    # Build y deploy del Frontend a Azure Static Web App.
│       ├── deploy-databricks.yml  # Ejecución / despliegue de notebooks y configuración en Databricks.
│       ├── deploy-postgres.yml    # Inicialización y/o migraciones del esquema en PostgreSQL.
│       ├── infra-deploy.yml       # Terraform init, plan y apply para el despliegue de infraestructura.
│       └── infra-destroy.yml      # Terraform destroy controlado para eliminación de infraestructura.
│
├── 1-infrastructure/
│   ├── modules/                   # Módulos reutilizables de Terraform.
│   │   ├── alerts/                # Alertas de monitoreo (Azure Monitor).
│   │   ├── backup_vault/          # Backup Vault y políticas de respaldo.
│   │   ├── container_app/         # Azure Container Apps para el backend.
│   │   ├── container_registry/    # Azure Container Registry (ACR).
│   │   ├── databricks_config/     # Configuración adicional del workspace Databricks.
│   │   ├── databricks_workspace/  # Workspace de Azure Databricks.
│   │   ├── firewall/              # Azure Firewall y reglas asociadas.
│   │   ├── key_vault/             # Azure Key Vault para secretos y credenciales.
│   │   ├── log_analytics/          # Log Analytics Workspace.
│   │   ├── network/               # VNet, subnets y endpoints privados.
│   │   ├── postgresql/             # Azure Database for PostgreSQL.
│   │   ├── resource_group/        # Resource Groups base del proyecto.
│   │   ├── route_table/            # Tablas de ruteo de red.
│   │   ├── static_web_app/         # Azure Static Web App para el frontend.
│   │   └── storage/                # Azure Storage / Data Lake Gen2.
│   │
│   ├── main.tf                    # Orquestación principal de los módulos Terraform.
│   ├── variables.tf               # Definición de variables.
│   ├── outputs.tf                 # Outputs expuestos para pipelines y otros módulos.
│   └── terraform.tfvars           # Valores de variables (sin secretos).
│
├── 2-database/
│   └── query.sql                  # Script DDL para creación del modelo (estrella) en PostgreSQL.
│
├── 3-databricks-notebooks/
│   ├── Limpiar.py                 # Proceso Bronce → Plata.
│   ├── Transformar.py             # Proceso Plata → Oro.
│   └── Vista.py                   # Creación de vistas semánticas en la capa Oro.
│
├── 4-backend/
│   ├── routes.py                  # Definición de endpoints de la API Flask.
│   ├── database.py                # Conexión y consultas a PostgreSQL.
│   ├── databricks_client.py       # Cliente para interactuar con la API de Databricks.
│   ├── azure_storage.py           # Acceso a Azure Data Lake Storage.
│   ├── config.py                  # Gestión de configuración y variables de entorno.
│   ├── requirements.txt           # Dependencias del backend.
│   └── Dockerfile                 # Imagen del contenedor del backend.
│
├── 5-frontend/
│   ├── src/
│   │   ├── components/            # Componentes React.
│   │   │   ├── FileUpload.jsx
│   │   │   ├── KpiDashboard.jsx
│   │   │   └── FlightExplorer.jsx
│   │   ├── services/              # Lógica de consumo de la API backend.
│   │   └── App.jsx                # Componente raíz y enrutador.
│   ├── index.html
│   ├── package.json
│   └── vite.config.js             # Configuración de Vite.
│
└── README.md                      # Descripción general del proyecto, arquitectura y pipelines.
```

---

## 🧩 Componentes Detallados

### 1. Infraestructura como Código (`1-infrastructure`)

Utiliza **Terraform** para definir y provisionar todos los recursos de Azure de manera declarativa y reproducible. El código está modularizado para facilitar su mantenimiento.

*   **Recursos Clave**:
    *   **Red**: Una VNet con subredes dedicadas y endpoints privados para asegurar la comunicación interna.
    *   **Almacenamiento**: Azure Data Lake Storage Gen2 con contenedores para las capas `bronze` y `silver`.
    *   **Base de Datos**: Azure Database for PostgreSQL (Flexible Server) para la capa `gold`.
    *   **Procesamiento**: Azure Databricks Workspace con SKU `premium` para soportar trabajos serverless.
    *   **Aplicaciones**: Azure Container App para el backend y Azure Static Web App para el frontend.
    *   **Seguridad**: Azure Key Vault para la gestión centralizada de secretos.
    *   **CI/CD**: Azure Container Registry para almacenar la imagen Docker del backend.

### 2. Base de Datos (`2-database`)

Contiene el script `query.sql` que define el **modelo en estrella** en la base de datos PostgreSQL. Este modelo es ideal para consultas analíticas y de BI.

*   **Tablas de Dimensiones**: `dim_date`, `dim_airline`, `dim_airport`, `dim_aircraft`.
*   **Tabla de Hechos**: `fact_flight_delays`, que contiene las métricas y las claves foráneas a las dimensiones.
*   **Vistas Analíticas**:
    *   `vw_flight_analytics`: Para exploración detallada de vuelos.
    *   `vw_flight_kpis`: Para KPIs agregados que alimentan el dashboard principal.

### 3. Notebooks de Databricks (`3-databricks-notebooks`)

Implementan el pipeline ETL siguiendo la **Arquitectura Medallion**.

*   **`Limpiar.py` (Bronce → Plata)**: Lee el CSV crudo, corrige tipos de datos, maneja nulos y guarda los datos limpios en formato Delta.
*   **`Transformar.py` (Plata → Oro)**: Carga los datos limpios de la capa Plata, crea las tablas de hechos y dimensiones y las puebla en PostgreSQL.
*   **`Vista.py` (Capa Semántica)**: Se ejecuta al final para crear o actualizar las vistas SQL en PostgreSQL, asegurando que los dashboards siempre tengan acceso a los datos más recientes de forma optimizada.

### 4. Backend (`4-backend`)

Desarrollado en **Flask**, actúa como el cerebro de la aplicación.

*   **Endpoints de API**:
    *   `/api/upload`: Recibe el archivo CSV, lo valida y lo sube a ADLS.
    *   `/api/flights/kpis`: Proporciona los datos agregados para el dashboard de KPIs.
    *   `/api/flights/explore`: Proporciona datos detallados para el explorador de vuelos.
    *   `/api/flights/filters`: Devuelve las opciones disponibles para los filtros del UI.
*   **Orquestación**: Se comunica con la API de Databricks para lanzar los trabajos de procesamiento de forma asíncrona.
*   **Contenerización**: Está diseñado para ser empaquetado en una imagen Docker y desplegado en Azure Container Apps.

### 5. Frontend (`5-frontend`)

Una interfaz de usuario moderna construida con **React** y **Tailwind CSS**.

*   **Subida de Archivos**: Un componente intuitivo para que el usuario cargue el archivo `flight_delay.csv`. Muestra el estado del procesamiento en tiempo real.
*   **Dashboard de KPIs**: Una vista que presenta los indicadores clave de rendimiento (KPIs) de forma agregada, con filtros interactivos y paginación.
*   **Explorador de Vuelos**: Una tabla que permite explorar los datos de cada vuelo de forma detallada, también con filtros y paginación.

### 6. CI/CD (`.github/workflows`)

Los pipelines de **GitHub Actions** automatizan el ciclo de vida del desarrollo y despliegue.

*   **`terraform.yml`**: Se activa en cambios a la carpeta `1-infrastructure`. Ejecuta `terraform plan` y `terraform apply` para mantener la infraestructura de Azure sincronizada con el código.
*   **`backend.yml`**: Construye la imagen Docker del backend, la publica en Azure Container Registry y despliega la nueva versión en Azure Container Apps.
*   **`frontend.yml`**: Construye la aplicación de React y la despliega en Azure Static Web Apps.

---

## 🚀 Cómo Empezar

1.  **Desplegar la Infraestructura**:
    *   Configura tus credenciales de Azure en los secretos de GitHub.
    *   Realiza un `push` a la rama `main` para activar el workflow de Terraform.

2.  **Desplegar las Aplicaciones**:
    *   Realiza cambios en las carpetas `4-backend` o `5-frontend` y haz `push` para activar sus respectivos pipelines de despliegue.

3.  **Usar la Aplicación**:
    *   Navega a la URL de la Static Web App.
    *   En la pestaña "Subir Archivo", selecciona el archivo `flight_delay.csv` y haz clic en "Subir y Procesar".
    *   Espera a que el pipeline finalice.
    *   Navega a las pestañas "Dashboard de KPIs" o "Explorador de Vuelos" para analizar los datos.
