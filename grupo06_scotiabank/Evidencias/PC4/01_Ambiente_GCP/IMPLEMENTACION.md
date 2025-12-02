# Guía Paso a Paso - Implementación desde Cero
## Dashboard KPIs de Riesgo - Scotiabank (Grupo 6)

Esta guía asume que **no tienes conocimientos previos de GCP**. Sigue cada paso en orden.

---

## Pre-requisitos

### 1. Instalar Google Cloud SDK (gcloud CLI)

**En Windows:**
```powershell
# Descargar e instalar desde:
# https://cloud.google.com/sdk/docs/install

# Verificar instalación
gcloud --version
```

**En macOS/Linux:**
```bash
# Descargar instalador
curl https://sdk.cloud.google.com | bash

# Reiniciar terminal y verificar
gcloud --version
```

### 2. Autenticarse en GCP

```bash
# Iniciar sesión con tu cuenta de Google
gcloud auth login

# Esto abrirá tu navegador para autenticación
# Sigue los pasos en el navegador
```

### 3. Configurar tu proyecto

```bash
# Listar proyectos disponibles
gcloud projects list

# Configurar proyecto por defecto
gcloud config set project grupo6-scotiabank

# Verificar configuración
gcloud config list
```

---

## Fase 1: Configuración Básica (15 minutos)

### Paso 1.1: Habilitar APIs necesarias

```bash
# Habilitar todas las APIs de una vez
gcloud services enable \
    storage.googleapis.com \
    dataproc.googleapis.com \
    bigquery.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudscheduler.googleapis.com \
    monitoring.googleapis.com \
    logging.googleapis.com

# Esperar 2-3 minutos para que se activen
# Verificar que estén habilitadas
gcloud services list --enabled
```

### Paso 1.2: Configurar región por defecto

```bash
# Establecer región principal
gcloud config set compute/region southamerica-east1
gcloud config set compute/zone southamerica-east1-b

# Verificar
gcloud config get compute/region
```

---

## Fase 2: Cloud Storage con Alta Disponibilidad (10 minutos)

### Paso 2.1: Crear bucket principal

```bash
# Definir nombre del bucket (debe ser único globalmente)
BUCKET_NAME="grupo6-scotiabank-sbs-data"

# Crear bucket en región principal
gsutil mb -p grupo6-scotiabank \
    -c STANDARD \
    -l southamerica-east1 \
    gs://$BUCKET_NAME/

# Verificar creación
gsutil ls
```

### Paso 2.2: Habilitar versionamiento (DR)

```bash
# Habilitar versionamiento para recuperación
gsutil versioning set on gs://$BUCKET_NAME/

# Verificar
gsutil versioning get gs://$BUCKET_NAME/
# Debe mostrar: Enabled
```

### Paso 2.3: Configurar lifecycle policy

```bash
# Crear archivo de configuración temporal
cat > /tmp/lifecycle.json <<'EOF'
{
  "lifecycle": {
    "rule": [
      {
        "action": {
          "type": "SetStorageClass",
          "storageClass": "NEARLINE"
        },
        "condition": {
          "age": 90,
          "matchesPrefix": ["bronze/"]
        }
      },
      {
        "action": {
          "type": "Delete"
        },
        "condition": {
          "numNewerVersions": 3,
          "isLive": false
        }
      }
    ]
  }
}
EOF

# Aplicar política
gsutil lifecycle set /tmp/lifecycle.json gs://$BUCKET_NAME/

# Verificar
gsutil lifecycle get gs://$BUCKET_NAME/
```

### Paso 2.4: Crear estructura de carpetas

```bash
# Crear estructura medallion
echo "Bronze layer - datos crudos SBS" | gsutil cp - gs://$BUCKET_NAME/bronze/.keep
echo "Silver layer - datos transformados" | gsutil cp - gs://$BUCKET_NAME/silver/.keep
echo "Gold layer - KPIs para Power BI" | gsutil cp - gs://$BUCKET_NAME/gold/.keep
echo "Scripts de procesamiento" | gsutil cp - gs://$BUCKET_NAME/scripts/.keep

# Verificar estructura
gsutil ls -r gs://$BUCKET_NAME/
```

### Paso 2.5: Probar versionamiento

```bash
# Crear archivo de prueba
echo "Versión 1" > /tmp/test.txt
gsutil cp /tmp/test.txt gs://$BUCKET_NAME/bronze/test.txt

# Modificar y subir nueva versión
echo "Versión 2" > /tmp/test.txt
gsutil cp /tmp/test.txt gs://$BUCKET_NAME/bronze/test.txt

# Ver versiones
gsutil ls -la gs://$BUCKET_NAME/bronze/test.txt

# Restaurar versión anterior (copiar el número de generación #xxxxx)
gsutil cp gs://$BUCKET_NAME/bronze/test.txt#[NUMERO_GENERACION] \
           gs://$BUCKET_NAME/bronze/test_restored.txt
```

