

# 🚀 Proyecto de Sistema de Inteligencia de Negocios: Análisis de Admisión CEPRE-UNI 2024

### *Implementación de una arquitectura Data Lakehouse para la Gestión Académica*

---

## 👤 Información del Estudiante
* **Nombre:** Cabana Cazani, Gabriel Alessandro
* **Código:** `20212541J`
* **Curso:** Sistema de Inteligencia de Negocios (Examen Sustitutorio)
* **Institución:** Universidad Nacional de Ingeniería (UNI)

---

## 🛠️ Tecnologías Utilizadas
| Capa | Herramienta | Función |
| :--- | :--- | :--- |
| **Almacenamiento** | Hadoop HDFS | Repositorio de datos distribuidos (Raw/Processed). |
| **Procesamiento** | Apache Spark (PySpark) | Motor de ETL, limpieza y modelado dimensional. |
| **Data Warehouse** | Apache Hive | Gestión de tablas estructuradas en formato Parquet. |
| **IDE / Notebook** | Apache Zeppelin | Desarrollo de scripts y experimentación. |
| **Visualización** | Microsoft Power BI | Dashboard interactivo de KPIs de gestión. |

---

## 📂 Estructura de Carpetas en HDFS
La arquitectura sigue la nomenclatura oficial y una organización por capas (Medallion Architecture):

```text
/user/alumno/Ex_Sustitutorio/
└── Cabana_Cazani_20212541J/               <-- Raíz del Proyecto
    ├── data/                              <-- Repositorio de Datos
    │   ├── raw/                           <-- Capa Bronce (Landing Zone)
    │   │   └── Alumnos_CEPRE.csv          <-- Dataset original (Datos Abiertos)
    │   │
    │   ├── processed/                     <-- Capa Plata (Modelo Estrella)
    │   │   ├── fact_admision/             <-- Tabla de Hechos (Parquet)
    │   │   ├── dim_carrera/               <-- Dimensiones Maestras
    │   │   ├── dim_modalidad/
    │   │   ├── dim_tiempo/
    │   │   ├── dim_geografia/
    │   │   ├── dim_candidato/
    │   │   └── dim_institucion/
    │   │
    │   └── curated/                       <-- Capa Oro (Reportes Agregados)
    │       ├── cur_reporte_carreras/      <-- KPIs por Especialidad
    │       └── cur_reporte_colegios/      <-- Ranking de Procedencia
    │
    ├── scripts/                           <-- Artefactos de Ingeniería
    │   ├── etl_admision.py                <-- Proceso Spark (Python)
    │   ├── schema_database.sql            <-- Estructura de Tablas (Hive SQL)
    │   └── export_to_csv.py               <-- Script de exportación para GitHub
    │
    └── notebooks/                         <-- Entorno de Desarrollo
        └── proyecto_admision_uni.json     <-- Exportación de Zeppelin Notebook
```

  Luego vamos al servicio de Hive para la creación de las tablas, ejecutamos lo siguiente, antes debemos crear nuestra base de datos con créate database db_cepreuni1, en el texto, está el código, expandir para ver el código completo, de igual manera se encuentra el código en el repositorio.
Link: https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/sql/Carga_tablas_Hive.sql
Usamos ese archivo para la carga SQL de las tablas de dimensiones y la tabla de hechos

Luego de crear las tablas nos vamos a usar Spark mediante Zeppelin
Creamos un nuevo notebook y ejecutamos para la limpieza
https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Lectura_Limpieza_bloque1.py
https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Carga_de_dimensiones_bloque2.py
https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Carga_final_hechos_bloque3.py
Ejecutamos en ese orden, primero la limpieza, luego la carga de dimensiones y finalmente la carga de hechos, estan ordenados por bloques

Luego de eso procedemos a crear reportes_kpis para almacenar en curated
https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/sql/tablas_kpis_curated.sql
Se corre eso para crear las tablas de los kpis
Y luego se corre en Zepellin para llenar las tablas, todo será en formato parquet
https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Llenado%20tablas_kpi.py
Se ejecuta ese código

Revisando nos daremos cuenta de que se realizó la carga en las carpetas processed y curated en formato parquet, en todas las tablas, luego procedemos a conectar nuestro servicio con Power BI para elaborar los dashboards, para eso debemos descargar un driver ODBC para Apache Hive.

https://www.cloudera.com/downloads/connectors/hive/odbc/2-6-4.html

Configuramos la conexión de Apache para poder conectarnos con el Power BI.
Vamos a obtener datos, escribimos ODBS, seleccionamos Hive, que acabamos de crear y nos mostrará las tablas de nuestra base de datos creada.
Luego procedemos a crear los Dashboards, para visualizar los dashboards se puede ir al siguiente Link

