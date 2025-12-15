# 📊 Implementación de Big Data para la Optimización de la Cadena de Valor en Nettalco

## 🧵 Descripción del Proyecto

Este proyecto presenta la **implementación de una arquitectura Big Data** orientada a optimizar los procesos productivos, logísticos y comerciales de **Nettalco S.A.**, empresa textil peruana dedicada a la fabricación y exportación de prendas de alta calidad.

La solución propuesta integra **procesamiento distribuido**, **analítica predictiva**, **automatización** y **visualización de datos**, permitiendo una toma de decisiones basada en datos, reducción de costos operativos y mejora de la competitividad internacional.

---

## 🎯 Objetivos

* Optimizar la **cadena de valor textil** mediante el uso de Big Data.
* Automatizar procesos críticos de producción y control de calidad.
* Analizar el comportamiento de clientes y patrones de venta.
* Implementar **predicción de ventas** para una mejor planificación productiva.
* Incorporar criterios de **sostenibilidad y eficiencia operativa**.

---

## 🏗️ Arquitectura de la Solución

La arquitectura del proyecto está basada en **Google Cloud Platform** y se compone de las siguientes capas:

* **Fuentes de datos**
  ERP Exactus, archivos CSV de producción, sensores IoT y APIs externas.

* **Almacenamiento**

  * Data Lake: Google Cloud Storage (datos crudos)
  * Data Warehouse: BigQuery (datos analíticos)

* **Procesamiento**

  * Batch: PySpark sobre Dataproc
  * Microbatch y análisis periódico

* **Análisis y Visualización**
  Dashboards interactivos en Looker Studio

---

## 🔄 Proceso ETL

1. **Extracción**
   Lectura de archivos CSV y datos estructurados desde Cloud Storage.

2. **Transformación**

   * Limpieza de datos (nulos, duplicados, formatos)
   * Cálculo de métricas clave (eficiencia operativa, ventas por cliente)
   * Agrupaciones y segmentación por fecha, cliente, talla y estilo

3. **Carga**
   Datos procesados almacenados en BigQuery para análisis y reporting.

---

## 📈 Principales Métricas Analizadas

* Total de prendas vendidas por cliente
* Productos y estilos más vendidos
* Eficiencia operativa diaria
* Ventas por franja horaria
* Frecuencia y promedio de compra por cliente
* Predicción de ventas mediante promedio móvil

---

## 🛠️ Tecnologías Utilizadas

* **Google Cloud Storage**
* **BigQuery**
* **PySpark**
* **SQL**
* **Looker Studio**
* **IoT (conceptual)**

---

## 🌱 Enfoque en Sostenibilidad

El proyecto considera prácticas sostenibles como:

* Reducción de desperdicios mediante control de calidad basado en datos
* Optimización del uso de recursos productivos
* Soporte a estándares ambientales exigidos por mercados internacionales

---

## 📊 Resultados Esperados

* Incremento de hasta **20% en la capacidad productiva**
* Reducción significativa de costos operativos
* Mejora en la calidad del producto y tiempos de entrega
* Mayor visibilidad del negocio a través de dashboards analíticos
* Fortalecimiento de la competitividad global de Nettalco

---

## 👥 Autores

* Roger Salvador Loayza Segura
* Francisco Leonel Grijalva Parra
* **Daniel Mauricio Otero Vicente**

---

## 📄 Contexto Académico

Este proyecto forma parte de un **trabajo académico de Big Data**, enfocado en la aplicación práctica de tecnologías de análisis de datos en la industria textil peruana.

---

✨ *Proyecto orientado a la transformación digital, la eficiencia operativa y la toma de decisiones basada en datos.*
