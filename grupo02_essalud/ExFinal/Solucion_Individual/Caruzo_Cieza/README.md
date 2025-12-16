# 📄 README.md

## Solución BI Cloud – Análisis de No-Show en Citas Médicas

**Curso:** Sistemas de Inteligencia de Negocios  
**Examen Final – Pregunta 3**  
**Alumno:** David Caruzo Cieza  
**Nube:** Google Cloud Platform (GCP)

---

## 1. Objetivo de la Solución

El objetivo de esta solución de Inteligencia de Negocios es **identificar los factores asociados a la inasistencia (“No-Show”) de pacientes a citas médicas**, con la finalidad de **mejorar los procesos de confirmación de citas y reducir pérdidas operativas** en el sistema de salud.

La solución permite analizar el comportamiento de los pacientes desde diferentes perspectivas:

- Demográfica (edad, género)
- Temporal (día, hora)
- Operativa (anticipación de la cita)
- Uso de recordatorios (SMS)

---

## 2. Selección de la Nube y Justificación Técnica

### ☁️ Nube Seleccionada: Google Cloud Platform (GCP)

La solución fue implementada en **Google Cloud Platform** debido a las siguientes razones técnicas:

- **Google Cloud Storage (GCS)** permite implementar un Data Lake escalable bajo el enfoque **bronce – plata – oro**.
- **BigQuery** ofrece un motor analítico columnar, altamente optimizado para consultas BI y conexión directa con herramientas de visualización.
- Integración nativa con herramientas de análisis como **Power BI**, sin necesidad de capas intermedias.
- Escalabilidad y bajo overhead operativo, ideal para soluciones BI cloud-native.

Esta selección permite una arquitectura **modular, reproducible y alineada a estándares empresariales de BI**.

---

## 3. Dataset Utilizado

Se utilizó el dataset público:

**Kaggle – Medical Appointment No Shows (May 2016)**

El dataset contiene información histórica de citas médicas, incluyendo:

- Identificador del paciente y de la cita
- Fecha de programación y fecha de atención
- Edad, género y condiciones médicas
- Indicador de asistencia o inasistencia (*No-show*)

**Nota:** El dataset fue cargado mediante CLI directamente a la capa **bronce/raw**.

**[CAPTURA AQUÍ: archivo CSV cargado en bronce/raw vía `gsutil ls`]**

---

## 4. Arquitectura de la Solución BI

La arquitectura implementada sigue un enfoque **Data Lake + Data Warehouse**, estructurado en capas:

CSV (Kaggle)

   ↓
   
GCS - BRONCE

   ├── raw
   ├── processed
   └── curated
   ↓
   
BigQuery - PLATA

   ├── Dimensiones
   └── Tabla de Hechos
   ↓
   
BigQuery - ORO

   ├── KPIs agregados
   ↓
Power BI

   ├── Dashboard Ejecutivo
   └── Dashboard Analítico
   


**[CAPTURA AQUÍ: diagrama general de arquitectura o estructura de buckets]**

---

## 5. Diseño del Data Lake (Bronce – Plata – Oro)

El Data Lake fue diseñado bajo el principio de **separación de responsabilidades por capa**:

### 🥉 Capa Bronce

- Almacena el dato original sin pérdida de información.
- Permite limpieza progresiva y validaciones.
- Facilita auditoría y trazabilidad.

### 🥈 Capa Plata

- Contiene el **modelo dimensional estrella**.
- Datos estructurados para análisis.
- Optimizada para consultas analíticas.

### 🥇 Capa Oro

- Contiene **KPIs agregados y listos para visualización**.
- Reduce complejidad de consultas en dashboards.
- Garantiza consistencia de métricas.

---

## 6. Problemática de Negocio

El **No-Show** representa una pérdida directa para el sistema de salud, ya que:

- Se asignan recursos médicos que no son utilizados.
- Se reduce la eficiencia operativa.
- Se incrementan costos indirectos.

La solución busca responder preguntas clave como:

- ¿Qué perfiles de pacientes presentan mayor tasa de no-show?
- ¿En qué días u horarios ocurre con mayor frecuencia?
- ¿La anticipación de la cita influye en la asistencia?
- ¿El envío de SMS reduce el no-show?

---

## 7. KPIs Definidos

Los principales indicadores generados en la capa oro son:

- **Tasa global de No-Show**
- **No-Show por rango de edad y género**
- **No-Show por día y hora**
- **No-Show por anticipación (lead time)**

Estos KPIs alimentan directamente los dashboards ejecutivos y analíticos.

