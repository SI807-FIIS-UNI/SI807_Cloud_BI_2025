#!/bin/bash
set -e

PROJECT_ID="final-julio-alvarez"

echo "Eliminando proyecto $PROJECT_ID..."
gcloud projects delete $PROJECT_ID --quiet

echo "Proyecto eliminado completamente."