**✅ Checkpoint:** Deberías tener un bucket con versionamiento y estructura de carpetas.

---

## Fase 3: Dataproc con Autoscaling (20 minutos)

### Paso 3.1: Crear política de autoscaling

```bash
# Crear archivo de configuración
cat > /tmp/autoscaling-policy.yaml <<'EOF'
workerConfig:
  minInstances: 2
  maxInstances: 8
  weight: 1
secondaryWorkerConfig:
  minInstances: 0
  maxInstances: 4
  weight: 1
basicAlgorithm:
  cooldownPeriod: 2m
  yarnConfig:
    scaleUpFactor: 0.5
    scaleDownFactor: 1.0
    scaleUpMinWorkerFraction: 0.0
    scaleDownMinWorkerFraction: 0.0
    gracefulDecommissionTimeout: 1m
EOF

# Crear política en GCP
gcloud dataproc autoscaling-policies import sbs-autoscaling-policy \
    --source=/tmp/autoscaling-policy.yaml \
    --region=southamerica-east1

# Verificar creación
gcloud dataproc autoscaling-policies describe sbs-autoscaling-policy \
    --region=southamerica-east1
```

### Paso 3.2: Crear cluster efímero de prueba

```bash
# Crear cluster con autoscaling (se auto-destruye en 30 min)
gcloud dataproc clusters create sbs-test-cluster \
    --region=southamerica-east1 \
    --zone=southamerica-east1-b \
    --master-machine-type=n1-standard-4 \
    --master-boot-disk-size=50GB \
    --num-workers=2 \
    --worker-machine-type=n1-standard-4 \
    --worker-boot-disk-size=50GB \
    --image-version=2.1-debian11 \
    --autoscaling-policy=sbs-autoscaling-policy \
    --max-idle=1800s \
    --enable-component-gateway \
    --bucket=grupo6-scotiabank-sbs-data \
    --properties=spark:spark.executor.memory=3g \
    --labels=env=test,type=ephemeral

# Esto tomará 3-5 minutos...
# Observar el progreso en la consola
```

### Paso 3.3: Verificar autoscaling

```bash
# Ver detalles del cluster
gcloud dataproc clusters describe sbs-test-cluster \
    --region=southamerica-east1

# Abrir UI de monitoreo (opcional)
# Ir a: console.cloud.google.com/dataproc/clusters
```

### Paso 3.4: Crear job de prueba

```bash
# Crear script de Spark simple
cat > /tmp/test_job.py <<'EOF'
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Test Autoscaling").getOrCreate()

# Generar datos de prueba
data = [(i, f"Registro {i}") for i in range(1000000)]
df = spark.createDataFrame(data, ["id", "descripcion"])

# Simular carga para probar autoscaling
df_aggregated = df.groupBy("id").count()
df_aggregated.show(10)

print(f"Total registros procesados: {df_aggregated.count()}")
spark.stop()
EOF

# Subir script a GCS
gsutil cp /tmp/test_job.py gs://grupo6-scotiabank-sbs-data/scripts/

# Ejecutar job
gcloud dataproc jobs submit pyspark \
    --cluster=sbs-test-cluster \
    --region=southamerica-east1 \
    gs://grupo6-scotiabank-sbs-data/scripts/test_job.py

# Observar logs en tiempo real
```

### Paso 3.5: Eliminar cluster de prueba

```bash
# Eliminar cluster (importante para ahorrar costos)
gcloud dataproc clusters delete sbs-test-cluster \
    --region=southamerica-east1 \
    --quiet

# O esperar 30 minutos para auto-eliminación
```

**✅ Checkpoint:** Has probado autoscaling en Dataproc.

---

## Fase 4: BigQuery con Disaster Recovery (15 minutos)

### Paso 4.1: Crear datasets en región principal

```bash
# Dataset Bronze
bq mk --dataset \
    --location=southamerica-east1 \
    --description="Bronze layer - Datos crudos de SBS" \
    --label=layer:bronze \
    --label=project:scotiabank \
    grupo6-scotiabank:bronze_sbs

# Dataset Silver
bq mk --dataset \
    --location=southamerica-east1 \
    --description="Silver layer - Datos transformados" \
    --label=layer:silver \
    --label=project:scotiabank \
    grupo6-scotiabank:silver_sbs

# Dataset Gold
bq mk --dataset \
    --location=southamerica-east1 \
    --description="Gold layer - KPIs para Power BI" \
    --label=layer:gold \
    --label=project:scotiabank \
    grupo6-scotiabank:gold_sbs

# Verificar creación
bq ls grupo6-scotiabank:
```

