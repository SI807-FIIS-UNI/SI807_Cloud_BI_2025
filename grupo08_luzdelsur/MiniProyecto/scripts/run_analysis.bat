@echo off
REM Script automatizado para ejecutar el pipeline completo de análisis (Windows)
REM Este script orquesta la ejecución secuencial de los 3 notebooks principales:
REM 1. Limpieza de datos, 2. EDA, 3. Generación de insights de negocio

echo ==========================================
echo Pipeline de Analisis de Datos de Ventas
echo ==========================================

REM Verificar que el entorno virtual exista antes de proceder
REM Si no existe, ejecuta automáticamente el script de configuración
if not exist venv (
    echo Entorno virtual no encontrado. Ejecutando configuracion...
    call scripts\setup_environment.bat
)

REM Activar el entorno virtual para usar las dependencias instaladas
REM Esto asegura que se usen las versiones correctas de pandas, jupyter, etc.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Crear directorio de resultados si no existe
REM Aquí se guardarán todas las visualizaciones y archivos de salida
if not exist results mkdir results

echo.
echo Paso 1/3: Limpieza y Preprocesamiento de Datos
echo ------------------------------------------
REM jupyter nbconvert ejecuta el notebook programáticamente
REM --execute: Ejecuta todas las celdas del notebook
REM --to notebook: Guarda la salida como un notebook ejecutado
REM Esto trata valores faltantes, detecta outliers y genera features
jupyter nbconvert --to notebook --execute --output-dir notebooks --output 01_data_cleaning_improved_executed.ipynb notebooks\01_data_cleaning_improved.ipynb

echo.
echo Paso 2/3: Analisis Exploratorio de Datos (EDA)
echo ------------------------------------------
REM Genera visualizaciones de distribuciones, correlaciones, tendencias temporales
REM y análisis geográfico para entender los patrones en los datos limpios
jupyter nbconvert --to notebook --execute --output-dir notebooks --output 02_eda_complete_executed.ipynb notebooks\02_eda_complete.ipynb

echo.
echo Paso 3/3: Analisis de Insights de Negocio
echo ------------------------------------------
REM Ejecuta segmentación RFM, clustering K-means, análisis de productos
REM y genera recomendaciones estratégicas accionables
jupyter nbconvert --to notebook --execute --output-dir notebooks --output 03_insights_business_executed.ipynb notebooks\03_insights_business.ipynb

echo.
echo ==========================================
echo Analisis completado exitosamente!
echo ==========================================
echo.
echo Resultados guardados en:
echo   - data\processed\sales_data_clean.csv (datos limpios)
echo   - results\*.png (visualizaciones en alta resolucion)
echo   - results\*.csv (metricas y segmentaciones exportadas)
echo   - results\business_insights.txt (recomendaciones estrategicas)
echo.
echo Revise los notebooks ejecutados en el directorio notebooks\
pause
