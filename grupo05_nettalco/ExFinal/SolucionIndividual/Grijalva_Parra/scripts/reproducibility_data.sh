#PLATA

bq extract --location=US \
us-accidents-481401:us_accidents_dw.dim_tiempo \
gs://us-accidents-bd/plata/dim/dim_tiempo.csv


bq extract --location=US \
us-accidents-481401:us_accidents_dw.dim_ubicacion \
gs://us-accidents-bd/plata/dim/dim_ubicacion.csv

bq extract --location=US \
us-accidents-481401:us_accidents_dw.dim_clima \
gs://us-accidents-bd/plata/dim/dim_clima.csv

bq extract --location=US \
us-accidents-481401:us_accidents_dw.fact_accidentes \
gs://us-accidents-bd/plata/fact/fact_accidentes.csv


#ORO

bq extract --location=US us-accidents-481401:us_accidents_dw.kpi_accidentes_clima \
gs://us-accidents-bd/oro/aggregates/kpi_accidentes_clima.csv

bq extract --location=US us-accidents-481401:us_accidents_dw.kpi_horas_criticas \
gs://us-accidents-bd/oro/aggregates/kpi_horas_criticas.csv

bq extract --location=US us-accidents-481401:us_accidents_dw.kpi_severidad_promedio \
gs://us-accidents-bd/oro/aggregates/kpi_severidad_promedio.csv