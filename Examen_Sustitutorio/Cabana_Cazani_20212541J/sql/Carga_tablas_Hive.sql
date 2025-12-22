DROP DATABASE IF EXISTS db_cepreuni1 CASCADE;
CREATE DATABASE db_cepreuni1;
USE db_cepreuni1;

-- 1. TABLA RAW (Lectura del CSV)
CREATE EXTERNAL TABLE raw_postulantes (
    IDHASH STRING, 
    COLEGIO STRING, 
    COLEGIO_DEPA STRING, 
    COLEGIO_PROV STRING, 
    COLEGIO_DIST STRING, 
    COLEGIO_PAIS STRING, 
    COLEGIO_ANIO_EGRESO STRING, 
    ESPECIALIDAD STRING, 
    ANIO_POSTULA INT, 
    CICLO_POSTULA INT, 
    DOMICILIO_DEPA STRING, 
    DOMICILIO_PROV STRING, 
    DOMICILIO_DIST STRING, 
    ANIO_NACIMIENTO INT, 
    NACIMIENTO_PAIS STRING, 
    NACIMIENTO_DEPA STRING, 
    NACIMIENTO_PROV STRING, 
    NACIMIENTO_DIST STRING, 
    SEXO STRING, 
    CALIF_FINAL DOUBLE, 
    INGRESO STRING, 
    MODO_INGRESO STRING, 
    FECHA_CORTE BIGINT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' 
STORED AS TEXTFILE
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/raw'
TBLPROPERTIES ("skip.header.line.count"="1");

-- 2. TABLAS DIMENSIONALES (Parquet)
CREATE EXTERNAL TABLE dim_carrera (id_carrera INT, nombre_carrera STRING) 
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/dim_carrera';

CREATE EXTERNAL TABLE dim_modalidad (id_modalidad INT, descripcion_modalidad STRING) 
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/dim_modalidad';

CREATE EXTERNAL TABLE dim_tiempo (id_tiempo INT, anio INT, ciclo INT, descripcion STRING) 
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/dim_tiempo';

CREATE EXTERNAL TABLE dim_geografia (id_geo STRING, departamento STRING, provincia STRING, distrito STRING, pais STRING) 
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/dim_geografia';

CREATE EXTERNAL TABLE dim_institucion (id_colegio INT, nombre_colegio STRING, id_geo_colegio STRING) 
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/dim_institucion';

CREATE EXTERNAL TABLE dim_candidato (id_candidato STRING, sexo STRING, anio_nacimiento INT, pais_nacimiento STRING) 
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/dim_candidato';

-- 3. TABLA DE HECHOS (Parquet + Particionada)
CREATE EXTERNAL TABLE fact_admision (
    id_tiempo INT, 
    id_candidato STRING, 
    id_carrera INT, 
    id_colegio INT, 
    id_modalidad INT, 
    id_geo_residencia STRING, 
    edad_postulacion INT, 
    anios_desde_egreso INT, 
    puntaje_final DOUBLE, 
    ingreso_flag INT, 
    cantidad INT
)
PARTITIONED BY (anio INT)
STORED AS PARQUET 
LOCATION '/user/alumno/Examen_Sustitutorio/Cabana_Cazani_20212541J/data/processed/fact_admision';