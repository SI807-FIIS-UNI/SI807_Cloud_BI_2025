# Informe General del Proyecto

Este documento presenta una **visión global y ordenada** del proyecto, describiendo cada una de las etapas del flujo **End-to-End**, desde la configuración inicial del entorno hasta la visualización final en Power BI.

El proyecto implementa una arquitectura de **Inteligencia de Negocios en la nube con Google Cloud Platform**, orientada al análisis epidemiológico y soporte a la toma de decisiones.

---

## Estructura del Proyecto

Cada sección del informe documenta una fase específica del ciclo de vida del dato. Los enlaces permiten acceder al detalle técnico y funcional de cada etapa.

1. **Configuración Inicial del Entorno**
   Preparación del proyecto en Google Cloud Platform, habilitación de servicios y definición de la base tecnológica.

   📁 [`1_Entorno/README.md`](1_Entorno/README.md)

2. **Configuración de Seguridad e IAM**
   Gestión de identidades, permisos y cuentas de servicio necesarias para la ejecución segura del pipeline.

   📁 [`2_Seguridad/README.md`](2_Seguridad/README.md)

3. **Extracción de Datos y Carga al Data Lake**
   Obtención de archivos CSV y carga inicial en Cloud Storage (capa Bronce).

   📁 [`3_Extracción/README.md`](3_Extracción/README.md)

4. **Transformación de Datos y Procesamiento con Dataproc**
   Implementación del proceso ETL mediante PySpark, incluyendo la habilitación y uso de Dataproc Serverless para las capas Plata y Oro.

   📁 [`4_Transformacion/README.md`](4_Transformacion/README.md)

5. **Carga a BigQuery y Construcción de KPIs**
   Almacenamiento de los datos procesados en BigQuery y creación de queries para indicadores clave de negocio.

   📁 [`5_Carga/README.md`](5_Carga/README.md)

6. **Orquestación del Proceso ETL**
   Automatización del pipeline mediante Cloud Run Functions, activadas por eventos en Cloud Storage.

   📁 [`6_Orquestacion/README.md`](6_Orquestacion/README.md)

7. **Visualización y Análisis en Power BI**
   Conexión con BigQuery, modelado visual y diseño del dashboard final para análisis epidemiológico.

   📁 [`7_Visualizacion/README.md`](7_Visualizacion/README.md)

---

## Resultado Final

La integración de estas etapas permite contar con una solución:

* Totalmente automatizada
* Escalable y orientada a eventos
* Basada en buenas prácticas de arquitectura cloud
* Enfocada en análisis de datos de salud y soporte a decisiones estratégicas

Este informe general actúa como **guía de navegación del repositorio** y como resumen ejecutivo del proyecto completo.