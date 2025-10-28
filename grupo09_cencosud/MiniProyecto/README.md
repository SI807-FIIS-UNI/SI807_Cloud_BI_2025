🧠 Ejercicio Colaborativo – Grupo 09 Cencosud

Autor: Larico Cruz, Diego Cesar

📘 Descripción general

Este proyecto forma parte del curso SI807 – Cloud Business Intelligence (FIIS – UNI).
El objetivo del ejercicio es aplicar un flujo de trabajo colaborativo en GitHub y desarrollar un análisis exploratorio de datos (EDA) utilizando Python y Google Colab, dentro del marco del repositorio oficial del curso:

👉 Repositorio oficial – SI807_Cloud_BI_2025

Cada grupo desarrolla su trabajo dentro de una carpeta asignada, siguiendo buenas prácticas de control de versiones, estructura de datos y documentación.

🧩 Estructura del proyecto
grupo09_cencosud/
│
├── data/
│   ├── raw/            → Dataset original (sin procesar)
│   └── processed/      → Dataset limpio y transformado
│
├── notebooks/          → Análisis exploratorio (EDA) en Jupyter o Google Colab
│
├── scripts/            → Funciones auxiliares o código de transformación
│
├── results/            → Tablas, gráficos y outputs finales
│
└── README.md           → Descripción del ejercicio y autores

📊 Dataset utilizado

Nombre: sales_data_sample.csv
Fuente: Kaggle – Sample Sales Data

Descripción:
Dataset con información de ventas de una empresa comercial. Incluye variables como fecha, país, línea de producto, cantidad vendida, precio unitario, estado del pedido y canal de venta.

Uso en este proyecto:
El dataset se utiliza para realizar un Análisis Exploratorio de Datos (EDA) que permita identificar patrones de venta, distribución geográfica, desempeño por producto y correlaciones entre variables numéricas.

🧮 Análisis realizado

El análisis exploratorio se realizó en Google Colab e incluye los siguientes pasos:

Carga del dataset y detección del encoding.

Revisión de estructura, tipos de datos y valores nulos.

Eliminación y/o imputación de valores faltantes.

Generación de estadísticas descriptivas.

Visualización de distribuciones, correlaciones y outliers.

Limpieza del dataset y guardado en data/processed.

Exportación de un resumen (resumen_eda.csv) y conclusiones gráficas en results/.

🧭 Flujo de trabajo (GitHub)

Cada miembro trabaja en una rama individual con el formato:
feature/grupo09-nombre-tarea

Los cambios se suben con commits descriptivos y en pasado.

Se crea un Pull Request (PR) hacia main, asignando al líder como revisor.

El líder del grupo revisa, aprueba y hace el Squash and Merge.

Finalmente, se sincroniza la rama principal (main) con el repositorio local.