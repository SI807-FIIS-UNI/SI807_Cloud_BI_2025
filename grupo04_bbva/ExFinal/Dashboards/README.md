# Dashboards – Niveles de Madurez (Practitioner / Continuous Integration)

Este directorio contiene la evidencia del **Dashboard de Niveles de Madurez**, implementado como una **aplicación web** (Frontend + Backend) y desplegado en **Azure Static Web Apps**.  
> Importante: **NO se utilizó Power BI**. La visualización se realiza desde un **frontend web** publicado por Azure.

---

## 1) Vista general del dashboard
El dashboard permite analizar la madurez (adopción) por **geografía, servicio y periodo**, para los dominios:
- **Practitioner**
- **Continuous Integration (CI)**

Incluye una vista **Global** (agregados y distribución de niveles) y una vista **por Servicio** (drill-down, tendencia y brechas por KPI).

<img width="912" height="462" alt="image" src="https://github.com/user-attachments/assets/50b4eb39-3078-4365-b225-42a8e0ed4aae" />


## 2) Acceso (Static Web Apps)

En su momento, el dashboard fue accesible mediante un enlace generado por Azure Static Web Apps con un formato similar a:

`https://yellow-coast-mmmmmmm.azurestaticapps.net`  *(URL censurada por privacidad)*

Actualmente, el enlace muestra error (404) debido a una limitación del entorno de prueba.

<img width="1600" height="817" alt="image" src="https://github.com/user-attachments/assets/38c464f7-12f9-4923-8d99-23b53f9dde67" />

## 3) Incidente: servicio no disponible por consumo de crédito (Azure Free Trial)

Durante el proceso de aprendizaje y despliegue en Azure, **no se gestionó adecuadamente el consumo de recursos** y el crédito del **plan gratuito (Free Trial)** se agotó.  
Como consecuencia, algunos recursos dejaron de estar disponibles, impactando el acceso público del dashboard.

Para sustentar esto se adjunta evidencia del estado de crédito y el consumo por recurso.

<img width="423" height="223" alt="image" src="https://github.com/user-attachments/assets/74a26c91-fe5a-4496-9c12-e9ae2ee9802b" />

<img width="855" height="310" alt="image" src="https://github.com/user-attachments/assets/4cd65bcd-d0a0-44cb-8c4f-dd7ad6ec4a3c" />


### ¿Por qué el Firewall puede ser tan costoso?
Es relativamente común que **Azure Firewall** consuma gran parte de un crédito pequeño (como el Free Trial) porque suele tener:
- costo base por hora (según SKU),
- costo por procesamiento/transferencia de datos,
- y recursos asociados (IP pública, reglas, logging).

En entornos académicos o de prueba, si no es estrictamente necesario, conviene:
- apagar/eliminar el firewall cuando no se use,
- usar alternativas más simples (NSG + reglas de red),
- revisar SKUs y monitorear costos desde Cost Management.

---

## 4) Nota de integridad del entregable (PC4)

Aunque el despliegue público ya no esté accesible por el agotamiento del crédito, se recalca que:
- **no se modificó nada del entregable** después de la presentación de la **PC4**,
- el sistema **funciona exactamente igual** a como fue demostrado (ETL, carga, KPIs y frontend),
- el inconveniente corresponde únicamente a disponibilidad del entorno cloud por falta de crédito.

---

