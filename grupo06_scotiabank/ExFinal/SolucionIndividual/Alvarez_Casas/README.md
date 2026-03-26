# DESARROLLO EXAMEN FINAL- Julio Cesar Alvarez Casas

## Pregunta 3

## 3.1. Justificación de Nube, despliege de servicios y EDA Inicial


La selección de la plataforma cloud se basó en los siguientes criterios técnicos, aplicables a cualquier tipo de CSV:

- Soporte nativo para almacenamiento de archivos CSV.
- Escalabilidad automática para cargas batch.
- Modelo serverless (sin gestión de infraestructura).
- Bajo costo para ejecuciones esporádicas.
- Seguridad por defecto y trazabilidad.
- Integración directa con Python para análisis exploratorio.
- Compatibilidad con arquitectura Medallion (Bronce–Plata–Oro).

---

### Comparación General: AWS vs Azure vs GCP

| Criterio | AWS | Azure | GCP |
|--------|-----|-------|-----|
| Almacenamiento de CSV | S3 (requiere configuración manual de seguridad) | ADLS Gen2 | Cloud Storage (seguridad por defecto) |
| Procesamiento batch | EMR / Glue (basado en clústeres) | Synapse Spark Pools | Dataproc Serverless |
| Gestión de infraestructura | Media–Alta | Media | Mínima |
| Escalamiento automático | Parcial | Parcial | Completo |
| Costos para uso académico | Moderados | Altos | Muy bajos / Free Tier |
| Integración con Python | Buena | Buena | Nativa y directa |
| Curva de aprendizaje | Media | Media–Alta | Baja |

---

### Ventajas Clave de GCP para Ingestión de CSV (Capa Bronce)

Google Cloud Platform resulta especialmente adecuada para escenarios donde:

- El dataset es desconocido hasta el momento del examen.
- Se requiere cargar archivos CSV rápidamente mediante CLI.
- Se necesita ejecutar scripts Python de EDA sin aprovisionar clústeres.
- Las ejecuciones son puntuales o de baja frecuencia.

Ventajas técnicas principales:

- Cloud Storage permite almacenar archivos CSV sin esquema previo.
- Cifrado automático y auditoría habilitados por defecto.
- Dataproc Serverless permite ejecutar procesamiento bajo demanda.
- Facturación por uso real, evitando costos fijos.
- Ecosistema integrado que facilita la evolución hacia capas Plata y Oro.

---

### Adecuación a Arquitectura Medallion

GCP se adapta de forma natural a una arquitectura Medallion:

```bash
/bronce
├── raw → CSV originales cargados vía CLI
├── processed → CSV con validaciones básicas y normalización inicial
└── curated → Datos listos para consumo analítico inicial
```
### Adecuación a Arquitectura Medallion
Antes de ejecutar el despliegue, se debe contar con la siguiente estructura local:
```bash
.
├── deploy.sh
├── destroy.sh
└── csv/
|    ├── archivo1.csv
|    ├── archivo2.csv
|    └── ...
└── zip/
```

Para este caso el Dataset a usar es el siguiente:
![1](docs/1-dataset-US_Accidents.png)

La carpeta csv/ contendrá todos los archivos CSV proporcionados en el examen.
![2](docs/2-archivos_csv.png)

## Autenticarse en GCP

## Pre-requisitos

### Instalar Google Cloud SDK (gcloud CLI)

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


```bash
# Iniciar sesión con tu cuenta de Google
gcloud auth login
# Esto abrirá tu navegador para autenticación
```

![3](docs/3-auth-gcp.png)


### Asignar permisos de ejecución
```bash
chmod +x deploy.sh destroy.sh
```
### Despliegue automático de la Capa Bronce

En este archivo se crea el proyecto, el ID, se vincula con una cuenta de facturación (valor que debe ser modificado para cada usuario), se crea el bucket. 

```bash
./deploy.sh
```

### Ejecucion del deploy
![4](docs/4.1deploy.png)

### Evidencia proyecto creado

