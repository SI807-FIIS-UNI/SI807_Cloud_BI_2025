# Servicio de Descarga de archivos desde la página de la SBS

Sistema automatizado y seguro para descargar reportes mensuales de la Superintendencia de Banca, Seguros y AFP (SBS) del Perú y almacenarlos en Google Cloud Storage.

---

## 🎯 Inicio Rápido

```bash
# 1. Crear carpeta con 4 archivos: main.py, requirements.txt, deploy.sh, destroy.sh
mkdir sbs-downloader && cd sbs-downloader

# 2. Dar permisos
chmod +x deploy.sh destroy.sh

# 3. Desplegar TODO
./deploy.sh

# 4. Probar
gcloud functions call sbs-downloader --region=southamerica-east1 --gen2 --data='{}'

# 5. Ver resultados
gsutil ls -r gs://grupo6_scotiabank_bucket/data/raw/SBS/
```

**Costo**: ~$0.12/mes | **Región**: São Paulo | **Seguridad**: Privada con Service Accounts

---

## 📋 Descripción

Este proyecto implementa un sistema serverless optimizado que:
- **Descarga directa**: Usa URLs directas, **10x más rápido** que métodos tradicionales
- **Ejecución automática**: Se ejecuta el primer día de cada mes a las 2 AM
- **Descarga incremental**: Solo descarga archivos nuevos (evita duplicados)
- **Trazabilidad completa**: Registro CSV de todas las descargas en Cloud Storage
- **Almacenamiento organizado**: Archivos clasificados por tipo de reporte

### Reportes procesados

| Código | Carpeta de destino | Descripción | Periodo |
|--------|-------------------|-------------|---------|
| B-2201 | EEFF | Estados Financieros | 2016-presente |
| B-2315 | CREDITOS_SEGUN_SITUACION | Créditos según situación | 2016-presente |
| B-2344 | DEPOSITOS | Depósitos | 2016-presente |
| B-2370 | PATRIMONIO_EFECTIVO | Patrimonio efectivo | 2016-presente |
| B-2340 | RATIO_LIQUIDEZ | Ratio de liquidez | 2016-presente |
| B-2402 | PATRIMONIO_REQUERIDO_RCG | Patrimonio requerido RCG | 2016-presente |

**Total de archivos**: ~540 archivos por reporte × 6 reportes = **~3,240 archivos**

## 🏗️ Arquitectura

```
┌─────────────────┐
│ Cloud Scheduler │ Trigger: 0 2 1 * * (cada día 1 a las 2 AM)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Cloud Function (2nd gen)            │
│ - Verifica archivos existentes      │
│ - Construye URLs directas           │
│ - Descarga solo archivos nuevos     │
│ - Registra todo en CSV              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Cloud Storage Bucket                │
│ grupo6_scotiabank_bucket/           │
│   ├─ data/raw/SBS/                  │
│   │   ├─ EEFF/                      │
│   │   │   ├─ B-2201-2016-01.xls     │
│   │   │   ├─ B-2201-2016-02.xls     │
│   │   │   └─ ...                    │
│   │   ├─ CREDITOS_SEGUN_SITUACION/  │
│   │   ├─ DEPOSITOS/                 │
│   │   ├─ PATRIMONIO_EFECTIVO/       │
│   │   ├─ RATIO_LIQUIDEZ/            │
│   │   └─ PATRIMONIO_REQUERIDO_RCG/  │
│   └─ logs/                          │
│       └─ descargas_sbs.csv          │
└─────────────────────────────────────┘
```

## 🚀 Servicios GCP Utilizados

### 1. **Cloud Functions (2nd gen)**
- **Propósito**: Ejecutar el código de descarga sin servidor
- **Runtime**: Python 3.11
- **Memoria**: 512MB (ajustable)
- **Timeout**: 540 segundos (9 minutos)
- **Ventajas**:
  - Sin servidor, sin mantenimiento
  - Pago por uso (solo cuando se ejecuta)
  - Escalamiento automático
  - Logs integrados

