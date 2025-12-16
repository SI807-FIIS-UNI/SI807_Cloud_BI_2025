# Evidencias del Pipeline (Capturas)

En esta sección se presentan las evidencias (capturas) del flujo completo implementado para el caso **Flight Delay and Causes**, incluyendo: **ingesta**, **EDA**, **modelo estrella**, **validación de logs ETL** y **dashboards**.



## 1) Ingesta de datos (Capa Bronce)

La ingesta consiste en leer el archivo **Flight_delay.csv** desde **ADLS Gen2** y almacenarlo como tabla **Delta** en Databricks (capa Bronce).  
Esta capa conserva los datos en formato *raw* para asegurar trazabilidad y permitir reprocesos.

<img width="886" height="449" alt="image" src="https://github.com/user-attachments/assets/a3d28989-28e3-48d0-8879-d7cc40cbfa06" />

<img width="886" height="296" alt="image" src="https://github.com/user-attachments/assets/844eee28-00ca-47e5-9952-b107ba972da6" />

---

## 2) EDA (Exploratory Data Analysis)

Se realizó un análisis exploratorio para comprender la estructura del dataset, tipos de datos, valores faltantes, distribución de retrasos y variables relevantes (causas: **Carrier**, **Weather**, **NAS**, **Security**, **Late Aircraft**, etc.).  
El objetivo del EDA fue guiar las transformaciones posteriores y validar que los campos críticos estén presentes y tengan coherencia.

<img width="886" height="450" alt="image" src="https://github.com/user-attachments/assets/3702cf4e-686d-4741-a97b-c27986a38d4e" />

---

## 3) Transformación y limpieza (Capa Plata / Silver)

En la capa Plata se aplicaron transformaciones de limpieza y estandarización, principalmente:
- Normalización de nombres de columnas (minúsculas y `_`).
- Eliminación de filas duplicadas.
- Preparación del dataset para consumo analítico posterior.

**Evidencia: Capa Plata en ejecución (Databricks / Silver)**  
<img width="886" height="450" alt="image" src="https://github.com/user-attachments/assets/72eb489a-a05e-4160-b5b4-0f504f3f354f" />


**Evidencia: salida / vista previa de la tabla Silver**  
<img width="886" height="379" alt="image" src="https://github.com/user-attachments/assets/de679abc-e751-4e80-99a2-4dbd4ed58804" />

---

## 4) Modelo Estrella y capa analítica (Capa Oro / Gold)

En la capa Oro se construyó el **modelo estrella** para análisis, separando:
- **Dimensiones**: tiempo, aerolínea y aeropuertos (origen y destino).
- **Hechos**: tabla central con retrasos y causas.

Este diseño facilita la analítica, el modelado en herramientas BI y la consulta eficiente por ejes (tiempo, aerolínea, origen/destino).

**Evidencia: diagrama del modelo estrella (generado en Power BI)**  
<img width="886" height="753" alt="image" src="https://github.com/user-attachments/assets/3b18b900-8900-4d14-a9ba-33917b2a22b2" />


**Evidencia: ejecución del notebook de Capa Oro (creación de dimensiones/hechos/KPIs)**  
<img width="886" height="450" alt="image" src="https://github.com/user-attachments/assets/b67978ea-a624-416e-a4bb-bd238183b0f3" />

<img width="886" height="451" alt="image" src="https://github.com/user-attachments/assets/5264a9ae-f599-4d1c-ab7f-47ff057542b6" />

---

## 5) Validación de ETL Logs (Bronce / Plata / Oro)

La validación del proceso ETL se realizó mediante verificación de logs y resultados en cada etapa:

### 5.1 Logs Capa Bronce
Se valida la correcta lectura del CSV y creación de la tabla Delta en Bronce (mensaje de éxito).

<img width="886" height="343" alt="image" src="https://github.com/user-attachments/assets/6fa2cb9b-1523-4dbe-b83f-6eeccc96cfd9" />


### 5.2 Logs Capa Plata
Se valida la limpieza del dataset, destacando eliminación de duplicados y creación de la tabla Silver.

<img width="886" height="375" alt="image" src="https://github.com/user-attachments/assets/03fc3a9f-2f15-4de2-8b8c-52f23c0f738d" />


### 5.3 Logs Capa Oro
Se valida la creación correcta de:
- Dimensiones (`dim_tiempo_gold`, `dim_aerolinea_gold`, `dim_origen_gold`, `dim_destino_gold`)
- Hechos (`fact_vuelos_gold`)
- KPIs (`kpis_reporte_gold`)

<img width="886" height="290" alt="image" src="https://github.com/user-attachments/assets/58826fcb-b639-476f-a42d-f9365c96fc12" />

---

## 6) Dashboards (Power BI)

Finalmente, se desarrolló un dashboard en **Power BI** consumiendo datos de la **capa Oro**, mostrando KPIs y visualizaciones para análisis ejecutivo:
- **Retraso promedio**
- **% de vuelos retrasados**
- **Ranking de aerolíneas**
- **Ranking de aeropuertos**
- **Minutos perdidos por causa de retraso**
- Visualizaciones de soporte (mapas / dispersión / tablas)

**Evidencia: Dashboard final en Power BI**  
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/af560c61-7abe-41a0-9eec-01971aed4d71" />


---

## OPINIÓN

Con estas evidencias se demuestra el flujo completo:
**Ingesta (Bronce) → Limpieza (Plata) → Modelo Estrella + KPIs (Oro) → Consumo BI (Power BI)**, con verificación de logs en cada fase.