---


# Pregunta 3 Examen
## 3.1 Ingestión y Estructuración – Capa BRONCE

---

## 3.1.1 Creación de la Estructura BRONCE

Se implementó la estructura de carpetas exigida en la rúbrica dentro de **Google Cloud Storage**, separando claramente las subcapas de la capa bronce:

bronce/

├── raw/

├── processed/

└── curated/


Esta estructura permite:

- Preservar el dato original  
- Realizar transformaciones progresivas  
- Mantener trazabilidad del dato  

**[CAPTURA AQUÍ: `gsutil ls gs://dl-bi-examen-caruzo/bronce/`]**

---

## 3.1.2 Carga del Dataset mediante CLI

El archivo CSV fue cargado directamente a la subcapa **bronce/raw** utilizando la línea de comandos, cumpliendo el requisito de carga por CLI.

```bash
gsutil cp KaggleV2-May-2016.csv gs://dl-bi-examen-caruzo/bronce/raw/
```

Este enfoque asegura:

- Reproducibilidad del proceso  
- Automatización  
- Evidencia clara de ingestión  

**[CAPTURA AQUÍ: ejecución del comando `gsutil cp`]**  
**[CAPTURA AQUÍ: `gsutil ls bronce/raw`]**

---

## 3.1.3 Transformación BRONCE / RAW → BRONCE / PROCESSED

En esta etapa se realizó la **conversión del CSV a formato Parquet**, optimizando el almacenamiento y el rendimiento para análisis posteriores.

### Script utilizado

`raw_to_processed.py`

Principales acciones realizadas:

- Lectura del CSV desde GCS  
- Normalización de nombres de columnas  
- Conversión de campos de fecha a tipo datetime  
- Almacenamiento en formato Parquet  

**Justificación técnica:**  
El formato Parquet es columnar, comprimido y ampliamente utilizado en soluciones de BI Cloud, mejorando tiempos de lectura y consumo de recursos.

**[CAPTURA AQUÍ: ejecución del script raw_to_processed.py]**  
**[CAPTURA AQUÍ: archivo Parquet en bronce/processed]**

---

## 3.1.4 Transformación BRONCE / PROCESSED → BRONCE / CURATED

En esta etapa se realizaron **validaciones y limpieza básica**, preparando el dataset para análisis exploratorio y modelado posterior.

### Script utilizado

`processed_to_curated.py`

Validaciones aplicadas:

- Eliminación de registros duplicados por `AppointmentID`  
- Eliminación de edades inválidas  
- Normalización de la variable objetivo (*No-show*)  
- Conversión de campos binarios a tipo entero  

**Justificación técnica:**  
La capa curated garantiza un dataset consistente y confiable para análisis, sin aplicar aún lógica de negocio compleja.

**[CAPTURA AQUÍ: ejecución del script processed_to_curated.py]**  
**[CAPTURA AQUÍ: archivo Parquet en bronce/curated]**

---

## 3.1.5 Análisis Exploratorio de Datos (EDA)

Se ejecutó un **EDA robusto**, alineado a los criterios de la rúbrica, para comprender el comportamiento del dataset y validar su calidad.

### Script utilizado

`eda_bronce_curated.py`

El EDA incluyó:

### ✔ Análisis de valores nulos

- Identificación de campos incompletos  
- Exportación de resultados a CSV  

### ✔ Estadísticas descriptivas

- Media, mínimo, máximo y percentiles  
- Análisis de variables numéricas  

### ✔ Distribuciones

- Histograma de edades para identificar outliers y sesgos  

### ✔ Correlaciones

- Matriz de correlación entre variables numéricas  
- Visualización mediante heatmap  

**Justificación técnica:**  
El EDA permite detectar patrones, validar supuestos y reducir riesgos antes del modelado dimensional.

**[CAPTURA AQUÍ: ejecución del script de EDA]**  
**[CAPTURA AQUÍ: archivo estadisticas.csv]**  
**[CAPTURA AQUÍ: gráfico de distribución de edad]**  
**[CAPTURA AQUÍ: heatmap de correlaciones]**

---

## 3.1.6 Evidencias y Logs

Todas las ejecuciones fueron registradas y almacenadas como evidencia del proceso ETL:

- Logs de ejecución  
- Archivos CSV con resultados del EDA  
- Imágenes generadas  

Estos archivos fueron almacenados en la carpeta **docs** del bucket.

**[CAPTURA AQUÍ: contenido de la carpeta docs en el bucket]**

