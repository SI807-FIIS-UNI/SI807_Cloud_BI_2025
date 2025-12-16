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

| KPI | Descripción | Fórmula (SQL / DAX / Pseudocódigo) | Grano recomendado |
|---|---|---|---|
| Ticket promedio (Average Ticket) | Promedio de gasto por transacción. | `AVG(Total_Cost)` | Global / por tienda / por ciudad / por promoción |
| Ingreso total (Total Revenue) | Suma de ventas totales. | `SUM(Total_Cost)` | Día/mes/año, tienda, ciudad, tipo_tienda |
| Unidades totales | Total de items comprados. | `SUM(Total_Items)` | Día/mes/año, tienda, ciudad, tipo_tienda |
| Unidades por ticket (Items per Ticket) | Promedio de unidades por transacción. | `AVG(Total_Items)` | Global / por tienda / por ciudad |
| Top productos (por ingreso) | Ranking de productos que más venden en dinero. | `SUM(Total_Cost) por Product` (tras explotar lista) y `ORDER BY DESC` | Producto, mes, tienda/ciudad |
| Top productos (por unidades) | Ranking de productos más comprados por volumen. | `COUNT(Product) o SUM(unidades_producto)` tras explotar lista | Producto, mes, tienda/ciudad |
| Frecuencia de compra (por cliente) | Qué tan seguido compra un cliente (transacciones por periodo). | `COUNT(Transaction_ID) por Customer_Name en periodo` | Cliente, mes |
| Recencia (días desde última compra) | Días desde la última compra del cliente hasta “hoy” o fin del dataset. | `DATEDIFF(max(Date_cliente), fecha_referencia)` | Cliente |
| Horas pico | Horas con más transacciones (o más ingresos). | `HOUR(Date)` y `COUNT(Transaction_ID)` (o `SUM(Total_Cost)`) por hora | Hora del día, día/mes |
| Tasa de descuento | Proporción de tickets con descuento aplicado. | `SUM(CASE WHEN Discount_Applied=True THEN 1 ELSE 0 END) / COUNT(*)` | Mes, tienda/ciudad, tipo_tienda |
| Impacto de promociones | Comparar ingreso promedio con promoción vs sin promoción. | `AVG(Total_Cost WHERE Promotion!='None') - AVG(Total_Cost WHERE Promotion='None')` | Promoción, mes, tienda |
| Mix por método de pago | Participación de cada método de pago en tickets o ingresos. | `% tickets: COUNT(*) por Payment_Method / COUNT(*) total` o `% ingreso: SUM(Total_Cost) por método / SUM(Total_Cost)` | Mes, ciudad, tienda |
| Combo frecuente (opcional) | Pares/sets de productos que aparecen juntos en un ticket. | Por cada `Transaction_ID`, generar combinaciones de productos y contar: `COUNT(*) por (prodA, prodB)` | Par de productos, mes |

## 3. Crear el PostgreSQL

<img width="886" height="448" alt="image" src="https://github.com/user-attachments/assets/727343f8-db20-4693-9715-7312246551c0" />

### 3.1. Crear Tablas Dimensionales (SQL)

