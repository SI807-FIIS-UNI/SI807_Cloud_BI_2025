# IMPLEMENTACIÓN DE SOLUCIÓN EN LA NUBE DEL DATASET DE KAGGLE Medical Appointment No Shows
## Fase 1 : Creación buckets en google cloud
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
### Dimensión Tiempo – dim_time

Propósito: Analizar el comportamiento de asistencia a lo largo del tiempo.

Permite responder preguntas como:
¿En qué meses hay más inasistencias?
¿Existe una tendencia temporal en el no-show?

### Dimensión Paciente – dim_patient

Propósito: Analizar características demográficas y sociales del paciente.

Incluye:

  Edad
  Género

Condición de beca (Scholarship)

Permite evaluar:

Relación entre edad y asistencia

Impacto de factores sociales en el no-show

### Dimensión Ubicación – dim_neighbourhood

Propósito: Analizar la distribución geográfica de las citas.

Permite identificar:

Zonas con mayor tasa de inasistencia

Posibles problemas de acceso o distancia

### Dimensión Condiciones Médicas – dim_conditions

Propósito: Analizar si condiciones clínicas influyen en la asistencia.

Incluye:

Hipertensión

Diabetes

Alcoholismo

Discapacidad

Permite responder:

¿Pacientes con ciertas condiciones faltan más o menos?

### Dimensión Comunicación – dim_communication

Propósito: Evaluar el impacto de recordatorios en la asistencia.

Incluye:

SMS recibidos

Permite analizar:

Efectividad de mensajes SMS en reducir el no-show

## Proceso ETL 
El archivo está dentro de la carpeta scripts
<img width="1319" height="173" alt="Captura de pantalla 2025-12-15 214332" src="https://github.com/user-attachments/assets/34663646-5d4e-42d1-9e5b-15eda6f47d12" />

## Moldelo estrella 
<img width="1426" height="498" alt="Captura de pantalla 2025-12-16 013146" src="https://github.com/user-attachments/assets/7af8557e-d8f5-4bc1-a961-1fd8b46187ec" />

## carga de las dimensiones a google cloude 

<img width="1910" height="774" alt="Captura de pantalla 2025-12-16 011456" src="https://github.com/user-attachments/assets/9568b125-de53-4e4c-ace8-1144cf5f7f23" />
🔗 [Script ETL – `ETL (2).py`](./Scripts/etl%20(2).py)
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
