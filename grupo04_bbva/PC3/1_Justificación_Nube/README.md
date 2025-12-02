# 1. Justificación del Uso de la Nube

## 1.1. Recordatorio del proyecto y contexto de migración

El proyecto desarrolla un flujo completo de Inteligencia de Negocios para monitorear los niveles de madurez **Practitioner** y **Continuous Integration (CI)** del BBVA, utilizando en su versión local:

- Ingesta manual de archivos CSV exportados desde el **Marco Playbook**.  
- Procesos ETL en **PySpark** sobre un entorno Hadoop/Hortonworks con **Zeppelin**.  
- Un **Data Warehouse relacional** con modelo estrella implementado en **PostgreSQL**.  
- Una **API en Flask** y un **dashboard web en React** para la visualización de KPIs.

La migración a la nube de Azure busca:

- Escalar el procesamiento distribuido de datos sin administrar servidores físicamente.  
- Simplificar la gestión de datos mediante un **Data Lake** y un **DW administrado en PostgreSQL**.  
- Mejorar la **seguridad, segmentación de red, cumplimiento y auditoría** usando servicios como  
  **Virtual Network, Network Security Groups, Azure Firewall, Private Endpoints, Private DNS Zone, Azure Key Vault, Azure Monitor, Log Analytics Workspace, Recovery Services Vault y Audit Logs**.  
- Mantener una capa de exposición moderna basada en **Container App + Static Web Apps** para la interfaz Flask/React.  
- Reducir el mantenimiento de infraestructura on-premise y riesgos asociados (hardware, energía, respaldos manuales, etc.).  
- Garantizar **costos controlables y trazables** mediante monitoreo y métricas centralizadas.

Para seleccionar el proveedor cloud se evaluaron tres opciones líderes del mercado: **AWS**, **Microsoft Azure** y **Google Cloud Platform (GCP)**, considerando siete características críticas para soluciones de **BI** y **Big Data**.

---

## 1.2. Criterios de evaluación utilizados

Los 7 criterios aplicados en la comparativa fueron:

1. Seguridad y cumplimiento normativo  
2. Escalabilidad y disponibilidad  
3. Pricing y modelo de costos  
4. Ecosistema de BI y análisis de datos  
5. Servicios Big Data y procesamiento distribuido  
6. Soporte y madurez de servicios  
7. Facilidad de migración y compatibilidad  

---

## 1.3. Análisis por criterio

### 1.3.2. Criterio 1: Seguridad y cumplimiento normativo

Los tres proveedores cuentan con catálogos amplios de certificaciones y servicios de seguridad. Sin embargo, en este proyecto el énfasis está en:

- **Aislamiento de red** (segmentación por VNet, subredes y reglas de tráfico).  
- **Acceso privado a servicios PaaS** (Private Endpoints + Private DNS Zone).  
- **Gestión segura de secretos** (Key Vault).  
- **Supervisión centralizada** (Azure Monitor + Log Analytics + Audit Logs).  
- **Respaldo y recuperación ante desastres** (Recovery Services Vault).  

**Comparación resumida**

| Aspecto clave                         | AWS                                                                 | Azure                                                                                                                                                 | GCP                                                                                  |
|--------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Enfoque de seguridad                 | Amplio portafolio de servicios de seguridad y compliance            | Enfoque de plataforma integrada: red privada (VNet), segmentación (NSG), Firewall, endpoints privados, Key Vault y monitoreo unificado               | Fuerte foco en protección de datos y seguridad gestionada para workloads            |
| Segmentación de red                  | VPC, Security Groups, NACLs                                         | Virtual Network, subredes, Network Security Groups y Azure Firewall para definir perímetros y políticas de tráfico                                   | VPC, firewall de red, reglas de IAM y políticas de organización                     |
| Acceso privado a servicios gestionados | Endpoints privados para ciertos servicios PaaS                      | Private Endpoints + Private DNS Zone para exponer servicios solo dentro de la VNet                                                                   | Private Service Connect para acceso privado                                          |
| Gestión de secretos                  | AWS KMS y Secrets Manager                                           | Azure Key Vault como almacén central cifrado de secretos, claves y certificados, integrado con los servicios de la solución                          | Cloud KMS y Secret Manager                                                           |
| Monitoreo y auditoría                | CloudTrail, CloudWatch                                              | Azure Monitor + Log Analytics Workspace + Audit Logs para métricas, logging y trazabilidad de acciones sobre recursos                                | Cloud Logging, Cloud Monitoring                                                      |
| Respaldo y recuperación              | Backup y servicios de DR específicos                                | Recovery Services Vault para backups y recuperación de máquinas y bases de datos, con retención configurable                                         | Backup/DR gestionado por servicios individuales                                      |
| Alineamiento con entorno bancario    | Alto                                                                 | Muy alto: modelo pensado para entornos enterprise regulados, con integración nativa de red privada, claves, monitoreo, auditoría y respaldo central | Medio-alto                                                                           |

