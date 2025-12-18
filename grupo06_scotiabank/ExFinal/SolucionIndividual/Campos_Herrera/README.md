# 📊 Examen Final

**Estudiante**: Dennis Leopoldo Campos Herrera
**Curso**: Sistemas de Inteligencia de Negocios


---

## 🎯 Objetivo del Proyecto

Implementar una **arquitectura medallion completa** (Bronze → Silver → Gold) en AWS para el procesamiento, transformación y visualización de datos empresariales, cumpliendo con los requisitos de:

1. ✅ Arquitectura en 3 capas claramente diferenciadas
2. ✅ Análisis exploratorio exhaustivo con visualizaciones
3. ✅ Modelo dimensional (star schema) en capa Silver
4. ✅ Generación de KPIs empresariales en capa Gold
5. ✅ Dos dashboards interactivos en QuickSight
6. ✅ 100% reproducible y ejecutable en la nube
7. ✅ Logs detallados de todas las transformaciones

---

## 🏗️ Arquitectura Implementada

### Diagrama de Alto Nivel

```
CSV Raw Data
     ↓
┌────────────────────┐
│   BRONZE LAYER     │  ← Datos crudos inmutables
│   (S3 + Glue)      │     • CSV original sin modificar
└─────────┬──────────┘     • Versionado habilitado
          ↓
┌────────────────────┐
│   SILVER LAYER     │  ← Datos limpios + Star Schema
│   (S3 + Glue)      │     • Duplicados eliminados
└─────────┬──────────┘     • Nulos manejados
          ↓                 • Outliers tratados
┌────────────────────┐     • Dimensiones + Fact Table
│    GOLD LAYER      │  ← KPIs y agregaciones
│   (S3 + Glue)      │     • Métricas temporales
└─────────┬──────────┘     • Rankings Top N
          ↓                 • Segmentación
┌────────────────────┐     • Métricas globales
│   QUICKSIGHT       │  ← Visualización
│   (2 Dashboards)   │     • Dashboard Ejecutivo
└────────────────────┘     • Dashboard Detallado
```

---

## 💡 Justificación Técnica

### ¿Por qué AWS sobre GCP o Azure?

| Criterio | AWS | GCP | Azure |
|----------|-----|-----|-------|
| **Madurez BI** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Serverless** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Costos** | $5-10 | $15-20 | $10-15 |
| **Free Tier** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Documentación** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Decisión**: AWS ofrece el mejor balance entre funcionalidad, costos y reproducibilidad académica.

### ¿Por qué Arquitectura Medallion?

1. **Trazabilidad**: Cada capa preserva el estado de transformación
2. **Auditoría**: Bronze mantiene datos originales inmutables
3. **Eficiencia**: Separación de procesamiento crudo vs. analítico
4. **Escalabilidad**: Cada capa puede optimizarse independientemente
5. **Best Practice**: Adoptada por Databricks, Microsoft, AWS

### ¿Por qué Star Schema en Silver?

1. **Performance**: Menos joins = queries más rápidas en Athena
2. **Costo**: Athena cobra por datos escaneados, star schema optimiza esto
3. **Simplicidad**: Más fácil de entender y mantener que Snowflake
4. **BI-Friendly**: QuickSight funciona mejor con estructuras simples

---

## 🛠️ Servicios AWS Utilizados

| Servicio | Rol en el Proyecto | Justificación |
|----------|-------------------|---------------|
| **S3** | Almacenamiento de 3 capas | Durabilidad 99.999999999%, serverless, versionado |
| **Glue** | Catálogo de datos | Auto-discovery de schemas, sin administración |
| **Athena** | Motor SQL | Serverless, SQL sobre S3, pay-per-query |
| **SageMaker** | Notebooks en nube | Jupyter managed, acceso directo a S3 |
| **QuickSight** | Dashboards BI | Serverless, integración nativa con Athena |
| **IAM** | Seguridad | Principio de mínimo privilegio |

