# 📁 Examen Final – Lógica de Evidencias y Entregables

Este repositorio contiene las evidencias solicitadas para el **Examen Final**.

## 📂 Estructura del repositorio

```
PC3/
│
├── 1_Ingestión y Estructuración – BRONCE/
│   ├── bronce/
│   │   ├── raw/              # CSV originales cargados mediante CLI
│   │   ├── processed/        # datos con limpieza básica (tipos, nulos, formatos)
│   │   └── curated/          # datos validados y listos para transformación
│   │
│   └── scripts/
│       ├── upload_cli.sh     # comandos CLI utilizados para la carga de datos
│       └── eda_minimo.py     # análisis exploratorio mínimo (EDA)
│
├── 2_Transformación y Modelo Dimensional – PLATA y ORO/
│   ├── plata/
│   │   ├── dimensions/       # tablas dimensión (modelo estrella)
│   │   ├── facts/            # tablas de hechos
│   │   └── scripts/
│   └── oro/
│       ├── kpis/             # KPIs finales para consumo analítico
│       └── scripts/       
│   
├── 3_Visualización de KPIs – Dashboards/
│   ├── dashboards/
│   └── scripts/
│
├── docs/                     # Evidencias globales del proyecto
│   ├── cli_ingestion/        # capturas de carga por CLI
│   ├── eda/                  # resultados del EDA
│   ├── modelo_estrella/      # diagrama y justificación del modelo
│   ├── etl_logs/             # logs de ejecución (plata y oro)
│   └── dashboards/           # capturas y justificación de visualizaciones
│
└── README.md
```
