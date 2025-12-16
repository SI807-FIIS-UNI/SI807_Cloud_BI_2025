# Dashboards (Power BI) – Visualización de KPIs de Retrasos de Vuelos

En esta carpeta se documenta el **dashboard desarrollado en Power BI** para analizar el dataset **Flight Delay and Causes**, utilizando como fuente los datos ya refinados en la **capa Oro (Gold)** dentro del ecosistema **Azure (Databricks + ADLS)**.

El objetivo del dashboard es responder, de forma visual y rápida, preguntas como:
- ¿Cuál es el **retraso promedio** de llegada?
- ¿Qué porcentaje de vuelos se considera **retrasado**?
- ¿Qué **aerolíneas** concentran más retraso?
- ¿Qué **aeropuertos** aparecen con mayor impacto?
- ¿Qué **causas** explican la mayor cantidad de minutos perdidos?

---

## Vista general del dashboard

**Título del dashboard:**  
**Análisis de Retrasos de Vuelos (KPIs y Ranking)**

<img width="1116" height="623" alt="image" src="https://github.com/user-attachments/assets/dade1c71-e512-4a00-8ee2-1a8dcc25974b" />

---

## Reproducibilidad (cómo conectarse y reconstruir el dashboard)

A continuación se describe un flujo reproducible para que cualquier persona pueda conectarse a la misma arquitectura (Azure Databricks) y **reconstruir el dashboard** en Power BI.

### 1) Requisitos previos
- Tener **Power BI Desktop** instalado.
- Tener acceso al workspace de **Azure Databricks** (con permisos de lectura a las tablas Gold).
- Contar con credenciales para autenticarte (ideal: **Azure AD / Microsoft Entra ID**; alternativa: **PAT token**).

> Nota: No se recomienda subir tokens al repositorio. Si usas PAT, guárdalo de forma segura.

### 2) Conexión desde Power BI a Azure Databricks
1. Abrir Power BI Desktop → **Obtener datos**.
2. Buscar el conector: **Azure Databricks**.
3. Completar los campos solicitados:
   - **Server hostname** (ejemplo):
     - `adb-3256800852464289.9.azuredatabricks.net`
   - **HTTP Path** (ejemplo):
     - `sql/protocolv1/o/3256800852464289/1216-061300-vshb2ahu`
4. En autenticación:
   - Seleccionar **Cuenta organizacional (Azure AD)** y hacer login, **o**
   - Seleccionar **Token personal (PAT)** e ingresar el token (si aplica).
5. Una vez conectado, seleccionar el catálogo/esquema y las tablas necesarias (Gold).
6. Elegir modo de carga:
   - **Import** (más rápido en visualización, copia local)
   - **DirectQuery** (consulta en vivo; depende del rendimiento/permiso)

---

## Fuente de datos utilizada (Capa Oro)

El dashboard se construye a partir de tablas Delta Gold publicadas en Databricks, principalmente:

- `fact_vuelos_gold` (tabla de hechos)
- `dim_tiempo_gold` (dimensión tiempo)
- `dim_aerolinea_gold` (dimensión aerolínea)
- `dim_origen_gold` (dimensión aeropuerto origen)
- `dim_destino_gold` (dimensión aeropuerto destino)
- `kpis_reporte_gold` (KPIs base por aerolínea)

> Recomendación: si vas a replicar el modelo estrella dentro de Power BI, carga **hechos + dimensiones** y crea las relaciones en el modelo.

---

## Componentes del dashboard y justificación

### 1) Tarjetas KPI (Cards)
Estas tarjetas resumen el estado general del sistema y permiten lectura ejecutiva.

- **Retraso Promedio (min)**: indica el promedio de minutos de retraso (llegada).
<img width="336" height="182" alt="image" src="https://github.com/user-attachments/assets/8acb65b3-fcb8-4158-a8e2-1b6b4b25c093" />

