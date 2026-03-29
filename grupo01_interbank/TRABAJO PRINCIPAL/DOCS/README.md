# VIDEO DE LAS CONFIGURACIONES
LINK : [video configuracion](https://drive.google.com/drive/folders/1L19x_wX0hwxIjKNr4SFnY9nE-gEJ5Fmr?usp=drive_link)

# Parámetros de Costos Cloud


| Parámetro                               | Valor Asumido          | Justificación |
|------------------------------------------|-------------------------|---------------|
| Volumen de Datos Crudos (Inicial)        | 500 GB                  | Se asume una cantidad moderada de datos para los 5 CSV iniciales. |
| Volumen de Datos Mensual (Nuevo)         | 100 GB                  | Representa la data incremental de Trading y saldos que llega cada mes. |
| Consultas de BI (Escaneo)                | 5 TB / Mes              | Uso analítico intensivo: 1,000 consultas complejas que escanean, en promedio, 5 GB cada una. |
| Tiempo de Procesamiento (Dataproc)       | 100 vCPU-Horas / Mes    | Proceso ETL diario o nocturno (1 vCPU-Hora por job × 30 días, más jobs de re-procesamiento). |
| Transferencia de Salida (Egress)         | 10 GB / Mes             | Tráfico saliente mínimo (e.g., enviar reportes a sistemas externos o a otro datacenter). |



# Costos Mensuales Estimados



| Servicio               | Componente de Costo         | Costo Mensual Estimado (USD) |
|------------------------|------------------------------|-------------------------------|
| BigQuery               | Análisis (Consultas)         | $38.57                        |
| BigQuery               | Almacenamiento (Activo)      |                               |
| Cloud Storage (GCS)    | Almacenamiento de Raw        | $9.90                         |
| Cloud Storage (GCS)    | Transferencia Saliente       |                               |
| Cloud Dataproc         | Cómputo (vCPU)               | $18.12                        |
| Cloud Dataproc         | VMs Subyacentes              |                               |
| Composer (Airflow)     | Ambiente Mínimo              | $350.86                       |
|                          |                               |                               |
| | TOTAL MENSUAL ESTIMADO (Mes 1)| $417.45 |
| | PROYECCIÓN ANUAL (12 Meses) | $5,009.40 |


<img width="409" height="676" alt="Cost" src="https://github.com/user-attachments/assets/8531f92b-5912-42de-8840-b992cdd84858" />



# Propuesta de Optimización de Costos

Para un uso a largo plazo (más de 6 meses) y con crecimiento de datos, se proponen las siguientes optimizaciones:

## Optimización de BigQuery (Análisis)

- Particionamiento y Clustering: 
Asegurarse de que las Tablas de Hechos y Dimensiones estén particionadas por fecha y clusterizadas por columnas.Esto reduce drásticamente la cantidad de TB que se escanean en cada consulta, manteniendo el costo bajo en el modelo On-Demand.

- Proyección de Compromiso:
Si el uso proyectado de TB escaneados se estabiliza por encima de 10 TB/mes, considerar adquirir Compromisos de Capacidad (Reservas de Slots). Esto reduce el costo por query hasta en un 60%, cambiando el modelo de pago variable a un gasto fijo predecible.


## Optimización de Cloud Storage (Almacenamiento)

- Ciclos de Vida de Objetos:
Mover los archivos CSV raw (más de 90 días de antigüedad y rara vez consultados) de la clase Standard a Nearline o Coldline Storage. Esto reduce el costo de almacenamiento por GB en un 50–70%.





