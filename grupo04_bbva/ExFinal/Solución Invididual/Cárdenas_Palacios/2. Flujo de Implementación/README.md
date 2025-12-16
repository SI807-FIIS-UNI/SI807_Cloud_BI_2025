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

## 


## 


## 

## 


## 
