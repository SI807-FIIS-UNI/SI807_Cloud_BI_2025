#  🏦 Proyecto BI Scotiabank 
## 🏗️ PC4 – Arquitectura Analítica en la Nube con Google Cloud Platform
El objetivo de este trabajo es implementar un flujo funcional de sistema de inteligencia de Negocio en la nube para la empresa Scotiabank que permitira:
- ✔ Obtener datos desde la web
- ✔ Procesarlos y almacenarlos en un Data Lake multicapa
- ✔ Transformarlos con PySpark
- ✔ Consolidar información en BigQuery
- ✔ Generar un esquema estrella en BigQuery
- ✔ Visualizar dashboards en Power BI

Información de implementación estructurada de recursos GCP en 👉 [IMPLEMENTACION.md](01_Ambiente_GCP/IMPLEMENTACION.md)

### Estructura de Carpetas

```json
/PC4
 ├── README.md                 # Documentación principal (este archivo)
 ├── 01_Ambiente_GCP/          # Creación del proyecto, IAM, VPC, buckets, claves
 ├── 02_WebScraping/           # Código Python para extracción de datos
 ├── 03_ETL/                   # Limpieza, consolidación, CSV, carga autom.
 ├── 04_DataLake/              # Raw / Trusted / Refined en GCS
 ├── 05_Procesamiento_Spark/   # Dataproc, PySpark, notebooks
 ├── 06_BigQuery/              # Tablas, consultas SQL
 ├── 07_PowerBI/               # Conexión con BigQuery + dashboards
 ├── Evidencias_Generales/     # Capturas, videos, PR, merges
 └── docs/                     
```
## 🧱 1. Arquitectura Avanzada en la Nube

Arquitectura desplegada sobre Google Cloud Platform (GCP) en el proyecto:

```
ID del Proyecto: grupo6-scotiabank
```

La solución integra servicios básicos, avanzados y complementarios para soportar un flujo completo de analítica de datos, desde la ingesta hasta el consumo en Power BI.

### ✔️ Servicios utilizados y evidencias de costos

Durante la implementación se hizo uso de los siguientes servicios en la nube:

| Servicio                 | Rol dentro de la Arquitectura                                       |
|--------------------------|----------------------------------------------------------------------|
| **Networking**           | Comunicación segura entre servicios, gestión de VPC, subredes y rutas privadas |
| **BigQuery**             | Motor analítico central para consultas SQL, creación de datasets y capas trusted/refined |
| **BigQuery Reservation** | Reserva de slots para consultas de alto rendimiento y procesamiento optimizado |
| **Dataproc**             | Procesamiento distribuido mediante PySpark para ETL y preparación de datos |
| **Compute Engine**       | Nodo de soporte y ejecución de tareas auxiliares o procesos puntuales |
| **Cloud Storage**        | Data Lake multicapa (raw → trusted → refined) para almacenamiento estructurado y no estructurado |
| **Cloud Run**            | Ejecución de servicios serverless para microcomponentes y automatización |
| **Cloud Run Functions**  | Funciones event-driven para orquestación y tareas desencadenadas por eventos |
| **Cloud Build**          | Construcción, empaquetado y despliegue automático de artefactos y pipelines |
                            

![1-facturacion_Servicios](Evidencias_generales\1-Facturacion_Actual.png)


### ✔️ Storage estructurado (raw / trusted / refined)

La estrutura actual de Bucket en Cloud Storage tiene la siguiente forma

![alt text](Evidencias_Generales/4-Bukckets.png)

El Bucket Principal como Data Lake es el de **"grupo6_scotiabank_bucket"**.

Por otro lado se tiene Buckets adicionales generados automáticamente por los servicios y recursos utilizados:

- **dataproc-temp-southamerica-west1-..Dataproc** : Área temporal donde Dataproc guarda metadatos, logs, intermediarios y staging

- **gcf-v2-sources-75587073872-southamerica-west1	Cloud Run / Cloud Functions** : Almacena el código fuente desplegado por funciones y servicios serverless, permitiendo versionamiento y redeploy

