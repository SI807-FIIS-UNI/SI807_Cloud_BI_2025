# Tabla de Hechos: `fact_vuelos_gold`

En esta carpeta se documenta la **tabla de hechos** del modelo dimensional (capa Oro) orientado al análisis de **retrasos de vuelos y sus causas**.

La tabla `fact_vuelos_gold` concentra las **métricas de retraso**, estado de **cancelación**, y los **minutos asociados a cada causa de demora**. Además, incluye atributos de fecha (año/mes/día) y claves descriptivas como aerolínea y aeropuertos (origen/destino), lo cual permite realizar análisis comparativos por compañía, ruta y periodo.

Este modelo busca responder preguntas como:
- ¿Qué aerolíneas presentan mayor porcentaje de retrasos?
- ¿En qué rutas (origen → destino) se registran mayores demoras?
- ¿Qué causas explican más minutos de retraso (Carrier, Weather, NAS, Security, Late Aircraft)?
- ¿Qué aerolíneas presentan más cancelaciones?

---

## Estructura de la tabla

| Campo | Descripción |
|------|-------------|
| year | Año del vuelo (derivado de la fecha). |
| month | Mes del vuelo (1-12). |
| day_of_month | Día del mes del vuelo (1-31). |
| day_of_week | Día de la semana (1-7 según la función `dayofweek` de Spark). |
| carrier_code | Código de aerolínea/carrier (ej. AA, DL, UA). |
| origin | Código IATA del aeropuerto de origen (ej. JFK, LAX). |
| dest | Código IATA del aeropuerto de destino (ej. SFO, MIA). |
| dep_delay | Minutos de retraso en salida (departure delay). |
| arr_delay | Minutos de retraso en llegada (arrival delay). |
| cancelled | Indicador de cancelación (0 = No, 1 = Sí). |
| delay_carrier | Minutos de retraso atribuibles a la aerolínea (mantenimiento, tripulación, combustible, etc.). |
| delay_weather | Minutos de retraso por condiciones climáticas. |
| delay_nas | Minutos de retraso por NAS (National Airspace System: congestión/control aéreo, etc.). |
| delay_security | Minutos de retraso por razones de seguridad. |
| delay_late_aircraft | Minutos de retraso por aeronave tardía proveniente de vuelos previos. |

---

## Relación con dimensiones

Aunque en esta capa Oro el hecho mantiene campos descriptivos (códigos y componentes de fecha), se complementa con las dimensiones para análisis y consistencia:

- **Tiempo:** `dim_tiempo_gold` (year, month, day_of_month, day_of_week)
- **Aerolínea:** `dim_aerolinea_gold` (carrier_code)
- **Aeropuertos:** `dim_origen_gold` y `dim_destino_gold` (airport_code)

> Nota: Este esquema corresponde al modelo generado en Databricks usando Delta Tables en la capa Oro.
