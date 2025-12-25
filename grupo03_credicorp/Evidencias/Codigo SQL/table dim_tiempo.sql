CREATE TABLE dim_tiempo (
    tiempo_key INT IDENTITY(1,1) PRIMARY KEY,
    fecha DATE,
    anio INT,
    mes INT,
    nombre_mes NVARCHAR(20),
    dia INT,
    hora INT,
    minuto INT,
    dia_semana INT,           -- 1=Domingo, 2=Lunes, etc.
    nombre_dia NVARCHAR(20),
    es_fin_de_semana BIT      -- 1 si es Sáb/Dom, 0 si no
);
GO