# 2. Escenarios de Escalabilidad, Elasticidad y Recuperación ante Desastres (DR)

## 2.1. Objetivo de la sección

Esta sección describe cómo la arquitectura en Azure está preparada para:
- Escalar ante distintos niveles de carga.
- Ajustar automáticamente los recursos (elasticidad) para no pagar por capacidad ociosa.
- Mantener alta disponibilidad del servicio.
- Recuperarse ante fallos graves mediante mecanismos de **backup y Disaster Recovery (DR)**.

Se centra en los servicios clave del proyecto:

- Azure Databricks  
- Data Lake en Azure (Bronze / Silver / Gold)  
- PostgreSQL gestionado en Azure  
- Azure App Service (backend Flask)  
- Azure Static Web Apps (frontend React)  
- Virtual Network (VNet), NSG, Azure Firewall, Private Endpoints, Private DNS Zone  
- Azure Key Vault  
- Azure Monitor + Log Analytics Workspace  
- Recovery Services Vault  
- Audit Logs  

---

## 2.2. Escenarios de carga

Para diseñar la escalabilidad, se consideran tres escenarios de carga típicos:

### 2.2.1. Escenario A – Carga base (operación normal)

- **Frecuencia de ETL**: mensual.
- **Volumen de datos**:
  - CSV Practitioner: ~50 MB/mes.
  - CSV CI: ~80 MB/mes.
  - Total ingesta: ~130 MB/mes.
- **Usuarios concurrentes**:
  - 20–30 usuarios internos consultando el dashboard.
- **Patrón de acceso**:
  - Picos de uso en horario laboral (consultas al dashboard).
  - Procesamiento intensivo solo en la ventana ETL mensual.
  - 
Este escenario corresponde al dimensionamiento base usado en la matriz de costos.

---

### 2.2.2. Escenario B – Crecimiento moderado

- **Volumen de datos**:
  - +20 % de crecimiento trimestral → ~156 MB/mes.
- **Usuarios concurrentes**:
  - 30–40 usuarios internos.
- **Impacto esperado**:
  - Más tiempo de cómputo en Databricks.
  - Más consultas y almacenamiento en PostgreSQL.
  - Más tráfico hacia App Service y Static Web Apps.

La arquitectura debe soportar este crecimiento con **ajustes menores de configuración** (escalado vertical/horizontal).

---

### 2.2.3. Escenario C – Pico puntual de consumo

- Auditoría interna, presentaciones o cierres trimestrales.
- Múltiples usuarios consultan el dashboard en paralelo.
- Consultas más pesadas sobre históricos completos.

En este escenario es clave poder **escalar temporalmente** App Service y, si es necesario, los recursos de PostgreSQL.

---

## 2.3. Estrategia de escalabilidad y elasticidad

### 2.3.1. Azure Databricks – Escalabilidad para el ETL

- **Tipo de clúster**: Standard_DC4as_v5 (4 vCores, 16 GB RAM).
- **Autoscaling de workers**:
  - Rango propuesto: Single node

**Configuración recomendada:**

- Política de auto-terminación: apagar el clúster tras 20 minutos sin actividad.
- Horario de ejecución del job:
  - Ventana ETL mensual programada (por ejemplo, madrugada o fuera de horario pico).

**Beneficios:**

- El clúster solo consume recursos durante:
  - Ingesta y limpieza (Bronze → Silver).
  - Transformaciones de negocio (Silver → Gold).
  - Carga al DW (PostgreSQL).
- El resto del tiempo no hay costo de cómputo en Databricks.
  
---

### 2.3.2. PostgreSQL en Azure – Escalabilidad vertical

PostgreSQL en Azure se dimensiona inicialmente con:

- **vCores**: 4 vCores (General Purpose).
- **Almacenamiento**: 25 GB (modelo estrella + índices).

La escalabilidad se resuelve principalmente de forma **vertical**:

- Aumento de vCores (por ejemplo, de 4 → 8) ante:
  - Incremento sostenido de consultas.
  - Picos de uso en cierres mensuales/trimestrales.
- Aumento de almacenamiento (por ejemplo, 25 → 50 GB) ante:
  - Crecimiento de históricos.
  - Nuevas tablas de hechos/dimensiones.

La plataforma permite aplicar estos cambios con mínimo downtime, manteniendo la lógica del modelo estrella intacta.

---

### 2.3.3. Azure App Service – Escalabilidad horizontal

- **Plan**: Standard S1.
- **Instancias**: 1 instancia base, con posibilidad de escalar horizontalmente.

**Reglas de autoscaling recomendadas:**

- Métrica: **CPU Percentage** o **HTTP Queue Length**.
- **Scale-out**:
  - Si CPU > 70 % durante 5 minutos → agregar 1 instancia (hasta un máximo de 3).
- **Scale-in**:
  - Si CPU < 40 % durante 10 minutos → eliminar 1 instancia (mínimo 1).

Esto permite:

- **Escalar horizontalmente** el backend Flask cuando hay más usuarios.
- Volver automáticamente a la capacidad mínima fuera de picos (elasticidad).

---

### 2.3.4. Azure Static Web Apps – Escalabilidad gestionada

Azure Static Web Apps ofrece:

- **Escalado automático gestionado por la plataforma** para el contenido estático.
- Uso de CDN y edge caching para mejorar tiempos de respuesta sin que el equipo tenga que gestionar servidores.

En la práctica:

- El costo y el esfuerzo de escalado del frontend son mínimos.
- La principal carga de procesamiento recae en App Service y PostgreSQL.

> *Colocar captura del recurso Static Web Apps mostrando el plan utilizado.*

---

