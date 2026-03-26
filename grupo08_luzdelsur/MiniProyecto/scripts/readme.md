# Directorio de Scripts

Este directorio contiene scripts de automatización para configuración del entorno y ejecución del análisis.

## Scripts Disponibles

### Scripts de Configuración

**`setup_environment.sh`** (Linux/Mac)
- Crea entorno virtual de Python
- Instala todas las dependencias desde requirements.txt
- Prepara el proyecto para ejecución
- Verifica compatibilidad de versión de Python

**`setup_environment.bat`** (Windows)
- Equivalente en Windows de setup_environment.sh
- Crea entorno virtual de Python
- Instala todas las dependencias
- Compatible con PowerShell/CMD

**Uso:**
```bash
# Linux/Mac
bash scripts/setup_environment.sh

# Windows
.\scripts\setup_environment.bat
```

---

### Scripts de Ejecución de Análisis

**`run_analysis.sh`** (Linux/Mac)
- Activa entorno virtual
- Ejecuta todos los notebooks en secuencia:
  1. Limpieza de datos
  2. EDA
  3. Insights de negocio
- Genera todas las salidas automáticamente
- Crea directorio de resultados si es necesario

**`run_analysis.bat`** (Windows)
- Equivalente en Windows de run_analysis.sh
- Ejecución automatizada del pipeline
- Genera todas las visualizaciones y reportes

**Uso:**
```bash
# Linux/Mac
bash scripts/run_analysis.sh

# Windows
.\scripts\run_analysis.bat
```

---

## Detalles de los Scripts

### Qué Hacen los Scripts de Configuración

1. Verificar instalación de Python (3.7+ requerido)
2. Mostrar versión de Python
3. Eliminar entorno virtual antiguo si existe
4. Crear nuevo entorno virtual llamado `venv`
5. Activar el entorno
6. Actualizar pip a última versión
7. Instalar todos los paquetes desde requirements.txt
8. Mostrar mensaje de éxito con próximos pasos

### Qué Hacen los Scripts de Análisis

1. Verificar existencia de entorno virtual (ejecutar setup si falta)
2. Activar entorno virtual
3. Crear directorio de resultados si es necesario
4. Ejecutar notebook 01 (limpieza de datos)
5. Ejecutar notebook 02 (EDA)
6. Ejecutar notebook 03 (insights de negocio)
7. Guardar notebooks ejecutados con sufijo `_executed`
8. Mostrar mensaje de completitud con ubicaciones de salida

## Requisitos

**Para scripts .sh (Linux/Mac):**
- Shell Bash
- Python 3.7+
- Permisos de ejecución: `chmod +x scripts/*.sh`

**Para scripts .bat (Windows):**
- Windows 10 o superior
- Python 3.7+ instalado y en PATH
- PowerShell o Command Prompt

## Solución de Problemas

**"Permission denied" (Linux/Mac):**
```bash
chmod +x scripts/setup_environment.sh
chmod +x scripts/run_analysis.sh
```

**"Python not found":**
- Instalar Python 3.7 o superior
- Agregar Python al PATH del sistema
- Verificar: `python --version` o `python3 --version`

**"Fallo en activación de entorno virtual":**
- Verificar módulo venv de Python: `python -m venv --help`
- Reinstalar Python con soporte para venv
- Usar Python del sistema (no conda) para venv

**"Jupyter not found":**
- Activar primero el entorno virtual
- Ejecutar script de setup nuevamente
- Instalación manual: `pip install jupyter notebook`

**Errores de "Module not found":**
- Asegurar que el entorno virtual esté activado
- Reinstalar requisitos: `pip install -r requirements.txt`
- Verificar que requirements.txt exista en la raíz del proyecto

## Notas

- Los scripts usan rutas relativas (ejecutar desde raíz del proyecto)
- El entorno virtual se crea en directorio `venv/`
- Los scripts son idempotentes (seguros para ejecutar múltiples veces)
- Notebooks ejecutados se guardan separadamente (originales sin cambios)
- Todos los scripts incluyen verificación de errores y mensajes de estado

## Personalización

Para modificar el pipeline de análisis:

1. Editar orden de ejecución de notebooks en scripts run_analysis
2. Agregar nuevos notebooks a la secuencia
3. Modificar directorios de salida según necesidad
4. Agregar pasos de pre/post-procesamiento

Ejemplo de adición a run_analysis.sh:
```bash
jupyter nbconvert --to notebook --execute \
    --output-dir notebooks \
    --output 04_analisis_personalizado_executed.ipynb \
    notebooks/04_analisis_personalizado.ipynb
```

## Mejores Prácticas

- Siempre ejecutar script de setup antes de primera ejecución
- Usar run_analysis para resultados reproducibles
- Verificar salida de scripts para errores
- Mantener scripts en control de versiones
- Documentar cualquier personalización
