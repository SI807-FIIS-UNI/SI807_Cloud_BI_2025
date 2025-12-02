# 4. PROYECCIÓN DE COSTOS (6 MESES) Y OPTIMIZACIÓN  

## 4.1. Escenario base (volumetría constante)  

Se considera el costo total mensual estimado del entorno Azure de **≈ 380 USD/mes**, manteniendo estable la volumetría de datos y el número de usuarios.  

| **Mes** | **Costo mensual (USD)** | **Costo acumulado (USD)** | **Observaciones**                                 |
|--------:|-------------------------|---------------------------|--------------------------------------------------|
| Mes 1   | 380.00                  | 380.00                    | Configuración inicial + primera carga de datos   |
| Mes 2   | 380.00                  | 760.00                    | Operación normal                                 |
| Mes 3   | 380.00                  | 1,140.00                  | Operación normal                                 |
| Mes 4   | 380.00                  | 1,520.00                  | Operación normal                                 |
| Mes 5   | 380.00                  | 1,900.00                  | Operación normal                                 |
| Mes 6   | 380.00                  | 2,280.00                  | Operación normal                                 |

**Supuestos del escenario base**

- Volumen de datos constante: ~130 MB/mes (CSV Practitioner + CI).  
- Usuarios concurrentes en el dashboard/backend: 20–30.  
- Ejecuciones de Databricks: 4 horas/mes.  
- Sin cambios en la arquitectura ni en el dimensionamiento de servicios.  
- Uso estable de:
  - **Azure Data Lake Storage Gen2** (capas Bronze/Silver/Gold).  
  - **Azure Databricks** (procesamiento Spark).  
  - **Base de datos gestionada en Azure (Azure Database for PostgreSQL)** como DW analítico.  
  - **Azure Container Apps** como backend (API Flask).  
  - **Azure Static Web Apps** como frontend React.  
  - **Azure Key Vault** (gestión de secretos).  
  - **Azure Monitor + Log Analytics Workspace** (observabilidad y alertas).  

---

## 4.2. Escenario de crecimiento (incremento 20 % en volumetría trimestral)  

En este escenario se proyecta un incremento del 20 % en la volumetría de datos a partir del segundo trimestre, lo que genera un aumento moderado de costos en servicios de cómputo y almacenamiento.

| **Mes** | **Volumen de datos** | **Usuarios concurrentes** | **Costo mensual (USD)** | **Costo acumulado (USD)** | **Δ vs escenario base**            |
|--------:|----------------------|---------------------------|--------------------------|----------------------------|------------------------------------|
| Mes 1   | 130 MB               | 25                        | 380.00                   | 380.00                     | –                                  |
| Mes 2   | 130 MB               | 25                        | 380.00                   | 760.00                     | –                                  |
| Mes 3   | 130 MB               | 25                        | 380.00                   | 1,140.00                   | –                                  |
| Mes 4   | 156 MB (+20 %)       | 30                        | 395.53                   | 1,535.53                   | +15.53/mes (≈ +4.1 %)              |
| Mes 5   | 156 MB               | 30                        | 395.53                   | 1,931.06                   | +15.53/mes                         |
| Mes 6   | 156 MB               | 30                        | 395.53                   | 2,326.59                   | +15.53/mes                         |

**Supuestos del escenario de crecimiento**

- **Trimestre 1 (Meses 1–3)**  
  - Volumen base: 130 MB/mes.  
  - Costo mensual: 380.00 USD.  

- **Trimestre 2 (Meses 4–6)**  
  - Volumen incrementado: 156 MB/mes (+20 %).  
  - Impacto estimado en costos:
    - **Data Lake Gen2:** +0.5 GB acumulado → **+0.12 USD/mes** aprox.  
    - **Databricks:** +1 hora de ejecución (5 h/mes) → **+1.08 USD/mes** aprox.  
    - **Base de datos (Azure Database for PostgreSQL):** +5 GB de almacenamiento (pasar de 25 GB a 30 GB) → **+1.25 USD/mes** aprox.  
    - **Azure Container Apps:** autoscaling ligeramente más agresivo (promedio 2 réplicas vs 1.5) → **+13.08 USD/mes** aprox.  
  - **Incremento total estimado:** ~**+15.53 USD/mes** (≈ **+4.1 %** sobre el escenario base).  

---

## 4.3. Estrategias de optimización de costos  

