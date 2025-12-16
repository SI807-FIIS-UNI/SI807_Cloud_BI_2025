# Flujo de Implementación
## 1. Creación del Grupo de Recurso
<img width="886" height="449" alt="image" src="https://github.com/user-attachments/assets/d1ed9148-c217-4e6e-907e-37248636441f" />

## 2. Creación del Storage Account (Datalake)
<img width="886" height="433" alt="image" src="https://github.com/user-attachments/assets/ec94b23b-1e64-47d5-8e44-23faf13c3709" />

### 2.1. Creación de los Contenedores en el Datalake
<img width="886" height="431" alt="image" src="https://github.com/user-attachments/assets/302db43b-8f37-4b1e-8a56-229d27f596a5" />

### 2.2. Creación de las Carpetas en el Datalake

#### 2.2.1 En bronce

- /raw
- /processed
- /curated

<img width="886" height="451" alt="image" src="https://github.com/user-attachments/assets/53e7c87d-fa38-4708-9494-2f7335845e39" />

- Usando CLI cargar CSV desde el escritorio: El archivo CSV llamado "" está en la carpeta "csv crudo"
<img width="1060" height="586" alt="image" src="https://github.com/user-attachments/assets/8fef19b0-e6f4-4f0f-81ab-ed4ddb99797b" />

```
az login
az storage blob upload `
  --account-name azdatalakefinal `
  --container-name bronce `
  --name raw/Retail_Transactions_Dataset.csv `
  --file "$env:USERPROFILE\Desktop\csv crudo\Retail_Transactions_Dataset.csv" `
  --auth-mode key
```

<img width="838" height="96" alt="image" src="https://github.com/user-attachments/assets/721d520a-f67b-4d25-ab52-c00f4da005ba" />
<img width="842" height="201" alt="image" src="https://github.com/user-attachments/assets/3713722c-2868-4c7c-b484-31e63bdfddaf" />
<img width="1629" height="250" alt="image" src="https://github.com/user-attachments/assets/9e22e6e1-886d-424d-a447-a208e9a436d8" />

#### 2.2.2 En plata

- /dimensiones
- /hechos

<img width="886" height="449" alt="image" src="https://github.com/user-attachments/assets/9ca9555b-a41c-4105-a118-7f1ff84fdbef" />

#### 2.2.3 En oro

- /kpis

<img width="886" height="448" alt="image" src="https://github.com/user-attachments/assets/ad87b0b4-01a6-4470-aebd-44768ba1334c" />

- Definir KPIs

Tipo de KPI | KPI | Descripción | Fórmula | Columnas Utilizadas
---|---|---|---|---
1 | Por fila (ETL) | Monto Total de Transacción | Valor total pagado en una transacción | `monto_total` | `fact_transacciones.monto_total`
2 | Por fila (ETL) | Total de Unidades | Cantidad total de ítems comprados en la transacción | `total_unidades` | `fact_transacciones.total_unidades`
3 | Por fila (ETL) | Precio Promedio Unitario | Precio promedio por unidad en la transacción | `monto_total / total_unidades` | `monto_total`, `total_unidades`
4 | Por fila (ETL) | Indicador de Descuento | Indica si la transacción tuvo descuento | `descuento_aplicado` | `fact_transacciones.descuento_aplicado`
5 | Por fila (ETL) | Ticket Unitario Normalizado | Métrica base para comparaciones entre transacciones | `precio_promedio_unitario` | `monto_total`, `total_unidades`
6 | Por fila (ETL) | Cantidad de Productos Distintos | Número de productos diferentes en la transacción | `COUNT(producto_id)` (tabla puente) | `fact_transaccion_producto.producto_id`
7 | Global (Dashboard) | Ventas Totales | Ingresos totales según filtros aplicados | `SUM(monto_total)` | `fact_transacciones.monto_total`
8 | Global (Dashboard) | Total de Transacciones | Número total de ventas realizadas | `COUNT(transaccion_id)` | `fact_transacciones.transaccion_id`
9 | Global (Dashboard) | Ticket Promedio | Gasto promedio por transacción | `SUM(monto_total) / COUNT(transaccion_id)` | `monto_total`, `transaccion_id`
10 | Global (Dashboard) | Unidades Vendidas | Total de unidades vendidas | `SUM(total_unidades)` | `fact_transacciones.total_unidades`
11 | Global (Dashboard) | Precio Promedio Global | Precio promedio por unidad vendida | `SUM(monto_total) / SUM(total_unidades)` | `monto_total`, `total_unidades`
12 | Global (Dashboard) | % Transacciones con Descuento | Proporción de transacciones con descuento | `SUM(descuento_aplicado::int) / COUNT(*)` | `descuento_aplicado`
13 | Global (Dashboard) | Ventas por Producto | Ingresos por producto vendido | `SUM(monto_total)` (join puente) | `fact_transacciones`, `fact_transaccion_producto`, `dim_producto`
14 | Global (Dashboard) | Productos Más Vendidos | Ranking de productos más comprados | `COUNT(producto_id)` | `fact_transaccion_producto.producto_id`

## 2.3 Dar Permisos CORS GET

<img width="1339" height="422" alt="image" src="https://github.com/user-attachments/assets/a41123fe-377a-43c2-9494-62ecb1d62ab7" />

## 3. Crear el PostgreSQL

<img width="886" height="448" alt="image" src="https://github.com/user-attachments/assets/727343f8-db20-4693-9715-7312246551c0" />

### 3.1. Crear Tablas Dimensionales (SQL)

```
DROP TABLE IF EXISTS fact_transaccion_producto CASCADE;
DROP TABLE IF EXISTS fact_transacciones CASCADE;

