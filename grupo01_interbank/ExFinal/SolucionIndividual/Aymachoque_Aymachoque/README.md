# AWS README
## Justificación técnica de la nube seleccionada: AWS (y por qué no GCP/Azure)
Se eligió **Amazon Web Services (AWS)** para implementar la solución BI porque ofrece un flujo completo, integrado y reproducible para un escenario “end-to-end” (ingesta → modelado → KPIs → dashboards) con herramientas serverless maduras y una curva de ejecución directa para el tiempo disponible.
### Por qué AWS encaja mejor con esta solución
- **Ruta BI completa y cohesionada:** Amazon S3 (data lake) + AWS Glue (catálogo) + Amazon Athena (SQL serverless) + Amazon QuickSight (dashboards) permiten cubrir BRONCE/PLATA/ORO con integración nativa y mínima fricción operativa.
- **Reproducibilidad y evidencias:** AWS facilita demostrar el proceso con **AWS CLI** y dejar trazabilidad (comandos, logs y salidas) en `docs/`, alineado con la exigencia de evidencias en vivo.
- **Operación “serverless” para análisis:** con Athena se consulta y transforma en SQL sin administrar servidores para consultas, acelerando el modelado dimensional y KPIs.
- **Seguridad y control:** IAM permite aplicar control de acceso por mínimo privilegio en S3, Glue, Athena y QuickSight, manteniendo el entorno ordenado para un caso evaluativo.

### Por qué no se eligió Google Cloud Platform (GCP)
- **Requería más configuración inicial en este contexto** (habilitación de servicios, permisos y vinculación de recursos) para alcanzar el mismo flujo end-to-end de forma rápida.
- La solución se puede construir en GCP (por ejemplo, GCS + BigQuery + Looker Studio), pero en esta implementación se priorizó una ruta en AWS con herramientas ya alineadas al enfoque S3/Glue/Athena/QuickSight.

### Por qué no se eligió Microsoft Azure
- Azure también es válido (por ejemplo, ADLS + Synapse/SQL + Power BI), sin embargo:
  - La **integración de BI con dashboards** tiende a depender fuertemente del ecosistema Power BI y su configuración, lo que añade pasos adicionales en un escenario de ejecución práctica.
  - Para este caso se priorizó un flujo donde el “DW lógico” y los KPIs queden inmediatamente consultables desde el data lake con SQL serverless (Athena) y conectables a dashboards (QuickSight) con mínima preparación.