### Paso 4.2: Crear datasets de backup en región DR

```bash
# Backup en us-east1 (Carolina del Sur)
bq mk --dataset \
    --location=us-east1 \
    --description="DR Backup - Bronze" \
    --label=type:backup \
    grupo6-scotiabank:bronze_sbs_backup

bq mk --dataset \
    --location=us-east1 \
    --description="DR Backup - Silver" \
    --label=type:backup \
    grupo6-scotiabank:silver_sbs_backup

bq mk --dataset \
    --location=us-east1 \
    --description="DR Backup - Gold" \
    --label=type:backup \
    grupo6-scotiabank:gold_sbs_backup

# Verificar
bq ls --project_id=grupo6-scotiabank
```

### Paso 4.3: Crear tabla de prueba

```bash
# Crear tabla de ejemplo en Gold
bq mk --table \
    grupo6-scotiabank:gold_sbs.kpis_riesgo \
    fecha:DATE,entidad:STRING,ratio_morosidad:FLOAT64,provision_requerida:FLOAT64

# Insertar datos de prueba
cat > /tmp/sample_data.json <<'EOF'
{"fecha": "2024-01-01", "entidad": "Scotiabank", "ratio_morosidad": 3.2, "provision_requerida": 450000}
{"fecha": "2024-01-01", "entidad": "BCP", "ratio_morosidad": 2.8, "provision_requerida": 380000}
{"fecha": "2024-01-01", "entidad": "Interbank", "ratio_morosidad": 3.5, "provision_requerida": 520000}
EOF

bq load --source_format=NEWLINE_DELIMITED_JSON \
    grupo6-scotiabank:gold_sbs.kpis_riesgo \
    /tmp/sample_data.json

# Verificar datos
bq query --use_legacy_sql=false \
'SELECT * FROM `grupo6-scotiabank.gold_sbs.kpis_riesgo`'
```

### Paso 4.4: Probar backup manual

```bash
# Copiar tabla a región de backup
bq cp -f \
    grupo6-scotiabank:gold_sbs.kpis_riesgo \
    grupo6-scotiabank:gold_sbs_backup.kpis_riesgo_20240101

# Verificar backup
bq query --use_legacy_sql=false \
'SELECT * FROM `grupo6-scotiabank.gold_sbs_backup.kpis_riesgo_20240101`'
```

### Paso 4.5: Crear script de backup automático

```bash
# Crear script reutilizable
cat > ~/bigquery_backup.sh <<'EOF'
#!/bin/bash
# Backup automático de BigQuery

PROJECT_ID="grupo6-scotiabank"
DATE=$(date +%Y%m%d)

echo "🔄 Iniciando backup de BigQuery - $DATE"

# Función para respaldar dataset
backup_dataset() {
    SOURCE=$1
    TARGET=$2
    
    echo "📦 Respaldando $SOURCE → $TARGET"
    
    TABLES=$(bq ls -n 1000 ${PROJECT_ID}:${SOURCE} | grep TABLE | awk '{print $1}')
    
    for TABLE in $TABLES; do
        echo "  ✓ $TABLE"
        bq cp -f \
            ${PROJECT_ID}:${SOURCE}.${TABLE} \
            ${PROJECT_ID}:${TARGET}.${TABLE}_${DATE}
    done
}

# Ejecutar backups
backup_dataset "bronze_sbs" "bronze_sbs_backup"
backup_dataset "silver_sbs" "silver_sbs_backup"
backup_dataset "gold_sbs" "gold_sbs_backup"

echo "✅ Backup completado"
EOF

chmod +x ~/bigquery_backup.sh

# Ejecutar prueba
~/bigquery_backup.sh
```

**✅ Checkpoint:** Tienes datasets con backup en región DR.

---

## Fase 5: Monitoreo y Alertas (10 minutos)

### Paso 5.1: Crear dashboard de monitoreo

```bash
# Ir a Cloud Console
echo "Abre: https://console.cloud.google.com/monitoring"
echo ""
echo "Crear dashboard manual:"
echo "1. Monitoring > Dashboards > Create Dashboard"
echo "2. Agregar gráficas:"
echo "   - Cloud Storage: Bytes almacenados"
echo "   - Dataproc: Número de workers activos"
echo "   - BigQuery: Bytes escaneados"
echo "   - Cloud Functions: Invocaciones y errores"
```

### Paso 5.2: Ver logs en tiempo real

