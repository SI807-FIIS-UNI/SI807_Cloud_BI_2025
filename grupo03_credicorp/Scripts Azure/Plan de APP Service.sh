#!/bin/bash

RG_NAME="grupo03-credicorp"
RG_LOCATION="southcentralus" 

ASP_NAME="ASP-grupo03credicorp-90b6"
ASP_LOCATION="centralus"
TEMPLATE_FILE="./app_service_plan_template.json"

echo "--- PASO 1: Creando/Verificando Grupo de Recursos ($RG_NAME en $RG_LOCATION) ---"
az group create --name "$RG_NAME" --location "$RG_LOCATION" --output none

if [ $? -ne 0 ]; then
  echo "Error: No se pudo crear el Grupo de Recursos. Saliendo."
  exit 1
fi

echo "Grupo de Recursos listo."

echo "--- PASO 2: Iniciando el despliegue del Plan de Servicio ($ASP_NAME) ---"
echo "Usando plantilla: $TEMPLATE_FILE"

az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --parameters appServicePlanName="$ASP_NAME" location="$ASP_LOCATION" \
  --name "Deployment-ASP-$(date +%Y%m%d%H%M)" 

if [ $? -eq 0 ]; then
  echo "✅ ¡Despliegue de Plan de Servicio de Aplicación completado exitosamente!"
else
  echo "❌ Error en el despliegue del Plan de Servicio de Aplicación."
fi