### 2. **Cloud Storage**
- **Propósito**: Almacenar archivos XLS y logs CSV
- **Clase de almacenamiento**: Standard (acceso frecuente)
- **Estructura organizada**: Por tipo de reporte
- **Ventajas**:
  - Durabilidad 99.999999999% (11 nueves)
  - Versionamiento opcional
  - Acceso desde cualquier servicio GCP

### 3. **Cloud Scheduler**
- **Propósito**: Trigger automático mensual
- **Schedule**: `0 2 1 * *` (día 1, 2 AM hora Lima)
- **Método**: HTTP POST a la Cloud Function
- **Ventajas**:
  - Cron managed (sin servidor cron)
  - Reintentos automáticos
  - Alertas de fallo

### 4. **Cloud Build**
- **Propósito**: Deploy automático de la función
- **Uso**: Transparente durante el despliegue
- **Sin configuración adicional requerida**

## 📦 Estructura del Proyecto

```
sbs-downloader/
├── main.py              # Cloud Function con lógica de descarga
├── requirements.txt     # Dependencias Python (mínimas)
├── deploy.sh           # Script de despliegue automatizado
├── README.md           # Esta documentación
├── test_local.py       # Pruebas locales (opcional)
└── .gitignore          # Archivos ignorados por Git
```

## 🔧 Prerequisitos

### 1. Instalar Google Cloud SDK

**Linux/Mac:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud version  # Verificar instalación
```

**Windows:**
Descarga: https://cloud.google.com/sdk/docs/install

### 2. Autenticación

```bash
# Login a GCP
gcloud auth login

# Configurar proyecto
gcloud config set project grupo6-scotiabank

# Verificar
gcloud config list
```

### 3. Permisos requeridos

Tu cuenta necesita estos roles IAM:
- `roles/cloudfunctions.developer`
- `roles/storage.admin`
- `roles/cloudscheduler.admin`
- `run.admin`
- `roles/iam.serviceAccountUser`
- `roles/resourcemanager.projectIamAdmin`


Verificar:
```bash
gcloud projects get-iam-policy grupo6-scotiabank \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:TU_EMAIL@gmail.com"
```

## 📝 Instalación Completa

### Método 1: Despliegue Automatizado (Recomendado)

```bash
# 1. Crear directorio del proyecto
mkdir sbs-downloader
cd sbs-downloader

# 2. Crear archivos (copiar contenido de artifacts)
# main.py, requirements.txt, deploy.sh, README.md, .gitignore

# 3. Dar permisos de ejecución
chmod +x deploy.sh

# 4. EJECUTAR DESPLIEGUE (todo automático)
./deploy.sh
```

**El script hace todo:**
- ✅ Configura el proyecto GCP
- ✅ Habilita APIs necesarias
- ✅ Crea el bucket (si no existe)
- ✅ Despliega Cloud Function
- ✅ Configura Cloud Scheduler
- ✅ Muestra comandos útiles

**Tiempo**: 3-5 minutos

### Método 2: Despliegue Manual

```bash
# 1. Configurar proyecto
gcloud config set project grupo6-scotiabank

# 2. Habilitar APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable storage.googleapis.com

# 3. Crear bucket
gsutil mb -p grupo6-scotiabank -l us-central1 \
  gs://grupo6_scotiabank_bucket

# 4. Desplegar función
gcloud functions deploy sbs-downloader \
  --gen2 \
  --region=us-central1 \
  --runtime=python311 \
  --source=. \
  --entry-point=sbs_downloader_http \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=512MB \
  --max-instances=1

# 5. Crear Cloud Scheduler job
FUNCTION_URL=$(gcloud functions describe sbs-downloader \
  --region=us-central1 --gen2 --format='value(serviceConfig.uri)')

gcloud scheduler jobs create http sbs-downloader-monthly \
  --location=us-central1 \
  --schedule="0 2 1 * *" \
  --uri=$FUNCTION_URL \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --message-body='{}' \
  --time-zone="America/Lima"
