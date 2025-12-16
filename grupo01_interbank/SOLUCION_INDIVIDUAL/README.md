# PREGUNTA 3.1

## SELECCIÓN DE LA NUBE

La nube que se eligió es Google Cloud Storage ya que ofrece tanto escalamiento y servicios serverless (Google Cloud Storage y BigQuery). Además que es sencillo realizar su configuración. 
Además ofrece un servicio conocido como looker studio para poder realizar visualizaciones muy llamativas y que ofrece una conexión directa con BigQuery para poder
realizar los dashboards a partir de la capa oro que está en BigQuery.

## IMPLEMENTACIÓN DE LA ESTRUCTURA

Se crea el bucket de bronce y se define carpetas en el cual tiene la estructura de la imagen.

<img width="1581" height="835" alt="image" src="https://github.com/user-attachments/assets/f5d1b5f5-0b77-45bf-8985-ddca62545407" />


## Cargar los CSV usando el CLI
Primero se realizó la carga al CLI para luego realizar la carga al bucket de destino que es bronce23/raw

<img width="1904" height="493" alt="image" src="https://github.com/user-attachments/assets/3c880182-9563-4917-8e23-5965b0eaf20a" />

<img width="1702" height="303" alt="image" src="https://github.com/user-attachments/assets/9edec431-d2a8-4674-9a8c-485e93a5deeb" />

<img width="1569" height="547" alt="image" src="https://github.com/user-attachments/assets/3622e4d7-50f6-41d5-84ce-31219c840546" />

## EJECUCIÓN DE LOS EDAs.

La ejecución de los EDAs se realiza en python usando jupyter local conectado con el bucket bronce raw que se ubica en GCS.

<img width="1841" height="852" alt="image" src="https://github.com/user-attachments/assets/522fea4e-0b99-4fe3-980f-e44d2904e22c" />

Analizando los tipos de Datos:

<img width="678" height="710" alt="image" src="https://github.com/user-attachments/assets/71c5f104-57ee-429a-966b-38819a576a89" />

Analizando la cantidad de nulos:

<img width="1915" height="837" alt="image" src="https://github.com/user-attachments/assets/3c1ab816-3afc-40e0-b522-69b3bfcd2d08" />


# PREGUNTA 3.2

## CONSTRUCCIÓN DEL MODELO ESTRELLA 
El dataset dado se trata de accidentes de transito que se han visto desde el periodo 2016 al 2023.
* La tabla de hechos se relaciona a justamente el asunto principal de la situación o de la data que son los accidentes.
* Las tablas de dimensiones contextualizan a la tabla de hechos. En este caso sería Dimensión de Tiempo, Dimensión de Ubicación y Dimensión de Clima.

<img width="792" height="728" alt="image" src="https://github.com/user-attachments/assets/b9f33fe4-161d-4de6-acb4-915dd489d237" />


## TABLAS DE HECHOS Y DIMENSIONES EN PLATA



## PROCESAMIENTO Y GENERACION DE KPIs 



## EVIDENCIAS DE ETL

```sql

```

# PREGUNTA 3.3

## DASHBOARDS CONECTADOS A LA CAPA ORO

### DASHBOARD 1

### DASHBOARD 2



