
# Justificación de la Elección de Google Cloud Platform (GCP)

## 1. Contexto del proyecto

El proyecto implementa un **pipeline de datos automatizado**, basado en una arquitectura **Medallion**.
El flujo completo se compone de:

* Detección automática de archivos mediante un **dispatcher serverless**.
* Ejecución de un proceso **ELT** para la capa Bronce en **BigQuery**.
* Procesamiento batch con **PySpark** para las capas Plata y Oro.
* Consumo analítico final mediante **Power BI**.

El diseño prioriza **automatización, bajo acoplamiento, escalabilidad y costos controlados**, considerando un volumen de datos moderado y ejecuciones batch.

---

## 2. Criterios de selección de la nube

Para la elección de la plataforma cloud se evaluaron los siguientes criterios:

* Capacidad de procesamiento **Spark sin gestión de clústeres**.
* Servicios **serverless** para minimizar operación y mantenimiento.
* Almacenamiento analítico escalable y orientado a BI.
* Integración directa con **Power BI**.
* Modelo de costos alineado con **uso esporádico y académico**.
* Disponibilidad regional cercana a Perú para reducir latencia.

---

## 3. Razones para elegir Google Cloud Platform

### 3.1 Arquitectura serverless de extremo a extremo

GCP permite implementar el pipeline completo sin infraestructura persistente:

* **Cloud Functions** actúa como dispatcher, reaccionando a eventos de carga de archivos.
* **Dataproc Serverless** ejecuta jobs PySpark bajo demanda, escalando automáticamente y apagándose al finalizar.
* **BigQuery** funciona como data warehouse completamente administrado para las capas Bronce, Plata y Oro.

Este enfoque elimina la necesidad de administrar clústeres, servidores o pools de recursos.

---

### 3.2 BigQuery como núcleo analítico

BigQuery ofrece ventajas clave para el proyecto:

* Escalamiento transparente sin configuración.
* SQL estándar (ANSI) adecuado para análisis y reporting.
* Integración nativa y estable con **Power BI**.
* Modelo *pay-per-query*, ideal para cargas de trabajo intermitentes.

Esto lo convierte en una opción óptima para la capa Oro y el consumo final.

---

### 3.3 Procesamiento Spark eficiente y económico

El uso de **Dataproc Serverless** permite:

* Ejecutar PySpark sin clústeres permanentes.
* Escalar dinámicamente según la carga.
* Pagar únicamente por el tiempo real de ejecución.

Para un proyecto con ejecuciones batch poco frecuentes, este modelo resulta más eficiente que alternativas basadas en clústeres tradicionales.

---

### 3.4 Costos y viabilidad académica

GCP destaca por su estructura de costos:

* Ausencia de costos fijos en BigQuery.
* Procesamiento Spark facturado por segundo.
* Amplio uso del *free tier* en escenarios de bajo volumen.

Esto permite desarrollar y operar el proyecto sin incurrir en costos significativos, manteniendo una arquitectura alineada con prácticas reales de la industria.

---

## 4. Conclusión

Google Cloud Platform fue seleccionada porque permite implementar una arquitectura Medallion completamente serverless, con procesamiento Spark bajo demanda, almacenamiento analítico escalable y una integración directa con Power BI. La combinación de simplicidad operativa, eficiencia en costos y madurez técnica la convierte en la opción más adecuada para este proyecto de Inteligencia de Negocios.