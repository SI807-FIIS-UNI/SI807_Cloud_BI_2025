# Examen Final – SI807-U  
**Nombre:** Loayza Segura Roger Salvador  
**Código de Proyecto:** `ef-si807u-20220018k`  
**Equipo:** `grupo05_nettalco`

---

## 📌 Objetivo del Proyecto
Construir una arquitectura de datos moderna en la nube (**Lakehouse**) utilizando **Google Cloud Platform (GCP)** para el análisis de retrasos en vuelos aéreos. El flujo de datos abarca tres capas:
- **Bronce**: Almacenamiento de datos crudos y procesados en Google Cloud Storage (GCS).
- **Plata**: Datos limpios y estructurados en BigQuery.
- **Oro**: Modelo dimensional (tipo estrella) optimizado para BI y visualización.

El proyecto finaliza con un dashboard interactivo en **Looker Studio**, alimentado directamente desde BigQuery.

---

## ☁️ Justificación del Uso de GCP

| Componente        | Servicio GCP                 | Justificación |
|-------------------|------------------------------|---------------|
| **Almacenamiento** | Google Cloud Storage (GCS)   | Ofrece almacenamiento de objetos altamente duradero, seguro y escalable, ideal para la capa Bronce de una arquitectura Lakehouse. |
| **Almacén de Datos** | BigQuery                  | Data Warehouse sin servidor, de alto rendimiento y bajo mantenimiento, perfecto para las capas Plata y Oro. Soporta consultas SQL rápidas y análisis a gran escala. |
| **Transformación** | Cloud Shell + Scripts Python | Permite ejecutar tareas de EDA y limpieza ligera usando bibliotecas como `pandas`, `gcsfs` y el SDK de GCP, sin necesidad de infraestructura adicional. |
| **Visualización**  | Looker Studio               | Herramienta gratuita integrada nativamente con BigQuery, ideal para crear dashboards interactivos sin costo ni complejidad adicional. |

---

## 🛠️ Pasos de Implementación:


![1](/grupo05_nettalco/EVIDENCIAS/1.png)

### 1. Inicializar el entorno de GCP mediante CLI

```bash
Id del proyecto: ef-si807u-20220018k
```

![1](/grupo05_nettalco/EVIDENCIAS/2.png)

# USO DEL CLI PARA CONFIGURAR EL PROYECTO COMO PRINCIPAL:

```bash
gcloud config set project ef-si807u-20220018k
```

![1](/grupo05_nettalco/EVIDENCIAS/3.png)

# CREACION DEL BUCKET:

```bash
BUCKET_NAME="bi-examen-final"
gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1

```


![1](/grupo05_nettalco/EVIDENCIAS/4.png)

# VISTA EN GOOGLE CLOUD STORAGE:

![1](/grupo05_nettalco/EVIDENCIAS/40.png)

# CREACION DE LAS CARPETAS BRONCE:

- bronce/raw

- bronce/processed

- bronce/curated

![1](/grupo05_nettalco/EVIDENCIAS/41.png)

# VISUALIZACION EN GCS:

![1](/grupo05_nettalco/EVIDENCIAS/42.png)

# CARGA DEL CSV USANDO CLI:

![1](/grupo05_nettalco/EVIDENCIAS/43.png)

![1](/grupo05_nettalco/EVIDENCIAS/44.png)

![1](/grupo05_nettalco/EVIDENCIAS/45.png)

# CAMBIAMOS LA DIRECCION DEL ARCHIVO:

Pasamos el archivo de la dirección base /home/r_loayza_s/ al gcs


```bash
BUCKET_NAME="bi-examen-final" 
NUEVO_ARCHIVO="Flight_delay.csv"
gcloud storage cp $NUEVO_ARCHIVO gs://$BUCKET_NAME/bronce/raw/$NUEVO_ARCHIVO

```

![1](/grupo05_nettalco/EVIDENCIAS/Imagen10.png)

# CARGA COMPLETADA:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen11.png)

COMPROBAMOS QUE SE ENCUENTRA CARGADO EL CSV:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen12.png)

![1](/grupo05_nettalco/EVIDENCIAS/Imagen13.png)

# ABRIMOS EL EDITOR DE GOOGLE CLOUD:



![1](/grupo05_nettalco/EVIDENCIAS/Imagen14.png)
![1](/grupo05_nettalco/EVIDENCIAS/Imagen15.png)

# CREAMOS LAS CARPETAS:


![1](/grupo05_nettalco/EVIDENCIAS/Imagen16.png)
![1](/grupo05_nettalco/EVIDENCIAS/Imagen17.png)

# CREACION DEL EDA Y EL PROCESO ETL:

```bash
BUCKET_NAME="bi-examen-final"
gcloud storage buckets create gs://$BUCKET_NAME --location=us-central1
pip install pandas google-cloud-storage fsspec gcsfs
python scripts/eda.py
```


