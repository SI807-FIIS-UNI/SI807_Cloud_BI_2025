#!/bin/bash

# ==============================================================================
# CONFIGURACIÓN DE VARIABLES GLOBALES
# ==============================================================================

# Variables del Grupo de Recursos
RG_NAME="grupo03-credicorp"
RG_LOCATION="southcentralus" 

# Variables de la Función (Se usarán como parámetros para la Plantilla)
APP_NAME="grupo-03-credicorp"
APP_LOCATION="centralus" 
ASP_NAME="ASP-grupo03credicorp-90b6"
# IMPORTANTE: El nombre de la Storage Account debe ser globalmente único y en minúsculas.
STORAGE_ACCOUNT_NAME="grupo03data20251201" 
RUNTIME_VERSION="Python|3.12"

TEMPLATE_FILE="./full_function_app_deployment.json"

# ==============================================================================
# PASO 1: ASEGURAR EL GRUPO DE RECURSOS
# ==============================================================================
echo "--- PASO 1: Creando/Verificando Grupo de Recursos ($RG_NAME en $RG_LOCATION) ---"
az group create --name "$RG_NAME" --location "$RG_LOCATION" --output none

if [ $? -ne 0 ]; then
  echo "Error: No se pudo crear el Grupo de Recursos. Saliendo."
  exit 1
fi

echo "Grupo de Recursos listo."
echo "--------------------------------------------------------"

# ==============================================================================
# PASO 2: DESPLIEGUE DE TODOS LOS RECURSOS (ASP, SA, AI, Function App)
# ==============================================================================
echo "--- PASO 2: Iniciando el despliegue de toda la infraestructura ---"
echo "Usando plantilla: $TEMPLATE_FILE"

az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --parameters \
    appName="$APP_NAME" \
    location="$APP_LOCATION" \
    appServicePlanName="$ASP_NAME" \
    storageAccountName="$STORAGE_ACCOUNT_NAME" \
    runtimeVersion="$RUNTIME_VERSION" \
  --name "Deployment-Full-App-$(date +%Y%m%d%H%M)" 
  
if [ $? -eq 0 ]; then
  echo "✅ ¡Despliegue de infraestructura de Azure Functions completado exitosamente!"
else
  echo "❌ Error crítico en el despliegue de la infraestructura."
  exit 1
fi

echo "--------------------------------------------------------"
echo "La Azure Function App ahora está lista para recibir el código."