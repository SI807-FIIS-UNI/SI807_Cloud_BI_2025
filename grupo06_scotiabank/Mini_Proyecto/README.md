## 🧭 MiniProyecto - Titanic

### 📘 Descripción General

Este proyecto forma parte del curso **Sistemas de Inteligencia de Negocio** y se desarrolla en el **repositorio oficial**:
🔗 [SI807_Cloud_BI_2025](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025)

El propósito es realizar un **análisis exploratorio y predictivo** del **Titanic Dataset**, aplicando buenas prácticas de colaboración en GitHub, limpieza de datos y modelado supervisado.

---

## 🚢 Dataset: Titanic - Machine Learning from Disaster

### 🔍 **Descripción del Dataset**

El conjunto de datos está dividido en dos grupos principales:

| Archivo                   | Descripción                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **train.csv**             | Contiene 891 registros de pasajeros, incluyendo la variable objetivo `Survived` (0 = No, 1 = Sí). Se usa para entrenar el modelo. |
| **test.csv**              | Contiene 418 registros sin la variable `Survived`. Se usa para evaluar el rendimiento del modelo.                                 |
| **gender_submission.csv** | Ejemplo de predicción donde se asume que todas las mujeres sobreviven. Sirve como plantilla de envío.                             |

📦 **Tamaño total:** 93.08 kB
📄 **Tipo:** CSV
🔑 **Licencia:** Sujeto a las reglas de la competencia de Kaggle
📊 **Fuente:** [Kaggle – Titanic: Machine Learning from Disaster](https://www.kaggle.com/c/titanic/data)

---

### 🧾 **Diccionario de Datos**

| Variable   | Definición                     | Tipo / Clave                                   |
| ---------- | ------------------------------ | ---------------------------------------------- |
| `Survived` | Supervivencia                  | 0 = No, 1 = Sí                                 |
| `Pclass`   | Clase del boleto               | 1 = Primera, 2 = Segunda, 3 = Tercera          |
| `Sex`      | Sexo del pasajero              | `male` / `female`                              |
| `Age`      | Edad en años                   | Numérico (fraccional si < 1 año)               |
| `SibSp`    | Nº de hermanos/esposos a bordo | Entero                                         |
| `Parch`    | Nº de padres/hijos a bordo     | Entero                                         |
| `Ticket`   | Número de boleto               | Texto                                          |
| `Fare`     | Tarifa pagada                  | Numérico                                       |
| `Cabin`    | Número de cabina               | Texto                                          |
| `Embarked` | Puerto de embarque             | C = Cherbourg, Q = Queenstown, S = Southampton |

📘 **Notas:**

* `Pclass` es un indicador del estatus socioeconómico (SES): 1️⃣ Alto, 2️⃣ Medio, 3️⃣ Bajo.
* Algunas edades son estimadas (`xx.5`).
* `SibSp` incluye cónyuges, `Parch` incluye padres e hijos.
* Algunos pasajeros viajaban solos o con niñeras, por lo que `Parch` puede ser 0.

---

## 🧹 Limpieza de Datos (`data/processed`)

Código utilizado para cargar y visualizar los archivos:

```python
import pandas as pd
from IPython.display import display

path_1 = r'../data/raw/gender_submission.csv'
path_2 = r'../data/raw/train.csv'
path_3 = r'../data/raw/test.csv'

# Cargar datasets
df_gender_submission = pd.read_csv(path_1)
df_titanic = pd.read_csv(path_2)
df_test = pd.read_csv(path_3)

# Mostrar datasets
def display_dataframe(df):
    if len(df) <= 5000:
        display(df)
    else:
        print("Archivo muy grande — mostrando primeras 200 filas:")
        display(df.head(200))

display_dataframe(df_gender_submission)
display_dataframe(df_titanic)
display_dataframe(df_test)
```

### 📊 **Resultados de la Carga**

* **train.csv:** 891 registros, 12 columnas
* **test.csv:** 418 registros, 11 columnas
* **gender_submission.csv:** 418 registros, 2 columnas

---

### ⚠️ **Valores Faltantes**

| Dataset                   | Columna                                    | Nº de valores nulos |
| ------------------------- | ------------------------------------------ | ------------------- |
| **train.csv**             | `Age` (177), `Cabin` (687), `Embarked` (2) | Sin valores nulos                 |
| **test.csv**              | `Age` (86), `Cabin` (327), `Fare` (1)      | Sin valores nulos                 |
| **gender_submission.csv** | Sin valores faltantes                      | Sin valores nulos                 |

🔧 **Acciones sugeridas:**

* Imputar `Age` con la mediana por clase (`Pclass`) y sexo (`Sex`).
* Reemplazar `Embarked` faltantes con el modo (`S`).
* Eliminar o agrupar `Cabin` como binario (“Tiene cabina” / “No tiene”).

---

## 🔬 Análisis Exploratorio (`notebooks`)

Instalación de dependencias y carga de datos:

```python
!pip install scikit-learn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report 
from pathlib import Path

FILE_PATHS = {
    "gender_submission": Path("../data/raw/gender_submission.csv"),
    "test": Path("../data/raw/test.csv"),
    "train": Path("../data/raw/train.csv")
}

for name, path in FILE_PATHS.items():
    if not path.exists():
        print(f"El archivo {path} no existe.")
    else:
        print(f"{name} cargado correctamente ({path})")
```

---

### 🧠 **Primeras Observaciones**

#### 🧾 Entrenamiento (`train.csv`)

| Característica | Observación                                        |
| -------------- | -------------------------------------------------- |
| `Pclass`       | Distribución desigual (más pasajeros en 3ra clase) |
| `Sex`          | Mayor número de hombres (577) que mujeres (314)    |
| `Age`          | Media ≈ 30 años, con 177 valores nulos             |
| `Survived`     | Tasa de supervivencia ≈ 38%                        |
| `Cabin`        | Alta cantidad de valores faltantes (≈ 77%)         |
| `Embarked`     | Mayoría embarcó en Southampton (S)                 |

---

## 📚 Estructura del Proyecto

```
SI807_Cloud_BI_2025/
│
├── data/
│   ├── raw/                # Datos originales
│   └── processed/          # Datos limpios
│
├── notebooks/              # EDA y visualizaciones
├── scripts/                # Funciones y modelos
├── results/                # Resultados finales
└── README.md               # Este documento
```

---

## 👥 Autores

| Rol            | Integrante                                            |
| -------------- | ----------------------------------------------------- |
| Líder de grupo | Julio Cesar Alvarez                                   |
| Miembros       | Moisés Espinal, Dennis Campos                         |
| Curso          | Sistemas de Inteligencia de Negocio                   |
| Universidad    | Facultad de Ingeniería Industrial y de Sistemas – UNI |

