# 🟦 PC3 – Migración del Proceso ETL a Google Cloud (Caso: SUTRAN)

Este proyecto forma parte de la PC3 del curso de Inteligencia de Negocios y tiene como objetivo migrar el proceso ETL a la nube utilizando servicios de Google Cloud Platform (GCP).


---

## 🌐 Infraestructura GCP utilizada

| Servicio       | Uso principal                                       |
|----------------|-----------------------------------------------------|
| **Cloud Storage**  | Almacenamiento de archivos CSV (raw, clean)        |
| **Dataproc + JupyterLab** | Limpieza de datos y transformación con PySpark  |
| **BigQuery**     | Carga de datos final en modelo estrella             |

---

## 🧪 Archivos procesados

- `BBDD_ONSV-PERSONAS_2021-2023.csv`
- `BBDD_ONSV-VEHICULOS_2021-2023.csv`
- `BBDD_ONSV-SINIESTROS_2021-2023.csv`

---

## 🧼 Proceso ETL resumido

1. **Carga de archivos CSV al bucket** en la carpeta `/raw/`
2. **Lectura y limpieza de datos con PySpark**, incluyendo:
   - Corrección de codificación (ISO-8859-1)
   - Eliminación de caracteres invisibles (`\ufeff`)
   - Conversión de tipos (`int`, `string`, `timestamp`)
3. **Creación del modelo estrella**:
   - `dim_persona`
   - `dim_vehiculo`
   - `dim_tiempo`
   - `dim_tipo_via`
   - `f_siniestro`
4. **Carga final a BigQuery** usando el conector Spark-BigQuery y bucket temporal `sutran-bucket-2025`

---

## 🧊 Modelo Estrella

```text
                +------------------+
                |  dim_persona     |
                +------------------+
                          |
                          |
+------------------+      |      +------------------+ 
|  dim_vehiculo    |------|------|  dim_tipo_via    |
+------------------+      |      +------------------+
                          |
                   +-------------+
                   | f_siniestro |
                   +-------------+
                          |
                   +--------------+
                   |  dim_tiempo  |
                   +--------------+

```

# 🧪 PC3 – Migración y Automatización del Proceso ETL en Google Cloud Platform (GCP)

Este proyecto detalla paso por paso cómo se migró un proceso ETL al entorno cloud (GCP) usando Dataproc (con PySpark), BigQuery y Cloud Storage, basado en datos abiertos de siniestros de tránsito (SUTRAN / ONSV).

---

## 📌 Objetivo

Implementar, automatizar y documentar un flujo ETL completo en Google Cloud, integrando Spark en Dataproc con BigQuery como destino final y almacenamiento intermedio en Cloud Storage.

---

## 🧰 Herramientas utilizadas

| Servicio            | Uso en el proyecto                                 |
|---------------------|----------------------------------------------------|
| **GCP Cloud Console**  | Creación del proyecto, buckets, permisos          |
| **Cloud Storage**      | Almacenamiento de archivos raw/clean              |
| **Dataproc + JupyterLab** | Limpieza, transformación y carga con PySpark     |
| **BigQuery**           | Carga final a modelo estrella                     |
| **Python / PySpark**   | Lógica ETL                                        |

---

## 📂 Requisitos previos

- Cuenta institucional con créditos disponibles en GCP
- Roles asignados: **Propietario** del proyecto y acceso a BigQuery, Dataproc, Storage
- SDK de GCP autenticado (si se usa localmente)
- Archivo `etl_pipeline_sutran.ipynb` (notebook principal) ubicado en la carpeta `notebooks/`

---

## 🧩 Pasos reproducibles del proceso

---

### 🔹 1. Crear el proyecto en GCP

- Proyecto: `shaped-icon-478404-p0`
- ID: `370944850430`

![01_info_project.png](/grupo10_sutran/evidencias/PC3/01_info_project.png)

---

### 🔹 2. Configurar y autenticar GCP

- Crear grupo de datos y bucket
- Bucket creado: `sutran-bucket-2025`

![02_configure_bucket.png](/grupo10_sutran/evidencias/PC3/02_configure_bucket.png)
![03_bucket_creado.png](/grupo10_sutran/evidencias/PC3/03_bucket_creado.png)

---

### 🔹 3. Subir archivos CSV al bucket

Subcarpeta `/raw/` con los archivos:

- `BBDD_ONSV-PERSONAS_2021-2023.csv`
- `BBDD_ONSV-VEHICULOS_2021-2023.csv`
- `BBDD_ONSV-SINIESTROS_2021-2023.csv`

![04_csv_upload.png](/grupo10_sutran/evidencias/PC3/04_csv_upload.png)
---

### 🔹 4. Autenticarse desde Dataproc / JupyterLab

- Clúster creado: `sutran-cluster`
- Autenticación vía cuenta institucional

![05_googlecloud_authentication.png](/grupo10_sutran/evidencias/PC3/05_googlecloud_authentication.png)
![06_cluster_dataproc_creation.png](/grupo10_sutran/evidencias/PC3/06_cluster_dataproc_creation.png)
![07_jupyter_lab_cluster.png](/grupo10_sutran/evidencias/PC3/07_jupyter_lab_cluster.png)

---

### 🔹 5. Lectura y limpieza de datos con PySpark

Usamos el notebook `etl_pipeline_sutran.ipynb` para realizar:

- Lectura de archivos desde `/raw/`
- Limpieza de caracteres BOM (`\ufeff`)
- Conversión de codificación a UTF-8
- Cast de columnas numéricas
- Escritura a `/clean/` y luego a Parquet

📎 Ver notebook: [notebooks/etl_pipeline_sutran.ipynb](/grupo10_sutran/notebooks/notebooks_jupyter_etl_pipeline_sutran.ipynb)

---

### 🔹 6. Crear datasets en BigQuery

- Dataset principal: `bi_sutran`
- 5 datasets fueron creados como evidencia

📸 ![08_creation_data_group.png](/grupo10_sutran/evidencias/PC3/08_creation_data_group.png)
📸 ![09_dataset_creation.png](/grupo10_sutran/evidencias/PC3/09_dataset_creation.png)

---

### 🔹 7. Modelo Estrella en BigQuery

Desde el notebook se genera y carga:

- `dim_persona`
- `dim_vehiculo`
- `dim_tiempo`
- `dim_tipo_via`
- `f_siniestro`

**Carga realizada con:**

```python
df.write \
  .format("bigquery") \
  .option("temporaryGcsBucket", "sutran-bucket-2025") \
  .option("table", "shaped-icon-478404-p0.bi_sutran.nombre_tabla") \
  .mode("overwrite") \
  .save()
```