![1](/grupo05_nettalco/EVIDENCIAS/Imagen18.png)


# SCRIPT DEL EDA EN PYTHON:

- [🐍 Scripts EDA](./grupo05_nettalco/scripts) - Código Python para la EDA minima


# SUBIDA DEL ARCHIVO A GCS:

Comando para copiar el archivo procesado de Cloud Shell a GCS

```bash
BUCKET_NAME="bi-examen-final"
PROCESSED_FILE="processed_Flight_delay.csv"
gcloud storage cp $PROCESSED_FILE gs://$BUCKET_NAME/bronce/processed/$PROCESSED_FILE
```

# SCRIPT DEL ETL EN PYTHON:

- [🐍 Scripts ETL](./grupo05_nettalco/scripts) - Código Python para la Transformacion y Carga


VISUALIZACION DE LA CAPA ORO Y PLATA EN BIGQUERY:

![1](/grupo05_nettalco/EVIDENCIAS/31.png)

![1](/grupo05_nettalco/EVIDENCIAS/32.png)

# LOGS EN VIVO DEL ETL

![1](/grupo05_nettalco/EVIDENCIAS/logs.png)

# MODELO ESTRELLA MINIMO:

![1](/grupo05_nettalco/EVIDENCIAS/Imagen19.png)


# DASHBOARD 1:

Aquí tienes la documentación detallada para el Dashboard 1, explicando el contexto de negocio y la justificación técnica de los campos seleccionados.

📊 Dashboard 1: Monitor Ejecutivo de Rendimiento de Vuelos
🎯 Propósito General
Este tablero es una herramienta de Nivel Estratégico (C-Level). Su objetivo no es mostrar cada detalle operativo, sino responder en menos de 5 segundos a la pregunta: "¿Estamos operando de manera eficiente o tenemos un problema de puntualidad?".

Se centra en la salud general de la operación aérea, permitiendo a los directivos detectar tendencias negativas (como un aumento progresivo en los retrasos) e identificar rápidamente a las aerolíneas con peor desempeño.

🧩 Desglose de Visualizaciones y Campos
1. Tarjetas de Resultados (KPIs Globales)
Lo primero que ve el usuario. Son los signos vitales del negocio.

Campos usados:

total_flights: Conteo total de filas en la tabla de hechos.

avg_dep_delay: Promedio del campo DepDelay (retraso en salida).

avg_arr_delay: Promedio del campo ArrDelay (retraso en llegada).

¿Por qué estos campos?

Contexto de Negocio: El volumen (total_flights) da la dimensión del análisis (no es lo mismo 100 vuelos que 500k). Los promedios de retraso son los indicadores clave de calidad (KPIs).

Diferenciación Clave: Se muestran ambos retrasos (Salida y Llegada) porque un vuelo puede salir tarde pero recuperar tiempo en el aire y llegar a tiempo. Si avg_dep_delay es alto pero avg_arr_delay es bajo, la eficiencia en vuelo es buena. Si ambos son altos, el sistema está colapsado.

2. Gráfico de Evolución Temporal
Para entender si la situación mejora o empeora.

Tipo: Serie de Tiempo (Líneas).

Campos usados:

Eje X: id_tiempo (Fecha YYYYMMDD convertida a fecha real).

Eje Y (Métricas): avg_dep_delay y avg_arr_delay.

¿Por qué estos campos?

Estacionalidad: El campo de tiempo permite detectar patrones. ¿Los retrasos ocurren siempre los viernes? ¿Hubo un pico en febrero por una tormenta de nieve?

Comparación Directa: Al graficar las dos líneas de retraso juntas, se visualiza la "brecha de recuperación". Si las líneas se separan, significa que las aerolíneas están gestionando bien el tiempo de vuelo para compensar salidas tardías.

3. Ranking de Aerolíneas (Top "Offenders")
Para identificar quién está bajando el promedio.

Tipo: Gráfico de Barras Horizontales.

Campos usados:

Dimensión: carrier_code (Código IATA de la aerolínea).

Métrica Principal: avg_arr_delay (Orden Descendente).

Tooltip (Info extra): total_flights.

¿Por qué estos campos?

Benchmarking: Permite comparar el rendimiento entre competidores.

Foco en el Cliente: Se ordena por avg_arr_delay (Llegada) y no por Salida, porque al pasajero lo que más le importa es llegar a tiempo. Un retraso en la salida es molesto, pero un retraso en la llegada rompe conexiones y planes.

Contexto de Volumen: El campo total_flights en el tooltip es vital para no juzgar mal. Una aerolínea con 1 solo vuelo y 300 min de retraso se vería "peor" que una con 10,000 vuelos y 15 min de promedio, aunque la segunda tenga un impacto operativo mayor.


![1](/grupo05_nettalco/EVIDENCIAS/DASHBOARD1.png)

Aquí puedes acceder a los tableros interactivos en vivo:

