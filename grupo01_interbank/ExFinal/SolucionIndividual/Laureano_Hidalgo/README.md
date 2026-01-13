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

<img width="1069" height="527" alt="image" src="https://github.com/user-attachments/assets/54c9add3-b12e-4336-9890-093d41fe807a" />


### Justificación de cada dimensión
DIM_DATE

- Central para análisis temporal (tendencias, estacionalidad, comparativos).
- Incluye year/month/day/dayofweek para evitar calcularlo en cada consulta.
- Clave date_key = yyyymmdd es estándar en DWH y eficiente.

DIM_CARRIER 

- uniquecarrier es un identificador natural y airline el nombre descriptivo.
- Permite analizar métricas por aerolínea: demoras promedio, cancelaciones, distribución de causas.

DIM_AIRPORT

- Los aeropuertos aparecen repetidos en millones de filas; separarlos reduce redundancia.
- Se modela una sola dimensión y en la fact se usan dos FKs:
- origin_airport_key y dest_airport_key
- Habilita análisis por aeropuerto de salida/llegada y por rutas.

DIM_AIRCRAFT 

- tailnum identifica el avión específico (alta utilidad para mantenimiento/calidad operativa).
- Permite detectar aeronaves con mayor incidencia de demora o cancelación.

DIM_FLIGHT

- flightnum por sí solo puede repetirse entre aerolíneas, por eso la clave natural es: (uniquecarrier, flightnum)
- Permite analizar comportamiento por número de vuelo y combinarlo con fecha/aeropuerto.

### Justificación de la tabla de hechos
fact_flight_delay

Contiene:
- Claves foráneas hacia dimensiones (date, carrier, flight, aircraft, airport origen/dest).

Métricas y tiempos:
- demoras (arrdelay, depdelay, y causas)
- duraciones (airtime, elapsed times)
- operaciones (taxiin, taxiout, distance)
- flags (cancelled, diverted)
- Metadatos (_source_path, _ingestion_ts) para trazabilidad y auditoría.

Ahora vamos con los KPIs de Oro
Demora promedio por aerolínea
<img width="486" height="318" alt="image" src="https://github.com/user-attachments/assets/b17c8d84-b88a-4f70-973e-788854523780" />

Porcentaje de vuelos cancelados por aerolínea
<img width="376" height="321" alt="image" src="https://github.com/user-attachments/assets/30b0fb49-f669-4684-8d96-bc4281952bec" />

Promedio de demora por aeropuerto
<img width="510" height="447" alt="image" src="https://github.com/user-attachments/assets/954cb681-93b4-4b34-bd42-3af4f623ebe7" />

Distancia promedio de vuelos por aerolínea
<img width="342" height="319" alt="image" src="https://github.com/user-attachments/assets/6cb2c3b6-1a21-43b8-a29a-5fec87a94be3" />

Tiempo promedio de taxi por ruta (origen y destino)
<img width="405" height="449" alt="image" src="https://github.com/user-attachments/assets/9e1872f7-5e7b-4eb8-b02a-90b5c5edee2d" />

Demora promedio por día de la semana
<img width="488" height="231" alt="image" src="https://github.com/user-attachments/assets/db841fa1-3f4d-4561-8da3-c43dc3d94549" />

Número de vuelos desviados por aerolínea
<img width="328" height="313" alt="image" src="https://github.com/user-attachments/assets/e03242f7-cbe7-4075-a7c2-2c517553189b" />

# DASHBOARDS
Ahora procedemos a utilizar las tablas creada para hacer los dashboards, para ello, utilizaremos Looker Studio

<img width="1446" height="597" alt="image" src="https://github.com/user-attachments/assets/dde60206-9831-4a9a-a4d4-d8525d61759a" />

Con ello, generamos los dashboards

<img width="1222" height="561" alt="image" src="https://github.com/user-attachments/assets/9dad508e-b144-4ac9-a32d-c6bb81d230a8" />

Link Dashboards: https://lookerstudio.google.com/reporting/ed6b735d-4bf4-43b3-91c4-0089e8cd3a96













