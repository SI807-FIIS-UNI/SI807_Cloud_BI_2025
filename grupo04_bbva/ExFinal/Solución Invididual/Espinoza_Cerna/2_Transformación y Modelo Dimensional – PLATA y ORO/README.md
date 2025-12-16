# Modelo Estrella Completo (Star Schema)

En esta etapa se diseñó e implementó un **modelo estrella completo** para el análisis de **retrasos de vuelos y sus causas** (Carrier, Weather, NAS, Security, Late Aircraft, etc.).  
El objetivo del modelo es **separar la información descriptiva (dimensiones)** de las **métricas del evento de vuelo (tabla de hechos)**, facilitando consultas analíticas rápidas, consistentes y fáciles de consumir (capa tipo **Gold/Semántica**).

---

## Diagrama entidad–relación (ERD)

A continuación se presenta el diagrama del modelo estrella (tabla de hechos al centro y dimensiones conectadas):

<img width="886" height="753" alt="image" src="https://github.com/user-attachments/assets/146d4d01-b551-44a9-843a-1321b2f0819e" />


## Descripción del modelo

### Granularidad del modelo (nivel de detalle)
La granularidad de la tabla de hechos es:

**Un registro por combinación de vuelo y su contexto analítico** (fecha del vuelo, aerolínea, aeropuerto de origen y destino), con sus métricas de retraso y causas.

Esto permite analizar retrasos por múltiples ejes: tiempo, aerolínea, ruta (origen/destino) y causas de demora.

---

## Componentes del modelo

### Tabla de hechos

## `fact_vuelos_gold`
Contiene las **métricas operacionales** asociadas al vuelo y las **causas del retraso**. También incluye campos de tiempo (año/mes/día/weekday) y códigos de aerolínea y aeropuertos para relacionarse con las dimensiones.

**Principales métricas/campos:**
- Retrasos: `dep_delay`, `arr_delay`
- Estado operativo: `cancelled`
- Causas del retraso (minutos):
  - `delay_carrier`
  - `delay_weather`
  - `delay_nas`
  - `delay_security`
  - `delay_late_aircraft`
- Contexto del vuelo:
  - `carrier_code`
  - `origin`
  - `dest`
  - `year`, `month`, `day_of_month`, `day_of_week`

---

### Tablas de dimensiones
Las dimensiones almacenan atributos descriptivos (catálogos) que permiten **filtrar, agrupar y segmentar** el análisis:

- **`dim_tiempo_gold`**: dimensión temporal derivada de la fecha del vuelo (`year`, `month`, `day_of_month`, `day_of_week`) e identificador `id_tiempo`.
- **`dim_aerolinea_gold`**: catálogo de aerolíneas mediante `carrier_code`.
- **`dim_origen_gold`**: catálogo de aeropuertos utilizados como origen (`airport_code`).
- **`dim_destino_gold`**: catálogo de aeropuertos utilizados como destino (`airport_code`).

**Relación clave del modelo:**  
La tabla de hechos se relaciona con aeropuertos en dos roles:
- `origin` → `dim_origen_gold.airport_code`
- `dest` → `dim_destino_gold.airport_code`

---

## Tabla de KPIs (capa de consumo)

## `kpis_reporte_gold`
Se generó una tabla adicional con indicadores agregados por aerolínea, orientada a consumo rápido en reportes o dashboards.

Ejemplos de KPIs calculados:
- `porcentaje_retrasos`: % de vuelos con retraso de llegada superior a 15 minutos
- `retraso_promedio_llegada`: retraso promedio de llegada por aerolínea

> Nota: Esta tabla tabla funciona como una capa “lista para BI”, reduciendo la necesidad de agregaciones repetitivas al consultar `fact_vuelos_gold`.

---

## Justificación técnica del modelo estrella

Se eligió un **modelo estrella** porque:

- **Optimiza analítica y BI**: simplifica consultas típicas (promedios, conteos, rankings) al centralizar métricas en una tabla de hechos.
- **Mejora desempeño**: favorece joins simples (hechos → dimensiones) y un diseño natural para indexación y particionado por tiempo.
- **Consistencia**: estandariza el uso de catálogos (aerolíneas y aeropuertos) evitando inconsistencias por valores repetidos o sucios.
- **Escalabilidad**: permite agregar nuevas dimensiones o métricas sin rediseñar el modelo (por ejemplo, una dimensión de rutas o estacionalidad).
- **Soporta preguntas del caso**:
  - ¿Qué aerolínea tiene mayor retraso promedio por mes?
  - ¿Qué causas generan más minutos de retraso por aerolínea?
  - ¿Qué rutas presentan mayores demoras y en qué días de semana?

---

## Relación con la arquitectura Medallion (Bronze/Silver/Gold)

Este modelo corresponde a la **capa Gold**, construida a partir de:
- **Bronze:** datos crudos (raw) cargados desde el CSV original.
- **Silver:** datos estandarizados (columnas normalizadas, duplicados eliminados y consistencia básica).
- **Gold:** modelo estrella y KPIs listos para consumo analítico.

---

## Consideraciones de implementación (Databricks + Delta)

El modelo se implementó sobre **Delta Tables** en Databricks, lo cual aporta:
- Persistencia confiable (ACID) y control de versiones.
- Mejor desempeño en lecturas analíticas.
- Facilidad para re-procesos (overwrite controlado) y evolución de esquema.

Además, el enfoque facilita la integración con herramientas de visualización (por ejemplo, Power BI) al contar con tablas consolidadas (`fact_vuelos_gold`, dimensiones y `kpis_reporte_gold`).
