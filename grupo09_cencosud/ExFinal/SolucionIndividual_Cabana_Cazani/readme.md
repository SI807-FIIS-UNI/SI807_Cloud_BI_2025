## 📋 Descripción del Proyecto
Solución de Business Intelligence en Google Cloud Platform (GCP) para el análisis de contaminación ambiental. El sistema ingesta datos crudos, los modela en un esquema dimensional y presenta dashboards para la toma de decisiones estratégicas y operativas.


# Examen Final BI - Solución Cloud de Calidad del Aire

## 📋 Descripción del Proyecto
Solución de Business Intelligence en Google Cloud Platform (GCP) para el análisis de contaminación ambiental. El sistema ingesta datos crudos, los modela en un esquema dimensional y presenta dashboards para la toma de decisiones estratégicas y operativas.

---

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

### Componentes
- **Tabla de Hechos (`fact_calidad_aire`):** Contiene las métricas numéricas (AQI, PM2.5, NO2) y claves foráneas.
- **Dimensión Ciudad (`dim_ciudad`):** Catálogo único de ciudades con IDs subrogados para normalizar nombres.
- **Dimensión Tiempo (`dim_tiempo`):** Desglose de fechas (Año, Mes, Día) para facilitar el análisis temporal (Drill-down).
### Justificación Técnica
Este diseño reduce la redundancia de datos (normalización de dimensiones) y mejora el rendimiento de BigQuery al permitir agregaciones rápidas sobre la tabla de hechos, cumpliendo con los estándares de Data Warehousing moderno.

---

## 📊 2. KPIs Relevantes

Se definieron métricas orientadas a la acción:

1.  **% de Días Críticos:** Proporción de días con categoría "Severe" (AQI > 400). *Justificación: Permite identificar riesgos sanitarios inmediatos.*
2.  **Contaminante Dominante:** Identifica el químico con mayor concentración por ciudad. *Justificación: Diferencia problemas de tráfico (NO2) vs. polvo (PM10).*
3.  **Tendencia de Calidad:** Promedio móvil mensual del AQI. *Justificación: Detecta patrones estacionales de contaminación.*
4.  **Concentración de BTX:** Monitoreo de Benceno, Tolueno y Xileno. *Justificación: Control de contaminantes industriales cancerígenos.*

---

## 🎨 3. Visualización y Diseño (Sustentación)

Se implementaron **2 Dashboards** en Looker Studio y scripts de evidencia estática:

### Dashboard Estratégico (Gerencial)
- **Diseño:** Uso de **Tarjetas (Scorecards)** y **Gráficos de Donut**.
- **Sustentación:** Los directivos requieren ver el estado general en segundos. El gráfico de Donut muestra la distribución global (Bueno vs Malo) de un vistazo, sin saturación técnica.

### Dashboard Técnico (Operativo)
- **Diseño:** Uso de **Mapas de Calor** y **Barras Apiladas**.
- **Sustentación:** Los técnicos necesitan identificar "dónde" y "qué". El mapa de calor resalta en rojo las ciudades críticas, y las barras apiladas descomponen la mezcla química para elegir la estrategia de mitigación adecuada.
