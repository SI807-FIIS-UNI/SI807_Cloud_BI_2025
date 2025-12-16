#!/bin/bash
set -e

# Crear carpetas (archivos .keep) en el bucket

gsutil cp /dev/null gs://us-accidents-bd/bronce/raw/.keep

gsutil cp /dev/null gs://us-accidents-bd/bronce/processed/.keep

gsutil cp /dev/null gs://us-accidents-bd/bronce/curated/.keep

gsutil cp /dev/null gs://us-accidents-bd/plata/dimensions/.keep

gsutil cp /dev/null gs://us-accidents-bd/plata/facts/.keep

gsutil cp /dev/null gs://us-accidents-bd/oro/kpis/.keep

gsutil cp /dev/null gs://us-accidents-bd/oro/aggregates/.keep

gsutil cp /dev/null gs://us-accidents-bd/scripts/.keep

gsutil cp /dev/null gs://us-accidents-bd/docs/.keep
