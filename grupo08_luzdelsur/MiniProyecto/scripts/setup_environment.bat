@echo off
REM Script de configuración para el proyecto de Análisis de Datos de Ventas (Windows)
REM Este script automatiza la creación de un entorno virtual aislado y la instalación
REM de todas las dependencias necesarias para ejecutar el pipeline de análisis

echo ==========================================
echo Configurando Entorno de Analisis de Ventas
echo ==========================================

REM Verificar que Python esté instalado en el sistema
REM Redirige la salida a nul para evitar mostrar mensajes de error en pantalla
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no esta instalado. Por favor instale Python 3.7 o superior.
    exit /b 1
)

echo Version de Python detectada:
python --version

REM Crear un entorno virtual para aislar las dependencias del proyecto
REM Esto evita conflictos con otros proyectos Python en el sistema
echo.
echo Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe. Eliminando version anterior...
    rmdir /s /q venv
)

python -m venv venv

REM Activar el entorno virtual recién creado
REM Esto cambia el contexto de Python para usar las librerías del entorno aislado
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip a la última versión para asegurar compatibilidad
REM pip es el gestor de paquetes que instalará las dependencias
echo.
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar todas las dependencias especificadas en requirements.txt
REM Incluye pandas, numpy, matplotlib, seaborn, plotly, scikit-learn, etc.
echo.
echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

echo.
echo ==========================================
echo Configuracion completada exitosamente!
echo ==========================================
echo.
echo Para activar el entorno manualmente, ejecute:
echo   venv\Scripts\activate
echo.
echo Para ejecutar el analisis completo, ejecute:
echo   scripts\run_analysis.bat
pause
