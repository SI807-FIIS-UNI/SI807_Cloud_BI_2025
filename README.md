# 🧠 SI807U – Sistemas de Inteligencia de Negocios (Fase Cloud) – 2025-II

Este repositorio centralizado es el entorno oficial del curso **SI807U – Sistemas de Inteligencia de Negocios** de la Universidad Nacional de Ingeniería, correspondiente al semestre **2025-II**.  
Aquí se desarrollará la **segunda parte del proyecto integrador**, enfocada en el **despliegue de soluciones de Business Intelligence en la nube** utilizando **Google Cloud Platform (GCP)**, **Azure** o **AWS**.

---

## 🎯 Fines del Repositorio

El objetivo principal de este repositorio es **centralizar y estandarizar** el trabajo de todos los grupos del curso en un entorno controlado, reproducible y colaborativo, simulando las prácticas profesionales de un equipo de datos corporativo.

**En este repositorio los estudiantes:**
- Migrarán su sistema BI local a un entorno **Cloud**.  
- Implementarán procesos **ETL automatizados** en servicios nativos de nube (Dataproc, Synapse, Glue, etc.).  
- Desplegarán **Data Warehouses** y modelos multidimensionales.  
- Publicarán **Dashboards analíticos** conectados en tiempo real (Power BI Service, Looker Studio o QuickSight).  
- Documentarán su arquitectura, scripts y bitácora técnica bajo control de versiones.  

---

## 🏗️ Estructura General del Proyecto

```
SI807U_Cloud_BI_2025/
│
├── grupo01_interbank/
├── grupo02_essalud/
├── grupo03_credicorp/
├── grupo04_bbva/
├── grupo05_nettalco/
├── grupo06_scotiabank/
├── grupo07_claro/
├── grupo08_luzdelsur/
├── grupo09_cencosud/
├── grupo10_sutran/
│
├── docs/
│   ├── guia_docente.md
│   ├── rubrica_evaluacion.xlsx
│   ├── plan_cloud.pdf
│
├── CONTRIBUTING.md
└── README.md
```

Cada carpeta de grupo contiene el proyecto completo del equipo (scripts ETL, consultas SQL, dashboards y documentación).

---

## 🧩 Metodología y Flujo de Trabajo

El desarrollo sigue el flujo **GitFlow**, con ramas protegidas para mantener la trazabilidad y control docente.

| Rama | Propósito |
|------|------------|
| `main` | Rama principal, aprobada y mantenida por el docente. |
| `develop` | Integración de cambios validados por los líderes de grupo. |
| `feature/grupoXX-init` | Ramas independientes por grupo de estudiantes. |

Cada grupo trabajará exclusivamente en su rama asignada y generará *Pull Requests* hacia `develop`, que serán revisadas y aprobadas por el docente.

---

## ☁️ Entornos Cloud Soportados

Cada grupo deberá elegir **uno de los tres entornos cloud oficiales**:

| Plataforma | Servicios Clave |
|-------------|----------------|
| **Google Cloud Platform (GCP)** | Cloud Storage, Dataproc, BigQuery, Composer, Looker Studio |
| **Microsoft Azure** | Azure Blob Storage, Data Factory, Synapse Analytics, Power BI Service |
| **Amazon Web Services (AWS)** | S3, Glue, Redshift, Step Functions, QuickSight |

---

## 🧰 Requerimientos Técnicos Mínimos

- Procesamiento ETL con Spark, Glue o Dataflow.  
- Almacenamiento estructurado en DW (BigQuery, Synapse, Redshift).  
- Dashboard analítico conectado al DW.  
- Documentación técnica reproducible (README, bitácora, scripts).  
- Uso correcto de control de versiones Git y buenas prácticas DevOps.

---

## 🧑‍💻 Roles dentro del Proyecto

| Rol | Responsabilidad |
|------|----------------|
| **Docente / Maintainer** | Administra el repositorio, revisa PRs, valida entregas. |
| **Líder de Grupo (Est. 01)** | Gestiona los merges hacia `develop`, coordina el trabajo. |
| **Miembros (Est. 02 y 03)** | Desarrollan tareas ETL, modelado y dashboards en sus ramas. |

---

## 🔒 Estructura de Permisos

- Cada grupo cuenta con un **equipo (Team)** propio dentro de la organización GitHub `SI807U-2025`.  
- Cada rama `feature/grupoXX-init` está protegida y solo su equipo puede realizar *push*.  
- Los merges a `main` requieren revisión docente.  

---

## 🧾 Documentación y Evaluación

Los entregables deberán incluir:
- **Plan de migración a la nube.**  
- **Arquitectura implementada (diagrama y descripción).**  
- **Scripts ETL y consultas SQL.**  
- **Capturas de ejecución y dashboards publicados.**  
- **Bitácora técnica y costos estimados.**

Las rúbricas y criterios están disponibles en `docs/rubrica_evaluacion.xlsx`.

---

## 📅 Cronograma General

| Semana | Actividad | Entregable |
|:--:|:--|:--|
| 1 | Elección de nube y diseño de arquitectura | Documento PDF + Diagrama Cloud |
| 2 | Migración de ETL | Scripts PySpark / Dataflow / Glue |
| 3 | Implementación del DW | Tablas, vistas y consultas OLAP |
| 4 | Dashboard y cierre técnico | Power BI / Looker / QuickSight + Informe final |

---

## 🧠 Buenas Prácticas

- Mantener los datos sensibles fuera del repositorio (`.env`, `.gitignore`).  
- Seguir las reglas de contribución descritas en `CONTRIBUTING.md`.  
- Nombrar correctamente las ramas y commits (`feat:`, `fix:`, `docs:`).  
- Generar Pull Requests con descripción clara y evidencia de pruebas.  

---

## 🏁 Créditos

Curso: **SI807U – Sistemas de Inteligencia de Negocios**  
Docente: **Ing. Fernando García** (`@webconceptos`)  
Universidad Nacional de Ingeniería – Facultad de Ingeniería Industrial y de Sistemas  
Semestre: **2025-II**

---

## 🔗 Enlaces Útiles

- 🌐 Organización GitHub: [https://github.com/SI807U-2025](https://github.com/SI807U-2025)  
- 📘 Repositorio central: [https://github.com/SI807U-2025/SI807_Cloud_BI_2025](https://github.com/SI807U-2025/SI807_Cloud_BI_2025)  
- 🧩 Guía de contribución: [CONTRIBUTING.md](./CONTRIBUTING.md)  
- 📊 Evaluación: [`docs/rubrica_evaluacion.xlsx`](./docs/rubrica_evaluacion.xlsx)
