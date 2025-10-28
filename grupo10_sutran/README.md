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
