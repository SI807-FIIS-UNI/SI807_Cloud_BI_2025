# Documentación Técnica: Fase 3.1 - Ingesta y Estructuración (Capa Bronce)

## 1. Selección de Proveedor de Nube
Para la implementación de esta arquitectura de datos se ha seleccionado **Google Cloud Platform (GCP)**. La justificación técnica de esta decisión se basa en tres pilares fundamentales:

* **Desacoplamiento de Cómputo y Almacenamiento:** GCP permite escalar el almacenamiento (Cloud Storage) independientemente del procesamiento (BigQuery/Dataproc), lo que optimiza costos y flexibilidad operativa.
* **Capacidades Serverless:** El uso de BigQuery elimina la necesidad de gestionar infraestructura de servidores, permitiendo el procesamiento de grandes volúmenes de datos (1M+ registros) con baja latencia.
* **Integración Nativa:** La sinergia entre Cloud Shell, Cloud Storage y BigQuery facilita la creación de pipelines de datos mediante scripts CLI y Python sin configuraciones complejas de red.

## 2. Arquitectura de Almacenamiento (Data Lake)
Se ha implementado una arquitectura de medallón (Medallion Architecture) sobre Google Cloud Storage para garantizar la trazabilidad y calidad del dato. La estructura de carpetas definida es la siguiente:

* **`/bronce/raw`**: Zona de aterrizaje para datos crudos e inmutables. Aquí se almacena el archivo `data.csv` original tal como fue recibido, preservando la fuente de verdad.
* **`/bronce/processed`**: Zona para datos limpios y normalizados. Almacena las tablas de dimensiones (`dim_product.csv`, `dim_city.csv`, etc.) generadas tras la limpieza y validación de tipos de datos.
* **`/bronce/curated`**: Zona de consumo para negocio. Contiene los reportes finales y KPIs exportados, listos para ser consumidos por herramientas de visualización o analistas de datos.
* **`/docs`**: Repositorio de evidencias, logs de ejecución y gráficos generados durante el Análisis Exploratorio de Datos (EDA).

## 3. Estrategia de Ingesta
La ingesta de datos se realizó mediante **Google Cloud CLI (gsutil/gcloud storage)** desde el entorno de Cloud Shell.

* **Método:** Carga por lotes (Batch Upload).
* **Justificación:** Dado el volumen estático del dataset (aprox. 1 millón de registros), la carga vía CLI ofrece la mayor eficiencia y reproducibilidad mediante scripts, evitando errores manuales de interfaz gráfica.
* **Validación Inicial (EDA):** Se ejecutó un script en Python (`etl.py`) sobre una muestra estadística de los datos para identificar la estructura de las columnas, detectar la naturaleza anidada del campo `Product` y validar formatos de fecha antes de la carga masiva.