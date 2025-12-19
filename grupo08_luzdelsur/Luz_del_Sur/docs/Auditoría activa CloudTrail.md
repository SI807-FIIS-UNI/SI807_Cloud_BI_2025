# Informe Técnico: Implementación de Auditoría y Gobernanza (AWS CloudTrail)

**Fecha:** 01 de Diciembre de 2025  
**Proyecto:** Sistema de Monitoreo y Trazabilidad de Eventos  
**Recurso:** AWS CloudTrail  
**Nombre del Trail:** `robot-trail`  
**Región:** sa-east-1 (São Paulo)  

---

## 1. Resumen Ejecutivo

Se ha habilitado y configurado exitosamente el servicio **AWS CloudTrail** para garantizar la gobernanza, el cumplimiento normativo y la auditoría operativa y de riesgos de la cuenta AWS.

El recurso desplegado, denominado `robot-trail`, actúa como el "sistema de vigilancia" principal, capturando tanto las acciones administrativas (cambios de configuración) como las acciones de datos (acceso a objetos S3), proporcionando una visión completa de la actividad realizada por usuarios humanos y roles de servicio (como AWS Glue).

---

## 2. Configuración del Trail (Registro de Seguimiento)

El Trail se ha configurado para operar de manera continua y resiliente, asegurando que ningún evento crítico se pierda.

| Parámetro | Estado Configurado | Descripción |
| :--- | :--- | :--- |
| **Estado** | `Registrando` (Activo) | El servicio está capturando eventos en tiempo real. |
| **Alcance** | `Multi-Región` | Captura eventos en todas las regiones, centralizándolos en `sa-east-1`. |
| **Almacenamiento** | `lds-s3-bucket-final` | Los logs se archivan permanentemente en este bucket S3. |
| **Validación de Archivos** | `Habilitado` | Garantiza la integridad de los logs (asegura que no han sido modificados). |
| **Última entrega** | `01 dic 2025, 04:21:16` | Confirmación de funcionamiento reciente. |

---

## 3. Alcance de la Auditoría (Tipos de Eventos)

Se ha implementado una configuración de **Auditoría Profunda**, superando la configuración básica por defecto al incluir eventos de datos.

### 3.1. Eventos de Administración (Management Events)
* **Configuración:** `Lectura` y `Escritura` (Todo).
* **Propósito:** Registra cambios en la infraestructura.
* **Ejemplos capturados:** Creación de usuarios IAM, modificación de Security Groups, despliegue de Lambdas.

### 3.2. Eventos de Datos (Data Events) - **Crítico**
* **Recurso Auditado:** `Amazon S3` (Todos los eventos).
* **Configuración:** `Select All` (Registrar todo).
* **Impacto Operativo:** Esta configuración es vital para el diagnóstico del Data Lake. Permite ver **quién** accede a **qué archivo** específico.
    * *Caso de Uso:* Permite rastrear las llamadas `GetObject` y `PutObject` realizadas por el Job de Glue sobre el archivo `raw_sector.csv`.

---

## 4. Integración con Monitoreo (CloudWatch Logs)

Para permitir el análisis en tiempo real y la creación de alertas, el Trail no solo guarda archivos en S3, sino que inyecta los eventos directamente en CloudWatch.

* **Grupo de Log:** `aws-cloudtrail-logs-014562355623-856cfe46`
* **Rol IAM Asociado:** `arn:aws:iam::014562355623:role/service-role/robot-trail`
* **Beneficio:** Permite buscar errores como "AccessDenied" inmediatamente sin tener que descargar archivos `.json.gz` desde S3.

---

## 5. Evidencia de Actividad Reciente

El análisis del historial de eventos confirma que el sistema está capturando la actividad de los servicios automatizados. Se han detectado eventos generados por el servicio de ETL (Glue).

* **Identidad detectada:** `GlueJobRunnerSession` (Rol asumido por Glue).
* **Eventos Registrados:**
    * `CreateLogGroup` / `CreateLogStream`: Glue preparando su salida de logs.
    * `RunStatement`: Ejecución de código dentro del Job.
* **Origen:** `glue.amazonaws.com` y `logs.amazonaws.com`.

---

## 6. Conclusión

La infraestructura de auditoría `robot-trail` está **operativa y conforme** a las mejores prácticas de seguridad.

1.  **Centralización:** Todos los logs van a un Bucket S3 seguro.
2.  **Visibilidad:** Se capturan operaciones a nivel de objeto (S3 Data Events).
3.  **Integridad:** La validación de archivos de log está activa.

El sistema está listo para ser utilizado en tareas de análisis forense y troubleshooting.