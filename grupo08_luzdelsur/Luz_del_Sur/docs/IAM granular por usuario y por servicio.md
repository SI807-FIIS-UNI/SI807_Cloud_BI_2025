# Informe Técnico: Implementación de Seguridad y Gestión de Accesos (IAM) en AWS

---

## 1. Resumen Ejecutivo

Se ha realizado una auditoría y reestructuración de los permisos en la cuenta de AWS para garantizar que tanto el equipo de desarrollo como los servicios automatizados (ETL con AWS Glue) operen sin interrupciones, respetando el principio de separación de identidades. 

El objetivo principal fue solucionar el error `AccessDenied` (403) que impedía la ejecución de Jobs, permitiendo al servicio Glue desencriptar (KMS) y leer datos (S3) de forma autónoma mediante roles específicos.

---

## 2. Gestión de Identidades Humanas (IAM Users & Groups)

Para evitar la gestión individual propensa a errores, se implementó una estrategia basada en **Grupos** para el equipo de ingeniería.

### 2.1. Creación del Grupo "developers"
Se creó un grupo de IAM para centralizar los permisos.
* **Nombre del Grupo:** `developers`
* **ARN:** `arn:aws:iam::014562355623:group/developers`
* **Miembros Asignados:** Se agregaron 5 usuarios activos:
  * `admin-Frey-1`
  * `dev2`
  * `dev3`
  * `dev4`
  * `dev5`

### 2.2. Política de Permisos ("developers-policy")
Se creó una política personalizada (`developers-policy`) que otorga herramientas específicas para el trabajo diario, evitando el uso indiscriminado de permisos de "AdministratorAccess".

* **Servicios Permitidos:**
    * **S3 (`s3:*`, `s3tables:*`):** Control total sobre el almacenamiento de objetos.
    * **Lambda (`lambda:*`):** Gestión completa de funciones serverless.
    * **Athena (`athena:*`):** Ejecución de consultas SQL sobre datos en S3.
    * **KMS (`kms:DescribeKey`, `kms:CreateGrant`):** Gestión de llaves de encriptación necesaria para leer datos protegidos.
    * **IAM (`iam:PassRole`):** Permiso crítico que permite a los desarrolladores asignar roles a servicios (ej. asignar un rol a un Job de Glue).

> **Estado:** Implementado y verificado (Ver imágenes de configuración de grupo).

---

## 3. Gestión de Identidades de Máquina (Service Roles)

Se diagnosticó que el error `Service Principal: glue.amazonaws.com is not authorized` se debía a que el **Rol de Servicio** carecía de permisos explícitos sobre los recursos de datos.

### 3.1. Configuración del Rol de Glue
Se modificó el rol que asume el servicio de Glue durante la ejecución de los jobs ETL.
* **Nombre del Rol:** `AWSGlueServiceRole-admin`
* **Políticas Asociadas:**
    1.  `AWSGlueServiceRole` (Administrada por AWS - Permisos base).
    2.  `AWSGlueServiceRole-admin-EZCRC-s3Policy` (Administrada por el cliente - **Corrección aplicada**).

### 3.2. Detalle de la Corrección (Política JSON)
En la política personalizada se agregaron permisos explícitos para solventar la falta de acceso a los datos y a las llaves de encriptación.

**Permisos clave agregados:**
1.  **S3 (`s3:GetObject`, `s3:PutObject`):** Permite al Job leer el archivo `raw_sector.csv` y escribir los resultados procesados.
2.  **KMS (`kms:Decrypt`, `kms:GenerateDataKey`):** Soluciona el problema de seguridad si el bucket tiene encriptación activada (SSE-KMS). Permite "abrir el candado" digital de los archivos.
3.  **Condición de Seguridad:** Se añadió `StringEquals` vinculada a la cuenta `014562355623` para limitar el ámbito del rol.

#### Extracto de la Política Aplicada:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole",
                "kms:Decrypt",
                "kms:GenerateDataKey",
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "*"
        }
    ]
}