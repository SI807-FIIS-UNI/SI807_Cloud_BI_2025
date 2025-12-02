# Arquitectura Cloud Propuesta
## Diagrama Arquitectónico
<img width="7871" height="5438" alt="image" src="https://github.com/user-attachments/assets/2a3882db-c9d2-4007-bfa3-e83630772943" />

El siguiente diagrama presenta la arquitectura completa implementada en Microsoft Azure, diseñada para automatizar y modernizar el proceso ETL y la visualización de los niveles de madurez tecnológica (Practitioner y Continuous Integration) del BBVA. Esta solución reemplaza el entorno local basado en Hortonworks Sandbox con una infraestructura cloud-native, escalable, segura y altamente disponible, manteniendo fielmente la lógica (Bronce, Plata, Oro) definida en el proyecto original.

La arquitectura se organiza en cuatro capas principales: Sources, Process Backend, Store y Serve, integradas por servicios gestionados de Azure que garantizan un rendimiento óptimo y una gestión simplificada. En la base, se encuentran los servicios de seguridad y gobernanza (Virtual Network, Private Endpoints, Azure Key Vault, etc.) que protegen todo el flujo de datos.

## Descripción del Flujo de Datos
1. Ingesta Manual (Sources → Process Backend): El Service Owner descarga manualmente los archivos CSV de métricas desde la plataforma interna Marco Playbook. A través de la interfaz web (Frontend React), sube estos archivos a la aplicación. El backend Flask valida inmediatamente el esquema del archivo (nombres de columnas, formato) y lo almacena en la Capa Bronce (/bronze/data_sucia/) del Azure Data Lake Storage Gen2 (ADLS Gen2). Este paso asegura que solo se procesen archivos válidos y establece el punto de partida para el ETL.

2. Transformación (Process Backend → Store): El backend Flask ejecuta el proceso de transformación directamente en su entorno, utilizando la librería pandas. Este proceso incluye:
Limpieza de datos (eliminación de columnas irrelevantes, manejo de nulos).
Estandarización (conversión de fechas a MM/DD/YYYY, limpieza de separadores numéricos).
Cálculo de KPIs básicos (por ejemplo, rfo_ok_pct, adopcion_total_pct).
Los datos transformados se escriben en la Capa Plata (/silver/data_limpia/) del ADLS Gen2. Nota: Databricks está provisionado en el entorno, pero no participa en el flujo crítico de ETL. Se mantiene como recurso opcional para auditorías o replays manuales.

3. Carga a la Capa Oro (Process Backend → Store): La API Flask toma los datos limpios de la capa Plata y los carga en la base de datos relacional PostgreSQL Flexible Server. Esta carga sigue el modelo estrella definido en el informe:
Se crean las tablas de dimensiones (dim_tiempo, dim_geografia, dim_servicio_n1).
Se inserta la tabla de hechos (fact_mediciones_practitioner / fact_mediciones_ci).
Se generan y actualizan las vistas materializadas (vw_practitioner_kpis, vw_ci_kpis) que contienen los KPIs finales y están optimizadas para consultas rápidas.
Este paso convierte los datos en información analítica lista para consumo.

4. Almacenamiento y Acceso (Store → Serve): Los datos ya procesados y estructurados residen en la Capa Oro (data_oro_practitioner / data_oro_ci) de PostgreSQL. La API Flask actúa como intermediario, exponiendo endpoints seguros para consultar estos datos (por ejemplo, /summary, /data, /certification-summary). Esta capa es la fuente de verdad para todas las visualizaciones y reportes.

5. Visualización y Consumo (Serve): La API Flask sirve los datos a la aplicación frontend React Dashboard (desplegada en Azure Static Web Apps). El dashboard presenta múltiples vistas interactivas:
Global View: Resumen de KPIs clave, distribución de certificaciones por geografía y porcentaje de adopción.
Service Owner View: Análisis detallado por servicio, con gráficos evolutivos (líneas), radar y gauge charts.
El usuario final (Service Owners / Engineering Managers) interactúa con estas vistas para tomar decisiones basadas en datos.

## Mapeo: Arquitectura Local → Arquitectura Cloud
La migración de la arquitectura local (Hortonworks Sandbox) a Azure implicó un cambio de paradigma hacia servicios gestionados, eliminando la necesidad de administrar infraestructura y mejorando significativamente la confiabilidad y escalabilidad. A continuación se detalla el mapeo de componentes:

| **Componente Local (On-Premises)** | **Servicio Azure (Cloud)**                                        | **Justificación**                                                                              |
| ---------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Hadoop HDFS (Bronce/Plata)         | Azure Data Lake Storage Gen2                                      | Reemplaza el almacenamiento local con un sistema distribuido y escalable, compatible con HDFS. |
| Apache Zeppelin + PySpark          | Flask API (Python + pandas)                                       | Eliminación de dependencia de Spark; ETL simplificado y más económico.                         |
| PostgreSQL (Oro)                   | Azure Database for PostgreSQL – Flexible Server                   | Base relacional gestionada con HA, escalado automático y cifrado.                              |
| Docker (Backend y Frontend)        | Azure Container Apps (Backend) + Azure Static Web Apps (Frontend) | Orquestación sin servidor, escalado automático, CI/CD nativo y CDN global.                     |
| Interfaz React                     | Azure Static Web Apps                                             | Entrega global, SSL automático, integración con GitHub Actions.                                |
| Seguridad local limitada           | VNet, Private Endpoints, NSG, Key Vault, Monitor, Policy          | Seguridad empresarial: aislamiento, secretos, monitoreo, cumplimiento y gobernanza.            |