### 🛫 Dashboard 1: Monitor Ejecutivo
> Visión estratégica del rendimiento y puntualidad de las aerolíneas.

[![Looker Studio](https://img.shields.io/badge/Looker_Studio-Ver_Dashboard_1-4285F4?style=for-the-badge&logo=looker&logoColor=white)](https://lookerstudio.google.com/reporting/4660d5a4-bd76-490a-9cb2-ce4a1f4b8ea4)


# DASHBOARD 2:

Aquí tienes la documentación detallada para el Dashboard 2, manteniendo el mismo formato profesional y estructura que el anterior.

Este contenido es ideal para añadir a tu README.md o presentar a los stakeholders.

📉 Dashboard 2: Análisis de Causas Raíz e Impacto Operativo
🎯 Propósito General
Este tablero es una herramienta de Nivel Operativo y Diagnóstico. Mientras el Dashboard 1 dice "estamos llegando tarde", este dashboard responde a la pregunta crítica: "¿POR QUÉ estamos llegando tarde y dónde debemos intervenir?".

Está diseñado para gerentes de operaciones, analistas de calidad y planificación logística. Su objetivo es desglosar los promedios generales para encontrar cuellos de botella específicos, diferenciando entre problemas internos (controlables por la aerolínea) y externos (clima, seguridad).

🧩 Desglose de Visualizaciones y Campos
1. Distribución de Causas de Retraso (Pareto de Problemas)
El corazón del análisis. Identifica el culpable principal.

Nombre Recomendado: "Impacto Promedio por Tipo de Incidencia"

Tipo: Gráfico de Barras Verticales o Treemap.

Campos usados:

Dimensión: causa (Carrier, Weather, NAS, Security, Late Aircraft).

Métrica: avg_delay (Minutos promedio generados por esa causa específica).

¿Por qué estos campos?

Diagnóstico de Responsabilidad: En la capa ETL "despivotamos" (Unpivot) las columnas de causas para crear este gráfico. Permite ver claramente si los retrasos son culpa de la gestión de la aerolínea (CarrierDelay, LateAircraftDelay) o factores externos (Weather, NAS).

Priorización: Si CarrierDelay es la barra más alta, la solución está en mejorar el mantenimiento y la tripulación. Si es NASDelay (Sistema Nacional de Espacio Aéreo), el problema es de tráfico aéreo y no se puede controlar internamente.

2. Matriz de Eficiencia Operativa (Volumen vs. Retraso)
Para entender la relación entre la cantidad de trabajo y la calidad del servicio.

Nombre Recomendado: "Matriz de Eficiencia: Volumen de Vuelos vs. Puntualidad"

Tipo: Gráfico de Dispersión (Scatter Plot).

Campos usados:

Eje X (Variable Independiente): total_flights (Volumen operativo).

Eje Y (Variable Dependiente): avg_arr_delay (Desempeño).

Dimensión (Burbuja): carrier_code.

¿Por qué estos campos?

Segmentación de Aerolíneas: Divide el mercado en cuatro cuadrantes lógicos:

Zona de Peligro (Alto Volumen / Alto Retraso): Aerolíneas grandes colapsadas. Prioridad 1.

Zona de Nicho (Bajo Volumen / Alto Retraso): Aerolíneas pequeñas ineficientes.

Zona de Excelencia (Alto Volumen / Bajo Retraso): Modelos a seguir (Escalabilidad exitosa).

Desmitificación: A veces se cree que "más vuelos = más retrasos". Este gráfico valida o refuta esa hipótesis visualmente.

3. Mapa de Calor Calendario (Detección de Anomalías)
Para bajar del año al día específico.

Nombre Recomendado: "Calendario de Puntos Críticos (Hotspots)"

Tipo: Tabla Pivotante con Mapa de Calor.

Campos usados:

Dimensión de Fila: id_tiempo (Fecha).

Métrica: avg_arr_delay (Coloreado de verde a rojo intenso).

Métrica de contexto: total_flights.

¿Por qué estos campos?

Granularidad: Los promedios mensuales esconden días desastrosos. Este gráfico permite identificar fechas específicas (ej: "¿Qué pasó el 14 de febrero?") donde el sistema falló.

Correlación de Eventos: Permite cruzar visualmente los datos con eventos del mundo real (huelgas, huracanes, festivos) para explicar los picos en los KPIs.


![1](/grupo05_nettalco/EVIDENCIAS/DASHBOARD2.png)

Aquí puedes acceder a los tableros interactivos en vivo:

### 📉 Dashboard 2: Análisis de Causas
> Diagnóstico operativo para identificar causas raíz de los retrasos.

[![Looker Studio](https://img.shields.io/badge/Looker_Studio-Ver_Dashboard_2-EA4335?style=for-the-badge&logo=looker&logoColor=white)](https://lookerstudio.google.com/reporting/6ade085f-ee13-4af9-a47b-697fedf4a9c4)


