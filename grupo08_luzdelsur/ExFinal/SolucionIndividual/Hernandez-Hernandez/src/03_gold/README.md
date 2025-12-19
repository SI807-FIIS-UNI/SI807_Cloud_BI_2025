### 3. Agregación de Valor y KPIs de Negocio – Capa ORO

La Capa Oro representa la etapa final del pipeline de ingeniería de datos, donde la información granular de la Capa Plata es transformada en **insights accionables** listos para ser consumidos por herramientas de visualización (Power BI) y el Data Warehouse.

#### Estrategia de KPIs y Reglas de Negocio
Se generaron dos tablas agregadas enfocadas en resolver la problemática principal: **"Identificar ciudades y periodos críticos de contaminación"**.

**1. Tabla: `oro_kpi_mensual` (Análisis de Tendencias)**
* **Objetivo:** Permitir el análisis de estacionalidad y evolución de la calidad del aire a lo largo del tiempo.
* **Transformación:** Agrupación de datos por `Ciudad`, `Año` y `Mes`.
* **Métricas Calculadas:**
    * `AQI_Promedio`: Promedio aritmético del índice de calidad del aire para suavizar picos diarios.
    * `PM2_5_Promedio`: Concentración media de partículas finas.
    * `AQI_Maximo`: Detección de los picos máximos de contaminación en el mes.

**2. Tabla: `oro_top_criticos` (Ranking de Riesgo)**
* **Objetivo:** Identificar las zonas geográficas que representan un mayor peligro para la salud pública.
* **Regla de Negocio (Business Rule):** Se definió como "Día Crítico" aquel donde el AQI supera los **200 puntos** (Categorías: *Poor*, *Very Poor*, *Severe*).
* **Transformación:** Filtrado de registros (`AQI > 200`) y conteo de ocurrencias por ciudad y año.
* **Resultado:** Un ranking ordenado descendentemente por `Dias_Criticos_High_Risk`, destacando las ciudades que requieren intervención inmediata.

#### Integración con Data Warehouse (Azure Synapse Analytics)
Para cumplir con los requisitos de una arquitectura empresarial moderna, los datos procesados en la Capa Oro no permanecen aislados en el Data Lake.

* **Persistencia:** Se implementó un proceso de escritura vía **JDBC** desde Azure Databricks hacia **Azure Synapse Analytics (Dedicated SQL Pool)**.
* **Beneficio:** Esto permite que los analistas de negocio consulten los KPIs utilizando SQL estándar y conecta nativamente con Power BI en modo "DirectQuery" o "Import" con alto rendimiento.

#### Scripts y Reproducibilidad
El código fuente de esta capa se encuentra en la carpeta `src/03_gold/`.

* **Script de Generación:** `src/03_gold/generacion_kpis.py`
    * *Función:* Realiza los JOINs entre hechos y dimensiones, aplica las agregaciones y filtros de negocio, y carga los resultados finales en Synapse.