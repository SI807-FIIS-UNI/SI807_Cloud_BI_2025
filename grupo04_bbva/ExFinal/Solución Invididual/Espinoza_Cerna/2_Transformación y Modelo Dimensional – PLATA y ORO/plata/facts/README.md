# Tabla de Hechos: `fact_flight_delays`

En esta carpeta se documenta la **tabla de hechos** del modelo dimensional para el análisis de **retrasos de vuelos y sus causas**.  
La tabla `fact_flight_delays` concentra las **métricas y atributos operativos** del vuelo (tiempos, demoras, distancia, cancelaciones y causas), y se relaciona con las dimensiones para permitir análisis por **fecha**, **aerolínea**, **aeropuerto de origen/destino** y **aeronave**.

Su objetivo es responder preguntas como:
- ¿Qué aerolíneas presentan mayores retrasos promedio?
- ¿Qué rutas (origen → destino) se retrasan más?
- ¿Qué causa de demora es más frecuente (clima, NAS, seguridad, etc.)?

## Estructura de la tabla

| Campo | Descripción |
|------|-------------|
| flight_delay_id (PK) | Identificador único del registro de retraso/vuelo. |
| date_id (FK) | Clave foránea hacia `dim_date` (fecha programada del vuelo). |
| airline_id (FK) | Clave foránea hacia `dim_airline` (aerolínea / carrier). |
| origin_airport_id (FK) | Clave foránea hacia `dim_airport` (aeropuerto de origen). |
| dest_airport_id (FK) | Clave foránea hacia `dim_airport` (aeropuerto de destino). |
| aircraft_id (FK, nullable) | Clave foránea hacia `dim_aircraft` (aeronave). Puede ser nulo si no hay TailNum. |
| flight_num | Número de vuelo. |
| dep_time | Hora real de salida (local, formato hhmm). |
| arr_time | Hora real de llegada (local, formato hhmm). |
| crs_arr_time | Hora programada de llegada (local, formato hhmm). |
| actual_elapsed_time | Tiempo real total del vuelo (min), incluye taxi-in/taxi-out. |
| crs_elapsed_time | Tiempo estimado/programado del vuelo (min). |
| air_time | Tiempo en el aire (min). |
| arr_delay | Retraso en llegada (min): diferencia entre llegada real y programada. |
| dep_delay | Retraso en salida (min). |
| distance | Distancia entre aeropuertos (millas). |
| taxi_in | Tiempo desde aterrizaje hasta puerta (min). |
| taxi_out | Tiempo desde puerta hasta despegue (min). |
| cancelled | Indica si el vuelo fue cancelado (true/false). |
| diverted | Indica si el vuelo fue desviado (true/false). |
| cancellation_code | Código/motivo de cancelación. |
| carrier_delay | Demora atribuida a la aerolínea (min). |
| weather_delay | Demora por clima (min). |
| nas_delay | Demora por NAS (National Airspace/System) (min). |
| security_delay | Demora por seguridad (min). |
| late_aircraft_delay | Demora por llegada tardía de la aeronave (min). |