**Conclusión**

En un contexto similar al de BBVA, donde la seguridad, el aislamiento de red y la trazabilidad son críticos, **Azure** ofrece una combinación sólida de:

- **Segmentación de red** (VNet, NSG, Firewall).  
- **Acceso privado a datos y servicios** (Private Endpoints, Private DNS Zone).  
- **Protección de secretos** (Key Vault).  
- **Monitoreo y auditoría centralizados** (Azure Monitor, Log Analytics, Audit Logs).  
- **Respaldo y recuperación** (Recovery Services Vault).

Esto permite construir un flujo BI de uso interno con un nivel de gobierno y cumplimiento alineado a entornos financieros.

---

### 1.3.3. Criterio 2: Escalabilidad y disponibilidad

Los tres proveedores dominan el mercado de nube y ofrecen altos niveles de disponibilidad. Para este proyecto, los aspectos más relevantes son:

- Escalar el **procesamiento distribuido** (PySpark en Databricks).  
- Escalar el **Data Warehouse relacional** (PostgreSQL administrado).  
- Publicar el **backend Flask** y el **frontend React** en servicios gestionados, sin administrar servidores físicos.  
- Proteger todo dentro de una **VNet** con controles de tráfico y monitoreo.

**Comparación resumida**

| Aspecto clave              | AWS                                                                   | Azure                                                                                                                                                 | GCP                                                             |
|---------------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| Cobertura global          | Líder histórico, gran número de regiones y zonas                      | Número de regiones muy alto, con fuerte presencia enterprise y escenarios híbridos                                                                   | Menos regiones, red muy optimizada                             |
| Escalabilidad de cómputo  | EC2 + Auto Scaling, ECS/EKS, Lambda                                   | Servicios de cómputo y contenedores desplegados dentro de una VNet, con reglas de NSG y Firewall; escalado horizontal configurado según la demanda   | GKE, Cloud Run, App Engine, Cloud Functions                    |
| Escalabilidad de datos    | S3 + Redshift/Aurora/RDS                                              | Azure Data Lake + PostgreSQL administrado, expuestos por Private Endpoints dentro de la VNet                                                         | Cloud Storage + BigQuery/Cloud SQL                             |
| Disponibilidad gestionada | Alta, con SLAs por servicio                                           | Alta, con SLAs competitivos y posibilidad de combinarlo con Recovery Services Vault para mejorar la estrategia de continuidad                        | Muy alta en servicios analíticos serverless                    |

**Conclusión**

Para un flujo **ETL + Data Lake + DW + API + frontend**, Azure permite:

- Desplegar los componentes críticos dentro de una **red privada (VNet)**.  
- Proteger el acceso con **NSG + Azure Firewall**.  
- Exponer servicios PaaS mediante **Private Endpoints**.  
- Monitorizar el comportamiento con **Azure Monitor + Log Analytics**.

Todo ello sin necesidad de administrar hardware propio y manteniendo la posibilidad de escalar los recursos a medida que crecen los volúmenes de datos o usuarios.

---

### 1.3.4. Criterio 3: Pricing y modelo de costos

AWS, Azure y GCP utilizan un modelo de **pago por uso**, con la opción de descuentos por compromisos de uso (reservas) y herramientas de control de costos.

Para este proyecto interesa:

- Poder **empezar pequeño** y crecer con el tiempo.  
- Pagar principalmente por **ejecuciones de Databricks** y capacidad del **DW PostgreSQL**.  
- Tener trazabilidad de los recursos que más consumen mediante **métricas y logs centralizados**.

**Comparación resumida**

| Aspecto clave                  | AWS                                                             | Azure                                                                                                                                | GCP                                                       |
|--------------------------------|------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| Modelo base                    | Pay-as-you-go + Reserved Instances / Savings Plans              | Pay-as-you-go + reservas por capacidad, con métricas unificadas vía Azure Monitor / Log Analytics                                      | Pay-as-you-go + descuentos por uso sostenido             |
| Visibilidad de costos          | Cost Explorer, Budgets                                          | Portal unificado con vistas de consumo por recurso, grupo de recursos o etiqueta, apoyado en métricas y logs de Azure Monitor         | Herramientas de presupuesto y uso                        |
| Ajuste a cargas BI tipo batch  | Viable, cuidando recursos siempre encendidos                    | Viable: se combinan SKUs pequeños, escalado por demanda y políticas de apagado de entornos no productivos                              | Muy competitivo en escenarios 100 % serverless           |

**Conclusión**

Aunque **GCP** resulta muy atractivo en escenarios totalmente serverless, en un proyecto que combina **Spark + DW relacional + aplicaciones web**, **Azure** ofrece un equilibrio razonable entre:

- Flexibilidad para crecer de forma gradual.  
- Herramientas nativas para entender dónde se está gastando (métricas y logs centralizados).  
- Opciones de reservas en aquellas capas que luego se estabilicen.

---

### 1.3.5. Criterio 4: Ecosistema de BI y análisis de datos

El proyecto actual construye dashboards y tablas interactivas mediante un **frontend React** publicado en **Static Web Apps**, consumiendo datos procesados por Databricks y almacenados en PostgreSQL.

Aun así, se consideró el **ecosistema de BI** de cada nube a nivel estratégico (posible evolución futura):

- AWS: QuickSight como solución BI principal.  
- Azure: ecosistema BI de Microsoft, integrado con plataformas de datos y servicios de Azure.  
- GCP: Looker y Looker Studio, muy orientados a entornos data/analytics.

**Conclusión**

Aunque la versión actual del proyecto utiliza un **dashboard propio (React)**, elegir Azure mantiene abierta la posibilidad de integrar, a futuro, herramientas BI del ecosistema Microsoft de forma natural, sin cambiar de proveedor de nube.

---

### 1.3.6. Criterio 5: Servicios Big Data y procesamiento distribuido

La arquitectura local está basada en **Spark sobre Hadoop**. En la nube se busca:

- Mantener la lógica en **PySpark**.  
- Dejar de manejar clústeres manualmente.  
- Aprovechar un **Data Lake** con capas Bronze/Silver/Gold.

En Azure, esto se resuelve con:

- **Azure Databricks** como entorno gestionado para notebooks PySpark.  
- **Azure Data Lake** para el almacenamiento en crudo y transformado.

**Comparación resumida**

| Aspecto                       | AWS                         | Azure                                                            | GCP                           |
|------------------------------|-----------------------------|------------------------------------------------------------------|-------------------------------|
| Spark gestionado             | EMR, Glue                   | Azure Databricks (servicio de primer nivel en la plataforma)     | Dataproc                      |
| Integración con Data Lake    | S3                          | Azure Data Lake con soporte natural para arquitectura Medallion  | Cloud Storage                 |
| Continuidad con arquitectura local | Requiere adaptar entorno | Migra notebooks PySpark y reemplaza HDFS por Data Lake con cambios mínimos | Requiere adaptar a Dataproc   |

**Conclusión**

Para un flujo **HDFS + PySpark + DW** ya existente, **Azure Databricks + Azure Data Lake** permiten migrar la lógica ETL casi de forma directa, añadiendo además:

- Mejor gobernanza de datos.  
- Mejor integración con la capa de seguridad y red (VNet, Key Vault, Monitor).

---

### 1.3.7. Criterio 6: Soporte y madurez de servicios

En cuota de mercado y madurez:

- **AWS** sigue liderando en participación.  
- **Azure** se sitúa en segundo lugar con fuerte foco enterprise.  
- **GCP** ocupa el tercer lugar, con foco en datos e IA.