## 3.2 Transformación y Modelo Dimensional – PLATA y ORO

---

## 3.2.1 Diseño del Modelo Dimensional (Capa PLATA)

Para abordar la problemática de **identificación de factores asociados al No-Show**, se diseñó un **modelo dimensional en estrella**, con un grano definido a nivel de **cita médica**.

### 🎯 Grano del modelo

> **Una fila en la tabla de hechos representa una cita médica única.**

Este grano permite analizar el comportamiento de asistencia desde múltiples dimensiones sin ambigüedad.

---

## 3.2.2 Modelo Estrella Implementado

### ⭐ Tabla de Hechos: `fact_citas`

Contiene las métricas clave del negocio y las llaves foráneas hacia las dimensiones.

**Principales campos:**

- `appointmentid`  
- `paciente_id`  
- `tiempo_id`  
- `barrio_id`  
- `lead_time` (anticipación en días)  
- `sms_received`  
- `no_show`  

---

### 🔵 Dimensiones

#### `dim_paciente`

Permite analizar el No-Show según características del paciente.

Campos relevantes:

- Género  
- Edad  
- Condiciones médicas  
- Beneficio social (Scholarship)  

---

#### `dim_tiempo`

Permite análisis temporal detallado.

Campos relevantes:

- Fecha de la cita  
- Día de la semana  
- Mes  
- Año  
- Hora de atención  

---

#### `dim_barrio`

Permite análisis geográfico.

Campos relevantes:

- Barrio (*Neighbourhood*)  

---

### 📐 Representación del Modelo Estrella


**[CAPTURA AQUÍ: diagrama del modelo estrella]**

![Diagrama estrella](docs/Captura%20de%20pantalla%202025-12-15%20213053.png)

---

## 3.2.3 Transformación BRONCE / CURATED → PLATA

A partir del dataset validado en la capa **curated**, se generaron las tablas dimensionales y la tabla de hechos en la capa **plata**, utilizando **BigQuery** como Data Warehouse analítico.

### Script utilizado

`curated_to_plata_star.py`

Principales transformaciones realizadas:

- Creación de claves sustitutas para dimensiones  
- Separación de atributos descriptivos y métricas  
- Cálculo del **lead time** (anticipación entre programación y cita)  
- Carga de dimensiones y hechos en BigQuery  

**Justificación técnica:**  
El uso de un modelo estrella optimiza consultas analíticas, reduce la complejidad de *joins* y es el estándar en soluciones BI empresariales.

**[CAPTURA AQUÍ: ejecución del script curated_to_plata_star.py]**  
**[CAPTURA AQUÍ: tablas PLATA creadas en BigQuery]**

---

## 3.2.4 Construcción de la Capa ORO (KPIs)

La capa **oro** consolida indicadores agregados listos para visualización, eliminando la necesidad de cálculos complejos en los dashboards.

### KPIs Generados

#### ✔ KPI 1 – Tasa Global de No-Show

- Total de citas  
- Total de inasistencias  
- Porcentaje de No-Show  

---

#### ✔ KPI 2 – No-Show por Edad y Género

- Segmentación por rangos etarios  
- Comparación por género  

---

#### ✔ KPI 3 – No-Show por Día y Hora

- Identificación de franjas críticas  
- Soporte para decisiones operativas  

---

#### ✔ KPI 4 – No-Show por Anticipación (Lead Time)

- Impacto del tiempo de anticipación en la asistencia  

---

### Script utilizado

`plata_to_oro_kpis.py`

Este script:

- Consulta directamente las tablas PLATA  
- Genera tablas agregadas en el dataset ORO  
- Garantiza consistencia de métricas para visualización  

**[CAPTURA AQUÍ: ejecución del script plata_to_oro_kpis.py]**  
**[CAPTURA AQUÍ: tablas ORO creadas en BigQuery]**

---

## 3.2.5 Evidencias del Proceso ETL

Durante la ejecución del proceso se generaron evidencias que validan la correcta ejecución del ETL:

- Logs de ejecución de scripts  
- Tablas creadas en BigQuery (PLATA y ORO)  
- Timestamps de ejecución  

Estas evidencias fueron almacenadas en la carpeta **docs** del bucket.

**[CAPTURA AQUÍ: carpeta docs con evidencias ETL]**


## 3.3 Visualización de KPIs – Dashboards

---

## 3.3.1 Herramienta de Visualización Seleccionada

### 📊 Power BI Desktop

Se utilizó **Power BI Desktop** como herramienta de visualización debido a:

