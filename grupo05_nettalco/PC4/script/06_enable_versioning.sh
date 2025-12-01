#!/bin/bash
# ====================================
# ENABLE VERSIONING
# ====================================
# Habilita el versionamiento en el bucket nettalco-data-bd_grupo05
# para mantener un historial de cambios en los datos

gsutil versioning set on gs://nettalco-data-bd_grupo05