- **% Vuelos Retrasados**: indica el porcentaje de vuelos con retraso por encima de un umbral (ej. >15 min).
<img width="332" height="186" alt="image" src="https://github.com/user-attachments/assets/8c736276-32cf-4eee-be79-c57f4b75de0e" />


**Justificación:** en analítica operativa, las tarjetas permiten detectar rápidamente si la situación global mejora o empeora sin revisar todo el detalle.

---

### 2) Filtro por Mes (Slicer)
- Permite segmentar el análisis por **mes**, y ver cómo cambian KPIs y rankings.

<img width="670" height="132" alt="image" src="https://github.com/user-attachments/assets/9eeaec35-33e5-4dba-ad07-2d3f188d4896" />


**Justificación:** los retrasos suelen ser estacionales (clima, demanda, congestión). El filtro habilita comparación temporal.

---

### 3) Gráfico “Minutos perdidos por causa de retraso”
Visualiza la suma de minutos de retraso por categoría:
- `delay_carrier`, `delay_weather`, `delay_nas`, `delay_security`, `delay_late_aircraft`

<img width="670" height="402" alt="image" src="https://github.com/user-attachments/assets/250e76cf-6311-4673-9ccf-8f781f49b061" />


**Justificación:** permite identificar si el problema es más **interno** (carrier/late aircraft) o **externo** (weather/NAS/security).

---

### 4) Ranking de Aerolíneas (barra horizontal)
- Comparación de aerolíneas por **retraso promedio** (u otra métrica seleccionada).

<img width="705" height="327" alt="image" src="https://github.com/user-attachments/assets/9d3907dc-bac7-4c53-9c7a-4ce2e7b77d26" />


**Justificación:** ayuda a detectar rápidamente aerolíneas con peor desempeño y priorizar análisis.

---

### 5) Ranking de Aeropuertos (mapa)
- Ubica aeropuertos y permite comparar impacto por localización.

<img width="552" height="230" alt="image" src="https://github.com/user-attachments/assets/2a8a1403-9273-4335-b4ef-4aba185a7803" />


**Justificación:** Los retrasos se concentran por hubs/regiones (congestión, clima, operación). El mapa facilita lectura geográfica.

---

### 6) Mapa de desempeño (dispersión: puntualidad vs frecuencia)
- Eje X: **Retraso promedio (min)**
- Eje Y: **% vuelos retrasados**

<img width="680" height="524" alt="image" src="https://github.com/user-attachments/assets/2cf9529a-4c23-4452-8632-48ee11b54af9" />



**Justificación:** permite separar aerolíneas en cuadrantes:
- Mucho retraso + alta frecuencia (crítico)
- Mucho retraso + baja frecuencia
- Bajo retraso + alta frecuencia (buen desempeño)
- Bajo retraso + baja frecuencia

---

### 7) Tabla de detalle (matriz)
- Tabla con valores por aerolínea: retraso promedio, porcentaje retrasos, etc.
- (Colocar imagen de la **tabla de detalle** aquí)

**Justificación:** respalda los gráficos con cifras exactas y permite auditoría rápida.

---

## Medidas sugeridas (si quieres recrearlas en Power BI)

> Si consumes directamente `kpis_reporte_gold`, algunas medidas ya vienen calculadas.  
> Si las recalculas en Power BI, una base típica es:

- **Retraso Promedio (min)** = promedio de `arr_delay`
- **% Vuelos Retrasados** = vuelos con `arr_delay > 15` / total vuelos * 100
- **Minutos por Causa** = suma de cada columna `delay_*`

---

## Notas de implementación
- Si usas el modelo estrella dentro de Power BI, verifica que las relaciones queden en cardinalidad **1 a muchos** desde dimensiones hacia hechos.
- Si un campo geográfico no se reconoce automáticamente en el mapa, configura la **categoría de datos** (por ejemplo, aeropuerto como “Texto” y/o usar coordenadas si existieran).

---


