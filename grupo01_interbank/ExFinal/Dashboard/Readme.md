## KPIs FINANCIEROS (RESULTADO DEL NEGOCIO)
### Utilidad Total
* ¿Qué mide? Resultado total generado.
* Objetivo del Script: Calcular la suma total de la columna utilidad de la tabla project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING.

```sql
SELECT SUM(utilidad) AS utilidad_total
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING`;
```

### Utilidad Mensual
* Objetivo del Script: Calcular la utilidad total generada por cada mes y año. Para ello, agrupa la suma de utilidad por df.anio y df.mes_num, uniendo la tabla de hechos con la tabla de dimensiones de fecha (DIM_FECHA).

```sql
SELECT
  df.anio,
  df.mes_num,
  SUM(f.utilidad) AS utilidad_mensual
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_FECHA` df
  ON f.id_fecha = df.id_fecha
GROUP BY df.anio, df.mes_num;
```

### Crecimiento Mes a Mes (MoM %)
* Objetivo del Script: Calcular el porcentaje de crecimiento de la utilidad comparado con el mes anterior. Utiliza una Common Table Expression (m) para obtener la utilidad mensual y luego aplica una función de ventana (LAG) para obtener la utilidad del mes inmediatamente anterior y calcular el porcentaje de crecimiento (MoM %).
```sql
WITH m AS (
  SELECT
    df.anio,
    df.mes_num,
    SUM(f.utilidad) AS utilidad
  FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
  JOIN `project-sin-477115.ESTRELLA.DIM_FECHA` df
    ON f.id_fecha = df.id_fecha
  GROUP BY df.anio, df.mes_num
)
SELECT
  *,
  SAFE_DIVIDE(
    (utilidad - LAG(utilidad,1 OVER (ORDER BY anio, mes_num)),
    LAG(utilidad) OVER (ORDER BY anio, mes_num)
  ) * 100 AS crecimiento_pct
FROM m;
```
### DASHBOARD
<img width="890" height="396" alt="image" src="https://github.com/user-attachments/assets/cfb1bd83-09fb-4e5c-ab2a-b7ed84649c41" />

## KPIs DE VOLUMEN Y EFICIENCIA

### Volumen Total Cambiado
* Objetivo del Script: Calcular la suma total del volumen_cambiado (volumen negociado o movido) de la tabla FACT_UTILIDAD_TRADING.
```sql
SELECT SUM(volumen_cambiado) AS volumen_total
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING`;
```

### Margen de Utilidad (%)
* Objetivo del Script: Calcular el margen de utilidad como porcentaje, dividiendo la suma total de utilidad entre la suma total del volumen_cambiado. Utiliza SAFE_DIVIDE para evitar errores de división por cero.

```sql
SELECT
  SAFE_DIVIDE(SUM(utilidad), SUM(volumen_cambiado)) * 100 AS margen_utilidad
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING`;
```

### Volumen vs Utilidad
* Seleccionar las columnas volumen_cambiado y utilidad para cada registro de la tabla. Esto permite un análisis detallado a nivel de fila para identificar operaciones donde el volumen fue alto pero la utilidad fue baja (o negativa).


```sql
SELECT
  volumen_cambiado,
  utilidad
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING`;
```

### DASHBOARD
<img width="890" height="380" alt="image" src="https://github.com/user-attachments/assets/e1501fa0-1b08-481c-a025-2581aeb4afa0" />


## KPIs DE CLIENTES

## Clientes Activos
* Objetivo del Script: Contar el número total de clientes únicos (id_cliente) que han realizado operaciones en la tabla FACT_UTILIDAD_TRADING.

```sql
SELECT COUNT(DISTINCT id_cliente) AS clientes_activos
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING`;
```

### Utilidad Promedio por Cliente
* Objetivo del Script: Calcular la utilidad promedio generada por cada cliente. Primero, calcula la utilidad total por cliente (subconsulta) y luego saca el promedio de esos totales.

```sql
SELECT AVG(utilidad_cliente) AS utilidad_promedio
FROM (
  SELECT id_cliente, SUM(utilidad) AS utilidad_cliente
  FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING`
  GROUP BY id_cliente
);
```

### Top 10 Clientes por Utilidad
* Objetivo del Script: Identificar y mostrar los nombres de los 10 clientes que han generado la mayor utilidad. La consulta une la tabla de hechos (FACT_UTILIDAD_TRADING) con la tabla de dimensiones de cliente (DIM_CLIENTE) para obtener el nombre, agrupa por cliente, ordena de forma descendente por utilidad y limita el resultado a 10.


```sql
SELECT
  dc.nombre_cliente,
  SUM(f.utilidad) AS utilidad
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_CLIENTE` dc
  ON f.id_cliente = dc.id_cliente
GROUP BY dc.nombre_cliente
ORDER BY utilidad DESC
LIMIT 10;
```
### DASHBOARD
<img width="890" height="368" alt="image" src="https://github.com/user-attachments/assets/fe06f4a2-7219-4101-a90b-6ad2e8d010c2" />