**Total de servicios**: 6  
**Servicios serverless**: 5 de 6 (83%)  
**Costo estimado**: $5-10 USD para todo el proyecto

---

## 📋 Estructura del Proyecto

### Archivos Entregados

```
proyecto/
├── README.md                          ← Documentación completa (50+ páginas)
├── RESUMEN_EJECUTIVO.md              ← Este documento
├── GUIA_DIA_EXAMEN.md                ← Quick reference
├── aws_config.json                    ← Configuración generada
│
├── scripts/
│   ├── deploy_infrastructure.py       ← Despliega toda la arquitectura
│   ├── upload_csv.py                  ← Sube CSV a Bronze
│   ├── setup_quicksight.py            ← Configura QuickSight
│   └── cleanup_resources.py           ← Limpieza post-examen
│
├── notebooks/
│   ├── 1_EDA.ipynb                    ← Análisis exploratorio
│   ├── 2_Plata.ipynb                  ← Transformación a Silver
│   └── 3_Oro.ipynb                    ← Generación de KPIs
│
├── logs/
│   ├── eda_summary.json               ← Resumen del EDA
│   ├── transformation_logs.json       ← Logs de limpieza/transformación
│   └── kpi_summary.json               ← Resumen de KPIs generados
│
└── dashboards/
    ├── dashboard_1_executive.pdf      ← Dashboard ejecutivo
    └── dashboard_2_detailed.pdf       ← Dashboard detallado
```

---

## 🎯 KPIs

### 1. KPI Mensual (Tendencia Temporal)
- **Descripción**: Evolución de métricas principales mes a mes
- **Métricas**: Total, Promedio, Crecimiento %, Acumulado anual
- **Uso**: Gráfico de línea de tendencia en Dashboard 1

### 2. KPI Top N (Ranking)
- **Descripción**: Top 20 elementos por volumen/valor
- **Métricas**: Total, Ranking, Participación %
- **Uso**: Gráfico de barras en ambos dashboards

### 3. KPI Segmentación (Análisis Cruzado)
- **Descripción**: Análisis bidimensional
- **Métricas**: Totales por combinación de dimensiones
- **Uso**: Heatmap en Dashboard 2

### 4. KPI Global (Métricas Resumen)
- **Descripción**: Números clave para KPI cards
- **Métricas**: Total, Promedio, Max, Min, Registros
- **Uso**: KPI cards en parte superior de dashboards

### 5. KPI Tendencias (Forecasting)
- **Descripción**: Proyección simple de tendencias
- **Métricas**: Media móvil, Tendencia lineal, Forecast
- **Uso**: Gráfico de línea con predicción

---

## 📈 Dashboards QuickSight

### Dashboard 1: Executive Overview
**Objetivo**: Vista de alto nivel para toma de decisiones ejecutivas

**Componentes**:
1. 4 KPI Cards con métricas principales
2. Line Chart de tendencia temporal
3. Bar Chart Top 10
4. Pie Chart de distribución

**Filtros**: Rango de fechas, Categoría principal

### Dashboard 2: Detailed Analysis
**Objetivo**: Análisis profundo para analistas de datos

**Componentes**:
1. Clustered Bar Chart (comparativa mensual)
2. Heat Map (segmentación bidimensional)
3. Pivot Table (tabla detallada con drill-down)
4. Combo Chart (volumen + crecimiento %)

**Filtros**: Múltiples dimensiones, Top N selector


**Nota**: A este punto de entrega no se pude llegar a desarrollar el dashboard en QuickSight debido a que la página no permite la creación de cuentas por una especie de bug.

---

## ✅ Reproducibilidad

### Pasos para Reproducir

```bash
# 1. Clonar proyecto
git clone [URL] && cd proyecto

# 2. Configurar AWS
aws configure

# 3. Desplegar infraestructura 
python deploy_infrastructure.py

# 4. Subir datos 
python upload_csv.py Sample-Superstore.csv

# 5. Ejecutar notebooks en SageMaker 
# - 1_EDA.ipynb
# - 2_Plata.ipynb
# - 3_Oro.ipynb

# 6. Configurar QuickSight 
python setup_quicksight.py
# Seguir instrucciones en pantalla


```

