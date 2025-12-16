## Justificación de la nube (Azure)

Para el desarrollo del caso **“Flight Delay and Causes”** se selecciona **Microsoft Azure** como plataforma cloud, debido a que ofrece un ecosistema integrado para **ingesta, almacenamiento, procesamiento, analítica y visualización** de datos, con capacidades nativas de **seguridad, gobierno y escalabilidad**.

### 1) Alineación con el tipo de datos y el objetivo analítico
El dataset contiene registros de vuelos y múltiples variables de retraso (por ejemplo: *CarrierDelay, WeatherDelay, NASDelay, SecurityDelay, LateAircraftDelay*), lo que requiere:
- **Carga de grandes volúmenes** (archivos tabulares tipo CSV/Parquet).
- **Transformaciones y limpieza** (tipos de datos, nulos, normalización a dimensiones/hechos).
- **Consultas analíticas** (KPIs y agregaciones por fecha, aerolínea y aeropuertos).

Azure facilita esta cadena de valor con servicios diseñados para analítica (Data Lake + procesamiento + motor SQL + BI).

### 2) Arquitectura recomendada y servicios Azure asociados
Azure permite implementar una arquitectura moderna tipo **Lakehouse / DWH** usando componentes administrados:

- **Azure Data Lake Storage Gen2 (ADLS Gen2):** almacenamiento económico y escalable para datos “brutos” (raw) y “curados” (silver/gold).
- **Azure Data Factory (ADF):** orquestación e ingesta de datos desde fuentes externas y automatización de pipelines ETL/ELT.
- **Azure Databricks o Azure Synapse (Spark):** procesamiento distribuido para transformaciones y preparación de datos.
- **Azure Synapse Analytics (SQL) / Azure SQL Database:** capa de consulta SQL para el modelo dimensional (tablas de hechos y dimensiones) y consumo analítico.
- **Power BI:** visualización y construcción de dashboards para analizar retrasos por aerolínea, rutas, fechas y causas.

Esta combinación reduce el esfuerzo de integración y acelera el tiempo de entrega del proyecto.

### 3) Escalabilidad y rendimiento
El volumen de datos puede crecer con nuevos periodos o fuentes (más aerolíneas, años, aeropuertos). Azure permite:
- **Escalar almacenamiento y cómputo bajo demanda**, pagando por uso.
- Manejar cargas variables (procesar lotes grandes en horas específicas y reducir recursos luego).
- Mejorar rendimiento con motores analíticos y particionamiento por fecha.

### 4) Seguridad, gobierno y control de acceso
Para un caso de datos analíticos, es importante controlar acceso y trazabilidad. Azure ofrece:
- **Azure Active Directory (Entra ID)** para autenticación y gestión de identidades.
- **RBAC** (control de acceso basado en roles) y políticas por recurso.
- **Cifrado en reposo y en tránsito** de forma nativa.
- Integración con gobierno/metadata (por ejemplo, catálogos y lineaje según el servicio elegido).

### 5) Mantenibilidad y enfoque “managed services”
Azure prioriza servicios administrados, lo cual:
- Reduce tareas operativas (parches, alta disponibilidad, backups).
- Facilita reproducibilidad (infra como código, pipelines versionados).
- Permite concentrarse en la lógica del modelo (dimensiones/hechos, vista semántica y KPIs).

### Elección
Se elige **Azure** por ser una plataforma robusta para proyectos de **analítica de datos**, con servicios integrados para construir un flujo completo **desde la ingesta hasta el consumo**, escalable, seguro y alineado con un modelo dimensional (hechos y dimensiones) como el utilizado en este proyecto.