### 4.3.1. Escalabilidad automática (autoscaling)  

La arquitectura aprovecha el autoscaling para ajustar los recursos a la demanda real y evitar sobreaprovisionamiento.

**Servicios con autoscaling recomendado**

| **Servicio**                     | **Métrica base**        | **Regla de scale-out**               | **Regla de scale-in**                 | **Rango min/máx** | **Ahorro mensual estimado**                                  |
|----------------------------------|-------------------------|--------------------------------------|---------------------------------------|--------------------|----------------------------------------------------------------|
| Azure Container Apps (backend)   | CPU Percentage          | CPU > 70 % durante 5 min             | CPU < 40 % durante 10 min             | 1–10 réplicas      | ~35 USD/mes (evita mantener 3 réplicas 24/7 si no hacen falta) |
| Azure Databricks                | Carga del clúster       | Workers utilizados > 80 %            | Workers idle > 5 min                  | 2–8 workers        | ~12 USD/mes (evita mantener 8 workers siempre activos)        |
| Base de datos gestionada (DB)   | Uso CPU / vCores        | Uso > 80 % durante 10 min            | Uso < 50 % durante 30 min             | 4–8 vCores         | ~175 USD/mes (subir a 8 vCores solo en picos concretos)       |

> Estos valores representan **ahorros potenciales** si se parte de un entorno sobredimensionado y se habilitan reglas de autoscaling bien calibradas.

**Beneficios clave del autoscaling**

- Reducir costos en horas de baja demanda (noches, fines de semana).  
- Mantener una buena experiencia de usuario durante picos de carga.  
- Evitar pagar por recursos ociosos (vCores, réplicas, workers).  

---

### 4.3.2. Instancias reservadas / Planes de ahorro

Una vez que la volumetría y el patrón de uso están estables (por ejemplo, después de 6 meses), tiene sentido considerar reservar capacidad o contratar **Planes de Ahorro** para ciertos servicios de cómputo.

**Servicios candidatos (compromiso 1 año)**

| **Servicio**                                         | **Configuración actual**         | **Costo mensual actual** | **Costo con RI / Savings Plan (1 año)** | **Descuento aprox.** | **Ahorro mensual** | **Ahorro anual** |
|------------------------------------------------------|----------------------------------|---------------------------|------------------------------------------|-----------------------|---------------------|-------------------|
| Base de datos gestionada (4 vCores)                  | Pay-as-you-go                    | 259.41 USD                | 180.00 USD                               | ≈ 30–31 %             | ~79.41 USD          | ~952.92 USD       |
| Azure Container Apps (cómputo equivalente backend)   | Pay-as-you-go                    | 69.35 USD                 | 50.54 USD                                | ≈ 27 %               | 18.81 USD           | 225.72 USD        |
| **Total ahorro estimado**                            |                                  |                           |                                          |                       | **~98.22 USD**      | **~1,178.64 USD** |

**Recomendación**

- Evaluar las métricas de uso reales durante los primeros **6 meses**.  
- Si el patrón es estable:
  - Aplicar **Reserved Instances / Savings Plans** de 1 año para:
    - La base de datos gestionada (Azure Database for PostgreSQL).  
    - El cómputo asociado al backend en Azure Container Apps.  
- El compromiso de 1 año ofrece buen equilibrio entre **descuento** y **flexibilidad**, sin atarse a contratos de 3 años.

**Ejemplo simplificado de ahorro en la base de datos**

- Costo actual mensual (pay-as-you-go, 4 vCores, con descuento corporativo aplicado): ≈ **259–260 USD**.  
- Costo con Reserved Instance / Savings Plan (1 año) + descuento corporativo: ≈ **176–180 USD/mes**.  
- Ahorro aproximado: **78–80 USD/mes → ~940–960 USD/año**.  

---

### 4.3.3. Almacenamiento por niveles (Hot / Cool)  

Para optimizar costos de almacenamiento en Azure Data Lake Storage Gen2, se puede definir una política de **Lifecycle Management** basada en la antigüedad de los datos.

**Política propuesta por capa Medallion**

| **Capa**            | **Tier actual** | **Tier optimizado** | **Regla de transición**                | **Ahorro estimado mensual** |
|---------------------|-----------------|---------------------|----------------------------------------|-----------------------------|
| Bronze (raw CSVs)   | Hot             | Cool                | Mover a Cool después de 90 días        | ~0.15 USD/mes               |
| Silver (Parquet)    | Hot             | Cool                | Mover a Cool después de 180 días       | ~0.10 USD/mes               |
| Gold (Delta Lake)   | Hot             | Hot (sin cambio)    | Mantener en Hot (acceso frecuente)     | 0.00 USD/mes                |

