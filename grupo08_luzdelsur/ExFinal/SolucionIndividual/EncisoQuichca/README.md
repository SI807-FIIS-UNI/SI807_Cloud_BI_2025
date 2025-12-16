
# Proyecto BI – Análisis de Accidentes de Tránsito (US Accidents)

## 1. Descripción del Proyecto
Este proyecto implementa una solución de **Business Intelligence en la nube** para el análisis de accidentes de tránsito en Estados Unidos, utilizando el dataset **US Accidents (2016–2023)**.  
El objetivo es identificar **patrones de ocurrencia, severidad y contexto climático** de los accidentes, permitiendo análisis por **ubicación, tiempo, zona horaria y clima** mediante dashboards analíticos.

---

## 2. Dataset
- **Fuente:** US Accidents Dataset (Kaggle)  
- **Periodo:** Febrero 2016 – Marzo 2023  
- **Naturaleza:** Datos de eventos de accidentes recopilados en tiempo real desde APIs de tráfico  
- **Volumen:** ~1 millón de registros (muestra procesada)

---

## 3. Justificación de la Plataforma (AWS)
Se eligió **Amazon Web Services (AWS)** por su soporte nativo para arquitecturas de **Data Lake** y analítica serverless:

- **Amazon S3:** almacenamiento escalable y económico para las capas Bronze, Silver y Gold.
- **AWS Glue:** ejecución de procesos ETL en PySpark y catalogación automática de datos.
- **Amazon Athena:** consultas SQL serverless directamente sobre datos en S3.
- **Power BI:** consumo analítico mediante conexión directa a Athena.

Esta combinación permite una solución **modular, escalable y sin administración de infraestructura**, alineada a buenas prácticas modernas de BI.

---

## 4. Arquitectura de la Solución
Flujo general:

CSV → S3 (Bronze Raw)  
→ Glue Visual ETL (Processed)  
→ Glue Visual ETL (Curated)  
→ Glue Notebook (Silver: Dim / Fact)  
→ Glue Notebook (Gold: KPIs)  
→ Athena Views  
→ Power BI Dashboards

Capas:
- **Bronze:** Ingesta y estandarización
- **Silver:** Modelo dimensional (Star Schema)
- **Gold:** KPIs agregados para consumo

---

## 5. Exploratory Data Analysis (EDA)

### Calidad del dato
- Columnas críticas (`severity`, `state`, `city`, `timezone`) presentan nulos mínimos o inexistentes.
- Variables climáticas presentan nulos parciales pero utilizables.
- Variables con alta ausencia de datos (coordenadas finales, campos poco relevantes) fueron descartadas.

### Hallazgos analíticos
- Alta concentración de accidentes en pocos estados (CA, TX, FL).
- Fuerte concentración urbana.
- Mayor incidencia en zonas horarias **US/Eastern** y **US/Central**.
- Variaciones de severidad asociadas a clima y ubicación.

**Conclusión:** El dataset es apto para un modelo estrella enfocado en severidad, ubicación, tiempo y clima.

---

## 6. Capa Bronze

### Raw
- Ruta S3:
`s3://ef_sin_bucket/bronze/raw/`
- Catalogado en:
`final_db_bronze.raw`

### Processed
Acciones:
- Cast de tipos
- Normalización de strings
- Conversión a Parquet

Ruta:
`s3://ef_sin_bucket/bronze/processed/`

### Curated
Columnas finales:
- severity
- state
- city
- timezone
- start_time
- variables climáticas

Ruta:
`s3://ef_sin_bucket/bronze/curated/`

---

## 7. Capa Silver – Modelo Dimensional

### Dimensiones
- `silver_dim_time`
- `silver_dim_location`
- `silver_dim_weather`

### Hechos
- `silver_fact_accidents`

Ruta:
`s3://ef_sin_bucket/silver/`

---

## 8. Capa Gold – KPIs
KPIs principales:
- Accidentes por estado
- Accidentes por ciudad
- Total de accidentes
- Accidentes por hora
- Accidentes por zona horaria
- Accidentes por clima

Ruta:
`s3://ef_sin_bucket/gold/`

---

## 9. Athena – Views
Ejemplo:

```sql
CREATE OR REPLACE VIEW vw_dataexfinal_accidents_by_state AS
SELECT state, accident_cnt, avg_severity
FROM kpi_accidents_by_state;
```

Views utilizadas:
- vw_dataexfinal_total_accidents
- vw_dataexfinal_accidents_by_state
- vw_dataexfinal_accidents_by_city
- vw_dataexfinal_accidents_by_hour
- vw_dataexfinal_accidents_by_timezone
- vw_dataexfinal_accidents_by_weather

---

## 10. Power BI – Dashboards

### Dashboard 1: Incidencia y Severidad
- Total de accidentes
- Accidentes por estado
- Top ciudades
- Accidentes por zona horaria
- Tooltips con severidad promedio

### Dashboard 2: Tiempo y Clima
- Accidentes por hora
- Accidentes por condición climática
- Severidad promedio por clima

---

## 11. Conclusión
La solución permite analizar accidentes desde una perspectiva geográfica, temporal y climática, utilizando una arquitectura Medallion sobre AWS que garantiza trazabilidad, escalabilidad y eficiencia para analítica BI.
