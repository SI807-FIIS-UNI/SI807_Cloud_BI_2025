# Directorio de Notebooks

Este directorio contiene notebooks de Jupyter para el pipeline de análisis de datos de ventas.

## Orden de Ejecución de Notebooks

Ejecutar los notebooks en la siguiente secuencia para flujo de datos apropiado:

### 1. Limpieza de Datos (`01_data_cleaning_improved.ipynb`)

**Propósito:** Limpiar y preprocesar datos de ventas raw

**Operaciones Clave:**
- Cargar datos raw desde `data/raw/sales_data_sample.csv`
- Analizar valores faltantes por columna
- Manejar valores faltantes inteligentemente (rellenar o eliminar)
- Convertir tipos de datos (fechas, numéricos)
- Detectar y analizar outliers usando método IQR
- Eliminar registros duplicados
- Validar integridad de datos (valores positivos)
- Crear nuevas características (componentes de fecha, métricas de ingresos)
- Exportar datos limpios a `data/processed/sales_data_clean.csv`

**Salida:** Dataset limpio listo para análisis

**Tiempo de ejecución:** ~1-2 minutos

---

### 2. Análisis Exploratorio de Datos (`02_eda_complete.ipynb`)

**Propósito:** Análisis estadístico y visual completo

**Análisis Clave:**
- **Univariado:** Distribución de variables numéricas y categóricas
- **Bivariado:** Ventas por línea de producto, país, territorio, tamaño de negociación
- **Multivariado:** Análisis de correlaciones, tabulaciones cruzadas
- **Series Temporales:** Tendencias mensuales, trimestrales y anuales
- **Análisis de Clientes:** Principales clientes y sus patrones
- **Estado de Órdenes:** Análisis de distribución e impacto

**Salidas:**
- Múltiples visualizaciones PNG en `results/`
- CSV de estadísticas resumen
- Insights estadísticos

**Tiempo de ejecución:** ~2-3 minutos

---

### 3. Insights de Negocio (`03_insights_business.ipynb`)

**Propósito:** Extraer inteligencia de negocio accionable

**Análisis Clave:**
- **Análisis RFM:** Segmentación de clientes (Recencia, Frecuencia, Monetario)
- **Clustering K-Means:** Agrupación no supervisada de clientes
- **Desempeño de Productos:** Ingresos, conteo de órdenes y métricas de eficiencia
- **Patrones Estacionales:** Análisis mensual y por día de la semana
- **Desempeño Geográfico:** Análisis por país y territorio
- **Recomendaciones Estratégicas:** Sugerencias de negocio basadas en datos

**Salidas:**
- Resultados de segmentación de clientes
- Métricas de desempeño de productos
- Documento de insights de negocio
- Gráficos de visualización estratégica

**Tiempo de ejecución:** ~2-3 minutos

---

## Ejecutar los Notebooks

### Ejecución Automatizada

Usar los scripts proporcionados para ejecutar todos los notebooks automáticamente:

**Windows:**
```powershell
.\scripts\run_analysis.bat
```

**Linux/Mac:**
```bash
bash scripts/run_analysis.sh
```

### Ejecución Manual

1. Activar entorno virtual
2. Iniciar Jupyter:
```bash
jupyter notebook
```
3. Abrir y ejecutar notebooks en orden (01 → 02 → 03)
4. Usar "Run All" o ejecutar celdas secuencialmente

## Notas

- Cada notebook es autocontenido con documentación en markdown
- Las visualizaciones se muestran inline y se guardan en `results/`
- Archivos de datos intermedios se guardan en `data/processed/`
- Versiones ejecutadas se guardan con sufijo `_executed`
- Todos los notebooks usan rutas relativas para portabilidad

## Requisitos

- El entorno virtual debe estar activado
- Todas las dependencias de `requirements.txt` instaladas
- El archivo de datos raw debe existir en `data/raw/`

## Solución de Problemas

**El kernel muere durante la ejecución:**
- Reducir tamaño de muestra de datos si la memoria es limitada
- Cerrar otras aplicaciones
- Reiniciar kernel y ejecutar nuevamente

**Errores de importación:**
- Asegurar que el entorno virtual esté activado
- Reinstalar requisitos: `pip install -r requirements.txt`

**Errores de archivo no encontrado:**
- Verificar que se está ejecutando desde el directorio raíz del proyecto
- Verificar que los datos raw existen en `data/raw/`
- Asegurar que los notebooks anteriores se completaron exitosamente

**Visualización no se muestra:**
- Usar comando mágico `%matplotlib inline`
- Actualizar matplotlib: `pip install --upgrade matplotlib`
- Verificar si se está ejecutando en Jupyter (no Python plano)
