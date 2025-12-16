# Tablas de Dimensiones

En esta carpeta se documentan las **dimensiones** del modelo, las cuales contienen información descriptiva (atributos) que permite **segmentar y analizar** los registros de la tabla de hechos `fact_flight_delays`.

Estas dimensiones soportan análisis como:
- Evolución de retrasos por **día/mes/año**.
- Comparación por **aerolínea**.
- Análisis por **aeropuerto de origen/destino**.
- Análisis por **aeronave** (Tail Number).

## Resumen de dimensiones

| Dimensión | Clave primaria | Descripción general | Principales atributos |
|----------|-----------------|---------------------|-----------------------|
| dim_date | date_id | Dimensión temporal basada en la fecha programada del vuelo. | flight_date, day_of_week, month, year |
| dim_airline | airline_id | Catálogo de aerolíneas (carrier) para análisis por compañía. | carrier_code, airline_name |
| dim_airport | airport_id | Catálogo de aeropuertos de origen y destino. | airport_code, airport_name |
| dim_aircraft | aircraft_id | Identifica aeronaves por tail number (matrícula). | tail_num |

## Detalle de campos por dimensión

### `dim_date`
| Campo | Descripción |
|------|-------------|
| date_id (PK) | Identificador único de la fecha. |
| flight_date | Fecha programada del vuelo (DATE). |
| day_of_week | Día de la semana (1=Lunes, 7=Domingo). |
| month | Mes (1-12). |
| year | Año (YYYY). |

### `dim_airline`
| Campo | Descripción |
|------|-------------|
| airline_id (PK) | Identificador único de la aerolínea. |
| carrier_code | Código único del carrier (ej. “AA”, “DL”). |
| airline_name | Nombre de la aerolínea. |

### `dim_airport`
| Campo | Descripción |
|------|-------------|
| airport_id (PK) | Identificador único del aeropuerto. |
| airport_code | Código IATA del aeropuerto (ej. “JFK”, “LAX”). |
| airport_name | Nombre descriptivo del aeropuerto. |

### `dim_aircraft`
| Campo | Descripción |
|------|-------------|
| aircraft_id (PK) | Identificador único de la aeronave. |
| tail_num | Matrícula / tail number de la aeronave. |
