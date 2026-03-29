
# 🧩 Pipeline AWS – Guía de Implementación (Estudiantes SI807U)

## 🎯 Objetivo
Implementar un pipeline funcional de **Business Intelligence en la nube** sobre AWS, desde la ingesta hasta la capa analítica, utilizando **S3, Glue, Athena y QuickSight**.

El objetivo final es que el grupo logre un flujo completo de:
```
S3 (raw) → Glue Job (PySpark) → S3 (curated) → Athena (SQL) → QuickSight (Dashboard)
```

---

## 🧱 1. Estructura recomendada en S3
```
s3://si807u-<grupo>-bi/
├── raw/
│   └── ecommerce/          # archivos CSV originales
├── curated/
│   └── ecommerce/          # parquet limpio
├── analytics/
│   └── results/            # salidas o datasets procesados
└── athena_results/
```

---

## ☁️ 2. Flujo del Pipeline
### 1️⃣ Ingesta de datos
- Subir `ecommerce_clean.csv` (desde tu EDA) a `s3://si807u-<grupo>-bi/raw/ecommerce/`

### 2️⃣ Catálogo Glue
- Crear base de datos: `raw_db`
- Crear Crawler con ruta `raw/ecommerce/`
- Ejecutar y verificar tabla `raw_db.ecommerce_clean`

### 3️⃣ Transformación con Glue Job (PySpark)
Ejecutar el Job `job_transform_aws.py` con:
```
--SOURCE s3://si807u-<grupo>-bi/raw/ecommerce/
--TARGET s3://si807u-<grupo>-bi/curated/ecommerce/
```
Resultado: archivos **Parquet particionados por año/mes** en `curated/`.

### 4️⃣ Consulta en Athena
Ejecutar los SQL del folder `/sql` en orden:
1. `00_create_analytics_db.sql`
2. `10_create_sales_curated.sql`
3. `20_kpi_sales_summary.sql`

### 5️⃣ Dashboard QuickSight
- Crear dataset desde Athena (`analytics_db.sales_curated`).
- Publicar dashboard “Ventas por Categoría”.

---

## 🧠 3. Reglas de Entrega
- Registrar cada paso en `/docs/bitacora_pipeline.md`
- Commit y Push a la rama `feature/grupoXX-init`
- PR hacia `develop` con descripción del flujo y evidencias (S3, Glue, Athena, QuickSight).

---

## 📈 4. Evaluación
| Fase | Descripción | Peso |
|------|--------------|------|
| Glue Job | Transformación raw→curated (PySpark) | 30% |
| Athena SQL | Base analítica y KPI | 30% |
| QuickSight | Dashboard BI funcional | 25% |
| Bitácora + GitHub | Evidencias y documentación | 15% |

---

## ✅ Checklist
- [ ] Dataset cargado en S3/raw
- [ ] Glue Crawler y Job ejecutados
- [ ] Tabla Athena creada y funcional
- [ ] Dashboard publicado en QuickSight
- [ ] PR con evidencias completado
