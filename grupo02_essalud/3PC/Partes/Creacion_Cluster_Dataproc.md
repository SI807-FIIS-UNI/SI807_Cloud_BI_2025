# ⚙️ Activación del Dataproc

Para esta parte es necesario haber realizado la [Habilitación Inicial](Habilitacion_Inicial.md).

---

## 1️. Definimos los parámetros a utilizar

Valores utilizados:

- **image-version:** 2.1-debian11  
  Incluye el conector **Spark → BigQuery** sin initialization-actions.
- **n1-standard-8** en workers  
  8 vCPU y 30 GB RAM, ideal para procesar las tablas pesadas.
- **bucket = $BUCKET_TEMP**  
  Dataproc usa este bucket como almacenamiento temporal (staging).

Parámetros que definimos:

```bash
PROJECT=grupo2-essalud
REGION=us-central1
ZONE=us-central1-a
CLUSTER_NAME=cluster-spark-essalud
IMAGE_VERSION=2.1-debian11
BUCKET_TEMP=grupo2-essalud-datalake

gcloud config set project $PROJECT
```

---

## 2️. Creación del cluster de Dataproc

Creamos un clúster con:

- Master: **n1-standard-4**
- Workers: **2 nodos n1-standard-8**
- Bucket temporal: **$BUCKET_TEMP**

Comando ejecutado:

```bash
gcloud dataproc clusters create $CLUSTER_NAME \
  --region=$REGION \
  --zone=$ZONE \
  --image-version=$IMAGE_VERSION \
  --master-machine-type=n1-standard-4 \
  --num-workers=2 \
  --worker-machine-type=n1-standard-8 \
  --bucket=$BUCKET_TEMP \
  --project=$PROJECT
```

---

## 3️. Creación de una política de autoescalabilidad

La autoescalabilidad permite aumentar o reducir nodos según la carga del trabajo.

Parámetros usados:

- Mínimo: **2 workers**
- Máximo: **6 workers**
- Target de CPU: **60%**

Comando ejecutado:

```bash
gcloud dataproc autoscaling-policies create autoscale-essalud \
  --region=$REGION \
  --worker-min-instances=2 \
  --worker-max-instances=6 \
  --worker-cpu-utilization-target=0.6
```

---

## 4️. Aplicamos la política de autoescalabilidad al cluster

```bash
gcloud dataproc clusters update $CLUSTER_NAME \
  --region=$REGION \
  --autoscaling-policy=autoscale-essalud
```

---

## 5️. Eliminación del cluster (solo al terminar todo el proceso)

Es importante borrar el cluster porque **Dataproc cobra por minuto de uso**, incluso cuando el cluster está inactivo.  
Eliminarlo evita costos innecesarios después de terminar el procesamiento.

Comando:

```bash
CLUSTER_NAME=cluster-spark-essalud
gcloud dataproc clusters delete $CLUSTER_NAME --region=$REGION
```

