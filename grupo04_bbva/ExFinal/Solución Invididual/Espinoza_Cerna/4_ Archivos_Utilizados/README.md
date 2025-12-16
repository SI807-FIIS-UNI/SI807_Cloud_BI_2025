# 📁 Estructura de los Archivos

A continuación se describe cada carpeta en detalle:

## 📂 1. Data_Cruda/

Contiene todos los datasets originales usados para:
- Construcción del modelo de datos
- Cálculo de KPIs
- Pruebas del pipeline

## 📂 2. KQLs/

Incluye el los querys para ver los Logs en el Log Analytics workspace

## 📂 3. Notebooks/

Include Jupyter/Databricks notebooks utilizados para:
- Limpieza y transformación inicial
- Análisis exploratorio (EDA)
- Validación estadística
- Construcción de KPIs
- Cada notebook está comentado paso a paso para facilitar la reproducibilidad.

## 📂 4. Querys/

- Contiene todas las consultas SQL utilizadas en el proyecto, organizadas por tipo:
- Validación de calidad (nulos, duplicados, consistencia)
- Cálculo de KPIs
- Integridad entre tablas
- Validaciones históricas
- Scripts de control
- Estas queries pueden ejecutarse en PostgreSQL, Databricks o el motor definido en el proyecto.

## 📂 5. backend/

API desarrollada en Python (Flask/FastAPI) que sirve:
- Endpoints de KPIs
- Filtros
- Agregaciones
- Conexión con PostgreSQL
- Integración con Databricks o Storage

Incluye:

- app.py
- config.py
- database.py
- Rutas para KPIs y datos

## 📂 6. frontend/

Interfaz web desarrollada en:
- HTML / CSS / JavaScript
- Tailwind / Bootstrap
- Gráficos con Chart.js / ECharts / Plotly

Funciones clave:

- Visualización de KPIs en tiempo real
- Filtros dinámicos
- Tablas interactivas
- Conexión con el backend vía API

