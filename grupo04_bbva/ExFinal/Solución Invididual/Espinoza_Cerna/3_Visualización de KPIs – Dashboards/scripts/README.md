# Scripts para visualización de datos y dashboards (Power BI)

En esta sección se documenta cómo se construyen los **dashboards** a partir de la **capa Gold** (datos limpios, modelados y listos para análisis).  
El objetivo es asegurar **reproducibilidad**, es decir, que cualquier persona externa pueda repetir el proceso y generar visualizaciones usando las tablas finales (hechos, dimensiones y KPIs).

> Nota: En este proyecto no se desarrollaron scripts de visualización en Python (matplotlib/plotly).  
> La visualización se realizó mediante **Power BI**, conectándose directamente a **Azure Databricks** para consumir las tablas de la capa Gold.

---

## Fuente de datos para los dashboards

Los dashboards se basan en las tablas generadas en la capa Gold, por ejemplo:

- `fact_vuelos_gold` (tabla de hechos con métricas y causas de retraso)
- `dim_tiempo_gold` (dimensión temporal)
- `dim_aerolinea_gold` (catálogo de aerolíneas)
- `dim_origen_gold` / `dim_destino_gold` (catálogos de aeropuertos)
- `kpis_reporte_gold` (tabla agregada de KPIs por aerolínea)

Estas tablas son el insumo directo para crear gráficos y métricas como:
- Porcentaje de vuelos con retrasos
- Retraso promedio de llegada por aerolínea
- Comparación de causas de retraso (Carrier/Weather/NAS/Security/Late Aircraft)
- Tendencias temporales por día/mes/año

---

## Reproducibilidad: conexión Power BI ↔ Azure Databricks

Para que cualquier usuario pueda reproducir los dashboards, se debe conectar **Power BI** a **Azure Databricks** siguiendo estos pasos generales:

1. Abrir **Power BI Desktop**.
2. Ir a **Obtener datos** → buscar el conector **Azure Databricks**.
3. Ingresar los parámetros de conexión del workspace.
4. Autenticarse mediante el inicio de sesión con cuenta (login) y validaciones de acceso solicitadas.

### Parámetros de conexión utilizados

En el conector de Azure Databricks, se ingresaron los siguientes valores:

- **Server Hostname (Databricks):**
  - `adb-3256800852464289.9.azuredatabricks.net`

- **HTTP Path:**
  - `sql/protocolv1/o/3256800852464289/1216-061300-vshb2ahu`

Con estos datos, Power BI puede conectarse y listar el catálogo de tablas disponibles en Databricks (especialmente las de la capa Gold), permitiendo construir visualizaciones directamente desde las fuentes analíticas.

> Recomendación: Para una reproducción completa en otro entorno, el usuario externo debe contar con permisos en el workspace de Azure Databricks y acceso a las tablas (o a un SQL Warehouse configurado).

---

## Modelo recomendado en Power BI

Para mantener consistencia con el enfoque analítico del proyecto, se recomienda replicar en Power BI un modelo tipo estrella:

- `fact_vuelos_gold` como tabla central (hechos)
- Dimensiones conectadas por campos clave:
  - Tiempo: `year`, `month`, `day_of_month`, `day_of_week` (o `id_tiempo` si se utiliza en el modelo)
  - Aerolínea: `carrier_code`
  - Origen: `origin` ↔ `dim_origen_gold.airport_code`
  - Destino: `dest` ↔ `dim_destino_gold.airport_code`

Además, `kpis_reporte_gold` puede usarse como tabla “lista para reporte” si el dashboard está orientado a KPIs por aerolínea sin necesidad de cálculos adicionales.

---

## Dashboards

Los dashboards finales fueron desarrollados en **Power BI** y se documentan con mayor detalle en una carpeta dedicada (diseño, páginas, filtros, medidas y capturas).  
Esta sección se enfoca únicamente en la **reproducibilidad del acceso a datos** y en el vínculo técnico entre Azure Databricks y Power BI.
