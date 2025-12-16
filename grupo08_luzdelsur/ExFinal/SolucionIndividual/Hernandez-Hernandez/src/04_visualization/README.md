## 3.3. Visualización y Reportes de Inteligencia de Negocios (BI)

### Arquitectura de Conexión (Lakehouse)
Se implementó una solución de **BI Moderno** conectando **Microsoft Power BI Desktop** directamente al clúster de **Azure Databricks**.
* **Estrategia:** Se utilizó el conector nativo de Databricks en modo **Import**, consumiendo tanto las tablas del Modelo Dimensional (Capa Plata) para exploración flexible, como las tablas Agregadas (Capa Oro) para KPIs pre-calculados.

### Descripción de Dashboards Implementados

Se diseñaron dos tableros estratégicos para cubrir diferentes necesidades de análisis:

#### 1. Monitor Histórico de Calidad del Aire (Tendencias)
*Enfoque: Análisis Exploratorio y Estacionalidad (2015-2020)*

![Dashboard Tendencias](src/img/dashboard_tendencias.png)
*(Nota: Inserta aquí la captura de tu primer dashboard)*

* **KPIs Generales:** Tarjetas superiores mostrando el AQI Promedio Histórico y el Máximo registrado, brindando contexto inmediato.
* **Evolución Temporal:** Gráfico de líneas interactivo que permite comparar la curva de contaminación de múltiples ciudades simultáneamente a lo largo de los años.
* **Matriz de Calor (Heatmap):** Tabla cruzada (Año vs Mes) con formato condicional. Permite detectar patrones estacionales a simple vista (ej. meses de invierno con alta intensidad de color rojo debido a la contaminación).
* **Geolocalización:** Mapa de burbujas que dimensiona la gravedad de la contaminación por ubicación geográfica.

#### 2. Reporte Ejecutivo: Zonas Críticas y Riesgo
*Enfoque: Toma de Decisiones y Alertas Sanitarias*

![Dashboard Riesgos](src/img/dashboard_riesgos.png)
*(Nota: Inserta aquí la captura de tu segundo dashboard)*

* **Ranking de Ciudades Peligrosas:** Gráfico de barras horizontales ordenado descendentemente por la métrica `Días Críticos` (AQI > 200), identificando rápidamente los focos de acción prioritaria (ej. Delhi, Ahmedabad).
* **Distribución de Severidad:** Gráfico de anillos (Donut Chart) que visualiza el porcentaje de registros clasificados como "Severe", "Poor", "Good", etc., permitiendo entender la proporción de riesgo global.
* **Análisis Regional (Treemap):** Visualización de jerarquía por `Estado`, donde el tamaño de los bloques representa la intensidad de contaminación en la región, facilitando la comparación entre provincias.
* **Detalle Tabular:** Tabla de resumen con barras de datos integradas para auditoría de cifras exactas por ciudad y año.

### Modelo de Datos en Power BI
Para soportar estos reportes, se recreó el **Esquema Estrella** dentro de Power BI, estableciendo relaciones activas entre la tabla de hechos y las dimensiones.

![Modelo Estrella Power BI](src/02_silver/modelo_estrella.png)

* **Tablas Importadas:**
    * `plata_fact_calidad_aire`: Contiene métricas detalladas y claves foráneas.
    * `plata_dim_tiempo`: Permite el filtrado jerárquico (Año > Trimestre > Mes).
    * `plata_dim_ciudad`: Permite la segmentación geográfica (Ciudad > Estado).
    * `oro_top_criticos`: Tabla auxiliar optimizada para el ranking de días de riesgo.