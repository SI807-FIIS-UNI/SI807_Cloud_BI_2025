# IMPLEMENTACIÓN DE SOLUCIÓN EN LA NUBE DEL DATASET DE KAGGLE Medical Appointment No Shows
## Justificación de la Elección de Google Cloud Platform (GCP)

Google Cloud Platform (GCP) fue seleccionada como la plataforma tecnológica para la implementación del proyecto debido a su enfoque nativo en analítica de datos, su capacidad de escalabilidad y su integración directa con herramientas de Business Intelligence.

**Orientación Nativa a Analítica y BI**

GCP ofrece servicios diseñados específicamente para el procesamiento y análisis de grandes volúmenes de datos. En particular, BigQuery permite ejecutar consultas analíticas complejas sobre datasets masivos sin necesidad de administrar infraestructura, lo cual resulta ideal para proyectos de analítica descriptiva y exploratoria, como el análisis de inasistencia a citas médicas.

**Arquitectura Serverless y Escalabilidad**

El uso de servicios serverless como BigQuery elimina la necesidad de gestionar servidores, configuraciones de clúster o escalamiento manual. Esto permite que el pipeline ETL se ejecute de manera eficiente tanto con volúmenes pequeños como con datasets de mayor tamaño, garantizando escalabilidad automática y alta disponibilidad.

**Integración con Data Lake en Cloud Storage**

Google Cloud Storage (GCS) permite implementar una arquitectura de Data Lake basada en capas (raw, processed, curated), facilitando:

Trazabilidad de los datos

Separación clara de responsabilidades

Reprocesamiento controlado de la información

Esta estructura es una práctica estándar en arquitecturas modernas de datos y se integra de forma natural con BigQuery.

**Alto Rendimiento en Consultas Analíticas**

BigQuery utiliza un motor de consultas distribuido y columnar, optimizado para agregaciones y análisis multidimensional. Esto resulta especialmente adecuado para la generación de KPIs y dashboards, ya que permite responder consultas complejas en segundos, incluso cuando el volumen de datos crece.

**Facilidad de Integración con Herramientas de Visualización**

GCP se integra de manera nativa con herramientas de visualización como Looker Studio, permitiendo consumir directamente las tablas de la capa ORO sin necesidad de procesos intermedios. Esto simplifica el flujo desde el ETL hasta la construcción de dashboards interactivos

**Seguridad y Control de Acceso**

Google Cloud proporciona mecanismos robustos de Identity and Access Management (IAM), permitiendo controlar de forma granular quién puede acceder a los datos, ejecutar consultas o modificar recursos. Esto es especialmente relevante en contextos de análisis de datos sensibles, como información relacionada con el sector salud.

**Adecuación al Contexto Académico y Profesional**

GCP ofrece un entorno ampliamente utilizado tanto en la industria como en entornos académicos, lo que permite aplicar buenas prácticas reales de Data Engineering. La experiencia adquirida en este proyecto es directamente transferible a escenarios profesionales de analítica y BI.

## Fase 1 : Creación buckets en google cloud
## 🏗️ Arquitectura Medallion

La arquitectura del proyecto sigue el enfoque **Medallion**, separando los datos por niveles de madurez:

- **Capa Bronce**: Datos crudos y procesados iniciales.
- **Capa Plata**: Datos limpios y transformados.
- **Capa Oro**: Datos analíticos listos para KPIs y dashboards.

---

## 🥉 Capa Bronce – Inicialización del Data Lake

En esta capa se almacena la información en su estado inicial, preservando la trazabilidad del dato.

### Comandos de creación del bucket y estructura