Los tres son proveedores “tier 1”, pero Azure está especialmente bien posicionado en entornos corporativos que ya utilizan tecnologías Microsoft.

**Conclusión**

Para un proyecto que desea parecerse a cómo trabajaría una empresa grande (como un banco) que ya usa herramientas Microsoft, **Azure** ofrece una alineación más directa en:

- Prácticas recomendadas.  
- Documentación y ejemplos.  
- Ecosistema de partners y soporte corporativo.

---

### 1.3.8. Criterio 7: Facilidad de migración y compatibilidad

El stack actual está conformado por:

- **PySpark + Zeppelin** (ETL).  
- **HDFS** (staging / data lake).  
- **PostgreSQL** (Data Warehouse relacional con modelo estrella).  
- **Flask** (backend).  
- **React** (frontend).

**Comparación resumida**

| Componente actual  | AWS                                   | Azure                                         | GCP                               |
|--------------------|----------------------------------------|-----------------------------------------------|-----------------------------------|
| PySpark + Zeppelin | EMR Notebooks / Glue                  | Azure Databricks (notebooks PySpark gestionados) | Dataproc + Notebooks              |
| HDFS (Hortonworks) | S3                                    | Azure Data Lake                               | Cloud Storage                     |
| PostgreSQL (DW)    | RDS PostgreSQL / Redshift             | PostgreSQL administrado en Azure (servicio PaaS) | Cloud SQL / BigQuery              |
| Flask + React      | ECS/EKS, Elastic Beanstalk, Amplify   | Azure Container Apps + Static Web Apps        | Cloud Run / GKE                   |

**Conclusión**

La migración “uno a uno” del stack actual es especialmente directa hacia **Azure**:

- ETL PySpark → notebooks en **Azure Databricks**.  
- HDFS → **Azure Data Lake**.  
- PostgreSQL local → **PostgreSQL administrado en Azure**.  
- Flask + React → **Container Apps + Static Web Apps**, con tráfico protegido dentro de una **VNet** y expuesto sólo a través de los puntos que se definan.

Esto reduce retrabajo y permite concentrarse en mejorar el flujo BI, no en reescribir toda la solución desde cero.

---

## 1.4. Matriz de Decisión

Se asignaron pesos porcentuales a cada uno de los 7 criterios según su relevancia para el proyecto y se calificó a cada proveedor en una escala 1–4:

- 1 = Regular  
- 2 = Bueno  
- 3 = Muy bueno  
- 4 = Excelente  

### 1.4.1. Evaluación ponderada por criterio

| Característica                                  | Peso | GCP | AWS | Azure |
|-------------------------------------------------|------|-----|-----|-------|
| Seguridad y Cumplimiento Normativo             | 20 % | 3   | 4   | 4     |
| Escalabilidad y Disponibilidad                 | 18 % | 4   | 4   | 4     |
| Pricing y Modelo de Costos                     | 16 % | 3   | 3   | 4     |
| Ecosistema de BI y Análisis de Datos           | 15 % | 3   | 3   | 4     |
| Servicios Big Data y Procesamiento Distribuido | 15 % | 4   | 3   | 4     |
| Soporte y Madurez de Servicios                 | 10 % | 3   | 4   | 4     |
| Facilidad de Migración y Compatibilidad        | 6 %  | 3   | 4   | 4     |

**Resumen de resultados**

| Proveedor | Puntuación ponderada (1–4) |
|-----------|----------------------------|
| GCP       | 3.33                       |
| AWS       | 3.54                       |
| Azure     | 4.00                       |

**Azure** obtiene la puntuación máxima posible (**4.00**), superando a **AWS (3.54)** y **GCP (3.33)** en la evaluación global, de acuerdo con los pesos definidos para los criterios del proyecto.

---

## 1.5. Decisión Final: Microsoft Azure

### 1.5.1. Justificación técnica

Azure obtiene la puntuación más alta porque ofrece la combinación óptima de características para este caso de uso:

1. **Plataforma de datos y procesamiento alineada con el stack actual**

   - **Azure Databricks** permite ejecutar los notebooks PySpark existentes con cambios mínimos.  
   - **Azure Data Lake** soporta la arquitectura **Medallion (Bronze, Silver, Gold)** para almacenar datos crudos y transformados.  
   - Un **PostgreSQL administrado en Azure** permite mantener el modelo estrella para KPIs Practitioner/CI.

2. **Capa de red y seguridad de nivel corporativo**

   - Todos los componentes se despliegan dentro de una **Virtual Network** con subredes específicas.  
   - El tráfico se controla con **Network Security Groups** y **Azure Firewall**, reduciendo la exposición a internet.  
   - El acceso a servicios PaaS se realiza mediante **Private Endpoints** y resolución mediante **Private DNS Zone**, evitando endpoints públicos.  
   - Las credenciales sensibles se almacenan en **Azure Key Vault**.  
   - La operación se supervisa con **Azure Monitor**, **Log Analytics Workspace** y **Audit Logs**.  
   - Los backups y la recuperación ante desastres se gestionan con **Recovery Services Vault**.

3. **Arquitectura de exposición moderna**

   - El **backend Flask** se ejecuta en **Azure Container Apps**.  
   - El **frontend React** se publica en **Azure Static Web Apps**, optimizado para SPAs.  
   - Ambos se integran con la VNet y con la capa de seguridad para exponer únicamente lo necesario.

En conjunto, Azure permite reproducir y mejorar la arquitectura local, pero con una red privada, controles de seguridad más finos, observabilidad centralizada y servicios gestionados.

---

### 1.5.2. Justificación financiera

A nivel financiero, Azure aporta:

- Un modelo **pay-as-you-go** que permite comenzar con tamaños de clúster y bases de datos modestos y crecer según la volumetría real.  
- Posibilidad de aplicar **descuentos por reserva de capacidad** en los componentes que se estabilicen (por ejemplo, DW PostgreSQL o capacidad de contenedores).  
- **Métricas y logs centralizados** (Azure Monitor + Log Analytics) para identificar rápidamente qué servicios son responsables de la mayor parte del consumo y ajustar el dimensionamiento.  
- Capacidad de **apagar o reducir** entornos no productivos (dev/test) fuera de horario, evitando pagar por recursos ociosos.

Esto facilita mantener controlado el presupuesto del proyecto y justificar los costos frente al equivalente on-premise.

---

### 1.5.3. Alineación con requerimientos del proyecto

El proyecto requiere migrar el pipeline:

> Ingesta CSV → Procesamiento Spark → Data Lake (Bronze/Silver/Gold) → DW PostgreSQL (modelo estrella) → API Flask → Dashboard React

**Mapeo a Azure:**

- **Ingesta y Data Lake**  
  - Los CSV del Marco Playbook se cargan y almacenan en **Azure Data Lake**, donde se organizan en capas Bronze/Silver/Gold.

- **Procesamiento distribuido**  
  - La lógica ETL en PySpark se migra a **Azure Databricks**, manteniendo el mismo lenguaje y patrón de notebooks, pero aprovechando un servicio gestionado.

- **Data Warehouse relacional**  
  - El modelo estrella se implementa en **PostgreSQL administrado en Azure**, conservando la estructura de hechos y dimensiones.

- **Capa de exposición**  
  - El **backend Flask** se despliega en **Azure Container Apps**.  
  - El **frontend React** se hospeda en **Azure Static Web Apps**, consumiendo la API expuesta desde Container Apps.

- **Seguridad, red y operación**  
  - Todo se ejecuta dentro de una **VNet** protegida con **NSG** y **Azure Firewall**.  
  - Los servicios PaaS se consumen mediante **Private Endpoints** y **Private DNS Zone**.  
  - Los secretos se gestionan en **Azure Key Vault**.  
  - La observabilidad y trazabilidad se centralizan en **Azure Monitor, Log Analytics Workspace y Audit Logs**.  
  - Los respaldos y la recuperación ante desastres se gestionan con **Recovery Services Vault**.

La combinación de:

- **Alineación técnica** con el stack actual,  
- **Arquitectura segura de red y datos**, y  
- **Modelo económico flexible y monitorizable**,  

Justifica de forma sólida la selección de **Microsoft Azure** como plataforma cloud para este caso de uso.