El Data Lake se organizó bajo la estructura recomendada para arquitecturas analíticas:
```
gs://grupo6_scotiabank_bucket/   
│   ├── Capa Bronce/ # Datos originales tal como se ingresa (Capa Bronce, data/raw/SBS)
├───├── data/
│   │   ├── historico/  #Archivos Consolidados
│   │   └── raw/   # Datos Extraidos del Web Scraping
│   │       └── SBS/
│   │           ├── CREDITOS_SEGUN_SITUACION/
│   │           ├── DEPOSITOS/
│   │           ├── EEFF/
│   │           ├── PATRIMONIO_EFECTIVO/
│   │           ├── PATRIMONIO_REQUERIDO_RCG/
│   │           └── RATIO_LIQUIDEZ/
│   ├── logs/
│   └── resources/
├───└── Capa Plata/ # Datos curados, limpios y tipificados (Capa Plata, trusted)
└───└── Capa Oro/   # Datos listos para explotación analítica (Power BI / BigQuery, refined)
    
```

![Buckets_Data_Lake](Evidencias_Generales/5-Buckets_Data_Lake.png)

👉 Este reparto permite separar la capa principal de datos del código operacional, garantizando gobernanza y control de versiones.


### ✔️ Visor BI en la nube

El consumo analítico se realiza mediante:

Power BI conectado a BigQuery


Se empleó:

- 1 Cuenta de servicio (Service Account)

- 2 Conexión segura por credenciales JSON

- 3 Modelo importado/DirectQuery según necesidad

Esto garantiza acceso controlado a datasets refinados sin exponer usuarios finales a los servicios de GCP.

📘 Para más detalle, revisa [07_PowerBI](07_PowerBI/README.md)

### ✔️ Seguridad, IAM, roles y gobierno

La seguridad fue implementada mediante IAM granular por miembro del equipo y por servicio, asignando permisos mínimos necesarios para cada flujo.

📘 Para más detalle, revisa [01_Ambiente_GCP](01_Ambiente_GCP/README.md)

## 🔐 2. Seguridad, IAM, Redes y Gobernanza 

### ✔️ IAM y roles 

Tal como se desarrollo en [01_Ambiente_GCP](01_Ambiente_GCP/README.md), se establecieron roles y claves de acceso para la analítica y contrucion de reportes.

Los roles para cada usuario son ingresados a travez del CLI de GCP, estos estran granularizados en:


- Roles generales : Son los roles otorgados en general al proyecto
- Roles para Scraping y carga de datos : Permite el uso de servicios como Cloud Run, Cloud Funtions y la creación de buckets para guardar los datos
- Roles para Procesamiento y ETL: Permite la creacion de recursos dataprocserverles para procesar los recursos a travez de las capas bronce, plata y oro creando la tabla de hechos final.

![Adicion_De_Roles](Evidencias_generales/2-Roles_IAM.png)

### ✔️ Registro de Logs

Para la observabilidad, el servicio de Loggins de GCP esta activado por defecto. Aqui se puede visualizar las fallas generadas en la ejecución de flujos desarrollardos por Cloud Run, Cloud Functions, BigQuery, Jobs, entre otros.

![Logging](Evidencias_generales/3-Observabilidad.png)

## 📂 3. Carga en Buckets / Data Lake — Evidencias

La carga hacia el Data Lake se realiza a través de tres componentes principales del pipeline. En este documento se separan y referencian las evidencias asociadas a cada etapa para facilitar la trazabilidad y la auditoría.

**Rutas de interés (en el repositorio)**  


- [02_WebScraping](02_WebScraping/README.md) — Descarga automática desde SBS  
- [03_ETL](03_ETL/README.md) — Ingesta, limpieza y carga Bronce (Cloud Function)  
- [04_DataLake](04_DataLake/README.md) — Organización del Data Lake (raw / trusted / refined)  

---

### 🔗 Módulos y roles en la carga

