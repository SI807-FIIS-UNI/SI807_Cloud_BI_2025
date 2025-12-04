# Costos – Análisis y optimización del entorno en Azure

En esta carpeta se documenta el **comportamiento de costos** del entorno completo desplegado en Azure para el proyecto del dashboard, así como una **proyección a 6 meses** y las **acciones de optimización** propuestas.

Los datos y gráficas utilizados se obtienen directamente del portal de Azure sobre la suscripción usada en la PC4.

---

### 4.1 Resumen general de la suscripción

En primer lugar se revisa el panel de la suscripción, donde se observa:

- Estado de la suscripción (**activa** y dentro del crédito disponible).
- Gráfico de **Spending rate and forecast**, que muestra el gasto acumulado del mes y una previsión si se mantuviera la misma tendencia.
- Tarjeta de **Costs by resource**, donde se identifican los servicios que más contribuyen al costo total (base de datos PostgreSQL, Databricks, firewall, etc.).
- Panel de **Top products by number of resources**, que indica qué tipos de recursos se han aprovisionado con mayor frecuencia (alertas, NSGs, etc.).

<img width="1865" height="907" alt="Captura de pantalla 2025-12-01 173046" src="https://github.com/user-attachments/assets/c93e1282-f76d-4f8e-be5b-0b2fe72bb115" />

---

### 4.2 Matriz de costos del entorno Azure

A partir del panel de costos por recurso, se elabora la siguiente **matriz de servicios y su rol en la solución**. No se incluyen montos exactos (ya visibles en las gráficas), sino el peso relativo y el tipo de consumo:

| Servicio / Recurso principal              | Rol en la solución                                             | Tipo de costo        | Comentario                                                                 |
|------------------------------------------|----------------------------------------------------------------|----------------------|----------------------------------------------------------------------------|
| Azure Database for PostgreSQL Flexible   | Base de datos transaccional del backend                        | Consumo mensual      | Es uno de los recursos con mayor peso; el costo crece con almacenamiento y vCores. |
| Azure Databricks                         | Capa de ingeniería de datos y notebooks de transformación      | Consumo por uso      | El costo depende fuertemente del tiempo de ejecución y del escalado de clusters.   |
| Azure Container Apps (bbva-backend-api)  | Backend Flask / API del dashboard                              | Consumo por vCPU/GB  | Costos moderados; el autoscaling ayuda a contener el gasto en escenarios académicos. |
| Azure Static Web Apps (bbva-dashboard-frontend) | Frontend React del dashboard                          | Muy bajo / casi fijo | El costo es bajo en el plan Free; aumenta si se pasa a planes Standard.   |
| Azure Firewall + NAT / red               | Seguridad perimetral, salida controlada a internet             | Consumo por hora + GB| Recurso relevante en el costo, especialmente si se mantiene encendido 24/7. |
| Azure Storage Account (stbbvadatalake)   | Data Lake (bronze/silver/gold) y ficheros de logs              | Almacenamiento + ops | Costos bajos en este escenario; puede crecer con más datos y accesos.     |
| Log Analytics Workspace                  | Centralización de logs y métricas                              | Ingesta de datos     | El costo aumenta con el volumen de logs enviados desde Container Apps, Firewall, etc. |

Esta matriz demuestra que el costo está alineado con la arquitectura diseñada: la mayor parte del gasto se concentra en los **servicios realmente críticos** (base de datos, Databricks, firewall y red).

---

### 4.3 Uso de beneficios *Free services for 12 months*

Azure ofrece un conjunto de servicios gratuitos por 12 meses, con límites mensuales de uso. En el panel de **Free services for 12 months** se observa:

- El servicio de **Azure Database for PostgreSQL** consume un porcentaje del límite mensual, pero se mantiene **“Unlikely to exceed”**.
- El **Container Registry** y otros servicios listados (almacenamiento, transferencia de datos, etc.) se encuentran todavía muy por debajo de sus límites.
- La mayoría de los servicios gratuitos aparecen como **“Not in use”** o con uso de **0 %**, lo que indica que el entorno está consumiendo solo lo necesario para la práctica.

<img width="1013" height="909" alt="Captura de pantalla 2025-12-01 173217" src="https://github.com/user-attachments/assets/94e1957a-0f77-4611-8938-6e44f2b6f33a" />

Este panel es clave para validar que la solución respeta el **presupuesto académico** y no sobrepasa los beneficios del plan gratuito.

---

### 4.4 Análisis de costos acumulados en el mes

