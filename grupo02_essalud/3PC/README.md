# Práctica Calificada 3

Se realizó la activación del entorno de GCP.  
La documentación detallada de cada parte se encuentra en los siguientes enlaces:

- 📌 [Instalación de GCloud](../3PC/Partes/Instalacion_GCloud.md)
- ⚙️ [Habilitación Inicial](../3PC/Partes/Habilitacion_Inicial.md)
- 📤 [Subida de los datos](../3PC/Partes/Subida_datos.md)
- 🔧 [Creación de Cluster para Dataproc](../3PC/Partes/Creacion_Cluster_Dataproc.md)

---

## 🏗️ Arquitectura

La arquitectura en GCP se representa de la siguiente manera:

<img src="../3PC/Media/Fotos/Gráficos/Arquitectura.png" width="480"/>

---

## 🗄️ Diseño de Datos

### 🥉 Capa Bronce  
<img src="../3PC/Media/Fotos/Gráficos/M_Bronce.png" width="480"/>

### 🥈 Capa Plata  
<img src="../3PC/Media/Fotos/Gráficos/M_Plata.png" width="480"/>

### 🥇 Capa Oro  
<img src="../3PC/Media/Fotos/Gráficos/M_Oro.png" width="480"/>

## 💰 Costos del proyecto

Los costos estimados mensualmente y proyectados anualmente se muestran en la matriz de costos:

<img src="../3PC/Media/Fotos/Gráficos/Matriz_de_costos.png" width="480"/>

Estos costos se calcularon utilizando la Google Cloud Pricing Calculator, la herramienta oficial de Google para estimar precios de servicios en la nube.

---

## 🏗️ Comparación de nubes

Evaluamos a GCP, AWS y Azure, los 3 proveedores de nube actualmente líderes en el mercado, según 6 criterios que consideramos esenciales para el proyecto EsSalud.

| **Característica**              | **Google Cloud Platform (GCP)**                                                                                   | **Amazon Web Services (AWS)**                                                               | **Microsoft Azure**                                                                 | **GANADOR**                                                                                       |
|---------------------------------|-------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| **1. Analítica y Big Data nativa** | BigQuery: DW totalmente serverless, separación de cómputo/almacenamiento, consultas muy rápidas sobre grandes volúmenes. | Athena + Redshift: Athena consulta en S3; Redshift requiere nodos y cierta administración. | Synapse Analytics: SQL on-demand + pool provisionado; requiere configuración.        | **GCP:** BigQuery es serverless y ofrece análisis a gran escala sin administrar infraestructura.   |
| **2. Escalabilidad Serverless**     | Dataflow + BigQuery: autoscaling completo en ETL y DW sin configuración.                                          | Lambda + EMR: Lambda escala, pero limitado; EMR requiere gestión de clusters.              | Functions + Synapse: Functions escala bien; Synapse depende de capacidad reservada. | **GCP:** Escala automáticamente en todas las capas sin intervención manual.                        |
| **3. Pricing y costo por procesamiento** | BigQuery: pago por TB consultado y almacenamiento económico; no requiere instancias.                               | Redshift: costo por nodos provisionados; Redshift Serverless más caro.                     | Synapse: precio por DWU; requiere pausar o ajustar capacidad.                        | **GCP:** El modelo por consulta reduce costos y elimina la necesidad de provisionar servidores.    |
| **4. Integración con BI**           | Looker Studio: gratuito, nativo y optimizado para BigQuery.                                                         | QuickSight: bueno pero con licencias por usuario o sesión.                                 | Power BI: potente, pero con licencias y conectores externos.                        | **GCP:** Looker Studio permite dashboards sin licencias ni configuraciones adicionales.            |
| **5. Seguridad e IAM**             | IAM + Service Accounts: permisos granulares y auditoría centralizada.                                              | AWS IAM: muy robusto y con políticas detalladas.                                            | Azure AD + RBAC: fuerte integración corporativa con AD.                             | **Empate:** Cumplen estándares altos y ofrecen IAM avanzado.                                       |
| **6. Servicios ETL/ELT**           | Dataflow: ETL serverless para batch/streaming; Dataproc: Spark gestionado con autoscaling.                           | AWS Glue: ETL gestionado, menos flexible que Beam/Spark.                                   | ADF Data Flows: bueno para diseño visual, menos potente en cargas grandes.          | **GCP:** Mejor combinación de ETL serverless (Beam) y Spark escalable.                            |
| **7. Ecosistema de ML**            | Vertex AI: ML unificado, AutoML, BigQuery ML integrado y pipelines MLOps.                                           | SageMaker: muy completo, pero más caro y complejo.                                          | Azure ML: fácil de usar, pero menos robusto en producción.                           | **GCP:** Vertex AI integra ML y DW de forma nativa y simplifica el despliegue.                    |

La matriz comparativa demuestra de manera concluyente que Google Cloud Platform es la alternativa más adecuada para este proyecto. 

Esta decisión está sustentada en un análisis técnico y económico profundo, donde BigQuery destaca como la solución más avanzada en analítica y Big Data, Dataflow asegura una escalabilidad serverless real sin gestión de infraestructura, y el modelo de pricing por consulta confirma la eficiencia financiera frente a esquemas basados en nodos. 

Además, la evidencia, pruebas y documentación técnica cargadas en el repositorio de GitHub respaldan de forma transparente cada una de estas caracteristicas, garantizando una selección plenamente alineada con los requerimientos del proyecto EsSalud.