| Módulo | Rol en la Carga | Ruta de evidencia |
|--------|-----------------|-------------------|
| **02_WebScraping** | Descarga automatizada de archivos desde la SBS y BCRP → sube a `gs://.../data/raw/` | [02_WebScraping](02_WebScraping/README.md) |
| **03_ETL (bronce-dispatcher)** | Ingesta, limpieza inicial y tabulado → inserción a BigQuery (dataset `bronce`) | [03_ETL](03_ETL/README.md) |
| **04_DataLake** | Organización física y políticas del bucket GCS (raw / trusted / refined) | [04_DataLake](04_DataLake/README.md) |



### 📁 Detalle de evidencias por etapa

### 🔸 1) Carga inicial — `02_WebScraping`
- **Qué valida:** Descargas automáticas, scheduling, logs de descarga, CSV de control.
- **Evidencias incluidas:**
  - `02_WebScraping/logs/descargas_sbs.csv`
  - Capturas: `02_WebScraping/evidencias/*.png`
  - Descripción del scheduler y comandos de despliegue.
- **Ruta:** [02_WebScraping](02_WebScraping/README.md)

---

### 🔸 2) Ingesta y ETL Bronce — `03_ETL`
- **Qué valida:** Cloud Function `bronce-dispatcher`, pipelines por reporte (SBS/BCRP), extracción, limpieza y carga a `bronce.*` en BigQuery.
- **Evidencias incluidas:**
  - Código fuente: `resources/bronce-dispatcher/`
  - Outputs de ejecución y logs: `03_ETL/evidencias/`
  - Capturas de las tablas `bronce.*` en BigQuery.
- **Ruta:** [03_ETL](03_ETL/README.md)

> **Nota:** El dispatcher identifica el pipeline a ejecutar según el prefijo del archivo y lanza la transformación adecuada (ej. `ratio_liquidez`, `creditos`, `depositos`).

---

### 🔸 3) Organización del Data Lake — `04_DataLake`
- **Qué valida:** Estructura medallion (`raw / trusted / refined`), versionamiento, lifecycle rules, políticas de retención y seguridad.
- **Evidencias incluidas:**
  - Configuración de lifecycle: `04_DataLake/lifecycle.json`
  - Output de `gsutil versioning get` y `gsutil lifecycle get`
  - Diagramas y explicación conceptual.
- **Ruta:** [04_DataLake](04_DataLake/README.md) 

## ☁️ 4. Implementación del ETL en la Nube

Esta sección presenta el flujo completo del **ETL Cloud-Native** desarrollado en Google Cloud Platform, desde la obtención de datos externos hasta su procesamiento analítico final. El pipeline está totalmente automatizado, sin intervenciones manuales, y sigue la arquitectura Medallion (Bronce → Plata → Oro).

---

### 🔁 Flujo General del ETL

```mermaid
flowchart TD
    A[02_WebScraping] -->|Archivos XLS/CSV| B[03_ETL - Cloud Function]
    B -->|Bronce| C[BigQuery]
    C -->|PySpark| D[05_Procesamiento_Spark - Dataproc]
    D -->|Plata / Oro| E[BigQuery Analítico]
    E --> F[Power BI]
```
## #📊 Tabla Resumen — Implementación del ETL en la Nube

| Fase del Pipeline | Servicio(s) GCP Utilizado(s) | Entregable / Resultado | Ruta del Detalle Técnico |
|------------------|-----------------------------|-----------------------|--------------------------|
| **Extracción** | Cloud Scheduler + Cloud Function | Descarga automatizada de archivos SBS/BCRP hacia el bucket RAW | [02_WebScraping](02_WebScraping/README.md) |
| **Ingesta y Normalización Inicial** | Cloud Function Gen2 | Limpieza base, metadatos y carga en BigQuery (Bronce) | [03_ETL](03_ETL/README.md) |
| **Data Lake** | Cloud Storage (GCS) | Organización del Data Lake bajo el modelo **Medallion**: Raw → Trusted → Refined | [04_DataLake](04_DataLake/README.md)  |
| **Procesamiento Distribuido** | Dataproc Serverless (PySpark) | Construcción de las capas **Plata** (limpieza profunda) y **Oro** (modelo analítico final) | [05_Procesamiento_Spark](05_Procesamiento_Spark/README.md)|
| **Modelado Analítico** | BigQuery | Tablas finales Oro: hechos, dimensiones, KPIs para BI | [06_BigQuery](06_BigQuery/README.md) |
| **Visualización** | Power BI | Dashboard conectado directamente al dataset Oro | [07_PowerBI](07_PowerBI/README.md) |

