



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

Para la construccion de un modelo estrella minimo se tuvo que recurrir a usar el servicio de dataproc para crear un cluster y ejecutar jupiter con el cual se podra realizar la transformacion de la Data

## 2.2. General tablas de dimensión y hechos

## 2.3. Procesar y generar KPIS

## 2.4. Evidencias de ETL y Logs 


### 3. Visualización de KPIS - Dashboards

## 3.1. Crear 2 dashboards 

## 3.2. Incluir KPIs 

## 3.3. Sustento de diseño
