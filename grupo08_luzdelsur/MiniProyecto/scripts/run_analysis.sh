#!/bin/bash

# Script automatizado para ejecutar el pipeline completo de análisis
# Este script orquesta la ejecución secuencial de los 3 notebooks principales:
# 1. Limpieza de datos, 2. EDA, 3. Generación de insights de negocio

# set -e: Detiene la ejecución si cualquier comando falla
# Esto garantiza la integridad del pipeline (si falla un paso, no continúa)
set -e

echo "=========================================="
echo "Pipeline de Analisis de Datos de Ventas"
echo "=========================================="

# Verificar que el entorno virtual exista antes de proceder
# Si no existe, ejecuta automáticamente el script de configuración
if [ ! -d "venv" ]; then
    echo "Entorno virtual no encontrado. Ejecutando configuracion..."
    bash scripts/setup_environment.sh
fi

# Activar el entorno virtual para usar las dependencias instaladas
# source ejecuta el script que modifica las variables de entorno del shell
# Esto asegura que se usen las versiones correctas de pandas, jupyter, etc.
echo "Activando entorno virtual..."
source venv/bin/activate

# Crear directorio de resultados si no existe (mkdir -p no falla si ya existe)
# Aquí se guardarán todas las visualizaciones y archivos de salida
mkdir -p results

echo ""
echo "Paso 1/3: Limpieza y Preprocesamiento de Datos"
echo "------------------------------------------"
# jupyter nbconvert ejecuta el notebook programáticamente
# --execute: Ejecuta todas las celdas del notebook en orden
# --to notebook: Guarda la salida como un notebook ejecutado (preserva resultados)
# Esto trata valores faltantes, detecta outliers y genera features
jupyter nbconvert --to notebook --execute \
    --output-dir notebooks \
    --output 01_data_cleaning_improved_executed.ipynb \
    notebooks/01_data_cleaning_improved.ipynb

echo ""
echo "Paso 2/3: Analisis Exploratorio de Datos (EDA)"
echo "------------------------------------------"
# Genera visualizaciones de distribuciones, correlaciones, tendencias temporales
# y análisis geográfico para entender los patrones en los datos limpios
jupyter nbconvert --to notebook --execute \
    --output-dir notebooks \
    --output 02_eda_complete_executed.ipynb \
    notebooks/02_eda_complete.ipynb

echo ""
echo "Paso 3/3: Analisis de Insights de Negocio"
echo "------------------------------------------"
# Ejecuta segmentación RFM, clustering K-means, análisis de productos
# y genera recomendaciones estratégicas accionables
jupyter nbconvert --to notebook --execute \
    --output-dir notebooks \
    --output 03_insights_business_executed.ipynb \
    notebooks/03_insights_business.ipynb

echo ""
echo "=========================================="
echo "Analisis completado exitosamente!"
echo "=========================================="
echo ""
echo "Resultados guardados en:"
echo "  - data/processed/sales_data_clean.csv (datos limpios)"
echo "  - results/*.png (visualizaciones en alta resolucion)"
echo "  - results/*.csv (metricas y segmentaciones exportadas)"
echo "  - results/business_insights.txt (recomendaciones estrategicas)"
echo ""
echo "Revise los notebooks ejecutados en el directorio notebooks/"
