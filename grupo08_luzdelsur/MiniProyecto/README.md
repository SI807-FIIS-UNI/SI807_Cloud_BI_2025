# Proyecto de Análisis de Datos de Ventas

Análisis Exploratorio de Datos (EDA) completo de transacciones de ventas con segmentación de clientes, análisis de desempeño de productos e insights de negocio.

## Estructura del Proyecto

```
MiniProyecto/
├── data/
│   ├── raw/                    # Datos originales sin procesar
│   │   └── sales_data_sample.csv
│   └── processed/              # Datos limpios y procesados
│       └── sales_data_clean.csv
├── notebooks/
│   ├── 01_data_cleaning_improved.ipynb      # Limpieza y preprocesamiento
│   ├── 02_eda_complete.ipynb                # Análisis Exploratorio
│   └── 03_insights_business.ipynb           # Insights y recomendaciones
├── results/                    # Visualizaciones y resultados del análisis
├── scripts/
│   ├── setup_environment.sh    # Configuración del entorno (Linux/Mac)
│   ├── setup_environment.bat   # Configuración del entorno (Windows)
│   ├── run_analysis.sh         # Ejecutar pipeline completo (Linux/Mac)
│   └── run_analysis.bat        # Ejecutar pipeline completo (Windows)
└── requirements.txt            # Dependencias de Python
```

## Requisitos

- Python 3.7 o superior
- Gestor de paquetes pip
- Soporte para entorno virtual

## Instalación

### Windows

1. Abrir PowerShell en el directorio del proyecto
2. Ejecutar el script de configuración:
```powershell
.\scripts\setup_environment.bat
```

### Linux/Mac

1. Abrir terminal en el directorio del proyecto
2. Hacer los scripts ejecutables:
```bash
chmod +x scripts/*.sh
```
3. Ejecutar el script de configuración:
```bash
bash scripts/setup_environment.sh
```

Esto realizará:
- Crear un entorno virtual
- Instalar todos los paquetes Python requeridos
- Preparar el proyecto para ejecución

## Uso

### Inicio Rápido - Pipeline Automatizado

**Windows:**
```powershell
.\scripts\run_analysis.bat
```

**Linux/Mac:**
```bash
bash scripts/run_analysis.sh
```

Esto ejecuta todos los notebooks en secuencia y genera todas las salidas.

### Ejecución Manual

1. Activar el entorno virtual:

**Windows:**
```powershell
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

2. Lanzar Jupyter:
```bash
jupyter notebook
```

3. Ejecutar notebooks en orden:
   - `01_data_cleaning_improved.ipynb` - Limpieza de datos
   - `02_eda_complete.ipynb` - Análisis exploratorio
   - `03_insights_business.ipynb` - Insights de negocio

## Componentes del Análisis

### 1. Limpieza de Datos (Notebook 01)
- Análisis y tratamiento de valores nulos
- Conversiones de tipos de datos
- Detección de outliers
- Eliminación de duplicados
- Validación de integridad
- Ingeniería de características

### 2. Análisis Exploratorio de Datos (Notebook 02)
- Análisis univariado (distribuciones)
- Análisis bivariado (relaciones)
- Análisis multivariado (correlaciones)
- Análisis de series temporales
- Análisis geográfico
- Análisis de clientes y productos

### 3. Insights de Negocio (Notebook 03)
- Segmentación de clientes (análisis RFM)
- Clustering K-means
- Métricas de desempeño de productos
- Análisis de patrones estacionales
- Desempeño geográfico
- Recomendaciones estratégicas

## Archivos de Salida

Después de ejecutar el análisis, se generan las siguientes salidas:

**Datos Procesados:**
- `data/processed/sales_data_clean.csv` - Dataset limpio

**Visualizaciones (PNG):**
- Gráficos de distribución
- Tendencias de ventas
- Gráficos de segmentación de clientes
- Gráficos de desempeño de productos
- Mapas de análisis geográfico
- Mapas de calor de correlaciones

**Resultados de Análisis (CSV):**
- `results/customer_rfm_analysis.csv` - Scores RFM
- `results/product_performance.csv` - Métricas de productos
- `results/geographic_analysis.csv` - Desempeño regional
- `results/summary_statistics.csv` - Estadísticas generales

**Insights:**
- `results/business_insights.txt` - Hallazgos clave y recomendaciones

## Características Principales

- **Análisis Reproducible**: Scripts automatizados aseguran resultados consistentes
- **Código Limpio**: Estructura modular bien documentada
- **Visualizaciones Profesionales**: Gráficos de alta calidad
- **Insights Accionables**: Recomendaciones basadas en datos
- **Escalable**: Fácil de adaptar para diferentes datasets

## Dependencias

Principales librerías utilizadas:
- pandas: Manipulación de datos
- numpy: Operaciones numéricas
- matplotlib: Gráficos
- seaborn: Visualizaciones estadísticas
- plotly: Gráficos interactivos
- scikit-learn: Machine learning (clustering)
- scipy: Análisis estadístico

Ver `requirements.txt` para la lista completa con versiones.

## Solución de Problemas

**Problemas con entorno virtual:**
- Asegurar que Python 3.7+ esté instalado
- Eliminar carpeta `venv` y ejecutar setup nuevamente

**Jupyter no encontrado:**
- Activar primero el entorno virtual
- Reinstalar: `pip install jupyter notebook`

**Errores de datos faltantes:**
- Asegurar que `data/raw/sales_data_sample.csv` exista
- Verificar encoding del archivo (debe ser latin1 o utf-8)

**Errores de permisos (Linux/Mac):**
- Hacer scripts ejecutables: `chmod +x scripts/*.sh`

## Notas

- Scripts (.sh) son para entornos Linux/Mac
- Archivos batch (.bat) son para Windows
- Todos los notebooks incluyen documentación en markdown
- Resultados se guardan automáticamente en directorio `results/`
- Notebooks ejecutados se guardan con sufijo `_executed`

## Contribuir

Al agregar nuevo análisis:
1. Crear nuevo notebook en directorio `notebooks/`
2. Actualizar este README con descripción del notebook
3. Agregar nuevas dependencias a `requirements.txt`
4. Documentar outputs en `results/readme.md`

## Licencia

Este proyecto es para propósitos educativos como parte del curso SI807 a cargo del profesor Hilario y el ayudante de cátedra García Atuncar