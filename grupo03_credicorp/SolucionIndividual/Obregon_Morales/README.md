# Solución Individual - Examen Final
## 3️⃣ Arquitectura del Pipeline

CSV (Kaggle)  
|
CAPA BRONCE (Azure Blob / Raw)  
|  
EDA (Calidad de Datos)  
|  
CAPA PLATA (Modelo Estrella)  
|  
CAPA ORO (KPIs)  
|  
Dashboard POWERBI  

---

## 4️⃣ Capa BRONCE – Ingesta de Datos

Objetivo  
Almacenar los datos en su forma original, sin transformaciones, garantizando trazabilidad.

Script  
01_ingesta_bronce.py

Descripción  
El script:
- Lee los CSV del dataset de calidad del aire  
- Crea el contenedor datalake si no existe  
- Sube los archivos a bronce/raw/  
- Genera evidencias de ejecución  

Evidencias  

![evidencia1](./evidencia1.png)

---

## 5️⃣ Capa BRONCE – Análisis Exploratorio (EDA)

Objetivo  
Evaluar la calidad, estructura y comportamiento de los datos antes de la modelación.

Script  
02_eda_bronce.py

Descripción  
El EDA analiza:
- Valores nulos  
- Tipos de datos  
- Estadísticas descriptivas  
- Valores únicos  
- Correlaciones  
- Outliers (IQR)  

Evidencias  

![evidencia2](./evidencia2.png)

![evidencia3](./evidencia3.png)
---

## 6️⃣ Capa PLATA – Modelo Dimensional

Objetivo  
Transformar los datos crudos en un modelo estrella optimizado para análisis.

Script  
03_transformacion_plata.py

Modelo Estrella

Tabla de Hechos  
fact_air_quality  
- AQI  
- PM2.5  
- PM10  
- NO2  
- CO  
- city_id  
- time_id  

Dimensiones  
- dim_city  
- dim_time  
- dim_contaminant  

Evidencias  

![evidencia4](./evidencia4.png)

---

## 7️⃣ Capa ORO – KPIs

Objetivo  
Generar indicadores clave ambientales para la toma de decisiones.

Script  
04_kpis_oro.py

KPIs Generados  
- AQI promedio  
- PM2.5 promedio  
- PM10 promedio  
- NO2 promedio  
- CO promedio  
- Fecha de proceso  

Evidencias  

![evidencia5](./evidencia5.png)
---


