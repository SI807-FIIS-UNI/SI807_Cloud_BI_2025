# INGESTIÓN Y ESTRUCTURACIÓN - BRONCE
Se procede a descargar la información desde el link proporcionado por el profesor
<img width="1449" height="890" alt="image" src="https://github.com/user-attachments/assets/543400ef-8f8c-4833-a202-c4cf6abf59d5" />

Luego se procede a crear los buckets dentro de GCP para poder subirlas y empezar a trabajar
<img width="1639" height="218" alt="image" src="https://github.com/user-attachments/assets/ae7650fb-c671-4a68-84c0-7ee96729cee7" />

Luego de haber subido la información, usamos dataproc para abrir un JupiterNotebook y poder limpiar la información
<img width="950" height="95" alt="image" src="https://github.com/user-attachments/assets/ac4a7b5d-2220-467b-a47f-bd107ca53fb1" />

Mediante el notebook procedmos a limpiar el csv (Scripts en otro archivo)
<img width="1903" height="950" alt="image" src="https://github.com/user-attachments/assets/77202a9b-eed6-44ec-9c13-e4aac6a6b7ab" />

Donde obtenemos las siguientes estadisticas:

<img width="675" height="531" alt="image" src="https://github.com/user-attachments/assets/a85c2449-d1f9-48b6-afdf-3316bf8638e1" />

Creandose asi el archivo en el processed
<img width="1633" height="408" alt="image" src="https://github.com/user-attachments/assets/1e7085a1-56a3-433d-80b7-8fa64eaeb7fd" />

Luego de pasar el archivo al curated, procedemos a la parte de Plata y Oro

# TRANSFORMACION Y MODELO DIMENSIONAL - PLATA Y ORO
Ahora procedemos a cargar la información en tabla de SQL.
Para esto usaremos BigQuery.
Creamos la tabla.
<img width="1656" height="819" alt="image" src="https://github.com/user-attachments/assets/be1c4e19-8d25-4fee-bd9a-40b26c448734" />

Con la tabla ya ingresada, creamos las dimensiones y la tabla de hechos para hacer el estrella (Scripts en otro archivo)







