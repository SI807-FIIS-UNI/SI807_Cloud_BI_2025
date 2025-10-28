# grupo10_sutran
Proyecto Cloud BI 2025-II

## 🧹 Limpieza de Datos – Proyecto Titanic

Este módulo documenta el **proceso de limpieza de los datasets del Titanic** (`train.csv`, `test.csv` y `gender_submission.csv`) antes de su análisis exploratorio o modelado predictivo.  
El trabajo se ejecuta en un **notebook** dentro de la carpeta `/notebooks/`, tomando los datos de `/data/raw/` y generando los resultados limpios en `/data/processed/`.

---

## ⚙️ Librerías necesarias

Archivo `requirements.txt` sugerido:
Instalación:
```bash
pip install -r requirements.txt
```

## Descripción de las tablas usadas

| Archivo                 | Descripción                                                 | Fuente           |
| ----------------------- | ----------------------------------------------------------- | ---------------- |
| `train.csv`             | Datos de entrenamiento que incluyen la etiqueta `Survived`. | Kaggle – Titanic |
| `test.csv`              | Datos de prueba sin la etiqueta objetivo.                   | Kaggle – Titanic |
| `gender_submission.csv` | Ejemplo de salida esperada (plantilla de predicción).       | Kaggle – Titanic |

## Transformaciones aplicadas
En el notebook se indica paso a paso los pasos realizados
[IR AL NOTEBOOK](notebooks/Limpieza_Titanic.ipynb)

| Tipo de transformación   | Descripción                                                          |
| ------------------------ | -------------------------------------------------------------------- |
| Eliminación de columnas  | Se eliminan `Cabin` y `Ticket` por su alto nivel de datos faltantes. |
| Imputación de edad       | Se reemplazan los valores nulos de `Age` con la mediana.             |
| Imputación de embarque   | Se reemplazan los valores nulos de `Embarked` con la moda.           |
| Imputación de tarifa     | En `test.csv`, los nulos en `Fare` se imputan con la mediana.        |
| Codificación de sexo     | `male` → 0, `female` → 1                                             |
| Codificación de embarque | `S` → 0, `C` → 1, `Q` → 2                                            |


### Archivos resultantes
| Archivo limpio          | Descripción                                                           |
| ----------------------- | --------------------------------------------------------------------- |
| `train_clean.csv`       | Dataset de entrenamiento sin valores nulos ni variables irrelevantes. |
| `test_clean.csv`        | Dataset de prueba limpio y con codificación homogénea.                |
| `gender_submission.csv` | Archivo copiado sin cambios (referencia de formato).                  |

🧠 Observaciones finales

El script equivalente se encuentra también en /scripts/clean_data.py.

La función clean_titanic_data() puede ser reutilizada para nuevas versiones de los datasets.

Todos los pasos garantizan que train y test mantengan consistencia de variables y tipos.

El dataset gender_submission.csv se conserva intacto ya que no requiere limpieza.
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
[IR AL NOTEBOOK](notebooks/EDA_Titanic.ipynb)

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