El reporte de **Cost analysis** para la suscripción muestra:

- Un **costo acumulado aproximado de 40 USD** en el mes analizado.
- Una curva de costos que crece en los días en los que se realizaron más pruebas de Databricks, despliegues del backend y creación de recursos de red.
- Gráficos de distribución del gasto:
  - Por **servicio**, donde destaca la base de datos PostgreSQL, Databricks, firewall/red y almacenamiento.
  - Por **región**, concentrado en *East US*.
  - Por **grupo de recursos**, principalmente `rg-bbva-dashboard` y el grupo asociado a Databricks.

<img width="1862" height="908" alt="Opera Snapshot_2025-12-01_172928_portal azure com" src="https://github.com/user-attachments/assets/acafec4b-49fd-43f4-852c-761941a3a130" />

Este análisis permite aterrizar la relación entre **decisiones de arquitectura** (usar firewall dedicado, VNet, Databricks, etc.) y su impacto directo en el costo mensual.

---

### 4.5 Proyección simplificada a 6 meses

Tomando como referencia un costo mensual aproximado de **40 USD**, y suponiendo que:

- la carga de trabajo se mantiene estable,
- no se realizan optimizaciones adicionales,
- y no se agregan nuevos servicios de alto consumo,

se puede hacer una proyección lineal:

| Horizonte | Suposición                         | Costo estimado |
|----------:|------------------------------------|----------------|
| 1 mes     | Situación actual                   | ~40 USD        |
| 3 meses   | Mismo patrón de uso                | ~120 USD       |
| 6 meses   | Mismo patrón de uso                | ~240 USD       |

> Nota: la proyección es **académica** y se basa en el comportamiento actual del entorno; en un escenario real se usarían budgets, alertas y análisis de tendencias más finos (por ejemplo, desglosados por día, por etiqueta de proyecto, etc.).

---

### 4.6 Estrategias de optimización de costos

A partir del análisis anterior se identifican varias acciones concretas para reducir o controlar los costos del entorno:

#### 4.6.1 Databricks

- Configurar **autoscaling** de clusters y timeouts de apagado automático tras periodos de inactividad.
- Evitar dejar clusters corriendo cuando no se utilizan notebooks.
- Centralizar notebooks y jobs en un único workspace para compartir recursos.

#### 4.6.2 Base de datos PostgreSQL

- Revisar el tamaño mínimo de vCores y almacenamiento necesario para la carga de trabajo del curso.
- Activar o ajustar el **auto-scale / auto-pause** si el modelo de servicio lo permite.
- Limpiar datos de pruebas antiguas para no crecer innecesariamente en almacenamiento.

#### 4.6.3 Firewall, VNet y red

- Mantener el firewall solo mientras se realizan pruebas prácticas; apagarlo fuera del horario de laboratorio si es posible.
- Usar **NSGs** bien definidos para evitar tráfico innecesario y limitar exposición.
- Revisar reglas de salida (egress) para minimizar tráfico hacia internet.

#### 4.6.4 Storage y Data Lake

- Clasificar los datos por niveles (**bronze, silver, gold**) y eliminar datasets temporales que ya no se usan.
- Aprovechar niveles de almacenamiento más económicos para datos históricos que se consultan poco.
- Configurar políticas de **lifecycle management** para mover o borrar blobs después de un tiempo.

#### 4.6.5 Monitoring y Log Analytics

- Ajustar qué logs se envían al workspace (`law-bbva-dashboard`), priorizando:
  - Auditoría de seguridad.
  - Logs de aplicación importantes.
- Reducir el envío de logs muy verbosos (debug) en entornos de laboratorio para evitar costos de ingesta innecesarios.

---

### 4.7 Conclusiones y relación con TCO on-premise vs. cloud

Desde el punto de vista del **TCO (Total Cost of Ownership)**, el escenario en Azure utilizado para la PC4 presenta las siguientes ventajas frente a un despliegue on-premise equivalente:

- No se incurre en costos iniciales de **hardware**, licencias de sistemas operativos, bases de datos ni infraestructura de red física.
- El costo es **100 % variable**: si se detienen los recursos (clusters, VMs, firewall, etc.), el gasto se reduce casi a cero.
- Se dispone de servicios avanzados (Databricks, Container Apps, Static Web Apps, Log Analytics, Firewall administrado, etc.) que serían complejos y costosos de replicar on-premise.
- La visibilidad de costos en tiempo real (portales y gráficas) permite ajustar el diseño de la solución de forma ágil.