## KPIs COMERCIALES (CANAL / EJECUTIVO)

### Utilidad por Canal
* Objetivo del Script: Calcular la utilidad total generada por cada canal comercial. Une la tabla de hechos con la tabla de dimensiones de canal (DIM_CANAL) y agrupa la suma de utilidad por el nombre del canal.

```sql
SELECT
  dca.nombre_canal,
  SUM(f.utilidad) AS utilidad
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_CANAL` dca
  ON f.id_canal = dca.id_canal
GROUP BY dca.nombre_canal;
```

### Ranking de Ejecutivos
* Objetivo del Script: Generar un ranking de ejecutivos comerciales basado en la utilidad total que han generado. Une la tabla de hechos con la tabla de dimensiones de ejecutivo (DIM_EJECUTIVO), agrupa por el nombre del ejecutivo y ordena los resultados de forma descendente por utilidad.

```sql
SELECT
  de.nombre_ejecutivo,
  SUM(f.utilidad) AS utilidad
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_EJECUTIVO` de
  ON f.id_ejecutivo = de.id_ejecutivo
GROUP BY de.nombre_ejecutivo
ORDER BY utilidad DESC;
```

### Distribución Canal vs Cliente
* Objetivo del Script: Contar la cantidad de clientes únicos que están asociados a cada canal. Une la tabla de hechos con la tabla de dimensiones de canal, y luego cuenta los IDs de cliente distintos (COUNT(DISTINCT f.id_cliente)) agrupando por el nombre del canal.

```sql
SELECT
  dca.nombre_canal,
  COUNT(DISTINCT f.id_cliente) AS clientes
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_CANAL` dca
  ON f.id_canal = dca.id_canal
GROUP BY dca.nombre_canal;
```
### DASHBOARD

<img width="890" height="252" alt="image" src="https://github.com/user-attachments/assets/c83ed9c2-5fe6-4707-b1c9-65d431164581" />


## SEGMENTOS Y COMUNICACIONES
### Total Comunicaciones 2025
* Objetivo del Script: Contar el número total de comunicaciones registradas en la tabla de hechos que ocurrieron durante el año 2025. Une las dimensiones de Comunicación y Fecha para filtrar por el año.


```sql
SELECT
  COUNT(id_comunicacion) AS total_comunicaciones_2025
FROM `project-sin-477115.ESTRELLA.DIM_COMUNICACION` dc
JOIN `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
  ON f.id_comunicacion = dc.id_comunicacion
JOIN `project-sin-477115.ESTRELLA.DIM_FECHA` df
  ON f.id_fecha = df.id_fecha
WHERE df.anio = 2025;
```

### Comunicaciones por Mes
* Objetivo del Script: Contar el número total de comunicaciones por cada mes y año. Agrupa el conteo por df.anio y df.mes_num para mostrar una serie temporal de la actividad de comunicación.

```sql
SELECT
  df.anio,
  df.mes_num,
  COUNT(f.id_comunicacion) AS comunicaciones_mes
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_FECHA` df
  ON f.id_fecha = df.id_fecha
GROUP BY df.anio, df.mes_num
ORDER BY df.anio, df.mes_num;
```

### Comunicaciones por Segmento
* Objetivo del Script: Contar el número total de comunicaciones por cada segmento de cliente. Une la tabla de hechos con la dimensión de Cliente y agrupa el conteo por dc.segmento_fx para evaluar qué segmentos reciben (o generan) más comunicaciones.

```sql
SELECT
  dc.segmento_fx,
  COUNT(f.id_comunicacion) AS total_comunicaciones
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_CLIENTE` dc
  ON f.id_cliente = dc.id_cliente
GROUP BY dc.segmento_fx
ORDER BY total_comunicaciones DESC;
```

### Utilidad por Comunicación
* Objetivo del Script: Calcular la utilidad total generada, desglosada por año, mes y segmento de cliente. Permite evaluar la rentabilidad de cada segmento a lo largo del tiempo.

```sql
SELECT
  df.anio,
  df.mes_num,
  dc.segmento_fx,
  SUM(f.utilidad) AS utilidad_total
FROM `project-sin-477115.ESTRELLA.FACT_UTILIDAD_TRADING` f
JOIN `project-sin-477115.ESTRELLA.DIM_CLIENTE` dc
  ON f.id_cliente = dc.id_cliente
JOIN `project-sin-477115.ESTRELLA.DIM_FECHA` df
  ON f.id_fecha = df.id_fecha
GROUP BY df.anio, df.mes_num, dc.segmento_fx
ORDER BY df.anio, df.mes_num;
```

### DASHBOARD

<img width="890" height="233" alt="image" src="https://github.com/user-attachments/assets/b4ff4500-6078-44b3-b0ff-9defa323d4fe" />