```bash
# Ver logs de Cloud Storage
gcloud logging read "resource.type=gcs_bucket" \
    --limit=10 \
    --format=json

# Ver logs de Dataproc (cuando hay cluster activo)
gcloud logging read "resource.type=cloud_dataproc_cluster" \
    --limit=10

# Ver logs de BigQuery
gcloud logging read "resource.type=bigquery_resource" \
    --limit=10
```

### Paso 5.3: Configurar alertas básicas

```bash
# Ver métricas de uso
gcloud monitoring metrics-descriptors list \
    --filter="metric.type:storage" \
    --limit=5

# Alerta para Cloud Storage (si se acerca a límite)
# Esto se hace mejor desde la consola web:
echo "Configurar desde: https://console.cloud.google.com/monitoring/alerting"
```

---

## Fase 6: Prueba End-to-End (30 minutos)

### Flujo completo de medallion architecture

#### Paso 6.1: Simular descarga de SBS

```bash
# Crear archivo CSV de ejemplo (simulando datos de SBS)
cat > /tmp/sbs_data_202401.csv <<'EOF'
ruc,entidad,ratio_capital,activos_totales,patrimonio,utilidad_neta
20100030595,Banco de Crédito del Perú,14.5,150000000000,18500000000,2500000000
20100123321,Scotiabank Perú,13.2,95000000000,12000000000,1800000000
20100047218,Interbank,15.1,78000000000,11500000000,1500000000
20382036655,BBVA Continental,14.8,88000000000,13000000000,1900000000
EOF

# Subir a Bronze (simula Cloud Function)
gsutil cp /tmp/sbs_data_202401.csv \
    gs://grupo6-scotiabank-sbs-data/bronze/sbs_data_202401.csv

# Verificar
gsutil ls -lh gs://grupo6-scotiabank-sbs-data/bronze/
```

#### Paso 6.2: Procesar Bronze → Silver (Dataproc)

```bash
# Crear script de transformación Spark
cat > /tmp/bronze_to_silver.py <<'EOF'
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round

spark = SparkSession.builder.appName("Bronze to Silver").getOrCreate()

# Leer Bronze
df_bronze = spark.read.csv(
    "gs://grupo6-scotiabank-sbs-data/bronze/sbs_data_202401.csv",
    header=True,
    inferSchema=True
)

# Transformaciones (limpiar, validar)
df_silver = df_bronze \
    .filter(col("ratio_capital") > 10) \
    .withColumn("ratio_morosidad", spark_round((col("activos_totales") * 0.03) / col("patrimonio"), 2)) \
    .select("ruc", "entidad", "ratio_capital", "ratio_morosidad", "utilidad_neta")

# Guardar en Silver
df_silver.write.mode("overwrite").parquet(
    "gs://grupo6-scotiabank-sbs-data/silver/datos_transformados_202401"
)

print(f"✓ Procesados {df_silver.count()} registros Bronze → Silver")
spark.stop()
EOF

# Subir script
gsutil cp /tmp/bronze_to_silver.py \
    gs://grupo6-scotiabank-sbs-data/scripts/

# Crear cluster efímero y ejecutar
gcloud dataproc clusters create sbs-etl-$(date +%H%M%S) \
    --region=southamerica-east1 \
    --zone=southamerica-east1-b \
    --master-machine-type=n1-standard-4 \
    --num-workers=2 \
    --worker-machine-type=n1-standard-4 \
    --image-version=2.1-debian11 \
    --autoscaling-policy=sbs-autoscaling-policy \
    --max-idle=600s \
    --bucket=grupo6-scotiabank-sbs-data

# Esperar a que cluster esté RUNNING (2-3 min)

# Ejecutar job (reemplaza CLUSTER_NAME con el nombre real)
CLUSTER_NAME="sbs-etl-XXXXXX"  # Usar el nombre del cluster creado

gcloud dataproc jobs submit pyspark \
    --cluster=$CLUSTER_NAME \
    --region=southamerica-east1 \
    gs://grupo6-scotiabank-sbs-data/scripts/bronze_to_silver.py
```

#### Paso 6.3: Cargar Silver → Gold (BigQuery)

