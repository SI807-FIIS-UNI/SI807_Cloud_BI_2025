



### 1. Ingestión y Estructuración - BRONCE

## 1.1. Justificacion de uso de GCP

Se decidio utilizar GCP por el ecosistema y facilidades que ofrece, con servicios como Dataproc, Spark, BiqQuery y Looker que se conectan muy bien entre si, proporcionando un buen desarrollo end-to-end

## 1.2. Implementar Estructura

Para la implementación de la estructura se realizo la creacion del bucket a utilizar en este proyecto llamado "bucket-ortiz-final", creado a travez del CLI

![evidencia01](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia01.png)

Una vez creado el bucket se procedio a crear la carpeta "Bronce" donde irian las carpetas "raw", "processed" y "curated"

![evidencia02](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia02.png)


## 1.3. Cargar los CSV utilizando CLI

Luego de haber creado las carpetas, seguimos con la carga del CSV utilizando CLI, primero subimos el archivo CSV al CLI para luego copiarlo dentro de la carpeta raw

![evidencia03](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia03.png)

Una vez copiado se ejecuta los comandos correspondientes para ubicarlo dentro de la carpeta raw y poder empezar con el manejo de datos

![evidencia04](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia04.png)


## 1.4. Ejecutar EDA mediante script Python

Se ejecuto un script en Python para realizar el EDA este script nos muestra los valores, tipos de valores, si son nulos, si hay errores dentro de nuestro DataSet

![evidencia05](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia05.png)

![evidencia06](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia06.png)

Dandonos como resultados lo siguiente:

![evidencia07](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia07.png)

![evidencia08](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia08.png)


### 2. Tranformación y Modelo Dimensional - PLATA Y ORO

## 2.1. Construir un modelo estrella

Para la construccion de un modelo estrella minimo se tuvo que recurrir a usar el servicio de dataproc para crear un cluster y ejecutar jupiter con el cual se podra realizar la transformacion de la Data, este cluster fue creado usando CLI con los siguiente comandos

![evidencia09](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia09.png)

Luego de eso ingresamos a JupiterLab y creamos un notebook para generar el modelo estrella

![evidencia10](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidencia10.png)


## 2.2. General tablas de dimensión y hechos

Una vez estando en JupiterLab se procede a ejecutar los scripts correspondientes a la limpieza de los datos y la creación de las tablas de dimensiones y hechos para armar el modelo estrella

![etl01](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/etl01.png)
![etl02](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/etl02.png)
![etl03](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/etl03.png)
![etl04](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/etl04.png)
![etl05](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/etl05.png)


## 2.3. Procesar y generar KPIS

Una vez teniendo el modelo estrella en nuestro servicio BigQuery, generamos KPIs usando scripts de Python en Jupiter

![kpi01](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/kpi01.png)
![kpi02](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/kpi02.png)
![kpi03](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/kpi03.png)
![kpi04](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/kpi04.png)
![kpi05](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/kpi05.png)

## 2.4. Evidencias de ETL y Logs 

Se evidencia que se realizo correctamente el proceso ETL y se muestran los logs

![evidenciaetl01](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl01.png)
![evidenciaetl02](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl02.png)
![evidenciaetl03](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl03.png)
![evidenciaetl04](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl04.png)
![evidenciaetl05](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl05.png)
![evidenciaetl06](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl06.png)
![evidenciaetl07](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/evidenciaetl07.png)


### 3. Visualización de KPIS - Dashboards

## 3.1. Crear 2 dashboards 

Una vez tenido los KPIS y el modelo Estrella en el BigQuery se procede a entrar a Looker Studio y conectarlo a nuestro BigQuery para extraer la Data para los Dashboard

![dashboard01](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/dashboard01.png)
![dashboard02](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/dashboard02.png)
![dashboard03](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/dashboard03.png)
![dashboard04](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/dashboard04.png)

## 3.2. Incluir KPIs 

Para la generacion de los graficos tambien se incluyeron los kpis generados por los script de phyton

![dashboard05](/grupo10_sutran/ExFinal/SolucionIndividual/Ortiz_Matamoros/docs/dashboard05.png)

Link del Looker: https://lookerstudio.google.com/reporting/329ed44d-f811-4222-ba37-f2e30b2afa53

## 3.3. Sustento de diseño

El diseño se separó en dos dashboards para facilitar la lectura y la toma de decisiones. El Dashboard 1 (Resumen Ejecutivo) concentra en la parte superior tarjetas KPI (volumen, retrasos promedio y porcentajes clave) y debajo una tendencia temporal, permitiendo evaluar rápidamente el estado general y su evolución. El Dashboard 2 (Análisis Operacional) profundiza el diagnóstico con rankings por aerolínea, top rutas y aeropuertos de origen, lo que ayuda a identificar focos de retraso y priorizar acciones. En ambos casos se consumen tablas ORO agregadas para asegurar rendimiento, consistencia y simplicidad en la visualización.