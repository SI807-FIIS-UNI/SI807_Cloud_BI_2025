-- ============================================================
-- MODELO DE DATOS PARA RETRASOS DE VUELOS
-- ============================================================

-- Dimension: Fecha del vuelo
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    flight_date DATE NOT NULL UNIQUE,
    day_of_week INT,
    month INT,
    year INT
);

-- Dimension: Aerolíneas
CREATE TABLE dim_airline (
    airline_id SERIAL PRIMARY KEY,
    carrier_code VARCHAR(10) NOT NULL UNIQUE,
    airline_name VARCHAR(255)
);

-- Dimension: Aeropuertos
CREATE TABLE dim_airport (
    airport_id SERIAL PRIMARY KEY,
    airport_code VARCHAR(10) NOT NULL UNIQUE,
    airport_name VARCHAR(255)
);

-- Dimension: Aeronaves
CREATE TABLE dim_aircraft (
    aircraft_id SERIAL PRIMARY KEY,
    tail_num VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla de Hechos: Métricas y detalles de los vuelos
CREATE TABLE fact_flight_delays (
    flight_delay_id SERIAL PRIMARY KEY,
    date_id INT NOT NULL,
    airline_id INT NOT NULL,
    origin_airport_id INT NOT NULL,
    dest_airport_id INT NOT NULL,
    aircraft_id INT, -- Puede ser nulo si no hay TailNum

    flight_num VARCHAR(20),
    dep_time VARCHAR(4),
    arr_time VARCHAR(4),
    crs_arr_time VARCHAR(4),
    actual_elapsed_time INT,
    crs_elapsed_time INT,
    air_time INT,
    arr_delay INT,
    dep_delay INT,
    distance INT,
    taxi_in INT,
    taxi_out INT,
    cancelled BOOLEAN,
    diverted BOOLEAN,
    cancellation_code VARCHAR(5),
    carrier_delay INT,
    weather_delay INT,
    nas_delay INT,
    security_delay INT,
    late_aircraft_delay INT,

    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (airline_id) REFERENCES dim_airline(airline_id),
    FOREIGN KEY (origin_airport_id) REFERENCES dim_airport(airport_id),
    FOREIGN KEY (dest_airport_id) REFERENCES dim_airport(airport_id),
    FOREIGN KEY (aircraft_id) REFERENCES dim_aircraft(aircraft_id)
);

-- Vista Agregada (Capa de Oro/Semántica)
CREATE OR REPLACE VIEW vw_flight_analytics AS
SELECT
    d.flight_date,
    d.day_of_week,
    al.airline_name,
    ao.airport_name AS origin_airport,
    ad.airport_name AS destination_airport,
    f.*
FROM fact_flight_delays f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_airline al ON f.airline_id = al.airline_id
JOIN dim_airport ao ON f.origin_airport_id = ao.airport_id
JOIN dim_airport ad ON f.dest_airport_id = ad.airport_id;
