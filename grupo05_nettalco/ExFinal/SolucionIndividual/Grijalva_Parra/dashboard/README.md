Power BI artifacts and reproducibility

- Place Power BI Desktop files (.pbix) here: `BI Accidentes USA (2016-2023).pbix`
- Store Power Query (M) in `scripts/`
- Save screenshots in `evidencias/`

Reproducibility options:
1. Direct connect Power BI to BigQuery (requires GCP account and BigQuery permissions).
2. Export ORO tables to CSV using `bq extract` and download via `gsutil cp`.

Example export command:

```bash
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

```
