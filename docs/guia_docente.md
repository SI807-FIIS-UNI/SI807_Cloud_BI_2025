# 🎓 Guía Docente – SI807U: Sistemas de Inteligencia de Negocios (Fase Cloud) – 2025-II

---

## 🧠 Presentación del Curso

La asignatura **Sistemas de Inteligencia de Negocios (SI807U)** busca que el estudiante integre los conocimientos adquiridos en analítica, gestión de datos y arquitectura empresarial, aplicándolos en el desarrollo de un **Sistema de Inteligencia de Negocios completo desplegado en la nube**.

Durante la **Fase Cloud**, los grupos migrarán su solución local hacia un entorno **Cloud Computing** profesional (GCP, Azure o AWS), empleando herramientas modernas de integración, almacenamiento y visualización de datos.

---

## 🎯 Objetivos Generales

- Aplicar los principios del **Business Intelligence moderno** en entornos distribuidos y escalables.  
- Diseñar e implementar una **arquitectura de datos en la nube** con procesos ETL automatizados.  
- Desarrollar un **Data Warehouse Cloud** y modelos multidimensionales para análisis OLAP.  
- Desplegar tableros analíticos conectados a fuentes en tiempo real.  
- Promover la **colaboración técnica y el versionamiento de proyectos** en GitHub.

---

## ☁️ Entornos Cloud Permitidos

Cada grupo elegirá **uno** de los siguientes proveedores:

| Proveedor | Servicios recomendados |
|------------|------------------------|
| **Google Cloud Platform (GCP)** | Cloud Storage, Dataproc, BigQuery, Composer, Looker Studio |
| **Microsoft Azure** | Blob Storage, Data Factory, Synapse Analytics, Power BI Service |
| **Amazon Web Services (AWS)** | S3, Glue, Redshift, QuickSight, Lambda |

---

## 🧩 Metodología de Trabajo

El curso se desarrolla bajo una metodología **proyecto-integrador** con evaluación continua.  
Cada grupo deberá demostrar avances tangibles en cada práctica y mantener un repositorio funcional, documentado y reproducible.

### 🔁 Flujo de trabajo colaborativo (GitFlow)

1. **Ramas protegidas:**  
   - `main` → rama estable revisada por el docente.  
   - `develop` → rama de integración.  
   - `feature/grupoXX-init` → rama exclusiva de cada grupo.

2. **Comandos básicos de trabajo**
   ```bash
   git checkout feature/grupoXX-init
   git pull origin feature/grupoXX-init
   # Desarrollar avances
   git add .
   git commit -m "feat: actualización del proceso ETL cloud"
   git push origin feature/grupoXX-init
   ```

3. Los *Pull Requests (PR)* hacia `develop` serán revisados y aprobados por el docente antes del *merge* final.

---

## 🧱 Estructura del Proyecto

Cada grupo debe mantener esta organización:

```
grupoXX_empresa/
│
├── etl/                  # Scripts y procesos de integración cloud
│   ├── scripts/
│   └── logs/
│
├── dw/                   # Data warehouse cloud
│   ├── ddl/
│   └── consultas/
│
├── dashboard/            # Dashboards y visualizaciones
│   ├── evidencias/
│   └── publicacion/
│
├── docs/                 # Documentación técnica
│   ├── arquitectura_cloud.pdf
│   ├── bitacora_tecnica.md
│   ├── costos_cloud.xlsx
│   └── informe_final.pdf
│
└── README.md
```

---

## 📅 Hitos de Evaluación

| Evaluación | Objetivo | Entregables |
|-------------|-----------|-------------|
| **Práctica 3 – Migración y Automatización ETL Cloud** | Desarrollar e implementar los procesos ETL en la nube. | Scripts PySpark/Dataflow/Glue, bitácora, documentación técnica. |
| **Práctica 4 – Implementación del Data Warehouse Cloud** | Construir el DW en la nube con modelo dimensional y consultas OLAP. | Scripts SQL, diseño dimensional, consultas OLAP, documentación. |
| **Examen Final – Despliegue Analítico e Integración Total** | Integrar todo el sistema BI Cloud, desplegar dashboards y presentar el informe final. | Dashboard publicado, video demostrativo, informe final PDF, repo reproducible. |

---

## 📊 Criterios de Evaluación

Los criterios de evaluación están definidos en `docs/rubrica_evaluacion.xlsx` y consideran:

- **Diseño arquitectónico y escalabilidad**.  
- **Automatización ETL Cloud y validación funcional**.  
- **Implementación del DW y consultas OLAP.**  
- **Dashboard analítico y claridad de KPIs.**  
- **Documentación técnica y trazabilidad en GitHub.**

---

## 🧑‍💻 Roles de Equipo

| Rol | Responsabilidad |
|------|----------------|
| **Estudiante 01 (Líder Técnico)** | Gestiona los merges, organiza las tareas, y asegura la reproducibilidad del entorno. |
| **Estudiante 02 (Data Engineer)** | Desarrolla los procesos ETL, maneja los pipelines y la limpieza de datos. |
| **Estudiante 03 (Data Analyst)** | Construye las consultas analíticas y diseña el dashboard final. |

---

## 🧠 Buenas Prácticas

- Mantener el código comentado y ordenado.  
- Evitar subir datos sensibles o credenciales.  
- Actualizar el README.md del grupo con cada avance importante.  
- Incluir capturas y evidencias de ejecución.  
- Comentar claramente cada *commit*.  

---

## 🏁 Evaluación Final

El **Examen Final** representa la culminación del proyecto y se evaluará mediante:

- Demostración del sistema desplegado en la nube.  
- Defensa técnica ante el jurado docente.  
- Presentación del informe y evidencias de ejecución.  
- Revisión del repositorio y cumplimiento de estándares.

---

**Docente Responsable:**  
**Ing. Fernando García** (`@webconceptos`)  
Universidad Nacional de Ingeniería – Facultad de Ingeniería Industrial y de Sistemas  
Semestre 2025-II  
Repositorio: [https://github.com/webconceptos/SI807_Cloud_BI_2025](https://github.com/webconceptos/SI807_Cloud_BI_2025)
