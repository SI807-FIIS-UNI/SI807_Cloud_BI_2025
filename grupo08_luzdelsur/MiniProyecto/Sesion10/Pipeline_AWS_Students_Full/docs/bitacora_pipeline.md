# 🧾 Bitácora Técnica del Pipeline AWS

## Grupo

Grupo: 8\
Integrantes: (pendiente)

------------------------------------------------------------------------

### 🪣 Paso 1 -- Carga de datos en S3

-   Bucket creado: si807u-grupo8-bi
-   Ruta de carga: raw/ecommerce/
-   Archivo cargado: ecommerce_clean.csv

------------------------------------------------------------------------

### ⚙️ Paso 2 -- Glue Data Catalog

-   Base creada: raw_db
-   Crawler configurado: Sí
-   Tablas detectadas: Ninguna (error)
-   Estado: Fallo en el crawler

------------------------------------------------------------------------

### 🧠 Paso 3 -- Glue Job PySpark

No se ejecutó por el error previo.

------------------------------------------------------------------------

### 💾 Paso 4 -- Athena

No ejecutado.

------------------------------------------------------------------------

### 📈 Paso 5 -- QuickSight

No ejecutado.

------------------------------------------------------------------------

### 🧩 Conclusión

El pipeline avanzó hasta Glue, pero el crawler falló y detuvo el
proceso.
