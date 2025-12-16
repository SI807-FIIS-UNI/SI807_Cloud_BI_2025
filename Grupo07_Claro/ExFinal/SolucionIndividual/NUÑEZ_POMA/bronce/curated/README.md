# Documentación Técnica: Fase 3.2 - Transformación y Modelado (Capas Plata y Oro)

## 1. Estrategia de Procesamiento Híbrido
Para la fase de transformación se adoptó un enfoque híbrido que aprovecha las fortalezas de Python y SQL:

1.  **Python (Pandas) para Parsing Complejo:** Se utilizó Python para procesar la columna `Product`, la cual contenía listas de cadenas de texto (ej. `['Prod A', 'Prod B']`). Python permite desglosar estas estructuras y normalizarlas eficientemente para generar los catálogos de dimensiones.
2.  **BigQuery (SQL) para Procesamiento Masivo:** La construcción de la tabla de hechos y el cruce de datos (JOINs) se delegó a BigQuery. Su motor distribuido permite procesar el millón de registros y realizar agregaciones en segundos, superando las limitaciones de memoria de un entorno local.

## 2. Diseño del Modelo Dimensional (Capa Plata)
Se implementó un **Esquema de Estrella (Star Schema)**, considerado el estándar de industria para sistemas analíticos (OLAP) por su eficiencia en consultas de lectura.

### Componentes del Modelo:
* **Tabla de Hechos (`fact_ventas`):** Tabla central transaccional. Contiene las claves foráneas hacia las dimensiones, métricas aditivas (`cantidad`, `precio_unitario`) y la dimensión temporal (`fecha_venta`).
    * *Normalización:* Se aplicó una técnica de `UNNEST` y `CROSS JOIN` para normalizar la relación "uno a muchos" de los productos. Una transacción con múltiples productos se desglosó en múltiples filas, permitiendo un análisis granular por ítem.
* **Tablas de Dimensión (`dim_*`):** Tablas periféricas desnormalizadas (`dim_city`, `dim_product`, `dim_customer`, etc.) que contienen los atributos descriptivos. Esto reduce la redundancia de texto en la tabla de hechos, optimizando el almacenamiento y el rendimiento.

## 3. Generación de KPIs (Capa Oro)
Sobre el modelo dimensional limpio, se generaron vistas agregadas de alto valor para el negocio. Se aplicaron funciones de agregación (`COUNT`, `SUM`, `AVG`) y agrupación lógica para responder a preguntas clave:

1.  **Desempeño Geográfico:** Ventas totales y volumen de transacciones por ciudad.
2.  **Comportamiento del Cliente:** Segmentación por categoría de consumidor.
3.  **Análisis de Producto:** Ranking de los productos con mayor rotación e ingresos.
4.  **Tendencia Temporal:** Evolución mensual de las ventas.

## 4. Persistencia y Automatización
El ciclo de vida del dato se cierra exportando los resultados calculados desde BigQuery hacia la carpeta `/curated` en Cloud Storage. Esto garantiza que la información procesada esté disponible de manera persistente y desacoplada del motor de base de datos, facilitando su integración con herramientas de Business Intelligence externas y cumpliendo con los requisitos de estructuración del Data Lake.