```
-- ============================================================
-- MODELO DIMENSIONAL - RETAIL TRANSACTIONS
-- PostgreSQL / pgAdmin
-- ============================================================

-- ============================================================
-- 1. DIMENSIÓN TIEMPO
-- ============================================================
CREATE TABLE dim_tiempo (
    tiempo_id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    anio INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    mes_nombre VARCHAR(20) NOT NULL,
    trimestre INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL,
    dia_semana_nombre VARCHAR(20) NOT NULL,
    semana_anio INTEGER NOT NULL,
    es_fin_semana BOOLEAN NOT NULL,
    CONSTRAINT chk_mes CHECK (mes BETWEEN 1 AND 12),
    CONSTRAINT chk_trimestre CHECK (trimestre BETWEEN 1 AND 4),
    CONSTRAINT chk_dia_semana CHECK (dia_semana BETWEEN 0 AND 6)
);

-- Índices para optimizar consultas
CREATE INDEX idx_dim_tiempo_fecha ON dim_tiempo(fecha);
CREATE INDEX idx_dim_tiempo_anio_mes ON dim_tiempo(anio, mes);
CREATE INDEX idx_dim_tiempo_trimestre ON dim_tiempo(anio, trimestre);

-- ============================================================
-- 2. DIMENSIÓN CLIENTE
-- ============================================================
CREATE TABLE dim_cliente (
    cliente_id SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(255) NOT NULL UNIQUE,
    categoria_cliente VARCHAR(50) NOT NULL,
    fecha_primer_compra DATE,
    fecha_ultima_compra DATE,
    CONSTRAINT chk_categoria CHECK (categoria_cliente IN ('Student', 'Young Adult', 'Professional', 'Middle-Aged', 'Senior', 'Homemaker', 'Teenager'))
);

-- Índices
CREATE INDEX idx_dim_cliente_nombre ON dim_cliente(nombre_cliente);
CREATE INDEX idx_dim_cliente_categoria ON dim_cliente(categoria_cliente);

-- ============================================================
-- 3. DIMENSIÓN PRODUCTO
-- ============================================================
CREATE TABLE dim_producto (
    producto_id SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(255) NOT NULL UNIQUE,
    categoria_producto VARCHAR(100),
    subcategoria_producto VARCHAR(100)
);

-- Índice
CREATE INDEX idx_dim_producto_nombre ON dim_producto(nombre_producto);
CREATE INDEX idx_dim_producto_categoria ON dim_producto(categoria_producto);

-- ============================================================
-- 4. DIMENSIÓN TIENDA
-- ============================================================
CREATE TABLE dim_tienda (
    tienda_id SERIAL PRIMARY KEY,
    ciudad VARCHAR(100) NOT NULL,
    tipo_tienda VARCHAR(50) NOT NULL,
    CONSTRAINT uq_tienda UNIQUE (ciudad, tipo_tienda),
    CONSTRAINT chk_tipo_tienda CHECK (tipo_tienda IN ('Supermarket', 'Convenience Store', 'Specialty Store', 'Warehouse Club', 'Department Store', 'Pharmacy'))
);

-- Índices
CREATE INDEX idx_dim_tienda_ciudad ON dim_tienda(ciudad);
CREATE INDEX idx_dim_tienda_tipo ON dim_tienda(tipo_tienda);

-- ============================================================
-- 5. DIMENSIÓN PROMOCIÓN
-- ============================================================
CREATE TABLE dim_promocion (
    promocion_id SERIAL PRIMARY KEY,
    nombre_promocion VARCHAR(100) NOT NULL UNIQUE,
    tipo_promocion VARCHAR(50)
);

-- Índice
CREATE INDEX idx_dim_promocion_nombre ON dim_promocion(nombre_promocion);

-- ============================================================
-- 6. DIMENSIÓN TEMPORADA
-- ============================================================
CREATE TABLE dim_temporada (
    temporada_id SERIAL PRIMARY KEY,
    nombre_temporada VARCHAR(20) NOT NULL UNIQUE,
    CONSTRAINT chk_temporada CHECK (nombre_temporada IN ('Spring', 'Summer', 'Fall', 'Winter'))
);

-- Poblar dimensión temporada (son valores fijos)
INSERT INTO dim_temporada (nombre_temporada) VALUES 
    ('Spring'),
    ('Summer'),
    ('Fall'),
    ('Winter');
```

## 3.2. Crear Tabla Hechos (SQL)

```
-- ============================================================
-- 7. TABLA DE HECHOS - TRANSACCIONES
-- ============================================================
CREATE TABLE fact_transacciones (
    transaccion_id BIGINT PRIMARY KEY,
    tiempo_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    tienda_id INTEGER NOT NULL,
    promocion_id INTEGER NOT NULL,
    temporada_id INTEGER NOT NULL,
    
    -- Métricas
    total_unidades INTEGER NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL,
    precio_promedio_unitario DECIMAL(10, 2) NOT NULL,
    
    -- Atributos degenerados (descriptivos de la transacción)
    metodo_pago VARCHAR(50) NOT NULL,
    descuento_aplicado BOOLEAN NOT NULL,
    numero_productos_distintos INTEGER NOT NULL,
    
    -- Claves foráneas
    CONSTRAINT fk_tiempo FOREIGN KEY (tiempo_id) REFERENCES dim_tiempo(tiempo_id),
    CONSTRAINT fk_cliente FOREIGN KEY (cliente_id) REFERENCES dim_cliente(cliente_id),
    CONSTRAINT fk_tienda FOREIGN KEY (tienda_id) REFERENCES dim_tienda(tienda_id),
    CONSTRAINT fk_promocion FOREIGN KEY (promocion_id) REFERENCES dim_promocion(promocion_id),
    CONSTRAINT fk_temporada FOREIGN KEY (temporada_id) REFERENCES dim_temporada(temporada_id),
    
    -- Constraints de validación
    CONSTRAINT chk_unidades CHECK (total_unidades > 0),
    CONSTRAINT chk_monto CHECK (monto_total > 0),
    CONSTRAINT chk_metodo_pago CHECK (metodo_pago IN ('Credit Card', 'Debit Card', 'Cash', 'Mobile Payment'))
);

-- Índices para optimizar consultas analíticas
CREATE INDEX idx_fact_tiempo ON fact_transacciones(tiempo_id);
CREATE INDEX idx_fact_cliente ON fact_transacciones(cliente_id);
CREATE INDEX idx_fact_tienda ON fact_transacciones(tienda_id);
CREATE INDEX idx_fact_promocion ON fact_transacciones(promocion_id);
CREATE INDEX idx_fact_temporada ON fact_transacciones(temporada_id);
CREATE INDEX idx_fact_fecha_cliente ON fact_transacciones(tiempo_id, cliente_id);
CREATE INDEX idx_fact_fecha_tienda ON fact_transacciones(tiempo_id, tienda_id);
```

<img width="398" height="195" alt="image" src="https://github.com/user-attachments/assets/a1ac7ff2-5ad6-4646-ba42-5ddc20619acd" />

## 

##






## 