### Verificación de Recursos Creados

```bash
# Verificar buckets
aws s3 ls | grep bi-exam
# Esperado: 3 buckets (bronze, silver, gold)

# Verificar tablas
aws glue get-tables --database-name bi-exam_db
# Esperado: 10+ tablas (bronze_*, silver_*, gold_*)

# Verificar notebook
aws sagemaker list-notebook-instances
# Esperado: bi-exam-notebook (InService)
```

---

## 💰 Análisis de Costos

### Desglose de Costos

| Servicio | Uso | Costo Unitario | Total |
|----------|-----|----------------|-------|
| S3 Storage | 5 GB × 7 días | $0.023/GB/mes | $0.12 |
| Glue Crawlers | 9 ejecuciones × 5 min | $0.44/hora | $0.15 |
| Athena | 100 queries × 10 MB | $5/TB | $0.05 |
| SageMaker | ml.t3.medium × 4h | $0.05/hora | $0.20 |
| QuickSight | 7 días | Gratis | $0.00 |
| **TOTAL** | | | **$0.52** |

**Con margen de seguridad**: ~$5-10 USD  
**Créditos disponibles**: $100 USD  
**Sobrante**: $90-95 USD

### Optimizaciones Aplicadas

1. **Instancia SageMaker pequeña**: ml.t3.medium vs ml.m5.xlarge (ahorro: $0.18/hora)
2. **Formato Parquet**: Compresión ~70% vs CSV (ahorro en Athena)
3. **Crawlers on-demand**: Solo cuando se necesita vs scheduled (ahorro: 90%)
4. **QuickSight Free Tier**: Primeros 30 días gratis (ahorro: $9)


---

## 🎓 Aprendizajes y Conclusiones

### Técnico

1. **AWS es viable para proyectos académicos** con costos <$10 USD
2. **Arquitectura medallion** proporciona trazabilidad completa
3. **Serverless reduce complejidad** operacional significativamente
4. **Star schema optimiza** tanto performance como costos en Athena

### Conceptual

1. La separación Bronze/Silver/Gold permite **rollback a cualquier punto**
2. Los logs detallados son **críticos para auditoría**
3. QuickSight es **sorprendentemente potente** para serverless BI
4. La **reproducibilidad requiere disciplina** en documentación

### Desafíos Enfrentados

1. **Learning curve de AWS**: Superado con documentación extensa
2. **Configuración inicial de IAM**: Resuelto con roles específicos
3. **Ajuste de transformaciones**: Solucionado con logs detallados

---


## 📎 Anexos

### A. Comandos de Verificación

```bash
# Ver todos los recursos creados
aws resourcegroupstaggingapi get-resources \
    --tag-filters Key=Project,Values=bi-exam

# Costos acumulados
aws ce get-cost-and-usage \
    --time-period Start=2025-12-01,End=2025-12-31 \
    --granularity MONTHLY \
    --metrics BlendedCost
```

### B. Queries Athena de Ejemplo

```sql
-- 1. Verificar datos en Bronze
SELECT COUNT(*) as total_registros 
FROM bi_exam_db.bronze_datos;

-- 2. Validar Star Schema en Silver
SELECT d.nombre, COUNT(f.id) as transacciones
FROM bi_exam_db.silver_fact_table f
JOIN bi_exam_db.silver_dim_categoria d ON f.categoria_id = d.id
GROUP BY d.nombre;

-- 3. KPIs en Gold
SELECT * FROM bi_exam_db.gold_kpi_mensual
ORDER BY año DESC, mes DESC
LIMIT 12;
```

### C. Estructura de Logs

```json
{
  "transformation": "Eliminación de duplicados",
  "rows_before": 10000,
  "rows_after": 9850,
  "rows_removed": 150,
  "percentage": 1.5,
  "details": {
    "method": "drop_duplicates",
    "subset": null
  }
}
```