```bash
# Verificar proyecto activo
gcloud config get-value project

# Definir variables
BUCKET_NAME="bi-examen-dataset-mauricio-otero"
REGION="us-central1"

# Crear bucket en Google Cloud Storage
gcloud storage buckets create gs://$BUCKET_NAME \
  --location=$REGION \
  --uniform-bucket-level-access

# Crear estructura de la Capa Bronce
gcloud storage cp /dev/null gs://$BUCKET_NAME/bronce/raw/.keep
gcloud storage cp /dev/null gs://$BUCKET_NAME/bronce/processed/.keep
gcloud storage cp /dev/null gs://$BUCKET_NAME/bronce/curated/.keep

# Verificar estructura
gcloud storage ls gs://$BUCKET_NAME/bronce/

""


En esta parte creamos el bucket con nombre "bi-examen-dataset-mauricio-otero", y luego dentro del bucket creamos la carpeta cobre con las 3 carpetas raw , processed y curated
aquí una visualización del codigo que se empleo para realizar esta fase  : 
## Imagen de la visualizaciónd del codigo empleado para crear el bucket y la carpeta cobre:
<img width="1913" height="964" alt="Captura de pantalla 2025-12-15 201044" src="https://github.com/user-attachments/assets/1724a440-768b-4783-b0ac-fe6c118116a6" />

## Visualización del bucket con las carpetas en la plataforma google cloude: 

<img width="533" height="761" alt="Captura de pantalla 2025-12-15 201639" src="https://github.com/user-attachments/assets/10aa210a-c5cf-4241-859e-f621a3fdfff9" />

Despues de eso se suben los archivos para luego subirlos al Bucket para realizar el EDA y el ETL 
## Subida de archivos en Cloud Shell Editor : 

<img width="957" height="967" alt="Captura de pantalla 2025-12-15 202455" src="https://github.com/user-attachments/assets/96b09aad-cd48-4d78-a97b-837f0db9a927" />
## subida de archivos al bucket de google cloude : 
se usan los comandos para subir el csv a google cloude para su posterior análisis 
<img width="1609" height="93" alt="Captura de pantalla 2025-12-15 202713" src="https://github.com/user-attachments/assets/a1f2a12a-45e9-4690-a65c-af68244d1b83" />

<img width="1920" height="1080" alt="Captura de pantalla (234)" src="https://github.com/user-attachments/assets/803d548c-bb21-4c0b-9d6d-893f39142907" />

## FASE 2 : IMPLEMMENTACIÓN DE EDA SIMPLE : 
en esta parte vamos a realizar un Análsis exploratorio de datos de manera simple, para ver el comportamiento de los datos el archivo lo llamaremos EDA.py, pero antes se crean las carpetas doc y Script para almancenar imagenes y código de lo que resulte del EDA y el proceso ETL que se implementará luego y además se descargan las librerías pandas ,  matplotlib ,  fsspec  y gcsfs para realizar el correcto EDA
## Creación de carpetas
<img width="1514" height="786" alt="Captura de pantalla 2025-12-15 203416" src="https://github.com/user-attachments/assets/ba398e3d-e6a7-40c9-a1c6-f79e4ec07634" />

## EDA : 
En la capa BRONCE se realizó un Análisis Exploratorio de Datos (EDA) con el objetivo de comprender la estructura, calidad y comportamiento inicial del dataset No-Show Medical Appointments antes de su transformación y modelado analítico.

El EDA incluyó:

Inspección estructural del dataset, mediante la revisión de dimensiones (número de filas y columnas), tipos de datos y presencia de valores nulos.

Visualización de las primeras observaciones (head) para validar la correcta lectura de los datos desde Google Cloud Storage.

Análisis estadístico básico de las variables numéricas, permitiendo identificar rangos válidos y posibles valores atípicos, especialmente en la variable Age.

Validación y normalización de variables clave, como la conversión de campos de fecha (ScheduledDay y AppointmentDay) a formato temporal y la estandarización de la variable objetivo No-show.

Generación de visualizaciones exploratorias, incluyendo la distribución de inasistencias y la relación entre edad y asistencia, con el fin de identificar patrones preliminares relevantes para el análisis posterior.

Como resultado del EDA, se obtuvo una versión limpia y consistente del dataset, la cual fue almacenada en la ruta bronce/processed. Este proceso permitió garantizar la calidad de los datos y sentó las bases para la construcción del modelo dimensional en la capa PLATA y la generación de KPIs en la capa ORO.

se crea el script con nano identificando la carpeta donde queremos crearla para este caso se hizo 
nano scripts / EDA.py
<img width="1449" height="593" alt="image" src="https://github.com/user-attachments/assets/9be1faf3-6169-44bb-9947-466d7bbc0c7b" />
<img width="1919" height="968" alt="Captura de pantalla 2025-12-15 212552" src="https://github.com/user-attachments/assets/636ca6b8-e7c7-4ee0-a2b2-dbfdae999900" />

# Visualizaciones del EDA 
<img width="640" height="480" alt="age_vs_noshow" src="https://github.com/user-attachments/assets/c6766dcc-fb4e-4cf4-8df6-603e4f54c8d4" />
<img width="640" height="480" alt="no_show_distribution" src="https://github.com/user-attachments/assets/dbc907af-ad31-4500-86dc-f68ca66f1947" />

🔗 [Script EDA – `eda (1).py`](./Scripts/eda%20(1).py)

Luego del análisis exploratorio de datos (EDA), se generó una versión limpia del dataset que fue almacenada en la capa BRONCE/processed para su posterior modelado dimensional.

<img width="1920" height="1080" alt="Captura de pantalla (235)" src="https://github.com/user-attachments/assets/385444c9-af93-4c03-aa91-4cd10d5302e0" />

## Fase 3 Transformación y Modelo Dimensional 
Se implementa un modelo dimensional tipo estrella debido a que el problema de análisis se centra en el estudio de eventos repetitivos (citas médicas) y sus métricas asociadas, las cuales requieren ser analizadas desde múltiples perspectivas como tiempo, paciente, ubicación y condiciones médicas.
El modelo estrella:

Simplifica las consultas analíticas.

Optimiza el rendimiento en motores OLAP como BigQuery.

Facilita la generación de KPIs y dashboards en la capa ORO.
Tabla de Hechos: fact_appointments
Rol

La tabla de hechos representa el evento central del negocio:

Una cita médica programada.

Granularidad

1 fila = 1 cita médica

Métricas principales

no_show (indicador de inasistencia)

Conteo de citas

Posibles métricas derivadas (porcentaje de no-show)

## Tablas de Dimensión

| Dimensión | Nombre de la tabla | Propósito | Análisis que permite |
|---------|------------------|-----------|----------------------|
| Tiempo | `dim_time` | Analizar el comportamiento de asistencia a lo largo del tiempo. | Identificar meses o fechas con mayor inasistencia y evaluar tendencias temporales del no-show. |
| Paciente | `dim_patient` | Analizar características demográficas y sociales del paciente. | Evaluar la relación entre edad y asistencia, diferencias por género y el impacto de factores sociales como la beca (Scholarship). |
| Ubicación | `dim_neighbourhood` | Analizar la distribución geográfica de las citas médicas. | Identificar zonas con mayor tasa de inasistencia y posibles problemas de acceso o distancia. |
| Condiciones Médicas | `dim_conditions` | Analizar si condiciones clínicas influyen en la asistencia a citas. | Evaluar la asistencia de pacientes con hipertensión, diabetes, alcoholismo o discapacidad. |
| Comunicación | `dim_communication` | Evaluar el impacto de los recordatorios en la asistencia. | Analizar la efectividad de los mensajes SMS en la reducción del no-show. |


## Moldelo estrella 
<img width="1426" height="498" alt="Captura de pantalla 2025-12-16 013146" src="https://github.com/user-attachments/assets/7af8557e-d8f5-4bc1-a961-1fd8b46187ec" />

## Proceso ETL 
El archivo está dentro de la carpeta scripts
<img width="1319" height="173" alt="Captura de pantalla 2025-12-15 214332" src="https://github.com/user-attachments/assets/34663646-5d4e-42d1-9e5b-15eda6f47d12" />

## carga de las dimensiones a google cloude 

<img width="1910" height="774" alt="Captura de pantalla 2025-12-16 011456" src="https://github.com/user-attachments/assets/9568b125-de53-4e4c-ace8-1144cf5f7f23" />
🔗 [Script ETL – `etl.py`](./Scripts/etl.py)


## Justificación de los KPIs 
El objetivo principal del proyecto es analizar el fenómeno de inasistencia a citas médicas (no-show), identificar patrones temporales, demográficos y sociales, y evaluar el impacto de acciones preventivas como los recordatorios vía SMS.
Para ello, se definieron KPIs en la capa ORO, organizados en dos dashboards complementarios: uno ejecutivo y otro analítico.
## KPI Global
**Total de Citas**

Definición: Número total de citas registradas.

Justificación: Proporciona el contexto general del volumen de atención médica. Es necesario para interpretar correctamente las tasas de inasistencia y evitar conclusiones sesgadas por tamaño de muestra.
**Total de No-Show**

Definición: Número total de citas a las que el paciente no asistió.

Justificación: Representa el impacto absoluto del problema. Cada no-show implica pérdida de recursos médicos, tiempo y costos operativos.
**Tasa de No-Show**

Definición: Proporción de citas no atendidas respecto al total de citas.

Justificación: Es el KPI principal del negocio. Permite medir la gravedad del problema y comparar periodos, zonas o grupos poblacionales de forma homogénea.

**Tasa de Asistencia**

Definición: Complemento de la tasa de no-show.

Justificación: Ofrece una visión positiva orientada al desempeño del sistema de salud y facilita la comunicación de resultados a nivel ejecutivo.

## KPIs Temporales
**No-Show por Tiempo**

Dimensión: Tiempo (fecha).

Justificación: Permite analizar la evolución de la inasistencia a lo largo del tiempo e identificar tendencias, estacionalidades o periodos críticos con mayor tasa de no-show.

Pregunta que responde:

¿Existen fechas o periodos donde la inasistencia aumenta significativamente?

## KPIs de Comunicación
**Impacto del SMS**

Dimensión: SMS recibido (Sí / No).

Justificación: Evalúa la efectividad de los recordatorios vía SMS como estrategia preventiva. Este KPI permite validar si la comunicación activa reduce la tasa de no-show y justificar su uso o mejora.

Pregunta que responde:

¿Los recordatorios SMS reducen realmente la inasistencia?

## KPIs Demográficos
**No-Show por Rango de Edad**

Dimensión: Edad (segmentada).

Justificación: Permite identificar grupos etarios con mayor riesgo de inasistencia y diseñar estrategias focalizadas según el perfil del paciente.

Pregunta que responde:

¿Qué rangos de edad presentan mayor tasa de no-show?

**No-Show por Género**

Dimensión: Género.

Justificación: Analiza posibles diferencias de comportamiento entre géneros y contribuye a estudios de equidad y accesibilidad en la atención médica.
## KPIs Geográficos
**No-Show por Ubicación (Neighbourhood)**

Dimensión: Zona geográfica.

Justificación: Permite detectar zonas con mayores problemas de asistencia, lo que puede estar relacionado con barreras de acceso, distancia, transporte o condiciones socioeconómicas.

Pregunta que responde:

¿Existen barrios con mayor concentración de inasistencias?

**KPIs Clínicos**
No-Show por Condiciones Médicas

Dimensión: Condiciones clínicas (hipertensión, diabetes, alcoholismo, discapacidad).

Justificación: Analiza si la presencia de condiciones médicas específicas influye en la asistencia a citas, apoyando decisiones clínicas y de gestión de pacientes crónicos.

Pregunta que responde:

¿Los pacientes con ciertas condiciones médicas asisten más o menos a sus citas?


## Elaboración del Dashboard 
**Conexión con de Bigquery y con Looker estudio**
se selecciona la opción de conectar con bigquery 
<img width="1920" height="1080" alt="Captura de pantalla (238)" src="https://github.com/user-attachments/assets/4a9808a5-05b7-4029-9557-28275c605a82" />

y luego se selecciona el proyecto , la tabla (en este caso el oro donde se encuentran los KPIs y seleccionados el que nos interesa) , en este caso seleccionaremos el kpi global, ya que es el principal y tiene una visión general del caso 
<img width="1920" height="1080" alt="Captura de pantalla (239)" src="https://github.com/user-attachments/assets/2f376ee4-eaab-40ff-ac3c-64588a191ecd" />

## Dashboard 1
Este dashboard presenta una visión global y resumida del fenómeno de no-show, permitiendo a los responsables del sistema de salud comprender rápidamente la magnitud del problema y sus principales patrones demográficos y clínicos.
**Objetivo del Dashboard**

Brindar una visión ejecutiva del desempeño general de las citas médicas, enfocándose en:

Nivel de asistencia e inasistencia

Distribución por género

Presencia de condiciones médicas relevantes

Volumen de citas a lo largo del tiempo

Este tablero está orientado a toma de decisiones estratégicas y monitoreo general.

<img width="1147" height="811" alt="Captura de pantalla 2025-12-16 024337" src="https://github.com/user-attachments/assets/1dc63610-913e-4091-9ef9-c7e70f227e7a" />


## 📊 Dashboard 1: Visión General del No-Show

> Monitoreo ejecutivo del comportamiento de inasistencia a citas médicas.

Este dashboard ofrece una **visión global y resumida** del fenómeno *no-show*, permitiendo comprender rápidamente la magnitud del problema, su impacto general y los principales patrones de asistencia.

Está orientado a **usuarios ejecutivos y tomadores de decisiones**, sirviendo como punto de partida para el análisis del desempeño del sistema de citas médicas.

---

### 📌 Indicadores Principales

- **Total de citas:** Volumen total de citas registradas.
- **Total de no-show:** Cantidad absoluta de inasistencias.
- **Tasa de no-show:** Indicador clave del nivel de inasistencia.
- **Tasa de asistencia:** Métrica complementaria de desempeño positivo.

---

### 📈 Análisis Incluido

- **Evolución temporal del volumen de citas**
- **Distribución por género**
- **Distribución por condiciones médicas relevantes**

Estos análisis permiten detectar patrones generales y servir de base para exploraciones más detalladas en el Dashboard 2.

---
<img width="1147" height="811" alt="Captura de pantalla 2025-12-16 024337" src="https://github.com/user-attachments/assets/43f33586-404e-4b26-8a77-51179d765033" />


### 🔗 Acceso al Dashboard

[![Looker Studio](https://img.shields.io/badge/Looker_Studio-Ver_Dashboard_1-EA4335?style=for-the-badge&logo=looker&logoColor=white)](https://lookerstudio.google.com/reporting/32d39dc5-f9dc-4a10-bf30-bea3552ba2e8)

---
## 📉 Dashboard 2: Análisis Operativo del No-Show

> Análisis detallado para identificar factores asociados a la inasistencia y apoyar acciones correctivas.

Este dashboard complementa la visión ejecutiva del Dashboard 1 mediante un **análisis operativo y segmentado** del fenómeno *no-show*, permitiendo identificar patrones y factores que influyen en la inasistencia a citas médicas.

---

### 🎯 Objetivo del Dashboard

Identificar **factores asociados al no-show** desde distintas perspectivas:
- Comunicación con el paciente
- Segmentación demográfica
- Condiciones médicas
- Distribución geográfica

Este tablero está orientado a **analistas y gestores operativos**, facilitando la toma de decisiones basada en datos.

---

### 🔍 Análisis Incluido

- **Impacto del SMS:** Evaluación de la efectividad de los recordatorios vía SMS en la reducción del no-show.
- **Análisis por rango de edad:** Identificación de grupos etarios con mayor riesgo de inasistencia.
- **Análisis por género:** Comparación de tasas de no-show entre hombres y mujeres.
- **Condiciones médicas:** Evaluación del impacto de condiciones como hipertensión y diabetes en la asistencia.
---

### 🧠 Valor del Dashboard

Este dashboard permite:
- Identificar **factores críticos** asociados a la inasistencia
- Priorizar **intervenciones operativas**
- Evaluar estrategias preventivas
- Complementar la visión general del Dashboard 1

---
<img width="1180" height="851" alt="Captura de pantalla 2025-12-16 030534" src="https://github.com/user-attachments/assets/3f8ec10b-4ff6-4682-8cf1-62288cc1ea60" />


### 🔗 Acceso al Dashboard

[![Looker Studio](https://img.shields.io/badge/Looker_Studio-Ver_Dashboard_2-EA4335?style=for-the-badge&logo=looker&logoColor=white)](https://lookerstudio.google.com/reporting/c7371ace-c371-4bbe-8d0a-7a8b8a7df6c1)

---

### 🧩 Relación con el Dashboard 1

- **Dashboard 1:** Visión ejecutiva del problema de no-show.
- **Dashboard 2:** Análisis operativo de causas y factores asociados.

Ambos dashboards reutilizan los KPIs definidos en la capa ORO, diferenciándose por su enfoque analítico.