**Ahorro anual aproximado:** **3 USD/año**.  
Aunque el monto es pequeño, ayuda a estandarizar buenas prácticas de **gobernanza** y **optimización de almacenamiento**.

---

### 4.3.4. Apagado de recursos no productivos  

En un entorno real con ambientes separados (desarrollo, pruebas, producción), se recomienda **apagar o reducir recursos no productivos** fuera de horario laboral.

**Ejemplo de políticas para entornos Dev/Test**

| **Recurso**                               | **Schedule sugerido**      | **Horas activas/mes**             | **Ahorro mensual estimado** |
|-------------------------------------------|----------------------------|-----------------------------------|-----------------------------|
| Databricks Cluster Dev                    | Lun–Vie 8:00–18:00         | 220 h vs 730 h (–70 %)            | ~18.20 USD                  |
| Base de datos Dev (2 vCores)              | Lun–Vie 8:00–20:00         | 260 h vs 730 h (–64 %)            | ~135.40 USD                 |
| Container Apps Dev (slots/servicios Dev)  | Solo durante deploys       | 8 h vs 730 h (–99 %)              | ~68.67 USD                  |

**Ahorro mensual total estimado:** ~**222.27 USD** (≈ **2,667 USD/año**).  

Estas optimizaciones aplican solo a **entornos no productivos**; producción se mantiene 24/7 para garantizar disponibilidad.

---

### 4.3.5. Monitoreo y alertas de costos  

Se recomienda usar **Azure Cost Management + Billing** junto con **Azure Advisor** para evitar sorpresas en la factura.

**Configuración sugerida de Azure Cost Management**

| **Tipo de alerta** | **Umbral**                     | **Acción**                                      | **Beneficio**                               |
|--------------------|---------------------------------|-------------------------------------------------|---------------------------------------------|
| Budget Alert       | Costo mensual > 500 USD         | Email a responsables + notificación (Teams/Slack) | Detección temprana de sobrecostos           |
| Anomaly Alert      | Incremento > 25 % vs promedio 7 días | Email a Service Owner                      | Identifica recursos mal configurados o fugas |
| Forecast Alert     | Proyección mensual > 600 USD    | Email a equipo BI/DevOps                       | Ajuste proactivo de recursos                |

**Azure Advisor – Recomendaciones de costo**

- Identifica automáticamente:  
  - Recursos de cómputo subutilizados.  
  - Almacenamiento huérfano (discos/logs no utilizados).  
  - Endpoints públicos innecesarios y configuraciones ineficientes.  
- Ahorro potencial típico: **15–30 USD/mes** corrigiendo recursos subutilizados.  
- Frecuencia recomendada de revisión: **semanal**.  

---

## 4.4. Comparación de costos: local vs cloud  

### 4.4.1. Análisis TCO (Total Cost of Ownership) a 3 años  

**Arquitectura local (Docker on-premise)**  

| **Categoría**                                    | **Año 1** | **Año 2** | **Año 3** | **Total 3 años** |
|--------------------------------------------------|----------:|----------:|----------:|-----------------:|
| **Hardware inicial**                             |           |           |           |                  |
| Servidor físico (32 vCores, 128 GB RAM, 2 TB SSD)| 8,500 USD | –         | –         | 8,500 USD        |
| Switch de red + firewall                         | 1,200 USD | –         | –         | 1,200 USD        |
| UPS (backup de energía)                          | 800 USD   | –         | –         | 800 USD          |
| **Infraestructura**                              |           |           |           |                  |
| Electricidad (servidor 24/7, 500 W)              | 525 USD   | 551 USD   | 579 USD   | 1,655 USD        |
| Refrigeración (data center)                      | 840 USD   | 882 USD   | 926 USD   | 2,648 USD        |
| Internet dedicado (100 Mbps)                     | 1,800 USD | 1,890 USD | 1,985 USD | 5,675 USD        |
| **Licencias software**                           |           |           |           |                  |
| PostgreSQL / Ubuntu / monitoreo OSS              | 0 USD     | 0 USD     | 0 USD     | 0 USD            |
| **Personal IT**                                  |           |           |           |                  |
| Administrador de sistemas (20 % FTE)             | 18,000 USD| 18,900 USD| 19,845 USD| 56,745 USD       |
| Soporte técnico incidencias                      | 6,000 USD | 6,300 USD | 6,615 USD | 18,915 USD       |
| **Mantenimiento**                                |           |           |           |                  |
| Reemplazo componentes (5 % anual)                | 425 USD   | 446 USD   | 469 USD   | 1,340 USD        |
| Actualizaciones software (tiempo IT)             | 1,200 USD | 1,260 USD | 1,323 USD | 3,783 USD        |
| **Backup / DR**                                  |           |           |           |                  |
| Discos externos para backup                      | 600 USD   | 300 USD   | 300 USD   | 1,200 USD        |
| Almacenamiento offsite                           | 480 USD   | 504 USD   | 529 USD   | 1,513 USD        |
| **Total anual**                                  | **40,370 USD** | **31,033 USD** | **32,571 USD** | **103,974 USD** |
| **Costo mensual promedio**                       | **3,364 USD** | **2,586 USD** | **2,714 USD** | **2,888 USD**   |

