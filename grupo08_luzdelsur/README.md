# 🌩️ Proyecto Cloud BI – Luz del Sur: Detección de Facturación Atípica en Lima Metropolitana

Repositorio oficial del proyecto **“Facturación Atípica”**, desarrollado por el **Grupo 08** del curso **SI807 – Sistemas de Inteligencia de Negocios** de la **Facultad de Ingeniería Industrial y de Sistemas (FIIS)** de la **Universidad Nacional de Ingeniería (UNI)**, en colaboración con **Luz del Sur**.

Este proyecto implementa un **pipeline de datos Cloud-Native**, basado en la **arquitectura Medallion (RAW → BRONZE → SILVER → GOLD)**, desplegado sobre **Amazon Web Services (AWS)**, con el objetivo de detectar, analizar y visualizar **casos de facturación eléctrica atípica** en Lima Metropolitana mediante técnicas estadísticas robustas, segmentación comercial y visualización geoespacial en **Power BI**.

---

## 📚 Contexto y Justificación del Proyecto

Luz del Sur requiere una solución escalable y automatizada para identificar **facturaciones inusuales** que puedan derivar de errores en medidores inteligentes, posibles casos de fraude energético o cambios abruptos en patrones de consumo. 

El enfoque tradicional basado en umbrales absolutos no es suficiente en un entorno con cientos de miles de suministros heterogéneos. Por ello, se propone una solución basada en **segmentación dinámica** y **detección estadística de anomalías**, que compara cada cliente con su grupo referente (por tipo de cliente y nivel de tensión).

> **Innovación clave**: Uso del **rango intercuartílico (IQR)** para definir umbrales adaptativos por segmento y período, eliminando falsos positivos en clientes de alto consumo legítimo.

---

## 🏗️ Arquitectura Técnica en AWS

La solución se despliega íntegramente en **Amazon Web Services (AWS)**, utilizando una arquitectura **100% serverless** que garantiza escalabilidad, bajo costo operativo y trazabilidad total del dato.

### Componentes Principales

| Capa | Servicio AWS | Función |
|------|--------------|--------|
| **Almacenamiento** | Amazon S3 | Data Lake con estructura Medallion (`raw/`, `bronze/`, `silver/`, `gold/`) |
| **Gobierno de Datos** | AWS Glue Data Catalog | Catálogo unificado de metadatos (`lds_raw`, `lds_curated`) |
| **Transformación** | AWS Glue Jobs (PySpark) | ETL batch: limpieza, tipado, joins, cálculo de tarifas y detección de anomalías |
| **Data Warehouse** | Amazon Redshift Serverless | Almacén analítico con esquema estrella optimizado para Power BI |
| **Consultas Ad-hoc / QA** | Amazon Athena | Validación de calidad y perfilamiento de datos |
| **Consumo BI** | Power BI Desktop | Dashboard ejecutivo mediante conector nativo a Redshift |
| **Orquestación** | Amazon EventBridge + AWS Lambda | Automatización de pipelines batch |
| **Seguridad** | AWS IAM | Gestión de roles con principio de mínimos privilegios |
| **Observabilidad** | Amazon CloudWatch | Centralización de logs y métricas |

> **Región**: `sa-east-1` (São Paulo, Brasil), elegida por su baja latencia en Perú, presencia de PoPs en Lima y cumplimiento normativo regional.

---

## 📂 Estructura del Repositorio

