# grupo10_sutran
Proyecto Cloud BI 2025-II

| Integrante                   | Rol                                | Rama                             |
| ---------------------------- | ---------------------------------- | -------------------------------- |
| **Jairo Del Río Gutiérrez**  | Exploratory Data Analysis (EDA)    | `feature/grupo10-eda-inicial`    |
| **Elias Ortiz Matamoroz**    | Limpieza y transformación de datos | `feature/grupo10-limpieza-datos` |


# 🧭 Análisis Exploratorio de Datos (EDA) – Titanic Dataset

## 🎯 Descripción del Proyecto

Este trabajo se aplicó un flujo de trabajo colaborativo usando Git y GitHub para el análisis del dataset **Titanic** (Kaggle).  
En el cual nos repartirmos los roles/responsabilidades para realizar el laboratorio, uno específicamente trabajo para el **Análisis Exploratorio de Datos (EDA)**, mientras que otro compañero se encargó de la **limpieza y transformación de datos**.

El objetivo principal del EDA es **conocer la estructura, calidad y patrones iniciales** del dataset, identificar variables relevantes y generar visualizaciones que sirvan de base para modelos predictivos futuros.

---

## 🧱 Estructura de Carpetas

La organización del repositorio sigue los lineamientos del curso, que se indicaron en el PDF del laboratorio

---

## ⚙️ Entorno de Trabajo

| Recurso | Versión / Herramienta |
|----------|------------------------|
| Python | 3.11 |
| IDE | VS Code / Jupyter Notebook |
| Control de versiones | Git + GitHub |
| Sistema operativo | Windows 10/11 |
| Colaboración | Rama `feature/grupo10-eda-inicial` |

---

## 🧩 Librerías Utilizadas

- **pandas** – Manipulación y análisis de datos
- **numpy** – Cálculos numéricos
- **matplotlib** – Visualización básica
- **seaborn** – Visualizaciones estadísticas
- **os** – Manejo de directorios

---

## 🚀 Pasos Realizados en el EDA
Revisar notebook para ver a detalle el código realizado para el EDA <br>
[IR AL NOTEBOOK](/notebooks/EDA_Titanic.ipynb)

### 1. Carga e inspección inicial de datos
- Lectura de los archivos `train.csv`, `test.csv` y `gender_submission.csv` desde `/data/raw/`.
- Exploración de dimensiones, tipos de datos y primeras observaciones (`head()`, `info()`, `describe()`).

### 2. Análisis de valores nulos
- Identificación de columnas con valores faltantes (`Age`, `Cabin`, `Embarked`).
- Visualización de nulos mediante gráficos de barras.

### 3. Distribución de variables clave
- Conteo de sobrevivientes (`Survived`).
- Distribución por género, clase, edad y tarifa (`Sex`, `Pclass`, `Age`, `Fare`).

### 4. Análisis bivariado
- Supervivencia según género y clase.
- Relación entre `Fare` y `Survived` mediante boxplots.
- Correlaciones numéricas con mapa de calor.

### 5. Generación y guardado de gráficos
- Exportación de los principales gráficos a `/results/` con nombres descriptivos (`.png`).
- Ejemplo:
  ```python
  plt.savefig('../results/sobrevivencia_por_genero.png', dpi=300, bbox_inches='tight')


## OBSERVACIONES Y CONCLUSIONES:
- Existen valores nulos importantes en Age, Cabin y Embarked.
- Las mujeres y pasajeros de clases altas (Pclass=1) tienen mayores tasas de supervivencia :0
- Las tarifas (Fare) parecen correlacionar con Survived.
- Por lo que se evidencia que las personas de clase alta tuvieron un mayor rate de supervivencia >:c
