# Modelo Estrella Completo (Star Schema)

En esta etapa se diseñó e implementó un **modelo estrella completo** para el análisis de **retrasos de vuelos y sus causas** (Carrier, Weather, NAS, Security, Late Aircraft, etc.).  
El objetivo del modelo es **separar la información descriptiva (dimensiones)** de las **métricas y eventos del vuelo (tabla de hechos)** para habilitar consultas analíticas rápidas, consistentes y fáciles de entender (capa tipo *Gold/Semántica*).

## Diagrama entidad–relación (ERD)

A continuación se presenta el diagrama generado desde el servicio de **PostgreSQL en Azure**, donde se visualiza la tabla de hechos al centro y sus dimensiones conectadas (estructura tipo estrella):

<img width="1568" height="1283" alt="Untitled" src="https://github.com/user-attachments/assets/73017bed-f6ef-4228-94a0-7c186fc262d9" />



## Descripción del modelo

### Granualidad del modelo (nivel de detalle)
La granualidad de la tabla de hechos es:  
**un registro por vuelo** (por fecha, aerolínea, aeropuerto origen, aeropuerto destino y aeronave si aplica).

Esto permite analizar retrasos por múltiples ejes: tiempo, aerolínea, rutas (origen/destino), aeronave y causas de demora.

---

## Componentes del modelo

### Tabla de hechos
**`fact_flight_delays`**  
Contiene las métricas operacionales del vuelo (tiempos, distancias, retrasos y causas) y llaves foráneas hacia las dimensiones.

**Principales métricas/campos:**
- Horarios: `dep_time`, `arr_time`, `crs_arr_time`
- Duraciones: `actual_elapsed_time`, `crs_elapsed_time`, `air_time`
- Retrasos: `arr_delay`, `dep_delay`
- Operación: `taxi_in`, `taxi_out`, `distance`
- Estado del vuelo: `cancelled`, `diverted`, `cancellation_code`
- Causas del retraso: `carrier_delay`, `weather_delay`, `nas_delay`, `security_delay`, `late_aircraft_delay`

---

### Tablas de dimensiones
Las dimensiones almacenan atributos descriptivos para filtrar, agrupar y segmentar el análisis:

- **`dim_date`**: permite análisis temporal (fecha, día de semana, mes, año).
- **`dim_airline`**: catálogo de aerolíneas (código de carrier y nombre).
- **`dim_airport`**: catálogo de aeropuertos (código IATA y nombre).
- **`dim_aircraft`**: catálogo de aeronaves (Tail Number).  
  > `aircraft_id` en hechos puede ser **NULL** si el dataset no trae `TailNum`.

**Relación clave del modelo:**  
La tabla de hechos referencia dos veces a `dim_airport`:
- `origin_airport_id` → aeropuerto de origen  
- `dest_airport_id` → aeropuerto de destino

---

## Capa semántica (vista de consumo)
Se creó la vista **`vw_flight_analytics`** como una capa de “oro” o semántica, uniendo la tabla de hechos con dimensiones para facilitar el consumo en consultas y dashboards (evita joins repetitivos y estandariza nombres/atributos).

---

## Justificación técnica del modelo estrella

Se eligió un **modelo estrella** porque:
- **Optimiza analítica y BI**: reduce complejidad para consultas agregadas (promedios, conteos, rankings).
- **Mejora desempeño**: joins controlados (hechos → dimensiones) y modelo preparado para índices por llaves foráneas.
- **Consistencia e integridad**: el uso de PK/FK estandariza códigos y evita duplicidades (aerolíneas/aeropuertos/fechas).
- **Escalabilidad**: permite agregar nuevas dimensiones o métricas (por ejemplo: `dim_route`, `dim_weather_station`) sin romper el modelo existente.
- **Facilita preguntas típicas del caso**:
  - ¿Qué aerolínea tiene mayor retraso promedio por mes?
  - ¿Qué rutas (origen→destino) presentan más demoras por causa NAS?
  - ¿En qué días de la semana aumentan las cancelaciones?

---

## Implementación en PostgreSQL sobre Azure (justificación técnica)
El modelo se desplegó en **PostgreSQL administrado en Azure** porque:
- Provee un servicio **gestionado** (parches, mantenimiento, alta disponibilidad y respaldos automáticos).
- Permite **escalar** recursos según crecimiento del dataset y carga analítica.
- Ofrece controles de **seguridad** (red, autenticación, cifrado en tránsito/almacenamiento).
- Se integra fácilmente con el ecosistema de Azure para analítica/visualización (por ejemplo, Power BI, Data Factory, Synapse, etc.).

---

 
