#!/bin/bash

# ==============================================================================
# CONFIGURACIÓN DE VARIABLES
# ==============================================================================
RG_NAME="grupo03-credicorp"
STORAGE_ACCOUNT_NAME="grupo03data"
SA_LOCATION="centralus" 
TEMPLATE_FILE="./storage_account_template.json"

# ==============================================================================
# PASO 1: DESPLIEGUE DE LA CUENTA DE ALMACENAMIENTO
# ==============================================================================
echo "--- Iniciando el despliegue de la Cuenta de Almacenamiento ($STORAGE_ACCOUNT_NAME) ---"
echo "Usando plantilla: $TEMPLATE_FILE"

# Se usa az deployment group create para aplicar la plantilla ARM
az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file "$TEMPLATE_FILE" \
  --parameters storageAccountName="$STORAGE_ACCOUNT_NAME" location="$SA_LOCATION" \
  --name "Deployment-Storage-$(date +%Y%m%d%H%M)" 
  
if [ $? -eq 0 ]; then
  echo "✅ ¡Despliegue de la Cuenta de Almacenamiento completado exitosamente!"
else
  echo "❌ Error en el despliegue de la Cuenta de Almacenamiento."
fi