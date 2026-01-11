USE db_cepreuni1;

-- 1. TABLA REPORTE POR CARRERA (KPIs de Ingreso por Especialidad)
-- Ubicación: .../data/curated/reporte_carreras
CREATE EXTERNAL TABLE cur_reporte_carreras (
    anio INT,
    nombre_carrera STRING,
    total_postulantes INT,
    total_ingresantes INT,
    tasa_ingreso_pct DOUBLE
)
STORED AS PARQUET
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/curated/reporte_carreras';

-- 2. TABLA REPORTE POR COLEGIO (Ranking de Colegios)
-- Ubicación: .../data/curated/reporte_colegios
CREATE EXTERNAL TABLE cur_reporte_colegios (
    nombre_colegio STRING,
    departamento STRING,
    total_postulantes INT,
    total_ingresantes INT
)
STORED AS PARQUET
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/curated/reporte_colegios';