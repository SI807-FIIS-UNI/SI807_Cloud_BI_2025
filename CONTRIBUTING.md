# 🧾 Guía de Contribución – SI807U Cloud BI 2025-II

Este documento describe las normas de trabajo colaborativo y las buenas prácticas que todos los grupos deben seguir dentro del repositorio **SI807_Cloud_BI_2025**.

---

## 🧠 Objetivo

Garantizar que cada grupo trabaje de forma organizada, trazable y reproducible dentro de su rama asignada.  
El cumplimiento de estas normas forma parte de la evaluación técnica del curso.

---

## 🧩 Estructura de ramas

Cada grupo tiene asignada una rama exclusiva:

| Grupo | Rama asignada | Propósito |
|:--:|:--|:--|
| 1 | `feature/grupo01-init` | Interbank |
| 2 | `feature/grupo02-init` | Essalud |
| 3 | `feature/grupo03-init` | Credicorp |
| 4 | `feature/grupo04-init` | BBVA |
| 5 | `feature/grupo05-init` | Netalco |
| 6 | `feature/grupo06-init` | Scotiabank |
| 7 | `feature/grupo07-init` | Claro Perú |
| 8 | `feature/grupo08-init` | Luz del Sur |
| 9 | `feature/grupo09-init` | Cencosud |
| 10 | `feature/grupo10-init` | Sutran |

Solo los miembros del grupo correspondiente pueden hacer *push* directo en su rama.

---

## ⚙️ Flujo de trabajo (GitFlow adaptado)

1. Clonar el repositorio central:
   ```bash
   git clone https://github.com/webconceptos/SI807_Cloud_BI_2025.git
   ```
2. Cambiar a la rama asignada:
   ```bash
   git checkout feature/grupoXX-init
   ```
3. Desarrollar los cambios en carpetas internas del grupo.
4. Realizar *commits* descriptivos con convención semántica:
   - `feat:` → nueva funcionalidad  
   - `fix:` → corrección  
   - `docs:` → documentación  
   - `refactor:` → mejora estructural  
   - `test:` → pruebas  
   - `data:` → nuevos datos o actualizaciones ETL
5. Subir los cambios:
   ```bash
   git add .
   git commit -m "feat: carga inicial del proceso ETL"
   git push origin feature/grupoXX-init
   ```

---

## 🧾 Convención de carpetas por grupo

```
grupoXX_nombreempresa/
│
├── etl/
│   ├── scripts/
│   │   ├── etl_cloud.py
│   │   ├── transform_spark.sql
│   │   └── validate_jobs.ipynb
│   └── logs/
│
├── dw/
│   ├── ddl/
│   │   ├── create_tables.sql
│   │   └── create_views.sql
│   └── consultas/
│       └── analisis_olap.sql
│
├── dashboard/
│   ├── evidencias/
│   │   ├── dashboard_final.pbix
│   │   └── screenshots/
│   └── publicacion/
│       └── link_dashboard.txt
│
├── docs/
│   ├── arquitectura_cloud.pdf
│   ├── bitacora_tecnica.md
│   ├── costos_cloud.xlsx
│   └── informe_final.pdf
│
└── README.md
```

---

## 🧑‍💻 Pull Requests y Revisión Docente

- Toda integración a `develop` o `main` debe realizarse mediante *Pull Request (PR)*.  
- El docente (`@webconceptos`) revisará código, reproducibilidad y documentación antes de aprobar.  
- Cada PR debe incluir:
  - Descripción del avance.  
  - Evidencias (capturas, logs, links).  
  - Integrantes responsables.

---

## ✅ Criterios de Aceptación

Un avance será aceptado si:
- Compila y se ejecuta sin errores.  
- Cumple la estructura definida.  
- Incluye README y bitácora actualizada.  
- El dashboard o servicio cloud está accesible.  

---

## 🧠 Buenas Prácticas

- No subir datos sensibles ni credenciales (.env, keys).  
- Usar `.gitignore` para carpetas temporales y binarios.  
- Evitar commits de archivos innecesarios (`.pyc`, `.DS_Store`, `.ipynb_checkpoints`).  
- Documentar cada paso del proceso técnico en Markdown (`docs/bitacora_tecnica.md`).

---

## 🏁 Control Docente

Cada *merge* aprobado por el docente será considerado una **entrega oficial**.  
Los avances no aprobados se contabilizan como pendientes de corrección.  

---
**Autor:** Ing. Fernando García – [@webconceptos](https://github.com/webconceptos)
