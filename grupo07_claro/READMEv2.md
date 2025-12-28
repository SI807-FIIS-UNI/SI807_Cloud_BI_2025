cat <<EOF > README.md

**# Examen Final: Sistema de Inteligencia de Negocios en GCP**



\*\*Estudiante:\*\* Willian Garro  

\*\*Curso:\*\* Sistema de Inteligencia de Negocios (SI 807-U)  

\*\*Fecha:\*\* Diciembre 2025  

\*\*Proyecto:\*\* Análisis de Ausentismo en Citas Médicas (No-Show Analytics)



---



**## 1. Selección de la Nube y Justificación Técnica (Rúbrica 3.1)**



Para la implementación de esta solución de Business Intelligence, se ha seleccionado \*\*Google Cloud Platform (GCP)\*\* basándose en los siguientes criterios técnicos:



1\.  \*\*Almacenamiento Escalable (Google Cloud Storage):\*\* Se utiliza GCS como \*Data Lake\* debido a su durabilidad del 99.99% y su capacidad para manejar datos no estructurados (CSV crudos) a bajo costo, facilitando la arquitectura de capas (Bronce/Raw).

2\.  \*\*Procesamiento Serverless (Cloud Shell + Python):\*\* El uso de Cloud Shell con Python preinstalado permite un despliegue inmediato de pipelines ETL sin necesidad de aprovisionar máquinas virtuales complejas, ideal para entornos ágiles y académicos.

3\.  \*\*Data Warehouse Nativo (BigQuery):\*\* Es el corazón de la solución. Permite consultas SQL de alta velocidad sobre grandes volúmenes de datos. Su arquitectura sin servidor escala automáticamente, separando el cómputo del almacenamiento.



---



**## 2. Arquitectura de Datos y Modelo Dimensional (Rúbrica 3.2)**



La solución sigue una arquitectura \*\*ELT/ETL por Capas (Medallion Architecture)\*\*:



\### 2.1 Flujo de Datos

\* \*\*Capa Bronce (Raw):\*\* Archivos CSV originales almacenados en GCS (`gs://.../bronce/raw`). Sin modificaciones.

\* \*\*Capa Plata (Trusted/Processed):\*\* Datos limpios, tipados y estructurados en un \*\*Modelo Estrella\*\* almacenados en BigQuery (`silver\_layer`).

\* \*\*Capa Oro (Refined):\*\* Tablas agregadas y KPIs listos para consumo por herramientas de visualización (`gold\_layer`).



\### 2.2 Justificación del Modelo Estrella

Se ha diseñado un esquema dimensional (Modelo Estrella) para optimizar el rendimiento de lectura (OLAP) y simplificar la creación de Dashboards.



\* \*\*Tabla de Hechos (`fact\_citas`):\*\* Contiene las métricas cuantitativas y claves foráneas.

&nbsp;   \* \*Granularidad:\* Una fila por cita médica.

&nbsp;   \* \*Métricas:\* `is\_noshow` (indicador de falta), `sms\_received`.

\* \*\*Dimensiones:\*\*

&nbsp;   \* \*\*`dim\_paciente`:\*\* Atributos del paciente (Género, Edad, Enfermedades base). Se desnormalizó para reducir JOINS complejos.

&nbsp;   \* \*\*`dim\_ubicacion`:\*\* Barrios y zonas geográficas.

&nbsp;   \* \*\*Tiempo:\*\* Manejado directamente mediante campos `DATE` en la tabla de hechos para aprovechar el particionamiento nativo de BigQuery.



---



**## 3. Definición de KPIs y Estrategia de Visualización (Rúbrica 3.3)**



Los scripts de la capa Oro (`etl\_gold.py`) calculan los siguientes indicadores clave de desempeño para la toma de decisiones:



| KPI | Definición Técnica | Objetivo de Negocio |

| :--- | :--- | :--- |

| \*\*Tasa de Ausentismo (%)\*\* | \\`(SUM(is\_noshow) / COUNT(\*)) \* 100\\` | Identificar la pérdida operativa por citas no atendidas. |

| \*\*Promedio de Espera (Días)\*\* | \\`AVG(appointment\_day - scheduled\_day)\\` | Evaluar si tiempos largos de espera aumentan la probabilidad de falta. |

| \*\*Ausentismo por Segmento\*\* | Tasa agrupada por \\`Rango\_Edad\\` y \\`Barrio\\` | Focalizar campañas de recordatorio (SMS/Llamadas) en grupos de riesgo. |



---



**## 4. Guía de Reproducibilidad**



Siga estos pasos para desplegar la solución completa desde cero en un entorno Google Cloud Shell.



\### Prerrequisitos

\* Proyecto GCP activo.

\* Archivo \\`KaggleV2-May-2016.csv\\` en el directorio raíz.



\### Paso 1: Configuración Inicial

\\`\\`\\`bash

export PROJECT\_ID="examen-final-bi-2025-garroore"

export BUCKET\_NAME="bucket-examen-final-bi-2025-garroore"

gcloud config set project \\$PROJECT\_ID

gcloud auth application-default login --no-launch-browser

\\`\\`\\`



\### Paso 2: Ingesta y EDA (Capa Bronce)

\\`\\`\\`bash

\# Crear entorno

python3 -m venv venv \&\& source venv/bin/activate

pip install pandas google-cloud-storage google-cloud-bigquery db-dtypes pyarrow



\# Ejecutar EDA

python eda.py \\$BUCKET\_NAME

\\`\\`\\`

\*Salida esperada:\* Reporte de calidad en \\`docs/evidencia\_eda.txt\\`.



\### Paso 3: Transformación (Capa Plata)

\\`\\`\\`bash

python etl\_silver.py \\$BUCKET\_NAME \\$PROJECT\_ID

\\`\\`\\`

\*Acción:\* Limpia datos, crea dimensiones/hechos y carga a BigQuery (\\`silver\_layer\\`).



\### Paso 4: Generación de KPIs (Capa Oro)

\\`\\`\\`bash

python etl\_gold.py \\$BUCKET\_NAME \\$PROJECT\_ID

\\`\\`\\`

\*Acción:\* Ejecuta SQL analítico y guarda resultados en BigQuery (\\`gold\_layer\\`) y GCS.



---



**## 5. Estructura de Archivos Entregada**



\\`\\`\\`text

/

├── eda.py              # Script de Análisis Exploratorio (Ingesta)

├── etl\_silver.py       # Pipeline de Transformación (Modelo Estrella)

├── etl\_gold.py         # Cálculo de KPIs y Analítica

├── dataset\_citas.csv   # Dataset Original (No incluido en ZIP por peso)

├── README.md           # Esta documentación

└── docs/               # Evidencias de Ejecución

&nbsp;   ├── evidencia\_eda.txt

&nbsp;   ├── log\_etl\_silver.txt

&nbsp;   └── log\_etl\_gold.txt

\\`\\`\\`

EOF

