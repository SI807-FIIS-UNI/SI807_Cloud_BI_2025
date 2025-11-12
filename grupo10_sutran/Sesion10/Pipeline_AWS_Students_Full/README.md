# 🧩 Pipeline AWS – Guía de Implementación (Estudiantes SI807U)

## 🎯 Objetivo
Implementar un pipeline funcional de **Business Intelligence en la nube** sobre AWS, desde la ingesta hasta la capa analítica, utilizando **S3, Glue, Athena y QuickSight**.

El objetivo final es que el grupo logre un flujo completo de:
```
S3 (raw) → Glue Job (PySpark) → S3 (curated) → Athena (SQL) → QuickSight (Dashboard)
```
## 1️⃣ Ingesta de datos

Primero descargamos los requerimientos.txt de EDA_Ecommerce_Full `pip install -r requirements.txt`

Ya que estamos usando para hacer todo Visual Studio Code, debemos crear un entorno:
```
python -m venv venv
.\venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```
Luego tuvimos que comentar las dos primeras líneas donde se usaba google.colab y agregamos la línea de código path.

Debido a un error que se debe a que se está usando **backslashes (`\`) en una cadena de texto en Python**, y algunos como `\U` o `\n` se interpretan como **caracteres especiales** (escape sequences). En tu caso, `\U` está causando el problema.

```
path = 'C:\\Users\\jairo\\Documents\\Proyectos\\aradiel_25-2\\taller_2\\archive\\Amazon Sale Report.csv'
#o
path = r'C:\Users\jairo\Documents\Proyectos\aradiel_25-2\taller_2\archive\Amazon_Sale_Report.csv'
```
Luego se tuvo que modificar bastante el código para adaptarlo al archivo csv “Amazon Sale report.csv”

Ocurre porque Windows CMD o PowerShell no soporta por defecto algunos emojis Unicode como “📦”

```UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4e6'

# Otro error
ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'
```

Instalamos AWSCLIV2.msi y verificamos en la terminal o cmd

![Consola](/Sesion10/Pipeline_AWS_Students_Full/images/image1.png)

Acá 🔑 Se te pedirá:

- **Access Key ID** → te lo da AWS IAM (si no lo tienes, debes generarlo).
- **Secret Access Key** → lo mismo.
- **Default region name** → por ejemplo: `us-east-1`
- **Output format** → pon: `json`

📝 Si no tienes claves aún, crea una en IAM:

- Ir a IAM Users
- Selecciona tu usuario o crea uno nuevo
- Activa acceso programático
- Genera las claves

Creamos el user y activamos el acceso programativo, esto nos generará un “Access Key” y “Secret Access Key”.

![IAM](/Sesion10/Pipeline_AWS_Students_Full/images/image2.png)

Descargamos el archivo .csv o podemos copiarlo las claves en un lugar seguro. Ya que no podremos ver el Secret Access Key nuevamente.

![Access Key](/Sesion10/Pipeline_AWS_Students_Full/images/image3.png)

Volvemos al cmd e ingresamos los datos que generamos y la configuración por default.

![Consola2](/Sesion10/Pipeline_AWS_Students_Full/images/image4.png)

Para poder subir el archivo CSV limpio al bucket damos permisos al usuario que creamos
En lugar de seleccionar una política existente, elige “Create inline policy”

![Permisos](/Sesion10/Pipeline_AWS_Students_Full/images/image5.png)

Pegamos este código y le damos en formato JSON, le damos a “Netx” y la nombramos “AllowS3Grupo10”
 ```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::si807u-10-bi",
        "arn:aws:s3:::si807u-10-bi/*"
      ]
    }
  ]
}
 ```

Luego que cremos el permiso al usuario que creamos en IAM, probamos en el CMD el siguiente comando

```
aws s3 cp "<ruta local>" <ruta s3 bucket>
```
![Permisos](/Sesion10/Pipeline_AWS_Students_Full/images/image6.png)

Vemos que esta vez si nos permitió hacer la carga del archivo csv que habíamos limpiado localmente.

## 2️⃣ Catálogo Glue
Ahora vamos a crear una base de datos Glue

1. Vamos a AWS Glue y creamos una base de datos con el nombre “raw_data”
![Database_created](/Sesion10/Pipeline_AWS_Students_Full/images/image7.png)

2.  Creamos el Crawler, ingresamos nombre y la ruta de la fuente de datos, en este en la carpeta donde guardamos el archivo CSV en S3.
3. Seleccionamos un rol existente o creamos uno por default, en nuestro caso ingresamos “AWSGlueServiceRole-lider”.
4. Target database: raw_data y la tabla de salida ecommerce_clean. Luego seleccionamos la frecuencia a On demand.
   
![configuration_crawler](/Sesion10/Pipeline_AWS_Students_Full/images/image8.png)

5. Luego nos dirigimos a la lista de Crawlers y corremos la que creamos
6. Vamos a “Tables” y verificamos que el schema este correcto
![schema](Sesion10\Pipeline_AWS_Students_Full\images\image9.png)

## 3️⃣ Transformación con Glue Job (PySpark)
En AWS Glue nos dirigimos a ETL jobs y Visual ETL para crear el script

[VER "job_transform_aws.py"](/Sesion10/Pipeline_AWS_Students_Full/scripts/job_transform_aws.py)

Nos estuvo dando errores, por lo que al revisar en CloudWatch nos dimos cuenta que faltó darle permisos a rol que se creó de poder ejecutar Scripts y escribir en S3.

![Rol_Policy](/Sesion10/Pipeline_AWS_Students_Full/images/image10.png)

Volvemos a correr el job y el script termina de ejecutarse correctamente

![job_run_summary](/Sesion10/Pipeline_AWS_Students_Full/images/image11.png)

## 4️⃣ Consulta en Athena

[VER "00_create_analytics_db.sql"](/Sesion10/Pipeline_AWS_Students_Full/sql/00_create_analytics_db.sql)

![00_create_analytics](/Sesion10/Pipeline_AWS_Students_Full/images/image12.png)

[VER "10_create_sales_curated.sql"](/Sesion10/Pipeline_AWS_Students_Full/sql/00_create_analytics_db.sql)

![10_create_sales_curateds](/Sesion10/Pipeline_AWS_Students_Full/images/image13.png)

[VER "20_kpi_sales_summary.sql"](/Sesion10/Pipeline_AWS_Students_Full/sql/20_kpi_sales_summary.sql)

![20_kpi_sales_summary](/Sesion10/Pipeline_AWS_Students_Full/images/image14.png)

[VER "20_kpi_sales_summary.sql"](/Sesion10/Pipeline_AWS_Students_Full/sql/20_kpi_sales_summary.sql)

![20_kpi_sales_summary](/Sesion10/Pipeline_AWS_Students_Full/images/image14.png)



---

## 🧱 1. Estructura recomendada en S3
```
s3://si807u-<grupo>-bi/
├── raw/
│   └── ecommerce/          # archivos CSV originales
├── curated/
│   └── ecommerce/          # parquet limpio
├── analytics/
│   └── results/            # salidas o datasets procesados
└── athena_results/
```

---

## ☁️ 2. Flujo del Pipeline
### 1️⃣ Ingesta de datos
- Subir `ecommerce_clean.csv` (desde tu EDA) a `s3://si807u-<grupo>-bi/raw/ecommerce/`