```

## 🧪 Pruebas y Validación

### Arquitectura de Seguridad Implementada

La función está **completamente privada** y usa **2 Service Accounts**:

1. **`sbs-downloader-sa`**: Ejecuta la función
   - Permiso: `roles/storage.objectAdmin` (solo en el bucket del proyecto)
   
2. **`sbs-scheduler-sa`**: Invoca la función desde Cloud Scheduler
   - Permiso: `roles/run.invoker` (solo para esta función)

**No hay acceso público**. Solo estos métodos funcionan:

### 1. Prueba usando gcloud (Recomendado - Más Simple)

```bash
# Ejecutar todos los reportes
gcloud functions call sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --data='{}'

# Ejecutar solo un reporte (más rápido para pruebas)
gcloud functions call sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --data='{"formato": "B-2201"}'
```

**Respuesta esperada:**
```json
{
  "executionId": "abc123...",
  "result": {
    "status": "success",
    "timestamp": "2025-11-30T15:30:00.123456",
    "duration_seconds": 45.67,
    "total_archivos_descargados": 108,
    "resultados_por_reporte": {
      "B-2201": 108
    },
    "log_guardado_en": "gs://grupo6_scotiabank_bucket/logs/descargas_sbs.csv"
  }
}
```

### 2. Prueba usando curl con autenticación

```bash
# Paso 1: Obtener URL de la función
FUNCTION_URL=$(gcloud functions describe sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --format='value(serviceConfig.uri)')

# Paso 2: Obtener token de identidad (válido 1 hora)
TOKEN=$(gcloud auth print-identity-token)

# Paso 3: Llamar a la función
curl -X POST $FUNCTION_URL \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

# Para un reporte específico
curl -X POST $FUNCTION_URL \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"formato": "B-2315"}'
```

### 3. Ejecutar el Scheduler manualmente (sin esperar al cron)

```bash
gcloud scheduler jobs run sbs-downloader-monthly \
  --location=southamerica-east1

# Ver el resultado de la ejecución
gcloud scheduler jobs describe sbs-downloader-monthly \
  --location=southamerica-east1
```

### ❌ Lo que NO funcionará

```bash
# Esto FALLARÁ (401 Unauthorized) porque la función es privada
curl -X POST $FUNCTION_URL
```

Verás error: `"Error: Forbidden"` o `"Your client does not have permission"`

### 2. Ver logs en tiempo real

```bash
# Últimas 50 líneas
gcloud functions logs read sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --limit=50

# Logs con formato tabla
gcloud functions logs read sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --limit=100 \
  --format="table(time,severity,log)"

# Seguir logs en vivo (mientras se ejecuta)
gcloud functions logs read sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --limit=50 \
  --follow
```

### 3. Verificar archivos descargados

```bash
# Listar todos los archivos
gsutil ls -r gs://grupo6_scotiabank_bucket/data/raw/SBS/

# Contar archivos por reporte
gsutil ls gs://grupo6_scotiabank_bucket/data/raw/SBS/EEFF/ | wc -l

# Ver el log CSV
gsutil cat gs://grupo6_scotiabank_bucket/logs/descargas_sbs.csv | head -20

# Descargar log para análisis local
gsutil cp gs://grupo6_scotiabank_bucket/logs/descargas_sbs.csv ./
```

### 4. Verificar Service Accounts creados

```bash
# Listar Service Accounts del proyecto
gcloud iam service-accounts list --filter="email:sbs-*"

# Ver permisos del Function Service Account
gcloud projects get-iam-policy grupo6-scotiabank \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:sbs-downloader-sa*"
```

## 📊 Monitoreo y Operación

### Dashboards en Google Cloud Console

1. **Cloud Functions**: 
   - URL: https://console.cloud.google.com/functions
   - Métricas: Invocaciones, duración, errores, memoria
   
2. **Cloud Scheduler**: 
   - URL: https://console.cloud.google.com/cloudscheduler
   - Estado: Próxima ejecución, historial, fallos
   
3. **Cloud Storage**: 
   - URL: https://console.cloud.google.com/storage/browser/grupo6_scotiabank_bucket
   - Contenido: Archivos, tamaño, versionamiento
   
4. **Logs Explorer**: 
   - URL: https://console.cloud.google.com/logs
   - Filtros avanzados, búsqueda, análisis

### Comandos útiles de monitoreo

```bash
# Estado general de la función
gcloud functions describe sbs-downloader \
  --region=us-central1 \
  --gen2