---


## 🧩 5. Consultas SQL y Validación del Modelo de Riesgo

Esta sección documenta las validaciones ejecutadas sobre la tabla central de hechos hecho_riesgo y sus dimensiones asociadas dentro del Data Warehouse desarrollado en Google BigQuery.

📘 Evidencia de Validación en [06_BigQuery](06_BigQuery/README.md).

### 🔍 5.1 Validación de Calidad de Datos


#### **(Script 1) Validación de valores nulos críticos**
- Verifica la existencia de registros incompletos en las claves de negocio y campos numéricos.  
**Objetivo:** asegurar que no existan hechos sin referencia dimensional.
![Evidencia_SQL1](06_BigQuery/Evidencias/1-SQL-Script1.png)



#### **(Script 2) Validación semántica contra límites definidos**
- Clasifica cada valor como **Óptimo / Amarillo / Riesgo** según los umbrales definidos para cada indicador.  
**Objetivo:** comprobar que los datos se interpretan correctamente antes de alimentar visualizaciones como semáforos o tacómetros en Power BI.

![Evidencia_SQL2](06_BigQuery/Evidencias/1-SQL-Script2.png)


#### **(Script 3) Validación de cobertura temporal del dataset**
- Revisa que cada indicador tenga registros en múltiples periodos, evitando series incompletas.  
**Objetivo:** garantizar que los análisis evolutivos no tengan huecos que distorsionen el análisis.

![Evidencia_SQL3](06_BigQuery/Evidencias/1-SQL-Script3.png)


### 📊 5.2 KPIs y Métricas Financieras

#### **(Script 4) KPI — Promedio histórico del indicador por banco**
- Calcula el valor medio de cada indicador por entidad bancaria.  
**Objetivo:** ofrecer una referencia sólida para evaluar el comportamiento relativo de cada banco.

![Evidencia_SQL4](06_BigQuery/Evidencias/1-SQL-Script4.png)


#### **(Script 5) KPI — Tendencia mensual (variación porcentual)**
- Analiza la evolución del valor del indicador mes a mes usando funciones de ventana (`LAG`).  
**Objetivo:** identificar si la situación financiera del banco mejora o empeora en el tiempo.  

![Evidencia_SQL5](06_BigQuery/Evidencias/1-SQL-Script5.png)

#### **(Script 6) KPI — Consolidado de salud financiera por banco**
- Resume la cantidad de indicadores en zonas **verde**, **amarilla** y **roja** para cada entidad financiera.  
**Objetivo:** facilitar una visión global del riesgo institucional y priorizar acciones preventivas.

![Evidencia_SQL6](06_BigQuery/Evidencias/1-SQL-Script6.png)


Los resultados obtenidos a partir de estos scripts se encuentran documentados mediante:

✔ Tablas con resultados visibles  
✔ Video demostrativo del proceso  
✔ Scripts SQL subidos al repositorio


Con la ejecución validada de los scripts:

| Categoría | Scripts | Resultado |
|----------|---------|-----------|
| Calidad de datos | 1–3 | Dataset íntegro y consistente |
| KPIs financieros | 4–6 | Métricas confiables para análisis |

Una vez validado los datos, estos pueden ser consumidos para el análisis.

Dashboard de ejemplo en 👉 [07_PowerBI](07_PowerBI/README.md)