### 2️⃣ Catálogo Glue
- Crear base de datos: `raw_db`
- Crear Crawler con ruta `raw/ecommerce/`
- Ejecutar y verificar tabla `raw_db.ecommerce_clean`

### 3️⃣ Transformación con Glue Job (PySpark)
Ejecutar el Job `job_transform_aws.py` con:
```
--SOURCE s3://si807u-<grupo>-bi/raw/ecommerce/
--TARGET s3://si807u-<grupo>-bi/curated/ecommerce/
```
Resultado: archivos **Parquet particionados por año/mes** en `curated/`.

### 4️⃣ Consulta en Athena
Ejecutar los SQL del folder `/sql` en orden:
1. `00_create_analytics_db.sql`
2. `10_create_sales_curated.sql`
3. `20_kpi_sales_summary.sql`

### 5️⃣ Dashboard QuickSight
- Crear dataset desde Athena (`analytics_db.sales_curated`).
- Publicar dashboard “Ventas por Categoría”.

---

## 🧠 3. Reglas de Entrega
- Registrar cada paso en `/docs/bitacora_pipeline.md`
- Commit y Push a la rama `feature/grupoXX-init`
- PR hacia `develop` con descripción del flujo y evidencias (S3, Glue, Athena, QuickSight).

---

## 📈 4. Evaluación
| Fase | Descripción | Peso |
|------|--------------|------|
| Glue Job | Transformación raw→curated (PySpark) | 30% |
| Athena SQL | Base analítica y KPI | 30% |
| QuickSight | Dashboard BI funcional | 25% |
| Bitácora + GitHub | Evidencias y documentación | 15% |

---

## ✅ Checklist
- [X] Dataset cargado en S3/raw
- [X] Glue Crawler y Job ejecutados
- [X] Tabla Athena creada y funcional
- [ ] Dashboard publicado en QuickSight
- [ ] PR con evidencias completado