**Costos ocultos de la arquitectura local**

- Sin alta disponibilidad nativa (riesgo de ~8 h/año de downtime).  
- Sin escalabilidad automática (servidor dimensionado para picos con alta ociosidad).  
- Sin disaster recovery geográfico.  
- Actualizaciones y parches manuales.  
- Seguridad más limitada (sin MFA, RBAC granular, auditoría centralizada, etc.).  

---

**Arquitectura cloud (Azure)** – *ejemplo ilustrativo de proyección a 3 años*  

> Los siguientes valores son un ejemplo que combina el costo base estimado del entorno (~380 USD/mes) con optimizaciones progresivas (autoscaling, apagado de entornos Dev/Test, descuentos) a partir del segundo año.

| **Categoría**                            | **Año 1** | **Año 2** | **Año 3** | **Total 3 años** |
|------------------------------------------|----------:|----------:|----------:|-----------------:|
| Servicios Azure (baseline aprox.)        | 5,168 USD | 5,373 USD | 5,588 USD | 16,129 USD       |
| **Descuentos y optimizaciones (Años 2–3)** |          |           |           |                  |
| – Reserved Instances / Savings Plans     | –         | –1,180 USD| –1,180 USD| –2,360 USD       |
| – Autoscaling optimizado                 | –         | –2,664 USD| –2,664 USD| –5,328 USD       |
| – Apagado de recursos Dev/Test           | –         | –2,667 USD| –2,667 USD| –5,334 USD       |
| **Costo neto servicios Azure (ejemplo)** | **5,168 USD** | **862 USD** | **1,077 USD** | **7,107 USD** |
| **Personal IT (reducido)**               |           |           |           |                  |
| Administrador cloud (≈ 5 % FTE)          | 4,500 USD | 4,725 USD | 4,961 USD | 14,186 USD       |
| **Total anual aproximado**               | **9,668 USD** | **5,587 USD** | **6,038 USD** | **21,293 USD** |
| **Costo mensual promedio**               | **806 USD** | **466 USD** | **503 USD** | **592 USD**    |

> Estos números son orientativos y muestran cómo, combinando autoscaling, reservas de capacidad/savings plans y apagado de entornos no productivos, el **TCO en Azure** puede ser muy inferior al de una solución on-premise equivalente.

---

### 4.4.2. Comparación directa (promedio mensual a 3 años)  

| **Concepto**                          | **Local** | **Cloud Azure** | **Diferencia**  |
|--------------------------------------|----------:|----------------:|-----------------|
| Costo mensual promedio (3 años)      | 2,888 USD | 592 USD         | **−79.5 %**     |
| Costo total 3 años                   | 103,974 USD | 21,293 USD     | **−82,681 USD** |
| **CAPEX inicial**                    | 10,500 USD | 0 USD          | **−100 %**      |
| **OPEX mensual Año 1**               | 3,364 USD | 806 USD        | **−76.0 %**     |

**ROI (Return on Investment) – ejemplo**

```text
Ahorro total estimado a 3 años: ~82,681 USD
Inversión en migración (desarrollo + pruebas): 15,000 USD (ejemplo)
ROI neto ≈ 67,681 USD
Periodo de recuperación (payback) ≈ 2.2 meses
