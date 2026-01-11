# grupo02_essalud
Proyecto Cloud BI 2025-II

# Integrantes
  - Jhon Carhuas Romero
  - Navhi Andrade Saavedra
  - David Caruzo Cieza

# 🎬 Proyecto Base de Datos Netflix – Ejercicio Colaborativo (SI807U)

Repositorio oficial del curso:  
🔗 [https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025](https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025)

Este proyecto tiene como finalidad desarrollar un análisis exploratorio y visual sobre el **dataset de Netflix Titles**, aplicando buenas prácticas colaborativas con GitHub y una estructura organizada de trabajo.

---

## 📋 1. Prerrequisitos

Antes de iniciar, asegúrate de contar con lo siguiente:

1. Usuario GitHub agregado a la organización **SI807-FIIS-UNI**.  
2. Tener instalado **Git**  
   ```bash
   git --version

# clonar repositorio
git clone https://github.com/SI807-FIIS-UNI/SI807_Cloud_BI_2025.git
cd SI807_Cloud_BI_2025

# Crear una rama personal de trabajo
feature/grupo02-nombre-tarea

# Estructura de carpetas
📦 SI807_Cloud_BI_2025/
 ┣ 📂 data/
 ┃ ┣ 📂 raw/           ← Datos originales sin procesar
 ┃ ┗ 📂 processed/     ← Datos limpios o transformados
 ┣ 📂 notebooks/       ← Análisis exploratorio o visualizaciones
 ┣ 📂 scripts/         ← Funciones y código auxiliar (ETL, limpieza, etc.)
 ┣ 📂 results/         ← Resultados finales y gráficos
 ┣ 📜 README.md        ← Documentación del ejercicio
 ┗ 📜 .gitignore       ← Archivos a excluir

# Flujo de trabajo de los miembros del grupo
git add .
git commit -m "Limpieza de datos Netflix – grupo03"
git push origin feature/grupo03-netflix-limpieza

# Flujo de trabajo del líder de equipo
Revisar y validar los Pull Requests.

Probar notebooks o scripts antes de aprobar.

Usar "Squash and Merge" para mantener el historial limpio.

Eliminar ramas integradas después del merge.

Actualizar main y notificar al grupo para que sincronicen.

# Resolución de conflicto
En caso de conflictos durante el merge:
git fetch origin
git checkout feature/grupo03-netflix-limpieza
git merge origin/main

Edita los archivos con los marcadores:

<<<<<<<
=======
>>>>>>>


Después de resolver manualmente:

git add .
git commit -m "Conflictos resueltos al integrar con main"
git push

# Archivo .gitignore recomendado

Agrega este contenido en el archivo .gitignore:

data/*.parquet
data/*.zip
data/*.gz
data/*.sav
__pycache__/
.ipynb_checkpoints/
.env
*.log

# Dataset sugerido: Netflix Titles

📂 Fuente: Netflix Titles Dataset – Kaggle

Descripción:
Contiene información de películas y series disponibles en Netflix, con columnas como:

show_id

type (Movie / TV Show)

title

director

cast

country

date_added

release_year

rating

duration

listed_in

description

Objetivo del análisis:

Limpiar y transformar los datos (tratamiento de nulos, formato de fechas).

Analizar la distribución de contenidos por país, género y año.

Crear visualizaciones para presentar los resultados.