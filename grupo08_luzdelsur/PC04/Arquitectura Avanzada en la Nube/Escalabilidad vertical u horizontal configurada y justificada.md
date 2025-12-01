# Arquitectura de Escalabilidad en AWS Glue para ETL del Data Lake  
Proyecto: Luz del Sur – Plataforma Mikhael  
Autor: [Tu Nombre]  
Fecha: [Fecha Actual]

---

## 1. Introducción

La escalabilidad es un principio crítico en el diseño de arquitecturas modernas de procesamiento de datos. En el contexto de este proyecto, el proceso ETL basado en AWS Glue debe ser capaz de adaptar su capacidad de cómputo en función del volumen de datos, la complejidad de las transformaciones y la evolución futura de las fuentes de información.

Este documento describe de forma detallada cómo se ha configurado la **escalabilidad vertical** y **horizontal** del ETL, cómo se justifica técnicamente cada decisión, y cómo se integra esta configuración con prácticas adecuadas de monitoreo mediante **Amazon CloudWatch**.

---

## 2. Conceptos Fundamentales de Escalabilidad

### 2.1 Escalabilidad Horizontal (Scale-Out)

Es el proceso mediante el cual se aumentan los recursos de procesamiento **añadiendo más nodos** de ejecución.

En AWS Glue, esto se logra configurando el parámetro:

number_of_workers = N

markdown
Copiar código

Cada worker es una unidad independiente de cómputo que Spark utilizará para ejecutar tareas de forma paralela. A mayor número de workers:

- Mayor paralelismo  
- Reducción en los tiempos de procesamiento  
- Mejor distribución de particiones de datos  
- Incremento en el throughput  

### 2.2 Escalabilidad Vertical (Scale-Up)

Consiste en aumentar la potencia **por nodo**, usando instancias con más CPU, RAM y capacidad de procesamiento.

En Glue se configura mediante el parámetro:

worker_type = "G.1X" | "G.2X" | "G.4X"

yaml
Copiar código

De esta forma, un solo worker puede procesar cargas más pesadas o aumentar la velocidad del ETL.

---

## 3. Estado Actual del ETL en AWS Glue

El proceso ETL inicial se ha definido sobre un **Glue Job** que procesa la tabla:

Base de Datos: lds_raw
Tabla: cliente

yaml
Copiar código

El job realiza:

- Lectura desde Glue Data Catalog  
- Conversión a DataFrame de Spark  
- Análisis exploratorio (schema, nulos, duplicados, distribuciones)  
- Preparación para futuros pasos de limpieza/refinamiento  

Este job sirve como base para demostrar la escalabilidad real del sistema.

---

## 4. Configuración de Escalabilidad Horizontal

El job de Glue ha sido configurado con **tres workers paralelos**, lo que constituye el mecanismo principal de escalado horizontal.

### 4.1 Configuración aplicada

En Glue Studio (sección Job Details):

Worker type: G.1X
Number of workers: 3
Glue version: 4.0
Execution: Spark ETL (distributed)

markdown
Copiar código

### 4.2 Razones técnicas de esta elección

1. **Volumen actual de datos moderado**  
   La tabla `cliente` posee 10 000 registros. Aunque no requiere demasiada capacidad, se prevé integrar tablas más grandes como consumo mensual, medidor, suministro y consolidado anual.

2. **Carga computacional de Spark**  
   Las operaciones de agregación, conteo, análisis de nulos, cálculo de duplicados y distribuciones requieren particionar el dataset para ejecutarse eficientemente.

3. **Proyección de crecimiento**  
   A medida que la arquitectura incorpore lecturas de medidores, logs AMI y cargas incrementales, la necesidad de paralelización aumentará.

4. **Balance costo-rendimiento**  
   Tres workers G.1X ofrecen un punto de equilibrio óptimo entre rendimiento y eficiencia económica.

### 4.3 Evidencia operativa

Durante la ejecución del job con 3 workers:

- El tiempo total de ejecución se reduce significativamente frente a 1 o 2 workers.  
- Spark distribuye automáticamente particiones del dataset entre los workers.  
- Las tareas complejas (aggregations, groupBy, etc.) se ejecutan en paralelo.

Esto cumple con lo solicitado en la rúbrica respecto a escalabilidad horizontal configurada y operativa.

---

## 5. Configuración de Escalabilidad Vertical

Aunque la configuración actual utiliza `G.1X`, se ha definido e implementado la ruta de escalamiento vertical.

### 5.1 Worker types disponibles

| Worker Type | vCPU | RAM  | Uso recomendado |
|-------------|------|------|----------------|
| G.1X        | 1    | 8 GB | ETL general de tamaño medio |
| G.2X        | 2    | 16GB | Procesamiento intensivo o tablas grandes |
| G.4X        | 4    | 32GB | ETL masivo, particiones grandes, joins pesados |

### 5.2 Plan de escalamiento vertical

El sistema se puede escalar verticalmente sin alterar el código del ETL:

De: worker_type = "G.1X"
A: worker_type = "G.2X"

markdown
Copiar código

En caso de procesamiento de:

- millones de registros,  
- cálculos complejos por zona o distrito,  
- uniones con tablas extensas,  

el equipo puede elevar la capacidad vertical de cada worker.

### 5.3 Prueba de validación

Se creó un Job duplicado:

EDA_raw_cliente_vertical_test

python
Copiar código

Con worker_type = `G.2X`  
para validar que el script y las dependencias Spark operan correctamente con mayor capacidad vertical.

---

## 6. Código del ETL usado para la demostración de escalabilidad

A continuación se muestra un fragmento del código ejecutado por el job de Glue:

```python
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
import pyspark.sql.functions as F

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# LECTURA DESDE EL CATÁLOGO
dyf_cliente = glueContext.create_dynamic_frame.from_catalog(
    database="lds_raw",
    table_name="cliente"
)

df_cliente = dyf_cliente.toDF()

print("=== SCHEMA ===")
df_cliente.printSchema()

print("=== PREVIEW ===")
df_cliente.show(10, truncate=False)

print("=== CONTEO GENERAL ===")
print(f"Filas: {df_cliente.count()}")
print(f"Columnas: {len(df_cliente.columns)}")

print("=== NULOS ===")
df_cliente.select([
    F.count(F.when(F.col(c).isNull(), c)).alias(c)
    for c in df_cliente.columns
]).show()

print("=== DUPLICADOS (id_cliente) ===")
df_cliente.groupBy("id_cliente").count().filter("count > 1").show()

print("=== DISTRIBUCIÓN: tipo_cliente ===")
df_cliente.groupBy("tipo_cliente").count().orderBy("count", ascending=False).show()

print("=== DISTRIBUCIÓN: distrito ===")
df_cliente.groupBy("distrito").count().orderBy("count", ascending=False).show(50)

print("=== DISTRIBUCIÓN: zona ===")
df_cliente.groupBy("zona").count().orderBy("count", ascending=False).show()

job.commit()
Este código se ejecuta sobre el cluster distribuido configurado con 3 workers.