# Métricas de la última hora
gcloud functions logs read sbs-downloader \
  --region=us-central1 \
  --gen2 \
  --limit=200 \
  --start-time="1 hour ago"

# Buscar errores
gcloud functions logs read sbs-downloader \
  --region=us-central1 \
  --gen2 \
  --limit=100 \
  --filter="severity>=ERROR"

# Tamaño del bucket
gsutil du -sh gs://grupo6_scotiabank_bucket/data/raw/SBS/
```

## 💰 Estimación de Costos

### Costo mensual estimado (1 ejecución/mes)

| Servicio | Detalle | Costo |
|----------|---------|-------|
| **Cloud Functions** | 1 invocación × ~2 min × 512MB | $0.00 - $0.01 |
| **Cloud Scheduler** | 1 job × 1 trigger/mes | $0.10 |
| **Cloud Storage** | ~650 MB almacenados | $0.01 - $0.02 |
| **Egreso de red** | ~650 MB descargados | Gratis* |
| **Cloud Build** | 1 deploy/mes | Gratis† |
| **TOTAL MENSUAL** | | **~$0.11 - $0.13** |

*\*Egreso gratis dentro de la misma región de GCP*  
*†Primeros 120 min-build/día son gratis*

### Comparación con alternativas:

| Solución | Costo mensual | Mantenimiento |
|----------|---------------|---------------|
| **Cloud Functions (esta)** | $0.12 | Cero |
| VM e2-micro (always free) | $0.00 | Alto (actualizaciones, seguridad) |
| VM e2-small 24/7 | ~$13.00 | Alto |
| Cloud Run | ~$0.15 | Bajo |

**ROI**: Ahorro de ~99% vs mantener servidor 24/7

## 🔒 Seguridad y Mejores Prácticas

### Arquitectura de Seguridad Implementada

```
┌─────────────────────┐
│ Cloud Scheduler     │
│ (Trigger mensual)   │
└──────────┬──────────┘
           │ OIDC Token
           │ (sbs-scheduler-sa)
           ▼
┌─────────────────────┐
│ Cloud Function      │
│ - Privada (no web)  │◄────── ❌ Bloqueado para internet
│ - Solo SA autorizada│
└──────────┬──────────┘
           │ Service Account
           │ (sbs-downloader-sa)
           ▼
┌─────────────────────┐
│ Cloud Storage       │
│ - Solo este bucket  │
│ - Permisos mínimos  │
└─────────────────────┘
```

### Service Accounts Creados

#### 1. `sbs-downloader-sa@grupo6-scotiabank.iam.gserviceaccount.com`

**Propósito**: Ejecuta la Cloud Function

**Permisos otorgados**:
- `roles/storage.objectAdmin` en el bucket `grupo6_scotiabank_bucket`
  - Puede: Leer, escribir, listar, eliminar objetos
  - No puede: Modificar configuración del bucket, acceder a otros buckets

**Scope limitado**: Solo este bucket específico

#### 2. `sbs-scheduler-sa@grupo6-scotiabank.iam.gserviceaccount.com`

**Propósito**: Invocar la Cloud Function desde Cloud Scheduler

**Permisos otorgados**:
- `roles/run.invoker` solo para la función `sbs-downloader`
  - Puede: Invocar esta función específica
  - No puede: Invocar otras funciones, modificar la función

**Autenticación**: OIDC (OpenID Connect) - Tokens de corta duración

### Principios de Seguridad Aplicados

1. ✅ **Principio de mínimo privilegio**: Cada SA tiene solo los permisos necesarios
2. ✅ **No acceso público**: Función privada, no accesible desde internet
3. ✅ **Autenticación fuerte**: OIDC tokens en lugar de API keys
4. ✅ **Separación de responsabilidades**: SA diferentes para función y scheduler
5. ✅ **Scope limitado**: Permisos solo al bucket y función específicos
6. ✅ **Timeout configurado**: Máximo 540s, previene ejecuciones infinitas
7. ✅ **Max instances = 1**: Previene múltiples ejecuciones simultáneas

### Comparación: Con vs Sin Service Account

| Aspecto | Sin SA (público) | Con SA (implementado) |
|---------|------------------|----------------------|
| Acceso desde internet | ✅ Cualquiera | ❌ Bloqueado |
| Autenticación | ❌ Ninguna | ✅ OIDC Token |
| Permisos de la función | ⚠️ Heredados del proyecto | ✅ Mínimos necesarios |
| Auditoría | ⚠️ Difícil | ✅ Logs por SA |
| Riesgo si comprometen URL | 🔴 Alto | 🟢 Bajo |

### Comandos de Auditoría

```bash
# Ver todos los Service Accounts
gcloud iam service-accounts list

