#!/bin/bash

# Script de configuración para el proyecto de Análisis de Datos de Ventas
# Este script automatiza la creación de un entorno virtual aislado y la instalación
# de todas las dependencias necesarias para ejecutar el pipeline de análisis

# set -e: Detiene la ejecución del script si cualquier comando falla
# Esto garantiza que no se continúe con pasos posteriores si hay errores
set -e

echo "=========================================="
echo "Configurando Entorno de Analisis de Ventas"
echo "=========================================="

# Verificar que Python 3 esté instalado en el sistema
# command -v retorna la ruta del ejecutable si existe, o nada si no está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no esta instalado. Por favor instale Python 3.7 o superior."
    exit 1
fi

echo "Version de Python detectada:"
python3 --version

# Crear un entorno virtual para aislar las dependencias del proyecto
# Esto evita conflictos con otros proyectos Python en el sistema
echo ""
echo "Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "El entorno virtual ya existe. Eliminando version anterior..."
    rm -rf venv
fi

python3 -m venv venv

# Activar el entorno virtual recién creado
# source ejecuta el script de activación que modifica las variables de entorno
# Esto cambia el contexto de Python para usar las librerías del entorno aislado
echo "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip a la última versión para asegurar compatibilidad
# pip es el gestor de paquetes que instalará las dependencias
echo ""
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar todas las dependencias especificadas en requirements.txt
# Incluye pandas, numpy, matplotlib, seaborn, plotly, scikit-learn, etc.
echo ""
echo "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Configuracion completada exitosamente!"
echo "=========================================="
echo ""
echo "Para activar el entorno manualmente, ejecute:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  venv\\Scripts\\activate     (Windows)"
echo ""
echo "Para ejecutar el analisis completo, ejecute:"
echo "  bash scripts/run_analysis.sh"
