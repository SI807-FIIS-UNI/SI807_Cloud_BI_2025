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


# PC 4 – Seguridad, IAM, Redes y Gobernanza en Google Cloud Platform  

Este documento presenta la configuración de seguridad, IAM, redes, firewall, políticas y auditoría implementadas en el proyecto.  
Se incluyen capturas de pantalla como evidencia, siguiendo la rúbrica del curso.

---

## 2. Seguridad, IAM, Redes y Gobernanza

---

### 2.1 IAM Granular (Roles personalizados + Políticas JSON)

Se definió un **rol personalizado** para restringir operaciones específicas sobre recursos del proyecto.  
El rol fue creado mediante un archivo **JSON** y aplicado a través de CLI (gsutil), cumpliendo los requisitos de la rúbrica relacionados a políticas personalizadas.

✔ Control de acceso granular  
✔ Rol creado mediante JSON  
✔ Aplicación vía CLI  
✔ Principio de mínimo privilegio aplicado  

**Evidencia:**  
![01_rol_json.png](/grupo10_sutran/evidencias/PC4/01_rol_json.png)

---

### 2.2 Red VPC Personalizada (Subred pública y privada)

Se diseñó e implementó una **VPC dedicada** al proyecto llamada `vpc-sutran-prod`, siguiendo buenas prácticas de arquitectura:

- **Subred pública**: permite salida controlada a internet y acceso estrictamente administrado.  
- **Subred privada**: aislada, utilizada para procesamiento interno (Dataproc, ETL, etc).  
- Rango CIDR asignado de acuerdo al diseño del proyecto.

✔ Segmentación correcta  
✔ Separación de cargas públicas y privadas  
✔ Buenas prácticas de arquitectura de red  

**Evidencias:**  
![02_subred01.png](/grupo10_sutran/evidencias/PC4/02_subred01.png)  
![03_subred02.png](/grupo10_sutran/evidencias/PC4/03_subred02.png)

---

### 2.3 Reglas de Firewall configuradas según políticas del proyecto

Se configuraron reglas de firewall alineadas al principio Zero Trust:

#### **Regla 1 – fw-ssh-public**
- Dirección: Entrada  
- Acción: Permitir  
- Origen: IP pública del desarrollador  
- Protocolo: TCP 22  
- Objetivo: permitir administración segura del cluster Dataproc

#### **Regla 2 – fw-internal**
- Dirección: Entrada  
- Acción: Permitir  
- Origen: 10.0.0.0/16 (rango interno de la VPC)  
- Protocolos: TCP/UDP internos  
- Objetivo: habilitar comunicación entre componentes internos

✔ Permisos mínimos  
✔ Acceso público limitado  
✔ Tráfico interno habilitado correctamente  

**Evidencias:**  
![04_reglafirewall01.png](/grupo10_sutran/evidencias/PC4/04_reglafirewall01.png)  
![05_reglafirewall02.png](/grupo10_sutran/evidencias/PC4/05_reglafirewall02.png)

---

### 2.4 Auditoría y Logging (Cloud Audit Logs)

Se activó el sistema de Auditoría de Google Cloud que registra:

- Cambios en IAM  
- Actividades administrativas  
- Accesos a datos  
- Eventos del sistema  
- Acciones denegadas por políticas

Esto proporciona trazabilidad completa para gobernanza y seguridad.

✔ Cloud Logging habilitado  
✔ Auditoría activa  
✔ Evidencias de logs generados  

**Evidencias:**  
![06_auditoria_logging.png](/grupo10_sutran/evidencias/PC4/06_auditoria_logging.png)  
![07_auditoria_logging.png](/grupo10_sutran/evidencias/PC4/07_auditoria_logging.png)

---

## 2.5 Gobernanza aplicada

Las decisiones de arquitectura siguen buenas prácticas de seguridad empresarial:

- Política de mínimo privilegio  
- Redes aisladas y segmentadas  
- Reglas de firewall estrictas  
- Auditoría activa  
- Roles personalizados y controlados por JSON  
- Configuración vía CLI para reproducibilidad  
- Separación entre componentes públicos/privados  

---
## 3. Scripts SQL del Proyecto

Todos los scripts SQL utilizados en el proceso de validación, construcción del modelo estrella,
cálculo de métricas, KPIs y funciones avanzadas se encuentran en:

**`/grupo10_sutran/scripts/`**

Accesibles desde los siguientes enlaces:

- [01_validacion.sql](/grupo10_sutran/scripts/01_validacion.sql)
- [02_join_modelo_estrella.sql](/grupo10_sutran/scripts/02_join_modelo_estrella.sql)
- [03_kpis.sql](/grupo10_sutran/scripts/03_kpis.sql)
- [04_funciones_ventana.sql](/grupo10_sutran/scripts/04_funciones_ventana.sql)
- [05_ranking.sql](/grupo10_sutran/scripts/05_ranking.sql)
- [06_ctes.sql](/grupo10_sutran/scripts/06_ctes.sql)

Cada script contiene consultas ejecutadas en BigQuery, organizadas según la rúbrica:

- **Validación de datos:** conteos, duplicados, nulos, tipos.  
- **Modelo estrella:** cruces completos entre hechos y dimensiones.  
- **KPIs:** agregaciones, tasas, métricas críticas.  
- **Funciones avanzadas:** LAG, RANK, OVER, PARTITION BY.  
- **CTEs:** análisis multi-dimensional con WITH.  

Las evidencias de ejecución (resultados y capturas de pantalla) están almacenadas en la carpeta `/evidencias/PC4/`.