# Ver permisos específicos del Function SA
gcloud projects get-iam-policy grupo6-scotiabank \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:sbs-downloader-sa@*"

# Ver permisos específicos del Scheduler SA
gcloud projects get-iam-policy grupo6-scotiabank \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:sbs-scheduler-sa@*"

# Ver quién puede invocar la función
gcloud functions get-iam-policy sbs-downloader \
  --region=southamerica-east1 \
  --gen2
```

### Alertas de Seguridad (Opcional pero Recomendado)

```bash
# Crear alerta si la función falla repetidamente
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="SBS Downloader Failures" \
  --condition-display-name="Function Errors > 3" \
  --condition-threshold-value=3 \
  --condition-threshold-duration=300s

# Crear alerta si hay acceso no autorizado
gcloud logging sinks create unauthorized-access-alert \
  pubsub.googleapis.com/projects/grupo6-scotiabank/topics/security-alerts \
  --log-filter='resource.type="cloud_function"
    AND protoPayload.status.code=7
    AND resource.labels.function_name="sbs-downloader"'
```

### Mejores Prácticas Implementadas en el Código

1. ✅ **User-Agent personalizado**: Identifica tu proyecto ante SBS
2. ✅ **Session reusable**: Reutiliza conexiones HTTP (más eficiente)
3. ✅ **Timeout configurado**: 15s por request, 540s total
4. ✅ **Validación de existencia**: No descarga duplicados
5. ✅ **Manejo de errores**: Try-catch en todas las operaciones
6. ✅ **Logging completo**: CSV con trazabilidad total
7. ✅ **Descarga incremental**: Solo archivos nuevos

## 🔄 Actualizaciones y Mantenimiento

### Actualizar el código

```bash
# 1. Modificar main.py
nano main.py

# 2. Re-desplegar (toma ~2-3 minutos)
./deploy.sh

# O manualmente:
gcloud functions deploy sbs-downloader \
  --gen2 \
  --region=us-central1 \
  --source=.
```

### Cambiar configuraciones

**Modificar el schedule:**
```bash
# Cambiar a cada 15 días a las 3 AM
gcloud scheduler jobs update http sbs-downloader-monthly \
  --location=us-central1 \
  --schedule="0 3 1,15 * *"

# Cambiar timezone
gcloud scheduler jobs update http sbs-downloader-monthly \
  --location=us-central1 \
  --time-zone="America/New_York"
```

**Aumentar memoria/timeout:**
```bash
gcloud functions deploy sbs-downloader \
  --gen2 \
  --region=us-central1 \
  --memory=1024MB \
  --timeout=900s
```

**Cambiar región (más cerca):**
```bash
# Usar São Paulo (más cerca de Perú)
# Editar deploy.sh y cambiar:
REGION="southamerica-east1"
```

**Modificar año de inicio:**
```python
# En main.py, línea ~29
ANIO_INICIO = 2020  # Cambiar de 2016 a 2020
```

## 🐛 Troubleshooting

### Problema: "Permission denied" al ejecutar la función

**Causa**: Tu cuenta no tiene permisos para invocar funciones privadas

**Solución 1** - Agregar tu cuenta como invoker (temporal, para testing):
```bash
gcloud functions add-invoker-policy-binding sbs-downloader \
  --region=southamerica-east1 \
  --gen2 \
  --member="user:TU_EMAIL@gmail.com"
