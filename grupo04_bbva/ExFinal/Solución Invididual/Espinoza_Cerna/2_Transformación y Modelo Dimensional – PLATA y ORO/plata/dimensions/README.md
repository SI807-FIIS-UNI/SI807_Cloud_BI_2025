# Tablas de Dimensiones (Capa Oro)

En esta carpeta se documentan las **dimensiones** del modelo dimensional (capa Oro), las cuales contienen información descriptiva que permite **segmentar y analizar** los registros de la tabla de hechos `fact_vuelos_gold`.

Estas dimensiones soportan análisis como:
- Evolución de retrasos por **día/mes/año**.
- Comparación por **aerolínea (carrier)**.
- Análisis por **aeropuerto de origen** y **aeropuerto de destino**.
- Análisis por patrones temporales (día del mes, día de semana).

---

## Resumen de dimensiones

| Dimensión | Clave principal | Descripción general | Principales atributos |
|----------|------------------|---------------------|-----------------------|
| dim_tiempo_gold | id_tiempo | Dimensión temporal derivada de la fecha del vuelo. | year, month, day_of_month, day_of_week |
| dim_aerolinea_gold | carrier_code | Catálogo de aerolíneas (carrier). | carrier_code |
| dim_origen_gold | airport_code | Catálogo de aeropuertos usados como origen. | airport_code |
| dim_destino_gold | airport_code | Catálogo de aeropuertos usados como destino. | airport_code |

---

## Detalle de campos por dimensión

## `dim_tiempo_gold`

| Campo | Descripción |
|------|-------------|
| id_tiempo | Identificador único generado en Databricks (`monotonically_increasing_id`). |
| year | Año del vuelo. |
| month | Mes del vuelo (1-12). |
| day_of_month | Día del mes (1-31). |
| day_of_week | Día de la semana (según Spark: 1-7). |

---

## `dim_aerolinea_gold`

| Campo | Descripción |
|------|-------------|
| carrier_code | Código único de la aerolínea/carrier (ej. AA, DL, UA). |

> Nota: En esta implementación se usa el código como identificador principal, ya que el dataset ya lo trae como valor estable.

---

## `dim_origen_gold`

| Campo | Descripción |
|------|-------------|
| airport_code | Código IATA del aeropuerto (ej. JFK, LAX). |

---

## `dim_destino_gold`

| Campo | Descripción |
|------|-------------|
| airport_code | Código IATA del aeropuerto (ej. SFO, MIA). |

---

## Relación con la tabla de hechos

La tabla `fact_vuelos_gold` contiene los campos `carrier_code`, `origin` y `dest`, que se conectan con estas dimensiones:

- `fact_vuelos_gold.carrier_code` → `dim_aerolinea_gold.carrier_code`
- `fact_vuelos_gold.origin` → `dim_origen_gold.airport_code`
- `fact_vuelos_gold.dest` → `dim_destino_gold.airport_code`

Además, la segmentación temporal se realiza con los atributos (`year`, `month`, `day_of_month`, `day_of_week`) generados en la dimensión tiempo.
