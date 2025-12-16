# Examen Final (SI-807) — Solución Individual (Aymachoque_Aymachoque)
Ruta de entrega (según rúbrica):
`Grupo01_Interbank/ExFinal/SolucionIndividual/Aymachoque_Aymachoque/`

Este repositorio documenta lo realizado **por consola (AWS CLI)** para construir el flujo **Bronce → Plata → Oro** con el dataset **Sample_Superstore.csv**, dejando **evidencias (scripts + logs)** y outputs en **Amazon S3**.

---

## 0) Resumen ejecutivo
✅ **Bronce (3.1)**  
- Bucket creado en `us-east-1`  
- Estructura `bronce/raw`, `bronce/processed`, `bronce/curated`  
- CSV cargado a `bronce/raw`  
- EDA ejecutado (con workaround de encoding)  
- Evidencias subidas a `docs/`

✅ **Plata (3.2)**  
- Limpieza + tipificación ejecutada  
- Modelo tipo estrella generado (dimensiones + fact)  
- CSVs publicados en `plata/dim` y `plata/fact`  
- Script y log subidos a `docs/`

✅ **Oro (3.2)**  
- KPIs generados y publicados en `oro/kpis/`  
- Script y log subidos a `docs/`

⏸️ **3.3 (BI / QuickSight / Athena)**  
- Se avanzó configuración (Athena output location + ejecución de queries)  
- QuickSight presentó problemas de permisos/roles/policies y también “No tables found” al listar tablas del catálogo.  
- Se documenta como **intento** con evidencias, pero **no se concluyó** la visualización final en QuickSight.

---

## 1) Entorno y recursos
### Región
- `us-east-1` (N. Virginia)

### Bucket principal (S3)
Se creó con timestamp para asegurar nombre único:

- **Bucket:** `exfinal-aymachoque-1765858502`

Verificación (se ejecutó y devolvió OK):
- `aws s3api head-bucket --bucket "$BUCKET"`

---

## 2) Estructura final en S3
### Bronce
- `s3://exfinal-aymachoque-1765858502/bronce/raw/`
- `s3://exfinal-aymachoque-1765858502/bronce/processed/`
- `s3://exfinal-aymachoque-1765858502/bronce/curated/`

Contenido confirmado en `raw/`:
- `.keep`
- `Sample_Superstore.csv` (~2.2 MB)

### Plata
- `s3://exfinal-aymachoque-1765858502/plata/dim/`
  - `dim_cliente.csv`
  - `dim_producto.csv`
  - `dim_region.csv`
  - `dim_tiempo.csv`
- `s3://exfinal-aymachoque-1765858502/plata/fact/`
  - `fact_ventas.csv`

### Oro
- `s3://exfinal-aymachoque-1765858502/oro/kpis/`
  - `kpi_region.csv`
  - `kpi_resumen.csv`
  - `kpi_segmento.csv`
  - `kpi_tendencia_mensual.csv`
  - `kpi_top_productos_profit.csv`

### Docs (evidencias)
- `s3://exfinal-aymachoque-1765858502/docs/`
  - `docs_bronce_31.txt`
  - `eda_bronce.py`
  - `eda_output_31.txt`
  - `plata_build.py`
  - `plata_build_log.txt`
  - `oro_kpis.py`
  - `oro_kpis_log.txt`
  - (intento 3.3) `run_athena_ddl_33.sh`
  - (intento 3.3) `athena_ddl_run_log.txt`
  - (y otros que se fueron generando durante el intento)

---