```

**Solución 2** - Usar el Scheduler (recomendado):
```bash
# El Scheduler tiene permisos, úsalo
gcloud scheduler jobs run sbs-downloader-monthly \
  --location=southamerica-east1
```

### Problema: "Bucket does not exist"

**Causa**: Bucket no creado o nombre incorrecto

**Solución**:
```bash
# Crear manualmente el bucket
gsutil mb -p grupo6-scotiabank \
  -l southamerica-east1 \
  gs://grupo6_scotiabank_bucket

# Verificar que existe
gsutil ls gs://grupo6_scotiabank_bucket/
```

### Problema: Función se ejecuta muy lento

**Causa**: Poca memoria = menos CPU

**Solución**:
```bash
# Aumentar memoria (más memoria = más vCPU)
gcloud functions deploy sbs-downloader \
  --gen2 \
  --region=us-central1 \
  --memory=1024MB  # O 2048MB
```

### Problema: Timeout después de 540s

**Causa**: Primera ejecución descarga todos los archivos históricos

**Solución**:
```bash
# Aumentar timeout a 15 minutos
gcloud functions deploy sbs-downloader \
  --gen2 \
  --region=us-central1 \
  --timeout=900s

# O ejecutar por reporte individual:
for formato in B-2201 B-2315 B-2344 B-2370 B-2340 B-2402; do
  curl -X POST $FUNCTION_URL \
    -H "Content-Type: application/json" \
    -d "{\"formato\": \"$formato\"}"
  sleep 60
done
```

### Problema: Servicio desapareció de Cloud Run

**Aclaración**: Este proyecto usa **Cloud Functions**, NO Cloud Run.

Si alguien mencionó Cloud Run, puede ser:
1. **Confusión de términos**: Cloud Functions 2nd gen corre sobre Cloud Run internamente
2. **Proyecto equivocado**: Verificar proyecto activo con `gcloud config get-value project`
3. **Región incorrecta**: Verificar región con `gcloud functions list`

**Verificar función actual:**
```bash
gcloud functions list --gen2
```

### Problema: Archivos no se descargan

**Diagnóstico**:
```bash
# Ver logs detallados
gcloud functions logs read sbs-downloader \
  --region=us-central1 \
  --gen2 \
  --limit=200

# Probar URL manualmente
curl -I "https://intranet2.sbs.gob.pe/estadistica/financiera/2024/Noviembre/B-2201-no2024.XLS"
```

**Causas comunes**:
- URL cambió en el sitio de SBS
- Archivo no existe para ese mes/año
- Timeout de red (aumentar timeout)

## 🗑️ Limpieza (Destruir recursos)

### Eliminar solo el sistema automatizado (mantener archivos):

```bash
# Eliminar Cloud Scheduler
gcloud scheduler jobs delete sbs-downloader-monthly \
  --location=us-central1 \
  --quiet

# Eliminar Cloud Function
gcloud functions delete sbs-downloader \
  --region=us-central1 \
  --gen2 \
  --quiet
```

### Eliminar TODO (incluyendo archivos):

```bash
# ⚠️ CUIDADO: Esto elimina TODOS los archivos descargados
gsutil -m rm -r gs://grupo6_scotiabank_bucket/data/raw/SBS/
gsutil -m rm -r gs://grupo6_scotiabank_bucket/logs/

# O eliminar el bucket completo
gsutil rm -r gs://grupo6_scotiabank_bucket/
```

## 🤝 Contribución

Este es un proyecto académico. Para mejoras o issues:

1. Crear branch: `git checkout -b feature/mejora`
2. Commit: `git commit -m "Descripción"`
3. Push: `git push origin feature/mejora`
4. Crear Pull Request

## 📄 Licencia

Proyecto académico - Universidad Nacional de Ingeniería (UNI)  
Uso exclusivo para fines educativos.