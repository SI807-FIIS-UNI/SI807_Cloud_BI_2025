# 📁 03_Modelo_Dimensional

## 3.1. Diagrama del modelo dimensional

El siguiente diagrama representa la estructura lógica del modelo estrella.

![Modelo estrella](../docs/imagenes/03.Modelo-estrella.png)


---

## 3.2. Tablas de dimensión

Las tablas de dimensión contienen atributos descriptivos que permiten segmentar y contextualizar las métricas.

**Dimensiones consideradas:**

* `dim_tiempo`
* `dim_aerolinea`
* `dim_origen`
* `dim_destino`
* `dim_causa`


---

## 3.3. Tabla de hechos

La **tabla de hechos centraliza** todas las métricas cuantitativas relacionadas con los vuelos, permitiendo realizar análisis analíticos eficientes y agregaciones por las distintas dimensiones (tiempo, aerolínea, aeropuerto de origen y destino, y causas de retraso).

Esta tabla incluye información como:

* **dep_delay**: minutos de retraso en la salida del vuelo
* **arr_delay**: minutos de retraso en la llegada
* **delay_minutes**: retraso total acumulado
* **vuelos_retrasados**: conteo de vuelos que presentan retraso
* **id_tiempo, id_aerolinea, id_origen, id_destino, id_causa**: claves foráneas que referencian a las dimensiones correspondientes



---

## 3.4. Scripts de generación

La construcción de las capas correspondientes al **modelo dimensional** (por ende, también la creación del modelo estrella en la capa oro) se realiza mediante un **job de Spark**, el cual se encuentra implementado en el siguiente archivo:


```text
resources/SparkJobs/jb_medallion.py
```

Este script forma parte del directorio `resources` y es ejecutado **de manera automática** por el componente `final-dispatcher` cuando se detecta la llegada de un nuevo archivo en la ruta `bronce/raw` del bucket de Google Cloud Storage.

En consecuencia, la **reproducibilidad del proceso ETL** queda garantizada una vez que el entorno ha sido desplegado correctamente mediante la ejecución del script `deploy.sh`, sin requerir intervenciones manuales adicionales para el procesamiento de datos.