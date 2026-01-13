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