```bash
# Cargar Parquet de Silver a BigQuery
bq load --source_format=PARQUET \
    --replace \
    grupo6-scotiabank:silver_sbs.datos_transformados \
    gs://grupo6-scotiabank-sbs-data/silver/datos_transformados_202401/*.parquet

# Verificar datos en Silver
bq query --use_legacy_sql=false \
'SELECT * FROM `grupo6-scotiabank.silver_sbs.datos_transformados`'

# Crear tabla agregada Gold (KPIs)
bq query --use_legacy_sql=false --destination_table=grupo6-scotiabank:gold_sbs.kpis_riesgo_202401 \
'
SELECT 
  DATE("2024-01-01") as fecha,
  entidad,
  ratio_capital,
  ratio_morosidad,
  utilidad_neta,
  CASE 
    WHEN ratio_morosidad > 5 THEN "ALTO"
    WHEN ratio_morosidad > 3 THEN "MEDIO"
    ELSE "BAJO"
  END as nivel_riesgo
FROM `grupo6-scotiabank.silver_sbs.datos_transformados`
ORDER BY ratio_morosidad DESC
'

# Ver resultado final
bq query --use_legacy_sql=false \
'SELECT * FROM `grupo6-scotiabank.gold_sbs.kpis_riesgo_202401`'
```

#### Paso 6.4: Conectar Power BI (simulado)

```bash
# Obtener credenciales para Power BI
echo "=== Configuración para Power BI ==="
echo ""
echo "1. Abrir Power BI Desktop"
echo "2. Get Data > More > BigQuery"
echo "3. Ingresar:"
echo "   Project: grupo6-scotiabank"
echo "   Dataset: gold_sbs"
echo "   Table: kpis_riesgo_202401"
echo ""
echo "4. Autenticarse con tu cuenta de Google"
echo "5. Crear visualizaciones con los KPIs"
```

#### Paso 6.5: Ejecutar backup

```bash
# Backup de todas las capas
~/bigquery_backup.sh

# Verificar backups
bq ls grupo6-scotiabank:gold_sbs_backup
```

**✅ Checkpoint Final:** Has completado un flujo end-to-end completo.

---

## Fase 7: Limpieza y Optimización de Costos

### Eliminar recursos de prueba

```bash
# Listar clusters activos (deben estar auto-eliminados)
gcloud dataproc clusters list --region=southamerica-east1

# Si quedan clusters, eliminarlos
gcloud dataproc clusters delete [CLUSTER_NAME] \
    --region=southamerica-east1 \
    --quiet

# Ver uso de storage
gsutil du -sh gs://grupo6-scotiabank-sbs-data/

# Opcional: Limpiar archivos de prueba
gsutil rm gs://grupo6-scotiabank-sbs-data/bronze/test.txt
```

### Verificar costos

```bash
# Ver estimación de costos en consola
echo "Revisar costos en:"
echo "https://console.cloud.google.com/billing"
echo ""
echo "Costos esperados con tu configuración:"
echo "  - Cloud Storage: $0.05/mes"
echo "  - BigQuery: $0.10/mes"
echo "  - Dataproc: $0 (solo cuando se usa)"
echo "  - Total: ~$0.15/mes"
```

---

## Resumen de Comandos Frecuentes

```bash
# Ver configuración actual
gcloud config list

# Ver todos los buckets
gsutil ls

# Ver todos los datasets de BigQuery
bq ls

# Ver clusters de Dataproc activos
gcloud dataproc clusters list --region=southamerica-east1

# Ver logs recientes
gcloud logging read --limit=20

# Ejecutar backup manual
~/bigquery_backup.sh
```

---

## Troubleshooting

### Error: "Permission denied"
```bash
# Verificar autenticación
gcloud auth list

# Re-autenticar si es necesario
gcloud auth login
```

### Error: "API not enabled"
```bash
# Habilitar API específica
gcloud services enable [API_NAME]

# Ejemplo:
gcloud services enable dataproc.googleapis.com
```

### Error: "Quota exceeded"
```bash
# Ver cuotas
gcloud compute project-info describe --project=grupo6-scotiabank

# Solicitar aumento de cuota desde:
# https://console.cloud.google.com/iam-admin/quotas
```

---

## Próximos Pasos para el Proyecto

1. ✅ Implementar Cloud Function para descarga automática de SBS
2. ✅ Programar ejecución mensual con Cloud Scheduler
3. ✅ Crear scripts de Spark para transformaciones completas
4. ✅ Configurar Power BI con conexión a BigQuery
5. ✅ Documentar arquitectura para el reporte académico
6. ✅ Ejecutar simulacro de Disaster Recovery

---

## Recursos Adicionales

- **Documentación oficial GCP:** https://cloud.google.com/docs
- **Tutoriales Dataproc:** https://cloud.google.com/dataproc/docs/tutorials
- **BigQuery best practices:** https://cloud.google.com/bigquery/docs/best-practices
- **Calculadora de costos:** https://cloud.google.com/products/calculator

---

**¿Necesitas ayuda?** Consulta los logs con `gcloud logging read` o revisa la consola web en https://console.cloud.google.com