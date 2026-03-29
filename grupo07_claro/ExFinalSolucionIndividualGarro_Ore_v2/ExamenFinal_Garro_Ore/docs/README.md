# Solución de Inteligencia de Negocios - Examen Final SI807
**Estudiante:** Willian Garro
**Ciclo:** 2025-II
**Curso:** Sistema de Inteligencia de Negocios

## 1. Justificación de la Nube (GCP)
Se seleccionó **Google Cloud Platform (GCP)** por las siguientes razones técnicas:
* **Integración Nativa:** Flujo fluido entre Cloud Storage (Data Lake) y BigQuery (Data Warehouse) sin necesidad de conectores complejos.
* **Eficiencia en Costos y Tiempos:** El uso de BigQuery permite consultas SQL sobre grandes volúmenes de datos en segundos (Serverless), ideal para el examen en vivo.
* **Gestión de Identidad:** Uso de IAM y Service Accounts para seguridad en el acceso a datos.

## 2. Arquitectura de Datos Implementada
Se desplegó una arquitectura **Lakehouse** siguiendo el patrón Medallion (Bronce, Plata, Oro):

### 2.1 Capa Bronce (Ingesta & Raw)
* **Objetivo:** Almacenamiento fiel del dato original.
* **Fuente:** Dataset CSV "Medical Appointment No Shows" (Kaggle).
* **Destino:** `gs://[BUCKET]/bronce/raw/`.
* **Proceso:** Ingesta vía Google Cloud CLI (`gcloud storage cp`).
* **Calidad:** Se ejecutó un script `eda.py` para perfilamiento de datos (ver `docs/evidencia_eda.txt`).

### 2.2 Capa Plata (Transformación & Modelado)
* **Objetivo:** Limpieza y estructuración.
* **Modelo Dimensional:** Esquema Estrella.
    * **Fact_Citas:** Tabla de hechos transaccional. Se calculó `LeadTimeDays` (días de anticipación).
    * **Dim_Paciente:** Dimensión conformada con atributos demográficos y patologías (Deduplicación por `PatientId`).
* **Tecnología:** Python (Pandas) para normalización y carga a BigQuery (`dataset: silver_layer`).

### 2.3 Capa Oro (Analítica & KPIs)
* **Objetivo:** Agregación para toma de decisiones.
* **KPI Principal:** **Tasa de Ausentismo (No-Show Rate)**.
* **Lógica:** Agrupación por Barrio, Rango de Edad y Género.
* **Resultado:** Tabla `gold_layer.kpi_resumen` en BigQuery lista para conexión con Power BI.

## 3. Instrucciones de Reproducibilidad
Para replicar esta solución en un entorno nuevo:

1.  **Configuración:**
    ```bash
    export PROJECT_ID="[TU_PROYECTO]"
    export BUCKET_NAME="[TU_BUCKET]"
    python3 -m venv venv && source venv/bin/activate
    pip install pandas google-cloud-storage google-cloud-bigquery db-dtypes
    ```

2.  **Ejecución del Pipeline:**
    Ejecutar los scripts en orden secuencial:
    ```bash
    python eda.py $BUCKET_NAME          # Genera perfilado
    python etl_silver.py $BUCKET_NAME $PROJECT_ID  # Crea modelo estrella
    python etl_gold.py $BUCKET_NAME $PROJECT_ID    # Genera KPIs
    ```

3.  **Visualización:**
    * Conectar Power BI a Google BigQuery.
    * Seleccionar Proyecto -> `gold_layer` -> `kpi_resumen`.

## 4. Evidencias
Los logs de ejecución se encuentran en la carpeta `/docs` de este repositorio:
* `evidencia_eda.txt`: Reporte de calidad de datos.
* `log_etl_silver.txt`: Conteo de registros procesados.
* `log_etl_gold.txt`: Muestra de los KPIs calculados.