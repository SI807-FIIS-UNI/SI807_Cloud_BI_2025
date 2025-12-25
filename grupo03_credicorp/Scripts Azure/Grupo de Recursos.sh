RESOURCE_GROUP_NAME="grupo03-credicorp"
LOCATION="southcentralus"

echo "Verificando y creando el Grupo de Recursos: $RESOURCE_GROUP_NAME en $LOCATION"

az group create \
  --name $RESOURCE_GROUP_NAME \
  --location $LOCATION

if [ $? -eq 0 ]; then
  echo "Grupo de Recursos '$RESOURCE_GROUP_NAME' está listo."
else
  echo "Error al crear/verificar el Grupo de Recursos."
fi