```text
grupo08_LuzdelSur/
│
├── etl/                    # Ingeniería de datos (código y procesos)
│   ├── scripts/            # Scripts PySpark (Bronze → Silver → Gold)
│   ├── logs/               # Registros de ejecución de Glue Jobs
│   └── raw/                # Muestras locales de datos crudos (solo para pruebas)
│
├── dw/                     # Lógica de datos y consultas
│   ├── ddl/                # Scripts de creación de bases y tablas externas
│   └── consultas/          # Queries SQL para vistas y validación (KPIs)
│
├── dashboard/              # Capa de visualización
│   ├── evidencias/         # Capturas del dashboard final
│   └── publicacion/        # Archivo .pbix listo para presentación
│
├── docs/                   # Documentación técnica y de gestión
│   ├── arquitectura_cloud.pdf
│   ├── bitacora_tecnica.md
│   ├── costos_cloud.xlsx
│   └── informe_final.pdf   # Documento oficial del proyecto (PC4)
│
└── README.md               # Este archivo
```

---

## 🧱 Pipeline de Datos: Arquitectura Medallion

### 🥉 Capa BRONZE (`lds_raw`)

- **Origen**: Archivos CSV planos (`cliente`, `suministro`, `medidor`, `tarifa`, `acumulado`, etc.)
- **Almacenamiento**: `s3://s1807-cloud-bi-grupo08/raw/`
- **Características**:
  - Ingesta 1:1 sin transformaciones de negocio
  - Particionamiento por periodo (`anio_mes`)
  - Actúa como **fuente de verdad inmutable**
- **Control de Calidad**:
  - Validación de nulos en claves primarias
  - Verificación de integridad temporal (`fecha_retiro ≥ fecha_instalacion`)
  - Detección de valores negativos en `energia_total_kwh`

**Ejemplo de validación en PySpark**:
```python
# Validación de consistencia temporal en medidores
inconsistencias = df.filter(F.col("fecha_retiro") < F.col("fecha_instalacion"))
print(f"Registros inconsistentes: {inconsistencias.count()}")
```

---

### 🥈 Capa SILVER (`lds_curated`)

- **Propósito**: Dataset limpio, tipado y listo para joins
- **Formato**: Apache Parquet + compresión Snappy
- **Tabla principal**: `consumo_mensual`
- **Grano**: `(id_suministro, id_medidor, anio_mes)`
- **Métricas**:
  - `energia_total_kwh`
  - `demanda_max_kw`
  - `n_registros`, `n_registros_error`, `pct_registros_error`

---

### 🥇 Capa GOLD (`lds_curated`)

- **Propósito**: Datos listos para BI, con lógica de negocio y detección de anomalías
- **Tabla principal**: `facturacion_teorica_mes`
- **Cálculo de facturación teórica**:
  ```text
  facturacion_teorica = (energia_total_kwh × cargo_energia) + cargo_fijo
  ```

- **Lógica de detección de anomalías (IQR)**:
  1. Segmentación por `(tipo_cliente, nivel_tension, anio_mes)`
  2. Cálculo de `Q1`, `Q3`, `IQR = Q3 - Q1`
  3. Umbral superior: `Q3 + 1.5 × IQR`
  4. Bandera: `es_atipico = 1` si `facturacion_teorica > umbral_superior` **y** `n_segmento ≥ 30`

> ✅ El umbral de 30 registros por segmento asegura robustez estadística (evita outliers en grupos pequeños).

---

## 📊 Modelo Dimensional y Vistas Analíticas

El modelo final se implementa en **Amazon Redshift Serverless** como un **Esquema Estrella** optimizado para Power BI:

- **Tabla de hechos central**: `vw_facturacion_atipicos`
  - Contiene métricas granulares y banderas de anomalía (`es_atipico`)
- **Vistas agregadas (dimensiones de análisis)**:
  - `vw_kpi_atipicos_zona_anual`
  - `vw_kpi_atipicos_distrito_mes`
  - `vw_kpi_atipicos_mes`

Estas vistas permiten:
- Tendencias temporales (% de atípicos por mes)
- Comparación geoespacial (por cono y distrito)
- Drill-down detallado para auditorías de campo

---

## 🔌 Conexión Power BI → Amazon Redshift

### Requisitos Técnicos