DROP TABLE IF EXISTS dim_producto CASCADE;
DROP TABLE IF EXISTS dim_tiempo CASCADE;
DROP TABLE IF EXISTS dim_cliente CASCADE;
DROP TABLE IF EXISTS dim_tienda CASCADE;
DROP TABLE IF EXISTS dim_metodo_pago CASCADE;
DROP TABLE IF EXISTS dim_temporada CASCADE;
DROP TABLE IF EXISTS dim_promocion CASCADE;

-- DIMENSIONES
CREATE TABLE dim_tiempo (
  tiempo_id BIGINT PRIMARY KEY,
  fecha DATE NOT NULL UNIQUE,
  anio INTEGER NOT NULL,
  mes INTEGER NOT NULL,
  mes_nombre VARCHAR(20) NOT NULL,
  trimestre INTEGER NOT NULL,
  dia INTEGER NOT NULL,
  dia_semana INTEGER NOT NULL,
  dia_semana_nombre VARCHAR(20) NOT NULL,
  semana_anio INTEGER NOT NULL,
  es_fin_semana BOOLEAN NOT NULL
);

CREATE TABLE dim_cliente (
  cliente_id BIGINT PRIMARY KEY,
  nombre_cliente VARCHAR(255) NOT NULL,
  categoria_cliente VARCHAR(50) NOT NULL
);

CREATE TABLE dim_tienda (
  tienda_id BIGINT PRIMARY KEY,
  ciudad VARCHAR(100) NOT NULL,
  tipo_tienda VARCHAR(50) NOT NULL,
  CONSTRAINT uq_tienda UNIQUE (ciudad, tipo_tienda)
);

