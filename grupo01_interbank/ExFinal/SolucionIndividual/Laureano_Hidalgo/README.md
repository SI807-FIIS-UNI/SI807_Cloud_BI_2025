# INGESTIÓN Y ESTRUCTURACIÓN - BRONCE
Se procede a descargar la información desde el link proporcionado por el profesor
<img width="1449" height="890" alt="image" src="https://github.com/user-attachments/assets/543400ef-8f8c-4833-a202-c4cf6abf59d5" />

Luego se procede a crear los buckets dentro de GCP para poder subirlas y empezar a trabajar
<img width="1639" height="218" alt="image" src="https://github.com/user-attachments/assets/ae7650fb-c671-4a68-84c0-7ee96729cee7" />

Luego de haber subido la información, usamos dataproc para abrir un JupiterNotebook y poder limpiar la información
<img width="950" height="95" alt="image" src="https://github.com/user-attachments/assets/ac4a7b5d-2220-467b-a47f-bd107ca53fb1" />

Mediante el notebook procedmos a limpiar el csv (Scripts en otro archivo)
<img width="1903" height="950" alt="image" src="https://github.com/user-attachments/assets/77202a9b-eed6-44ec-9c13-e4aac6a6b7ab" />

Donde obtenemos las siguientes estadisticas:

<img width="675" height="531" alt="image" src="https://github.com/user-attachments/assets/a85c2449-d1f9-48b6-afdf-3316bf8638e1" />

Creandose asi el archivo en el processed
<img width="1633" height="408" alt="image" src="https://github.com/user-attachments/assets/1e7085a1-56a3-433d-80b7-8fa64eaeb7fd" />

Luego de pasar el archivo al curated, procedemos a la parte de Plata y Oro

# TRANSFORMACION Y MODELO DIMENSIONAL - PLATA Y ORO
Ahora procedemos a cargar la información en tabla de SQL.
Para esto usaremos BigQuery.
Creamos la tabla.
<img width="1656" height="819" alt="image" src="https://github.com/user-attachments/assets/be1c4e19-8d25-4fee-bd9a-40b26c448734" />

Con la tabla ya ingresada, creamos las dimensiones y la tabla de hechos para hacer el estrella (Scripts en otro archivo)

# Diagrama ERD (Modelo Estrella)

```mermaid
erDiagram
  DIM_DATE ||--o{ FACT_FLIGHT_DELAY : "date_key (1:N)"
  DIM_CARRIER ||--o{ FACT_FLIGHT_DELAY : "carrier_key (1:N)"
  DIM_FLIGHT ||--o{ FACT_FLIGHT_DELAY : "flight_key (1:N)"
  DIM_AIRCRAFT ||--o{ FACT_FLIGHT_DELAY : "aircraft_key (1:N)"
  DIM_AIRPORT ||--o{ FACT_FLIGHT_DELAY : "origin_airport_key (1:N)"
  DIM_AIRPORT ||--o{ FACT_FLIGHT_DELAY : "dest_airport_key (1:N)"

  DIM_DATE {
    INT64  date_key PK
    DATE   date
    INT64  year
    INT64  month
    INT64  day
    INT64  dayofweek
  }

  DIM_CARRIER {
    INT64  carrier_key PK
    STRING uniquecarrier
    STRING airline
  }

  DIM_FLIGHT {
    INT64  flight_key PK
    STRING uniquecarrier
    STRING flightnum
  }

  DIM_AIRCRAFT {
    INT64  aircraft_key PK
    STRING tailnum
  }

  DIM_AIRPORT {
    INT64  airport_key PK
    STRING airport_code
    STRING airport_name
  }

  FACT_FLIGHT_DELAY {
    INT64 date_key FK
    INT64 carrier_key FK
    INT64 flight_key FK
    INT64 aircraft_key FK
    INT64 origin_airport_key FK
    INT64 dest_airport_key FK
  }

### Justificación de cada dimensión
DIM_DATE

- Central para análisis temporal (tendencias, estacionalidad, comparativos).
- Incluye year/month/day/dayofweek para evitar calcularlo en cada consulta.
- Clave date_key = yyyymmdd es estándar en DWH y eficiente.

DIM_CARRIER 

- uniquecarrier es un identificador natural y airline el nombre descriptivo.
- Permite analizar métricas por aerolínea: demoras promedio, cancelaciones, distribución de causas.

DIM_AIRPORT

- Los aeropuertos aparecen repetidos en millones de filas; separarlos reduce redundancia.
- Se modela una sola dimensión y en la fact se usan dos FKs:
- origin_airport_key y dest_airport_key
- Habilita análisis por aeropuerto de salida/llegada y por rutas.

DIM_AIRCRAFT 

- tailnum identifica el avión específico (alta utilidad para mantenimiento/calidad operativa).
- Permite detectar aeronaves con mayor incidencia de demora o cancelación.

DIM_FLIGHT

- flightnum por sí solo puede repetirse entre aerolíneas, por eso la clave natural es: (uniquecarrier, flightnum)
- Permite analizar comportamiento por número de vuelo y combinarlo con fecha/aeropuerto.

### Justificación de la tabla de hechos
fact_flight_delay

Contiene:
- Claves foráneas hacia dimensiones (date, carrier, flight, aircraft, airport origen/dest).

Métricas y tiempos:
- demoras (arrdelay, depdelay, y causas)
- duraciones (airtime, elapsed times)
- operaciones (taxiin, taxiout, distance)
- flags (cancelled, diverted)
- Metadatos (_source_path, _ingestion_ts) para trazabilidad y auditoría.