- **Conector**: Conector nativo de Power BI para Amazon Redshift
- **Endpoint**: `workgroup.<id>.us-east-1.redshift-serverless.amazonaws.com`
- **Base de datos**: `dev`
- **Esquema**: `bi` (contiene las vistas lógicas)

### Configuración en Power BI

1. **Obtener datos** → **Amazon Redshift**
2. Ingresar credenciales y seleccionar vistas en esquema `bi`
3. **Modo de conexión**: **Import** (dataset embebido en `.pbix`)
4. **Modelo relacional**: Relaciones uno a muchos entre vistas maestras y tabla de hechos

> La conexión directa a Redshift (vs. Athena) garantiza **mejor rendimiento en joins complejos** y **estabilidad en dashboards ejecutivos**.

---

## ☁️ Gestión de Costos y Eficiencia Operativa

### Supuestos Técnicos (Baseline)

| Parámetro | Valor |
|----------|-------|
| Medidores | 500,000 |
| Registros/día | 12 millones |
| Volumen mensual (crudo) | ~72 GB |
| Volumen optimizado (Parquet) | ~25 GB |

### Costo Mensual Proyectado (TCO)

| Categoría | Costo (S/ con IGV) |
|----------|------------------|
| Almacenamiento y ETL (S3, Glue, Athena) | S/ 224.00 |
| Data Warehouse (Redshift Serverless) | S/ 2,810.50 |
| Visualización (QuickSight/Power BI) | Depende de licencias Microsoft |
| **Total Estimado** | **S/ 7,671.81** (con QuickSight Enterprise) |

> **Nota**: Si Luz del Sur ya cuenta con licencias de Power BI Pro, este costo se reduce significativamente.

### Escalabilidad Financiera

Al triplicar el volumen de datos (36M registros/día), el costo solo se incrementa en **2.16x**, demostrando la **no linealidad** y eficiencia del modelo serverless de AWS.

---

## 🛡️ Seguridad y Gobernanza

- **Principio de mínimos privilegios**: roles IAM definidos (`bi-admin`, `bi-data-engineer`, `bi-analyst`)
- **Cifrado**: habilitado en tránsito (TLS) y en reposo (SSE-S3)
- **Soberanía de datos**: procesamiento en región sudamericana (`sa-east-1`)
- **Cumplimiento**: AWS cumple con ISO 27001, SOC 2 y PCI DSS
- **Auditoría**: logs centralizados en CloudWatch

---

## 🔄 Orquestación y Automatización

- **Amazon EventBridge**: agenda la ejecución diaria del pipeline
- **AWS Lambda**: valida la llegada de archivos a `raw/` y dispara Glue Jobs
- **Flujo batch**: diseñado para reprocesamiento histórico y escalado futuro a tiempo real (con Kinesis)

---

## 🧑‍💻 Equipo de Trabajo – Grupo 08

| Rol | Integrante |
|-----|-----------|
| **Data Engineering & Cloud Architecture** | Enciso Quichca, Frey Mauricio |
| **Data Modeling, QA & Statistical Logic** | Gordillo Inocente, Mikhael León |
| **Business Intelligence & Dashboard Design** | Hernández Hernández, Jahir Alejandro |

**Curso**: SI807 – Sistemas de Inteligencia de Negocios  
**Facultad**: Ingeniería Industrial y de Sistemas – UNI  
**Fecha de entrega**: 21 de noviembre de 2025

---

## 📄 Documentación Adjunta

- **Informe Técnico Completo**: [`docs/informe_final.pdf`](docs/informe_final.pdf)
- **Análisis Financiero**: [`docs/costos_cloud.xlsx`](docs/costos_cloud.xlsx)

---

> 💡 Este proyecto demuestra cómo una arquitectura **serverless, escalable y económica** en AWS puede resolver problemas reales del sector energético, combinando **ingeniería de datos rigurosa**, **estadística aplicada** y **visualización estratégica**, todo ello dentro de un marco académico con impacto industrial.