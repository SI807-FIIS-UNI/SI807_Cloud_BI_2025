@echo off
SETLOCAL

echo ============================================
echo   EJECUCION AUTOMATICA - EXAMEN FINAL SI807
echo ============================================
echo.

REM --------------------------------------------
REM 1. Crear entorno virtual si no existe
REM --------------------------------------------
IF NOT EXIST ".venv" (
    echo [INFO] Creando entorno virtual .venv
    python -m venv .venv
    IF ERRORLEVEL 1 GOTO ERROR
) ELSE (
    echo [INFO] Entorno virtual .venv ya existe
)

REM --------------------------------------------
REM 2. Activar entorno virtual
REM --------------------------------------------
echo [INFO] Activando entorno virtual
call .venv\Scripts\activate.bat
IF ERRORLEVEL 1 GOTO ERROR

REM --------------------------------------------
REM 3. Actualizar pip
REM --------------------------------------------
echo [INFO] Actualizando pip
python -m pip install --upgrade pip
IF ERRORLEVEL 1 GOTO ERROR

REM --------------------------------------------
REM 4. Instalar dependencias
REM --------------------------------------------
echo [INFO] Instalando dependencias
pip install -r requirements.txt
IF ERRORLEVEL 1 GOTO ERROR

REM --------------------------------------------
REM 5. Ejecutar procesos BI
REM --------------------------------------------
echo.
echo [1/5] Ingesta de datos - BRONCE
python scripts\01_ingesta_bronce.py
IF ERRORLEVEL 1 GOTO ERROR

echo.
echo [2/5] Analisis exploratorio - EDA
python scripts\02_eda_exploratorio.py
IF ERRORLEVEL 1 GOTO ERROR

echo.
echo [3/5] Transformacion y modelo dimensional - PLATA
python scripts\03_transformacion_plata.py
IF ERRORLEVEL 1 GOTO ERROR

echo.
echo [4/5] Generacion de KPIs - ORO
python scripts\04_kpis_oro.py
IF ERRORLEVEL 1 GOTO ERROR

echo.
echo [5/5] Generacion de dashboards
python scripts\05_visualizacion.py
IF ERRORLEVEL 1 GOTO ERROR

echo.
echo ============================================
echo  PROCESO COMPLETADO EXITOSAMENTE
echo ============================================
echo.
pause
exit /b 0

:ERROR
echo.
echo ============================================
echo  ERROR EN LA EJECUCION DEL PROCESO
echo ============================================
echo Revisar logs y dependencias
echo.
pause
exit /b 1
