#!/bin/bash

# ==============================================================================
# CONFIGURACIÓN DE VARIABLES
# ==============================================================================
RG_NAME="grupo03-credicorp"
AI_NAME="grupo-03-credicorp"
AI_LOCATION="centralus" 
TEMPLATE_FILE="./app_insights_template.json"

# ==============================================================================
# PASO 1: DESPLIEGUE DE APPLICATION INSIGHTS
# ==============================================================================
echo "--- Iniciando el despliegue de Application Insights ($AI_NAME) ---"
echo "Usando plantilla: $TEMPLATE_FILE"

az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --parameters appInsightsName="$AI_NAME" location="$AI_LOCATION" \
  --name "Deployment-AppInsights-$(date +%Y%m%d%H%M)" 
  
if [ $? -eq 0 ]; then
  echo "✅ ¡Despliegue de Application Insights completado exitosamente!"
else
  echo "❌ Error en el despliegue de Application Insights."
fi