### 2.3.5. Almacenamiento – Data Lake y Blob

El Data Lake está dimensionado para:

- Volumen inicial bajo (< 20 GB).
- Crecimiento proyectado controlado (decenas de GB).

La escalabilidad es **prácticamente ilimitada**, y se gestiona mediante:

- Aumento de capacidad de la cuenta de almacenamiento (automático en la práctica).
- Opcionales reglas de Lifecycle Management para mover datos antiguos a tiers más baratos (Cool).

---

## 2.4. Alta disponibilidad (HA)

Aunque se trata de un entorno académico/prototipo, la arquitectura sigue principios de alta disponibilidad:

### 2.4.1. Servicios gestionados con SLA

- **PostgreSQL en Azure**:
  - Alta disponibilidad gestionada por la plataforma.
  - SLA elevado (99.95–99.99 % según configuración).
- **App Service y Static Web Apps**:
  - Plataformas PaaS con múltiples instancias gestionadas por Azure.
- **Cuenta de almacenamiento (Data Lake + Blob)**:
  - Redundancia **LRS** por defecto (tres réplicas dentro de la misma región).

<img width="1864" height="908" alt="image" src="https://github.com/user-attachments/assets/a90cfa2d-72ee-42b2-bcf7-f3e33d116166" />

---

### 2.4.2. Red y acceso

- **Virtual Network + subredes**:
  - Segmentación lógica entre servicios de datos, backend y componentes de seguridad.
- **Network Security Groups + Azure Firewall**:
  - Reglas explícitas de entrada/salida reducen la superficie de ataque.
- **Private Endpoints + Private DNS Zone**:
  - Acceso interno a recursos de datos (Data Lake, PostgreSQL) sin exposición pública.

Este diseño disminuye el riesgo de caídas por ataques externos o configuraciones inseguras.

<img width="1862" height="906" alt="image" src="https://github.com/user-attachments/assets/4c291f22-b1ee-4c1d-92f6-52fec06d2c08" />

---

## 2.5. Estrategia de backup y Disaster Recovery (DR)

### 2.5.1. Objetivos de DR

- **RPO (Recovery Point Objective)** esperado:
  - Horas, dependiendo de la frecuencia de backups configurada.
- **RTO (Recovery Time Objective)** esperado:
  - Horas, dependiendo de los procedimientos de restauración.

Estos valores son adecuados para un entorno académico/prototipo, pero el diseño puede ajustarse a escenarios productivos.

---

### 2.5.2. Recovery Services Vault

Se utiliza **Recovery Services Vault** para gestionar copias de seguridad de recursos críticos:

- Backups de **PostgreSQL** (base de datos de modelo estrella).
- Opcionalmente, copias de App Service (configuración) y de la cuenta de almacenamiento.

**Configuración típica:**

- Frecuencia de backup: diaria.
- Retención: 30–35 días.
- Almacenamiento redundante: LRS (en este entorno).

<img width="1862" height="905" alt="image" src="https://github.com/user-attachments/assets/76fb28cd-c06d-4a37-88ce-66a760747560" />

---

### 2.5.3. Estrategia de backup por componente

| Componente               | Estrategia de backup                                                 | Comentarios clave                                   |
|-------------------------|----------------------------------------------------------------------|-----------------------------------------------------|
| Data Lake (Bronze/Silver/Gold) | Copias redundantes + export ocasional a otra cuenta / región opcional | Datos pueden regenerarse desde históricos CSV si es necesario. |
| CSV originales en Blob  | Conservación de los últimos meses como “fuente de verdad”            | Permiten reprocesar el ETL desde cero.             |
| PostgreSQL (DW)         | Backups automáticos gestionados por Azure + Recovery Services Vault  | Punto más crítico desde el punto de vista analítico. |
| App Service (backend)   | Código almacenado en GitHub + backups de configuración opcionales    | La infraestructura se puede recrear vía IaC/portal.|
| Static Web Apps         | Código en GitHub (fuente de despliegue)                              | Se vuelve a desplegar a partir del repositorio.    |
| Configuración de secretos (Key Vault) | Export de configuración (con cuidado) + documentación | Los secretos se reemiten en caso extremo.          |

---

### 2.5.4. Procedimiento de recuperación (ejemplo)

Escenario: pérdida de la base de datos PostgreSQL (corrupción lógica o fallo grave).

1. **Detección**  
   - Azure Monitor dispara una alerta de error crítico (por ejemplo, fallos de conexión constantes).

2. **Identificación del punto de restauración**  
   - El equipo revisa los backups disponibles en **Recovery Services Vault**.
   - Se elige un punto de restauración anterior al incidente (según RPO).

3. **Restauración de la base de datos**  
   - Se realiza la restauración a un nuevo servidor o sobre el actual (según la política).
   - Se actualizan las cadenas de conexión en **Azure Key Vault** si cambia el endpoint.

4. **Validación**  
   - Se ejecutan consultas de validación sobre el modelo estrella.
   - Se verifica que el dashboard vuelve a mostrar métricas correctas.

5. **Reprocesamiento opcional**  
   - Si es necesario, se reprocesa el ETL en Databricks a partir de las capas Bronze/Silver/Gold o desde los CSV originales.

---

  - Key Vault + Audit Logs  
  refuerza la seguridad y la gobernanza de la solución ante incidentes operativos y de seguridad.

Esta documentación, junto con las capturas de Azure, demuestra que la arquitectura no sólo funciona en condiciones normales, sino que está preparada para crecer, ajustarse a la demanda y recuperarse ante fallos, cumpliendo con los criterios de **escalabilidad, elasticidad, alta disponibilidad y DR** de la rúbrica de la práctica.
