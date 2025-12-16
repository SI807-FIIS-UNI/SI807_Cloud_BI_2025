# Alumno: Cabana Cazani Gabriel
# Codigo: 20212541J

# Examen Final BI - Solución Cloud de Calidad del Aire

## 📋 Descripción del Proyecto
Solución de Business Intelligence en Google Cloud Platform (GCP) para el análisis de contaminación ambiental. El sistema ingesta datos crudos, los modela en un esquema dimensional y presenta dashboards para la toma de decisiones estratégicas y operativas.


## ☁️ Justificación Técnica de la Nube (GCP)

Se seleccionó **Google Cloud Platform (GCP)** sobre otras alternativas (AWS/Azure) por las siguientes razones técnicas y de negocio:

1.  **Arquitectura Serverless (BigQuery):**
    * A diferencia de un Data Warehouse tradicional (como Redshift o SQL Server), BigQuery no requiere provisión de servidores. Esto elimina la carga operativa de mantenimiento y permite escalar de Gigabytes a Petabytes automáticamente.
2.  **Rendimiento Analítico (Almacenamiento Columnar):**
    * BigQuery utiliza almacenamiento columnar (Capacitor), lo que optimiza drásticamente las consultas de agregación típicas de BI (SUM, AVG, COUNT) frente a bases de datos orientadas a filas.
3.  **Ecosistema Integrado:**
    * La conexión entre **Cloud Storage** (Data Lake), **BigQuery** (Data Warehouse) y **Looker Studio** (Visualización) es nativa. Esto reduce la latencia de los datos y elimina la necesidad de conectores ODBC/JDBC complejos o licencias externas de visualización (como Power BI Pro o Tableau).
4.  **Costo-Eficiencia (Separación Cómputo/Almacenamiento):**

---

## 🏗️ 1. Modelo de Datos (Esquema Estrella)

Se construyó un **Modelo Estrella Mínimo** para optimizar las consultas analíticas:

📖 Diccionario de Datos del Modelo Estrella

#### 1. Tabla de Hechos: `fact_calidad_aire`
Contiene las mediciones diarias y las métricas químicas. Se conecta a las dimensiones a través de IDs numéricos.

| Tipo | Campo | Descripción |
| :--- | :--- | :--- |
| **FK** | `id_ciudad` | Llave foránea conectada a `dim_ciudad`. |
| **FK** | `id_tiempo` | Llave foránea conectada a `dim_tiempo`. |
| **Métrica** | `AQI` | Índice de Calidad del Aire (Valor numérico global). |
| **Métrica** | `PM2_5` | Partículas finas (< 2.5 µm). Principal agente de riesgo. |
| **Métrica** | `PM10` | Partículas respirables (< 10 µm). |
| **Métrica** | `NO2` | Dióxido de Nitrógeno (Tráfico vehicular). |
| **Métrica** | `SO2` | Dióxido de Azufre (Industria). |
| **Métrica** | `CO` | Monóxido de Carbono. |
| **Métrica** | `O3` | Ozono troposférico. |
| **Métrica** | `Benzene`, `Toluene`, `Xylene` | Compuestos BTX (Tóxicos industriales). |
| **Atributo** | `AQI_Bucket` | Categoría textual del aire (Good, Moderate, Severe). |

#### 2. Dimensión: `dim_ciudad`
Catálogo maestro de ubicaciones geográficas.

| Tipo | Campo | Descripción |
| :--- | :--- | :--- |
| **PK** | `id_ciudad` | Llave primaria subrogada (Auto-incremental). |
| **Atributo** | `City` | Nombre estandarizado de la ciudad (Ej: "Delhi"). |

#### 3. Dimensión: `dim_tiempo`
Desglose cronológico para facilitar el análisis temporal (Drill-down).

| Tipo | Campo | Descripción |
| :--- | :--- | :--- |
| **PK** | `id_tiempo` | Llave primaria subrogada (YYYYMMDD). |
| **Atributo** | `Date` | Fecha completa (Formato DATE). |
| **Atributo** | `anio` | Año (Ej: 2020). |
| **Atributo** | `mes` | Número de mes (1-12). |
| **Atributo** | `dia` | Día del mes (1-31). |
### Justificación Técnica
Este diseño reduce la redundancia de datos (normalización de dimensiones) y mejora el rendimiento de BigQuery al permitir agregaciones rápidas sobre la tabla de hechos, cumpliendo con los estándares de Data Warehousing moderno.

## 📊 3. KPIs y Métricas Relevantes

Se definieron 8 métricas clave para cubrir distintos ángulos de la problemática ambiental:

1.  **Resumen Global (Scorecards):** Promedio histórico, Máximo registrado y Total de ciudades.
    * *Justificación:* Permite a la gerencia evaluar la magnitud del proyecto en segundos.
2.  **Top Ciudades Contaminadas:** Ranking de ciudades por AQI promedio.
    * *Justificación:* Benchmarking geográfico para asignar presupuestos a las zonas más afectadas.
3.  **Tendencia Temporal:** Evolución mensual del AQI.
    * *Justificación:* Detecta patrones estacionales (ej. empeoramiento en invierno) para planificación a largo plazo.
4.  **% de Días Críticos:** Conteo de días con categoría "Severe" (AQI > 200).
    * *Justificación:* KPI de alerta temprana para identificar riesgos sanitarios inmediatos.
5.  **Distribución de Calidad:** Porcentaje de días Buenos vs. Moderados vs. Severos.
    * *Justificación:* Visión holística de la habitabilidad general del aire.
6.  **Mix de Contaminantes:** Promedio de PM2.5, PM10, NO2, SO2 y CO por ciudad.
    * *Justificación:* Descompone el problema para diferenciar causas físicas (polvo) de químicas (combustión).
7.  **Contaminante Dominante:** Identifica el químico con el valor máximo en cada ciudad.
    * *Justificación:* Determina el foco principal de mitigación (ej. restringir tráfico vs. regular construcción).
8.  **Concentración de BTX:** Monitoreo de Benceno, Tolueno y Xileno.
    * *Justificación:* Control específico de contaminantes industriales cancerígenos que requieren regulación estricta.

## 🎨 3. Visualización y Diseño (Sustentación)

Se implementaron **2 Dashboards** en Looker Studio y scripts de evidencia estática:

### Dashboard Estratégico (Gerencial)
- **Diseño:** Uso de **Tarjetas (Scorecards)** y **Gráfico de líneas**.
- **Sustentación:** Los directivos requieren ver el estado general en segundos. El gráfico de Líneas muestra la tendencia del impacto de los gases en el tiempo.

### Dashboard Técnico (Operativo)
- **Diseño:** Uso de **Mapas de Calor** y **Barras Apiladas**.
- **Sustentación:** Los técnicos necesitan identificar "dónde" y "qué". El mapa de calor resalta en rojo las ciudades críticas, y las barras apiladas descomponen la mezcla química para elegir la estrategia de mitigación adecuada.
# Link de Dashboard: 
https://lookerstudio.google.com/reporting/061c979c-610e-459e-9ac6-8bfbb79e763c
# Rama: gabrielcabanac-patch-8
Los scripts ejecutados se encuentran en la carpeta docs