- Conexión nativa con **Google BigQuery**  
- Capacidad de análisis interactivo  
- Uso extendido en entornos empresariales  
- Separación clara entre modelo de datos y visualización  

**Nota:** La conexión se realizó **directamente a la capa ORO**, garantizando consistencia y performance.

---

## 3.3.2 Conexión Power BI ↔ BigQuery (Capa ORO)

El flujo de conexión fue el siguiente:

1. Power BI Desktop  
2. *Get Data* → **Google BigQuery**  
3. Autenticación con cuenta GCP  
4. Selección del proyecto y dataset **dw_oro**  
5. Carga de tablas KPI  

**Justificación técnica:**  
Conectarse a la capa oro evita cálculos redundantes en la herramienta de visualización y asegura que los dashboards consuman métricas oficiales y validadas.

**[CAPTURA AQUÍ: ventana de conexión Power BI a BigQuery]**  
**[CAPTURA AQUÍ: selección del dataset dw_oro]**

---

## 3.3.3 Dashboard 1 – Visión Ejecutiva del No-Show

### 🎯 Objetivo

Brindar una visión rápida y clara del impacto global del No-Show para la toma de decisiones gerenciales.

### 📌 Visualizaciones incluidas

#### KPI Card – Tasa Global de No-Show

- Fuente: `kpi_no_show_global`  
- Métrica: `tasa_no_show_pct`  

---

#### KPI Card – Total de No-Shows

- Fuente: `kpi_no_show_global`  
- Métrica: `total_no_show`  

---

#### Gráfico de Barras – No-Show por Anticipación

- Fuente: `kpi_no_show_lead_time`  
- Eje X: `rango_anticipacion`  
- Valor: `tasa_no_show_pct`  

---

#### Tabla Resumen

- Fuente: `kpi_no_show_lead_time`  
- Métricas: total de citas, no-shows y tasa  

**Justificación de diseño:**  
Los indicadores tipo *card* permiten una lectura inmediata del problema, mientras que el análisis por anticipación identifica puntos de intervención temprana.

**[CAPTURA AQUÍ: Dashboard Ejecutivo completo]**

---

## 3.3.4 Dashboard 2 – Análisis Demográfico y Temporal

### 🎯 Objetivo

Identificar patrones de No-Show por perfil del paciente y momento de la cita.

### 📌 Visualizaciones incluidas

#### Barras Apiladas – No-Show por Edad y Género

- Fuente: `kpi_no_show_edad_genero`  
- Eje X: `rango_edad`  
- Leyenda: `gender`  
- Valor: `tasa_no_show_pct`  

---

#### Heatmap – No-Show por Día y Hora

- Fuente: `kpi_no_show_tiempo`  
- Filas: `dia_semana`  
- Columnas: `hora`  
- Valor: `tasa_no_show_pct`  

---

#### Barras – Volumen de Citas por Día

- Fuente: `kpi_no_show_tiempo`  
- Eje X: `dia_semana`  
- Valor: `total_citas`  

**Justificación de diseño:**  
La combinación de gráficos permite detectar simultáneamente **frecuencia**, **volumen** y **patrones temporales**, facilitando acciones operativas.

**[CAPTURA AQUÍ: Dashboard Analítico completo]**

---

## 3.3.5 Reproducibilidad de la Visualización

Para reproducir los dashboards:

1. Tener acceso al proyecto GCP  
2. Abrir Power BI Desktop  
3. Conectarse a BigQuery  
4. Seleccionar el dataset **dw_oro**  
5. Cargar las tablas KPI  
6. Abrir o recrear los dashboards según las visualizaciones descritas  

**Nota:** La solución no requiere transformación adicional en Power BI, ya que los KPIs están materializados en la capa oro.

---

## 4. Conclusiones

La solución desarrollada demuestra una **implementación completa de BI Cloud**, integrando:

- Ingestión por CLI  
- Data Lake con capas bronce, plata y oro  
- Modelo dimensional estrella  
- KPIs alineados a una problemática real  
- Dashboards conectados directamente a la nube  

El enfoque permite **mejorar la toma de decisiones**, reducir pérdidas por inasistencia y escalar la solución a otros contextos del sector salud.

---

## 5. Sustentación Técnica Final

> La arquitectura y los dashboards fueron diseñados bajo principios de escalabilidad, trazabilidad y performance, utilizando servicios cloud-native y buenas prácticas de Inteligencia de Negocios.

**[CAPTURA AQUÍ: vista general del proyecto completo]**




