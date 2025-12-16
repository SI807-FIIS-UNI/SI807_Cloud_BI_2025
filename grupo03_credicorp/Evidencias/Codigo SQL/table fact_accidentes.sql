CREATE TABLE fact_accidentes (
    fact_id INT IDENTITY(1,1) PRIMARY KEY,
    source_id NVARCHAR(50),          -- El ID original del CSV (ej. A-1)
    
    -- Claves Foráneas (Foreign Keys)
    fk_ubicacion INT,
    fk_clima INT,
    fk_tiempo_inicio INT,            -- Relación con dim_tiempo (Inicio)
    fk_tiempo_fin INT,               -- Relación con dim_tiempo (Fin)
    
    -- Métricas / Hechos
    severity INT,                    -- 1 a 4
    distance_mi DECIMAL(10,4),       -- Distancia afectada
    duration_minutes DECIMAL(10,2),  -- Calculado (End_Time - Start_Time)
    start_lat DECIMAL(9,6),          -- Latitud exacta inicio
    start_lng DECIMAL(9,6),          -- Longitud exacta inicio
    end_lat DECIMAL(9,6),            -- Latitud exacta fin
    end_lng DECIMAL(9,6),            -- Longitud exacta fin
    description NVARCHAR(MAX),
    
    -- Indicadores de Infraestructura (Booleans/Bits)
    amenity BIT,
    bump BIT,
    crossing BIT,
    give_way BIT,
    junction BIT,
    no_exit BIT,
    railway BIT,
    roundabout BIT,
    station BIT,
    stop BIT,
    traffic_calming BIT,
    traffic_signal BIT,
    turning_loop BIT,
    
    -- Fases del día (Astronómicas)
    sunrise_sunset NVARCHAR(20),
    civil_twilight NVARCHAR(20),
    nautical_twilight NVARCHAR(20),
    astronomical_twilight NVARCHAR(20),

    -- Definición de restricciones (Foreign Keys)
    CONSTRAINT FK_Fact_Ubicacion FOREIGN KEY (fk_ubicacion) REFERENCES dim_ubicacion(ubicacion_key),
    CONSTRAINT FK_Fact_Clima FOREIGN KEY (fk_clima) REFERENCES dim_clima(clima_key),
    CONSTRAINT FK_Fact_TiempoInicio FOREIGN KEY (fk_tiempo_inicio) REFERENCES dim_tiempo(tiempo_key),
    CONSTRAINT FK_Fact_TiempoFin FOREIGN KEY (fk_tiempo_fin) REFERENCES dim_tiempo(tiempo_key)
);
GO