![4.2](docs/4.2cuenta_creada.png)

### Estructura Generada GCP

![4.3](docs/4.3estructura_raw_procesed_curated.png)

### Desarrollo del Eda

El análisis exploratorio fue desarrolladoe en el archivo eda.ipynb del repositorio.

![5.1](docs/5.1valores_nulos.png)


## 3.2. Estrella completo,ETL ejecutado en vivo,KPIs generados y validados. Scripts correctos

Para el desarrollo del modelo estrella en este caso, se esta tomando el dataset reducido de 1000 filas visto que el archivo total tiene un peso de 2.8g. Justificación de limitaciones de tiempo.

![6](docs/6.%20dataset_reducirdo.png)

Para poder usar spark se seleciono la reguion de us-central1 y se habilitaron las apis necesarias.

![7](docs/7.Sparknotebbok.png)



## 3.3. Visualización

Para la visualizacion se creo una cuenta de servicio la cual generará una llave para la cuentaque podra ser utilizada como credenciales en PowerBI.


### Creación de la cuenta de servicio

Esta sera la cuenta de servicio que permitira la visualización del PowerBI
```bash
gcloud iam service-accounts create sa-visualizacion-dashboard \
  --display-name="Cuenta de Servicio - Visualización Dashboards Power BI"
```

## Generación de Clave JSON (Credencial Temporal)
```bash
gcloud iam service-accounts keys create \
  sa-visualizacion-dashboard-key.json \
  --iam-account=sa-visualizacion-dashboard@grupo6-scotiabank.iam.gserviceaccount.com
```
![10](docs/10.Clave-_cuenta_servico.png)

La clave se genera en el directorio de ejecución de Cloud Shell.

### Descarga a entorno local
```bash
cloudshell download sa-visualizacion-dashboard-key.json
```

![11](docs/11.Clave_cuenta.png)

## Asignación de Roles (Acceso Simplificado)

Para garantizar compatibilidad con datasets que utilizan ACL clásico y facilitar la conexión desde Power BI, se asignaron los siguientes roles a nivel proyecto:
```bash
gcloud projects add-iam-policy-binding grupo6-scotiabank \
  --member="serviceAccount:sa-visualizacion-dashboard@grupo6-scotiabank.iam.gserviceaccount.com" \
  --role="roles/bigquery.user"
```

En cumplimiento de buenas prácticas de seguridad, las claves de la cuenta de servicio deben eliminarse una vez finalizado el periodo de uso o evaluación.

Consideraciones

- Cada cuenta de servicio puede tener un máximo de 10 claves activas.

- Se recomienda eliminar claves antiguas antes de generar nuevas.

Comando CLI para eliminar una clave existente
```bash
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=sa-visualizacion-dashboard@grupo6-scotiabank.iam.gserviceaccount.com
```

Este comando revoca inmediatamente el acceso asociado a la clave, asegurando el principio de mínimo privilegio y evitando accesos no autorizados posteriores.

## Replicación para el Docente

### Rol otorgado

Las claves de acceso para las cuentas de usuario deberan ser descargadas en el dispositivo del usuario y evitar ser compartidas o subidas a un repositorio público. Por tal motivo se asigno un rol de administrador de cuentas de servicio lo que le permite crear su propia clave de acceso para replicación del Dashboard.

```bash
gcloud projects add-iam-policy-binding grupo6-scotiabank --member=user:fgarcia@webconceptos.com  --role="roles/iam.serviceAccountKeyAdmin"
```
![13](docs/13.Rol_docente.png)

Con este rol el usuario puede:

- Crear claves

- Eliminar claves

- Descargar el JSON al momento de crearlas

Replicar:
```bash
gcloud iam service-accounts keys create sa-visualizacion-dashboard-key.json \
  --iam-account=sa-visualizacion-dashboard@grupo6-scotiabank.iam.gserviceaccount.com
```

Descargar Clave:

```bash
cloudshell download sa-visualizacion-dashboard-key.json
```

