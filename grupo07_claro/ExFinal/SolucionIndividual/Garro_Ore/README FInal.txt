# Documentación Técnica: Solución BI End-to-End (Examen Final)

Curso: Sistema de Inteligencia de Negocios (SI 807-U)  
Alumno: Willian Jesús Garro Oré
  

## 1. Resumen de la Solución

Se ha implementado una arquitectura de datos moderna tipo ELT (Extract, Load, Transform) sobre Google Cloud Platform (GCP) para analizar el ausentismo en citas médicas. La solución procesa el dataset "Medical Appointment No Shows" migrando los datos desde un entorno local hacia un Data Lake en la nube, estructurando un Data Warehouse y finalizando con la visualización de KPIs.

### Arquitectura Lógica
La solución sigue el patrón de diseño Medallion:

1.  Capa Bronce (Raw Zone):Almacenamiento inmutable del archivo fuente en Cloud Storage.
2.  Capa Plata (Refined Zone):Datos limpios, tipados y modelados bajo esquema Estrella en BigQuery.
3.  Capa Oro (Aggregated Zone):Tablas sumarizadas orientadas a métricas de negocio para consumo de Dashboards.

---

## 2. Infraestructura y Configuración

Se han aprovisionado los siguientes recursos en el proyecto de GCP `sis-bi-2025-wgarro`:

* Google Cloud Storage (GCS):
    * Bucket: `gs://uni-datalake-bi-final/`
    * Ruta de Ingesta: `/landing/raw/dataset_citas.csv`
* Google BigQuery:
    * Dataset: `bi_citas_dw`
    * Tablas: `fact_citas`, `dim_paciente`, `dim_tiempo`, `dim_lugar`, `kpi_resumen_noshow`.
* Entorno de Ejecución:
    * Python 3.10 con librerías `pandas`, `google-cloud-storage`, `pandas-gbq`.

---

## 3. Flujo de Procesamiento y Ejecución

Los scripts se encuentran numerados secuencialmente en la carpeta `/src` para replicar el pipeline.

### Paso 1: Ingesta y Exploración (Capa Bronce)
* Script: `src/01_ingest_eda.py`
* Acción: Se utiliza el SDK de Python para subir el archivo local al bucket. Posteriormente, se ejecuta un análisis exploratorio (EDA) que valida la integridad de los datos (conteo de nulos, validación de tipos de datos en columnas `Age` y `ScheduledDay`).
* Resultado: Archivo disponible en `gs://uni-datalake-bi-final/landing/raw/`.

### Paso 2: Transformación y Modelado (Capa Plata)
* Script: `src/02_etl_silver.py`
* Limpieza de Datos:
    * Estandarización de nombres de columnas a *snake_case*.
    * Conversión de fechas (`ScheduledDay`, `AppointmentDay`) a formato `DATE` estándar ISO.
    * Codificación de variables categóricas (`No-show`: Yes=1, No=0) para facilitar agregaciones matemáticas.
    * Eliminación de registros inconsistentes (ej. Edad < 0).
* Modelado Dimensional (Esquema Estrella):
    * Hechos (`fact_citas`): Contiene las métricas y claves foráneas. Se calculó la métrica derivada `dias_anticipacion`.
    * Dimensiones:
	* `dim_paciente` (Atributos demográficos y patológicos).
        * `dim_lugar` (Ubicación geográfica/Barrios).
        * `dim_tiempo` (Desagregación temporal: día, mes, año, día de semana).
* Resultado: Tablas persistidas en BigQuery Dataset `bi_citas_dw`.

### Paso 3: Generación de Valor (Capa Oro)
* Script: `src/03_kpi_gold.py`
* Acción: Ejecución de consultas SQL sobre la capa plata para generar la tabla `kpi_resumen_noshow`.
* Lógica de Negocio: Se agruparon los datos por perfil demográfico y temporal para calcular la **Tasa de No-Show** porcentual pre-calculada. Esto optimiza el rendimiento del dashboard al evitar cálculos en tiempo de lectura.

---

## 4. Visualización

El reporte final se ha desplegado en Looker Studio conectando mediante el conector nativo de BigQuery a la tabla de la Capa Oro.

* KPIs Visualizados: Tasa de Ausentismo Global, Distribución por Género y Heatmap de Ausentismo por Barrio.
* Interactividad: Filtros dinámicos por Grupo Etario y Día de la Semana.

## 5. Justificación Técnica

1.  ¿Por qué Cloud Storage?
    Provee una capa de desacoplamiento necesaria. Almacenar el archivo *raw* asegura que siempre se pueda reprocesar la data desde cero en caso de errores en la lógica de transformación sin perder la fuente original.

2.  ¿Por qué BigQuery?
    Como almacén de datos *serverless*, permite ejecutar consultas analíticas complejas sobre el modelo estrella en milisegundos. Su integración nativa con las librerías de Python (`pandas-gbq`) facilita la carga de dataframes transformados sin necesidad de gestionar infraestructura de servidores (VMs).

3.  Estrategia de Modelado:
    Se optó por desnormalizar los datos del paciente en una dimensión separada (`dim_paciente`) para reducir la redundancia, ya que un mismo paciente puede tener múltiples citas. Esto reduce el costo de almacenamiento y mejora la consistencia de los atributos del paciente.