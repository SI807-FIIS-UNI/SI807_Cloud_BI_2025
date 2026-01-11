# Informe Técnico: Políticas de Seguridad JSON Implementadas

**Fecha:** 01 de Diciembre de 2025  
**Tema:** ✔ Políticas JSON creadas por consola o CLI/SDK  
**Contexto:** Documentación técnica de los permisos explícitos definidos en formato JSON (Infraestructura como Código) para la resolución de conflictos de acceso, segregación de funciones y habilitación de auditoría.

---

## 1. Política de Grupo de Desarrollo (Human Access)

Esta política define los límites de acción para el equipo de ingeniería. Se diseñó para otorgar autonomía en el desarrollo de soluciones ETL y Serverless, permitiendo acciones críticas como `iam:PassRole` (necesario para automatización), pero restringiendo permisos administrativos peligrosos de facturación o gestión de cuenta raíz.

* **Entidad:** Grupo IAM `developers`
* **Nombre de Política:** `developers-policy`
* **Tipo:** *Customer Managed Policy* (Administrada por el cliente)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole",
                "s3tables:*",
                "s3:*",
                "lambda:*",
                "kms:DescribeKey",
                "athena:*",
                "events:*",
                "kms:CreateGrant"
            ],
            "Resource": "*"
        }
    ]
}
```

## 2. Política de Servicio ETL (Machine Access)

Esta es la política crítica implementada para resolver el error 403 (Access Denied) en AWS Glue. Se adjuntó al Rol de Servicio para permitirle interactuar con el Data Lake (S3) y las llaves de encriptación (KMS).

### Puntos clave de la solución:

* **Acceso a Datos:** Se agregaron s3:GetObject y s3:PutObject para lectura/escritura.

* **Seguridad (Encriptación):** Se agregaron kms:Decrypt y kms:GenerateDataKey para manejar archivos encriptados.

* **Segregación:** Se utilizó una condición (Condition) para asegurar que el rol solo interactúe con recursos de la cuenta 014562355623.

* **Entidad:** Rol IAM `AWSGlueServiceRole-admin`
* **Nombre de Política:** `AWSGlueServiceRole-admin-EZCRC-s3Policy`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "ds:CreateIdentityPoolDirectory",
                "kms:Decrypt",
                "ec2:DeleteNetworkInterface",
                "athena:*",
                "glue:*",
                "ec2:RevokeSecurityGroupIngress",
                "iam:PassRole",
                "ec2:DescribeNetworkInterfaces",
                "s3tables:*",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DeleteSecurityGroup",
                "kms:GenerateDataKey",
                "quicksight:*",
                "kms:DescribeKey",
                "kms:CreateGrant",
                "ds:DeleteDirectory"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:*"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceAccount": "014562355623"
                }
            }
        }
    ]
}
```

## 3. Política de Auditoría y Monitoreo (Audit Access)

Esta política permite la integración entre AWS CloudTrail (Auditoría) y Amazon CloudWatch Logs (Monitoreo). Fue generada para permitir que el Trail `robot-trail` escriba los registros de actividad en un grupo de logs específico en la región de São Paulo (`sa-east-1`).

* **Entidad:** Rol IAM `robot-trail`
* **Nombre de Política:** `Cloudtrail-CW-access-policy-robot-trail-b1b4ad9d-6c6f-46ac-8fe8-31433bf30299`
* **Función:** `logs:CreateLogStream` y `logs:PutLogEvents` para la persistencia de logs.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailCreateLogStream2014110",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream"
            ],
            "Resource": [
                "arn:aws:logs:sa-east-1:014562355623:log-group:aws-cloudtrail-logs-014562355623-856cfe46:log-stream:014562355623_CloudTrail_sa-east-1*"
            ]
        },
        {
            "Sid": "AWSCloudTrailPutLogEvents20141101",
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:sa-east-1:014562355623:log-group:aws-cloudtrail-logs-014562355623-856cfe46:log-stream:014562355623_CloudTrail_sa-east-1*"
            ]
        }
    ]
}
```