CREATE TABLE dim_metodo_pago (
  metodo_pago_id BIGINT PRIMARY KEY,
  metodo_pago VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE dim_temporada (
  temporada_id BIGINT PRIMARY KEY,
  nombre_temporada VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE dim_promocion (
  promocion_id BIGINT PRIMARY KEY,
  nombre_promocion VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE dim_producto (
  producto_id BIGINT PRIMARY KEY,
  nombre_producto VARCHAR(255) NOT NULL UNIQUE
);
```

## 3.2. Crear Tabla Hechos (SQL)

```
-- FACT PRINCIPAL (1 fila por transacción) - SIN producto_id
CREATE TABLE fact_transacciones (
  transaccion_id BIGINT PRIMARY KEY,
  tiempo_id BIGINT NOT NULL,
  cliente_id BIGINT NOT NULL,
  tienda_id BIGINT NOT NULL,
  metodo_pago_id BIGINT NOT NULL,
  temporada_id BIGINT NOT NULL,
  promocion_id BIGINT NOT NULL,

  total_unidades INTEGER NOT NULL,
  monto_total DECIMAL(10,2) NOT NULL,
  precio_promedio_unitario DECIMAL(10,2) NOT NULL,
  descuento_aplicado BOOLEAN NOT NULL,

  CONSTRAINT fk_tiempo FOREIGN KEY (tiempo_id) REFERENCES dim_tiempo(tiempo_id),
  CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES dim_cliente(cliente_id),
  CONSTRAINT fk_tienda FOREIGN KEY (tienda_id) REFERENCES dim_tienda(tienda_id),
  CONSTRAINT fk_metodo_pago FOREIGN KEY (metodo_pago_id) REFERENCES dim_metodo_pago(metodo_pago_id),
  CONSTRAINT fk_temporada FOREIGN KEY (temporada_id) REFERENCES dim_temporada(temporada_id),
  CONSTRAINT fk_promocion FOREIGN KEY (promocion_id) REFERENCES dim_promocion(promocion_id),

  CONSTRAINT chk_unidades CHECK (total_unidades > 0),
  CONSTRAINT chk_monto CHECK (monto_total > 0)
);

-- FACT PUENTE (muchos productos por transacción)
CREATE TABLE fact_transaccion_producto (
  transaccion_id BIGINT NOT NULL,
  producto_id BIGINT NOT NULL,
  PRIMARY KEY (transaccion_id, producto_id),
  CONSTRAINT fk_ftp_transaccion FOREIGN KEY (transaccion_id) REFERENCES fact_transacciones(transaccion_id),
  CONSTRAINT fk_ftp_producto FOREIGN KEY (producto_id) REFERENCES dim_producto(producto_id)
);
```

<img width="398" height="195" alt="image" src="https://github.com/user-attachments/assets/a1ac7ff2-5ad6-4646-ba42-5ddc20619acd" />
<img width="1500" height="931" alt="image" src="https://github.com/user-attachments/assets/bdbc1bfa-4987-45dc-be04-5b9b3f2860fb" />

## 4. Crear el Databricks

<img width="886" height="450" alt="image" src="https://github.com/user-attachments/assets/8bf4b66a-5c43-48aa-a283-c60717960991" />

### 4.1. Crear el Cluster

<img width="886" height="450" alt="image" src="https://github.com/user-attachments/assets/30d890af-c461-4eda-b97b-4b4bb35c0b59" />

### 4.2. Crear y Subir los Notebooks

<img width="1917" height="989" alt="image" src="https://github.com/user-attachments/assets/e6585de0-f2a9-4073-a9dd-06175a5a8eee" />

### 4.3. Crear el Job

<img width="1860" height="941" alt="image" src="https://github.com/user-attachments/assets/adb48583-8c2a-4e5f-9487-e690934bf0bf" />

## 5. Crear el Frontend

<img width="886" height="459" alt="image" src="https://github.com/user-attachments/assets/b5fb3bdb-3287-4a32-9980-50948ded114c" />

- Se realiza la codificacion del frontend y se genera la carpeta dist

## 6. Se Crea el Static Web Apps

<img width="886" height="450" alt="image" src="https://github.com/user-attachments/assets/cace53d0-e604-4898-8613-6a15db88e85b" />

- Se sube el frontend a un repositorio privado. Para que lo reciba el static webapps.

<img width="1863" height="938" alt="image" src="https://github.com/user-attachments/assets/41aba64e-f196-441b-b547-3d31de7763c0" />
<img width="1862" height="939" alt="image" src="https://github.com/user-attachments/assets/6fc0243f-c398-455a-80ea-ffa497885d65" />

## 7. Dashboard Funcional

<img width="1600" height="864" alt="image" src="https://github.com/user-attachments/assets/a89a6f28-28a2-4a65-9d12-e1a9033f53a5" />

- Link del Dashboard: https://yellow-meadow-0f17f000f.3.azurestaticapps.net/
