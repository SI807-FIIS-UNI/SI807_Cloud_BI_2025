## 3.1. Ingestión y Estructuración – Capa BRONCE

### 1. Selección y Justificación de la Nube
Para esta solución de Business Intelligence se ha seleccionado **Microsoft Azure** por las siguientes razones técnicas:
* **Almacenamiento Jerárquico (ADLS Gen2):** A diferencia de un Blob Storage tradicional, Azure Data Lake Storage Gen2 permite una estructura de directorios jerárquica real (`raw/`, `processed/`, `curated/`), lo cual es indispensable para organizar las capas de datos en una arquitectura Medallion.
* **Integración Nativa:** El ecosistema Azure permite una integración fluida entre el almacenamiento (Data Lake), el procesamiento (Databricks) y el warehosuing (Synapse Analytics) bajo un mismo grupo de recursos y gestión de identidad (Entra ID).
* **Escalabilidad y Costo:** El uso de Databricks permite separar el cómputo del almacenamiento, optimizando costos mediante clústeres que se apagan automáticamente tras la ingesta.

### 2. Implementación de Estructura de Datos
Se ha implementado una arquitectura de **"Medallion Architecture"** (Bronce, Plata, Oro) dentro del contenedor `bronce` en el Data Lake `datalakemichi1`.

* **Estructura de Carpetas:**
    * `bronce/raw`: Almacenamiento de archivos CSV originales tal cual llegaron de la fuente (Inmutable).
    * `bronce/processed`: Datos limpios y estandarizados (Capa Plata).
    * `bronce/curated`: Datos agregados listos para consumo (Capa Oro).

### 3. Proceso de Ingesta (CLI)
La carga de los archivos CSV (`city_day.csv`, `station_hour.csv`, etc.) se realizó utilizando **Azure CLI** mediante Azure Cloud Shell. Esto garantiza un proceso de carga rápido, seguro y scriptable, evitando cargas manuales propensas a errores.

* **Script utilizado:** `src/01_bronze/ingesta_cli.sh`
* **Comando principal ejecutado:**
    ```bash
    az storage fs file upload -s "archivo.csv" -p "raw/archivo.csv" -f "bronce" --account-name "datalakemichi1"
    ```

### 4. Análisis Exploratorio de Datos (EDA)
Se ejecutó un proceso de EDA mínimo utilizando **PySpark** en Azure Databricks para validar la integridad de los datos antes de su transformación.

* **Script utilizado:** `src/01_bronze/eda_script.py`
* **Validaciones realizadas:**
    * Inferencia automática de esquemas (`inferSchema=True`).
    * Conteo de registros por archivo.
    * Conversión inicial de formato CSV a **Delta Lake** (Tablas Bronze) para habilitar el versionado y transacciones ACID desde el inicio.

---
### Instrucciones de Reproducibilidad (Capa Bronce)

1.  **Ingesta:**
    * Abrir Azure Cloud Shell (Bash).
    * Subir el script `src/01_bronze/ingesta_cli.sh`.
    * Ejecutar: `bash ingesta_cli.sh`.

2.  **EDA y Tablas Delta:**
    * Importar el notebook `src/01_bronze/eda_script.py` en Azure Databricks.
    * Ejecutar el cluster y correr todas las celdas.
    * Verificar que las tablas `bronze_city_day`, `bronze_stations`, etc., aparecen en el Catálogo de Databricks.