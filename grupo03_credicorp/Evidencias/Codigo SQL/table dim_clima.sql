CREATE TABLE dim_clima (
    clima_key INT IDENTITY(1,1) PRIMARY KEY,
    Temperature_F DECIMAL(5,2),      -- Temperatura
    Wind_Chill_F DECIMAL(5,2),       -- Sensación térmica
    Humidity_Percent DECIMAL(5,2),   -- Humedad
    Pressure_In DECIMAL(5,2),        -- Presión
    Visibility_Mi DECIMAL(5,2),      -- Visibilidad
    Wind_Direction NVARCHAR(20),     -- Dirección del viento
    Wind_Speed_Mph DECIMAL(5,2),     -- Velocidad del viento
    Precipitation_In DECIMAL(5,2),   -- Precipitación
    Weather_Condition NVARCHAR(100)  -- Condición general (ej. Rain, Clear)
);
GO