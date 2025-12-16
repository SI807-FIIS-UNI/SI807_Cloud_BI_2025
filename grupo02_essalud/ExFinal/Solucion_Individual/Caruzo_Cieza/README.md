# 📄 README.md

## Solución BI Cloud – Análisis de No-Show en Citas Médicas

**Curso:** Sistemas de Inteligencia de Negocios  
**Examen Final – Pregunta 3**  
**Alumno:** David Caruzo Cieza  
**Nube:** Google Cloud Platform (GCP)

---

## 1. Objetivo de la Solución

El objetivo de esta solución de Inteligencia de Negocios es **identificar los factores asociados a la inasistencia (“No-Show”) de pacientes a citas médicas**, con la finalidad de **mejorar los procesos de confirmación de citas y reducir pérdidas operativas** en el sistema de salud.

La solución permite analizar el comportamiento de los pacientes desde diferentes perspectivas:

- Demográfica (edad, género)
- Temporal (día, hora)
- Operativa (anticipación de la cita)
- Uso de recordatorios (SMS)

---

## 2. Selección de la Nube y Justificación Técnica

### ☁️ Nube Seleccionada: Google Cloud Platform (GCP)

La solución fue implementada en **Google Cloud Platform** debido a las siguientes razones técnicas:

- **Google Cloud Storage (GCS)** permite implementar un Data Lake escalable bajo el enfoque **bronce – plata – oro**.
- **BigQuery** ofrece un motor analítico columnar, altamente optimizado para consultas BI y conexión directa con herramientas de visualización.
- Integración nativa con herramientas de análisis como **Power BI**, sin necesidad de capas intermedias.
- Escalabilidad y bajo overhead operativo, ideal para soluciones BI cloud-native.

Esta selección permite una arquitectura **modular, reproducible y alineada a estándares empresariales de BI**.

---

## 3. Dataset Utilizado

Se utilizó el dataset público:

**Kaggle – Medical Appointment No Shows (May 2016)**

El dataset contiene información histórica de citas médicas, incluyendo:

- Identificador del paciente y de la cita
- Fecha de programación y fecha de atención
- Edad, género y condiciones médicas
- Indicador de asistencia o inasistencia (*No-show*)

**Nota:** El dataset fue cargado mediante CLI directamente a la capa **bronce/raw**.

**[CAPTURA AQUÍ: archivo CSV cargado en bronce/raw vía `gsutil ls`]**

---

## 4. Arquitectura de la Solución BI

La arquitectura implementada sigue un enfoque **Data Lake + Data Warehouse**, estructurado en capas:

CSV (Kaggle)
   ↓
GCS - BRONCE
   ├── raw
   ├── processed
   └── curated
   ↓
BigQuery - PLATA
   ├── Dimensiones
   └── Tabla de Hechos
   ↓
BigQuery - ORO
   ├── KPIs agregados
   ↓
Power BI
   ├── Dashboard Ejecutivo
   └── Dashboard Analítico


**[CAPTURA AQUÍ: diagrama general de arquitectura o estructura de buckets]**

---

## 5. Diseño del Data Lake (Bronce – Plata – Oro)

El Data Lake fue diseñado bajo el principio de **separación de responsabilidades por capa**:

### 🥉 Capa Bronce

- Almacena el dato original sin pérdida de información.
- Permite limpieza progresiva y validaciones.
- Facilita auditoría y trazabilidad.

### 🥈 Capa Plata

- Contiene el **modelo dimensional estrella**.
- Datos estructurados para análisis.
- Optimizada para consultas analíticas.

### 🥇 Capa Oro

- Contiene **KPIs agregados y listos para visualización**.
- Reduce complejidad de consultas en dashboards.
- Garantiza consistencia de métricas.

---

## 6. Problemática de Negocio

El **No-Show** representa una pérdida directa para el sistema de salud, ya que:

- Se asignan recursos médicos que no son utilizados.
- Se reduce la eficiencia operativa.
- Se incrementan costos indirectos.

La solución busca responder preguntas clave como:

- ¿Qué perfiles de pacientes presentan mayor tasa de no-show?
- ¿En qué días u horarios ocurre con mayor frecuencia?
- ¿La anticipación de la cita influye en la asistencia?
- ¿El envío de SMS reduce el no-show?

---

## 7. KPIs Definidos

Los principales indicadores generados en la capa oro son:

- **Tasa global de No-Show**
- **No-Show por rango de edad y género**
- **No-Show por día y hora**
- **No-Show por anticipación (lead time)**

Estos KPIs alimentan directamente los dashboards ejecutivos y analíticos.

---

