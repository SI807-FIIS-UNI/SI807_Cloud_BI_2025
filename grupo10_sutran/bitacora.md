# 🛠️ Bitácora Técnica – PC3: Migración y Automatización del Proceso ETL en GCP

## 📅 Semana 1 – Preparativos iniciales
- [✔] Se activó cuenta institucional con créditos en GCP.
- [✔] Se creó el proyecto `shaped-icon-478404-p0`.
- [✔] Se otorgó el rol de **Propietario** a la cuenta usada.
- [✔] Se creó el bucket `sutran-bucket-2025` para almacenamiento temporal.

## ⚠️ Observaciones:
- Se mostró un mensaje sobre la falta del tag `environment` (no afecta el proceso técnico).

---

## 📅 Semana 2 – Configuración de servicios
- [✔] Se subieron archivos CSV de personas, vehículos y siniestros en `raw/`.
- [✔] Se habilitó y configuró el clúster Dataproc.
- [✔] Se instaló JupyterLab desde Dataproc.
- [✔] Se configuró el entorno PySpark en el notebook.

## ⚠️ Problemas detectados:
- ❗ El clúster se eliminó por inactividad (GCP lo borra si no se usa).
- ✅ Solución: se recreó el clúster y se continuó desde Jupyter.

---

## 📅 Semana 3 – Proceso ETL en PySpark
- [✔] Se leyó cada archivo CSV con codificación `ISO-8859-1`.
- [✔] Se eliminaron caracteres invisibles como BOM (`\ufeff`) en nombres de columnas.
- [✔] Se realizó `cast()` de columnas numéricas (`int`) para siniestros.
- [✔] Se guardó la data limpia como Parquet.

## ⚠️ Problemas detectados:
- ❗ Errores de columna no encontrada (`ID_TIPO_VIA`, `CODIGO_PERSONA`, etc.).
- ✅ Solución: se verificó que esas columnas no existen en los datos actuales. Se corrigieron los nombres y se ajustaron las dimensiones.

---

## 📅 Semana 4 – Carga a BigQuery
- [✔] Se crearon manualmente los datasets en BigQuery: `bi_sutran`.
- [✔] Se cargaron correctamente las tablas del modelo estrella.

## ⚠️ Problemas detectados:
- ❗ Error: `IllegalArgumentException: Either temporary or persistent GCS bucket must be set`.
- ✅ Solución: se agregó la opción `.option("temporaryGcsBucket", "sutran-bucket-2025")`.

- ❗ Error: `Not found: Dataset shaped-icon-478404-p0:bi_sutran`.
- ✅ Solución: el dataset no existía, se creó manualmente desde BigQuery UI.

---

## ✅ Estado final
- [✔] Archivos limpios en Parquet
- [✔] Carga funcional a BigQuery
- [✔] Evidencias organizadas
- [✔] Notebook reproducible

