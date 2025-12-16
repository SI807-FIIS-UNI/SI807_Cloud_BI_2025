CREATE TABLE dim_ubicacion (
    ubicacion_key INT IDENTITY(1,1) PRIMARY KEY,
    Street NVARCHAR(255),
    City NVARCHAR(100),
    County NVARCHAR(100),
    State NVARCHAR(50),
    Zipcode NVARCHAR(20),
    Country NVARCHAR(50),
    Timezone NVARCHAR(50),
    Airport_Code NVARCHAR(20)
);
GO