## 3.2. Transformación y Modelo Dimensional – Capa PLATA

### 1. Diseño del Modelo Dimensional (Esquema Estrella)
Para optimizar las consultas analíticas en la capa Plata, se diseñó un **Modelo Estrella** que normaliza la información en tablas de hechos y dimensiones. Esto facilita el cruce de datos entre las mediciones de calidad del aire y los atributos geográficos y temporales.

* **Esquema Lógico:**
    * **`plata_fact_calidad_aire` (Tabla de Hechos):** Contiene las métricas numéricas diarias (PM2.5, PM10, AQI, NO2, etc.) y las claves foráneas (`Fecha`, `Ciudad`).
    * **`plata_dim_ciudad` (Dimensión):** Catálogo único de ciudades enriquecido con su "Estado" (provincia/región), derivado de la tabla maestra de estaciones.
    * **`plata_dim_tiempo` (Dimensión):** Calendario generado a partir de las fechas existentes, desglosando Año, Mes, Día, Trimestre y Día de la Semana para análisis temporal.

### 2. Estrategia de Limpieza y Transformación (ETL)
Se utilizó **PySpark** en Azure Databricks para procesar los datos de la capa `bronce` y generar la capa `plata`. Las principales reglas de negocio aplicadas fueron:

* **Estandarización de Nombres:**
    * Se renombraron columnas conflictivas como `PM2.5` (cuyo punto `.` causaba errores de sintaxis en Spark SQL) a `PM2_5`.
    * Se tradujeron campos clave como `Date` -> `Fecha` y `City` -> `Ciudad` para mantener consistencia en español.

* **Manejo de Nulos (Data Quality):**
    * **Métricas:** Los valores nulos en columnas críticas como `AQI`, `PM2.5` y `PM10` fueron imputados con `0`. Esto se decidió para evitar la eliminación de registros completos que pudieran tener otros contaminantes válidos, permitiendo un análisis parcial sin romper las agregaciones.
    * **Integridad:** Se filtraron registros con fechas o ciudades nulas para asegurar la integridad referencial del modelo estrella.

* **Tipado de Datos:** Conversión explícita de todas las métricas de contaminantes a tipo `Double` y fechas a tipo `Date`.

### 3. Scripts y Reproducibilidad
El código fuente de esta capa se encuentra en la carpeta `src/02_silver/`.

* **Script de Transformación:** `src/02_silver/transformaciones.py`
    * *Función:* Lee las tablas bronze, aplica las reglas de limpieza y escribe las tablas Delta `plata_...`.
* **Script de Validación:** `src/02_silver/validacion_calidad.py`
    * *Función:* Ejecuta conteos, verifica nulos en claves primarias y realiza un `JOIN` de prueba entre la Fact y las Dims para garantizar la integridad del modelo.

#### Instrucciones de Ejecución:
1. Asegurarse de que la capa Bronce esté cargada.
2. Ejecutar el notebook de transformación en Databricks.
3. Verificar la creación de las tablas en el Hive Metastore:
    * `plata_dim_tiempo`
    * `plata_dim_ciudad`
    * `plata_fact_calidad_aire`