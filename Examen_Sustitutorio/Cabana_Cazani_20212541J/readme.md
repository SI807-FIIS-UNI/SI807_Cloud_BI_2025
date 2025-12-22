

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

# ⚙️ Guía de Ejecución y Despliegue Técnico

El proceso de implementación sigue un flujo lógico de ingeniería de datos: desde la definición de estructuras en el Data Warehouse hasta la visualización final.

---

### 1. 🗄️ Configuración del Data Warehouse (Apache Hive)
Antes de procesar los datos con Spark, preparamos el entorno en **Hive**. Primero, creamos la base de datos y luego ejecutamos el script DDL para definir las tablas del modelo estrella.

* **Paso A:** Crear la base de datos: 
    ```sql
    CREATE DATABASE db_cepreuni1;
    ```
* **Paso B:** Ejecutar la creación de tablas (Hechos y Dimensiones):
    * [🔗 Script SQL: Carga de Tablas Hive](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/sql/Carga_tablas_Hive.sql)

---

### 2. ⚡ Procesamiento ETL con Apache Spark (Zeppelin)
Utilizamos **PySpark** dentro de Apache Zeppelin para transformar los datos crudos. Los scripts están organizados por bloques y deben ejecutarse en el siguiente orden:

1.  **Bloque 1: Lectura y Limpieza** Lectura del CSV desde la capa *Raw* y aplicación de filtros de calidad.  
    * [📄 Script: Lectura_Limpieza_bloque1.py](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Lectura_Limpieza_bloque1.py)
2.  **Bloque 2: Carga de Dimensiones** Generación de tablas maestras y almacenamiento en la capa `processed`.  
    * [📄 Script: Carga_de_dimensiones_bloque2.py](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Carga_de_dimensiones_bloque2.py)
3.  **Bloque 3: Carga de Hechos** Carga final de la tabla `fact_admision` integrando las llaves foráneas.  
    * [📄 Script: Carga_final_hechos_bloque3.py](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Carga_final_hechos_bloque3.py)

---

### 3. 📊 Generación de KPIs (Capa Curated)
Para asegurar la rapidez del Dashboard, se calculan los KPIs y se almacenan físicamente en formato **Parquet**:

1.  **Esquema de Reportes:** [🔗 Script SQL: tablas_kpis_curated.sql](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/sql/tablas_kpis_curated.sql)
2.  **Proceso de Llenado:** [📄 Script PySpark: Llenado_tablas_kpi.py](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/blob/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/etl/Llenado%20tablas_kpi.py)

---

### 4. 📈 Conectividad y Visualización (Power BI)
La conexión entre el ecosistema Hadoop y la capa de BI se realiza mediante protocolos estándar:

* **Driver ODBC:** Se requiere la instalación del conector de Cloudera para Hive.  
    * [⬇️ Descargar Cloudera ODBC Driver for Apache Hive](https://www.cloudera.com/downloads/connectors/hive/odbc/2-6-4.html)
* **Configuración en Power BI:**
    1.  Ir a **Obtener Datos** > **ODBC**.
    2.  Seleccionar el DSN configurado para el servidor Hive.
    3.  Importar las tablas de la base de datos `db_cepreuni1`.
* **Acceso al Dashboard:** Puedes visualizar los resultados finales en el siguiente enlace:
    * [🔗 Ver Dashboard de Power BI](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025/tree/ExSusti_Cabana_Cazani_20212541J/Examen_Sustitutorio/Cabana_Cazani_20212541J/dashboards)

---

