# IMPLEMENTACIÓN DE SOLUCIÓN EN LA NUBE DEL DATASET DE KAGGLE Medical Appointment No Shows
## Fase 1 : Creación buckets en google cloud
En esta parte creamos el bucket con nombre "bi-examen-dataset-mauricio-otero", y luego dentro del bucket creamos la carpeta cobre con las 3 carpetas raw , processed y curated
aquí una visualización del codigo que se empleo para realizar esta fase  : 
## Imagen de la visualizaciónd del codigo empleado para crear el bucket y la carpeta cobre:
<img width="1913" height="964" alt="Captura de pantalla 2025-12-15 201044" src="https://github.com/user-attachments/assets/1724a440-768b-4783-b0ac-fe6c118116a6" />

## Visualización del bucket con las carpetas en la plataforma google cloude: 

<img width="533" height="761" alt="Captura de pantalla 2025-12-15 201639" src="https://github.com/user-attachments/assets/10aa210a-c5cf-4241-859e-f621a3fdfff9" />

Despues de eso se suben los archivos para luego subirlos al Bucket para realizar el EDA y el ETL 
## Subida de archivos en Cloud Shell Editor : 

<img width="957" height="967" alt="Captura de pantalla 2025-12-15 202455" src="https://github.com/user-attachments/assets/96b09aad-cd48-4d78-a97b-837f0db9a927" />
## subida de archivos al bucket de google cloude : 
se usan los comandos para subir el csv a google cloude para su posterior análisis 
<img width="1609" height="93" alt="Captura de pantalla 2025-12-15 202713" src="https://github.com/user-attachments/assets/a1f2a12a-45e9-4690-a65c-af68244d1b83" />

<img width="1920" height="1080" alt="Captura de pantalla (234)" src="https://github.com/user-attachments/assets/803d548c-bb21-4c0b-9d6d-893f39142907" />

## FASE 2 : IMPLEMMENTACIÓN DE EDA SIMPLE : 
en esta parte vamos a realizar un Análsis exploratorio de datos de manera simple, para ver el comportamiento de los datos el archivo lo llamaremos EDA.py, pero antes se crean las carpetas doc y Script para almancenar imagenes y código de lo que resulte del EDA y el proceso ETL que se implementará luego y además se descargan las librerías pandas ,  matplotlib ,  fsspec  y gcsfs para realizar el correcto EDA
## Creación de carpetas
<img width="1514" height="786" alt="Captura de pantalla 2025-12-15 203416" src="https://github.com/user-attachments/assets/ba398e3d-e6a7-40c9-a1c6-f79e4ec07634" />
