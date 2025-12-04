# Despliegue de Dashboard BBVA en la Nube

## 0. Descargar Archivos

Obtenga los archivos [aqui](../5_Archivos_Utilizados/) y extraigalos en el escritorio.

## 0.5. Loguearse

```
az login
```
Luego ingresar con una cuenta autorizada y dar enter (para seleccionar la subcripción por default)

## 1. Asignar Roles AIM

Obtener UPN
```
az ad user list --query "[].{name:displayName, upn:userPrincipalName}" -o table
```

Obtener los Object ID
```
$PERSONA1 = (az ad user show --id "UPN_DE_LA_PERSONA1" --query id -o tsv)
$PERSONA2 = (az ad user show --id "UPN_DE_LA_PERSONA2" --query id -o tsv)
$PERSONA3 = (az ad user show --id "UPN_DE_LA_PERSONA3" --query id -o tsv)
```

Asignar Roles

- Persona 1
```
$RG_ID = (az group show -n rg-bbva-dashboard --query id -o tsv)
$ACR_ID = (az acr show -n acrbbvadashboard -g rg-bbva-dashboard --query id -o tsv)
$BACKEND_ID = (az containerapp show -n bbva-backend-api -g rg-bbva-dashboard --query id -o tsv)
$FRONTEND_ID = (az staticwebapp show -n bbva-dashboard-frontend -g rg-bbva-dashboard --query id -o tsv)
$ENV_ID = (az containerapp env show -n managedEnvironment-vnet -g rg-bbva-dashboard --query id -o tsv)
$LAW_ID = (az monitor log-analytics workspace show -n law-bbva-dashboard -g rg-bbva-dashboard --query id -o tsv)
```
```
az role assignment create --assignee $PERSONA1 --role "Contributor"                --scope $RG_ID
az role assignment create --assignee $PERSONA1 --role "AcrPull"                   --scope $ACR_ID
az role assignment create --assignee $PERSONA1 --role "AcrPush"                   --scope $ACR_ID
az role assignment create --assignee $PERSONA1 --role "Container Apps Contributor" --scope $ENV_ID
az role assignment create --assignee $PERSONA1 --role "Contributor"                --scope $BACKEND_ID
az role assignment create --assignee $PERSONA1 --role "Contributor"                --scope $FRONTEND_ID
az role assignment create --assignee $PERSONA1 --role "Log Analytics Contributor"  --scope $LAW_ID
```

- Persona 2
```
$DBW_ID = (az databricks workspace show -n dbw-bbva-dashboard -g rg-bbva-dashboard --query id -o tsv)
$KV_ID = (az keyvault show -n kv-bbva-dashboard --query id -o tsv)
$PG_ID = (az postgres flexible-server show -n pg-bbva-dashboard -g rg-bbva-dashboard --query id -o tsv)
$BKP_ID = (az dataprotection backup-vault show -n rg-bbva-dashboard-backup -g rg-bbva-dashboard --query id -o tsv)
$ST_ID = (az storage account show -n stbbvadatalake -g rg-bbva-dashboard --query id -o tsv)
```
```
az role assignment create --assignee $PERSONA2 --role "Owner"                    --scope $DBW_ID
az role assignment create --assignee $PERSONA2 --role "Key Vault Secrets Officer" --scope $KV_ID
az role assignment create --assignee $PERSONA2 --role "Contributor"               --scope $PG_ID
az role assignment create --assignee $PERSONA2 --role "Backup Contributor"        --scope $BKP_ID
az role assignment create --assignee $PERSONA2 --role "Storage Account Contributor" --scope $ST_ID
az role assignment create --assignee $PERSONA2 --role "Storage Blob Data Contributor" --scope $ST_ID
```

- Persona 3
```
$VNET_ID = (az network vnet show -n vnet-bbva-dashboard -g rg-bbva-red --query id -o tsv)

$FW_ID = (az network firewall show -n fw-bbva-dashboard -g rg-bbva-red --query id -o tsv)
$FW_PIP_ID = (az network public-ip show -n pip-firewall -g rg-bbva-red --query id -o tsv)

$RT_ID = (az network route-table show -n rt-firewall -g rg-bbva-red --query id -o tsv)

$FWPOL_ID = (az network firewall policy show -n policy-bbva-firewall -g rg-bbva-red --query id -o tsv)

$DNS_ACR = (az network private-dns zone show -n privatelink.azurecr.io -g rg-bbva-red --query id -o tsv)
$DNS_BLOB = (az network private-dns zone show -n privatelink.blob.core.windows.net -g rg-bbva-red --query id -o tsv)
$DNS_DFS = (az network private-dns zone show -n privatelink.dfs.core.windows.net -g rg-bbva-red --query id -o tsv)
$DNS_PG = (az network private-dns zone show -n privatelink.postgres.database.azure.com -g rg-bbva-red --query id -o tsv)
$DNS_KV = (az network private-dns zone show -n privatelink.vaultcore.azure.net -g rg-bbva-red --query id -o tsv)

$PE_ACR = (az network private-endpoint show -n pe-acr -g rg-bbva-red --query id -o tsv)
$PE_KV = (az network private-endpoint show -n pe-keyvault -g rg-bbva-red --query id -o tsv)
$PE_PG = (az network private-endpoint show -n pe-postgresql -g rg-bbva-red --query id -o tsv)
$PE_BLOB = (az network private-endpoint show -n pe-storage-blob -g rg-bbva-red --query id -o tsv)
$PE_DFS = (az network private-endpoint show -n pe-storage-dfs -g rg-bbva-red --query id -o tsv)

$NIC_ACR = (az network nic show -n pe-acr.nic.6d2eb155-47cf-42d6-81a1-c410338567d8 -g rg-bbva-red --query id -o tsv)
$NIC_KV = (az network nic show -n pe-keyvault.nic.b5962fc2-ffae-45a5-817e-361e905d86cf -g rg-bbva-red --query id -o tsv)
$NIC_PG = (az network nic show -n pe-postgresql.nic.98fda535-3b45-4cbd-aa88-bce0137ebc0c -g rg-bbva-red --query id -o tsv)
$NIC_BLOB = (az network nic show -n pe-storage-blob.nic.fe524dcc-3035-4f13-a043-962b5e72edbd -g rg-bbva-red --query id -o tsv)
$NIC_DFS = (az network nic show -n pe-storage-dfs.nic.dff6e04d-160d-4a36-8273-4fc845f54b7a -g rg-bbva-red --query id -o tsv)

$NSG_CA = (az network nsg show -n nsg-containerapp -g rg-bbva-red --query id -o tsv)
$NSG_DB = (az network nsg show -n nsg-databricks -g rg-bbva-red --query id -o tsv)
$NSG_KV = (az network nsg show -n nsg-keyvault -g rg-bbva-red --query id -o tsv)
$NSG_PG = (az network nsg show -n nsg-postgresql -g rg-bbva-red --query id -o tsv)
$NSG_ST = (az network nsg show -n nsg-storage -g rg-bbva-red --query id -o tsv)
```
```
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $VNET_ID
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $FW_ID
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $RT_ID
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $FWPOL_ID
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $FW_PIP_ID
```
```
az role assignment create --assignee $PERSONA3 --role "Private DNS Zone Contributor" --scope $DNS_ACR
az role assignment create --assignee $PERSONA3 --role "Private DNS Zone Contributor" --scope $DNS_BLOB
az role assignment create --assignee $PERSONA3 --role "Private DNS Zone Contributor" --scope $DNS_DFS
az role assignment create --assignee $PERSONA3 --role "Private DNS Zone Contributor" --scope $DNS_PG
az role assignment create --assignee $PERSONA3 --role "Private DNS Zone Contributor" --scope $DNS_KV
```
```
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $PE_ACR
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $PE_KV
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $PE_PG
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $PE_BLOB
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $PE_DFS
```
```
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NIC_ACR
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NIC_KV
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NIC_PG
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NIC_BLOB
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NIC_DFS
```
```
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NSG_CA
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NSG_DB
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NSG_KV
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NSG_PG
az role assignment create --assignee $PERSONA3 --role "Network Contributor" --scope $NSG_ST
```

## Crear Resource Group
```
az group create --name rg-bbva-dashboard --location eastus
```
## 1.5 Crear key vault

- Registrar el provider
```
az provider register --namespace Microsoft.KeyVault
```

- Crear el vault
```
az keyvault create --name kv-bbva-dashboard --resource-group rg-bbva-dashboard --location eastus
```

- Configurar la policy
```
$USER_OBJECT_ID = az ad signed-in-user show --query id -o tsv
$KV_ID = az keyvault show --name kv-bbva-dashboard --query id -o tsv

az role assignment create --assignee $USER_OBJECT_ID --role "Key Vault Secrets Officer" --scope $KV_ID
```

## 2. Crear Storage Account

```
az storage account create --name stbbvadatalake --resource-group rg-bbva-dashboard --location eastus --sku Standard_LRS `
    --kind StorageV2 --hns true
```

Se crean los contenedores Bronce y Silver
```
az storage container create --account-name stbbvadatalake --name bronze --auth-mode login
az storage container create --account-name stbbvadatalake --name silver --auth-mode login
```

Se crean las carpetas Data Sucia y Data Limpia
```
az storage fs directory create --account-name stbbvadatalake --file-system bronze `
    --name data_sucia --auth-mode login
az storage fs directory create --account-name stbbvadatalake --file-system bronze `
    --name data_sucia/data_sucia_continuous_integration --auth-mode login
az storage fs directory create --account-name stbbvadatalake --file-system bronze `
    --name data_sucia/data_sucia_practitioner --auth-mode login
az storage fs directory create --account-name stbbvadatalake --file-system silver `
    --name data_limpia --auth-mode login
az storage fs directory create --account-name stbbvadatalake --file-system silver `
    --name data_limpia/data_limpia_continuous_integration --auth-mode login
az storage fs directory create --account-name stbbvadatalake --file-system silver `
    --name data_limpia/data_limpia_practitioner --auth-mode login
```

Obtenga los archivos data sucia [aqui](../5_Archivos_Utilizados/Data_Cruda/) y extraigalos en el escritorio.

Guardar Connection String en Key Vault
```
$AZURE_STORAGE_CONNECTION_STRING = az storage account show-connection-string --name stbbvadatalake `
    --resource-group rg-bbva-dashboard --query connectionString -o tsv

az keyvault secret set --vault-name kv-bbva-dashboard --name "azure-storage-connection-string" `
    --value "$AZURE_STORAGE_CONNECTION_STRING"
```

## 3. Crear PostgreSQL Flexible Server
```
az postgres flexible-server create --name pg-bbva-dashboard --resource-group rg-bbva-dashboard --location centralus `
    --admin-user adminuser --admin-password "SecurePass123!" --sku-name Standard_D2ds_v5 --tier GeneralPurpose `
    --storage-size 128 --version 18 --public-access all
```

Guardar credenciales de PostgreSQL en Key Vault
```
az keyvault secret set --vault-name kv-bbva-dashboard --name "db-host" --value "pg-bbva-dashboard.postgres.database.azure.com"
az keyvault secret set --vault-name kv-bbva-dashboard --name "db-port" --value "5432"
az keyvault secret set --vault-name kv-bbva-dashboard --name "db-user" --value "adminuser"
az keyvault secret set --vault-name kv-bbva-dashboard --name "db-password" --value "SecurePass123!"
az keyvault secret set --vault-name kv-bbva-dashboard --name "db-name-practitioner" --value "data_oro_practitioner"
az keyvault secret set --vault-name kv-bbva-dashboard --name "db-name-ci" --value "data_oro_ci"
```

Crear la bases de datos data_oro_practitioner y data_oro_ci
```
az postgres flexible-server db create --resource-group rg-bbva-dashboard --server-name pg-bbva-dashboard `
    --database-name data_oro_practitioner
az postgres flexible-server db create --resource-group rg-bbva-dashboard --server-name pg-bbva-dashboard `
    --database-name data_oro_ci
```

Crear las tablas practitioner (Ingresar la contraseña: SecurePass123!)
```
psql `
  -h pg-bbva-dashboard.postgres.database.azure.com `
  -p 5432 `
  -U adminuser `
  -d data_oro_practitioner `
  -f "$env:USERPROFILE\Desktop\Querys\query_practitioner.sql" `
  --set=sslmode=require
```

Crear las tablas continuous integration (Ingresar la contraseña: SecurePass123!)
```
psql `
  -h pg-bbva-dashboard.postgres.database.azure.com `
  -p 5432 `
  -U adminuser `
  -d data_oro_ci `
  -f "$env:USERPROFILE\Desktop\Querys\query_ci.sql" `
  --set=sslmode=require
```

Obtenga los archivos query [aqui](../5_Archivos_Utilizados/Querys/) y extraigalos en el escritorio.

## 4. Crear Databricks

```
az databricks workspace create --name dbw-bbva-dashboard --resource-group rg-bbva-dashboard `
    --location eastus --sku standard --managed-resource-group rg-bbva-dashboard-db-managed --public-network-access Enabled
```

Obtener acceso admin (Borrar Cache si es necesario)
```
az role assignment create `
    --role "Owner" `
    --assignee $(az ad signed-in-user show --query id -o tsv) `
    --scope $(az databricks workspace show --name dbw-bbva-dashboard --resource-group rg-bbva-dashboard --query id -o tsv)
```

Obtener la Key del Datalake
```
$DL_KEY = az storage account keys list --account-name stbbvadatalake --resource-group rg-bbva-dashboard --query "[0].value" `
    -o tsv
```

Guardar la Key del Datalake en Key Vault
```
az keyvault secret set --vault-name kv-bbva-dashboard --name "datalake-key" --value "$DL_KEY"
```

Crear el cluster - Obtener el Token (User Settings → Generate Token)
```
$DATABRICKS_TOKEN = "PONER AQUI EL TOKEN"

$WORKSPACE_URL = az databricks workspace show --name dbw-bbva-dashboard --resource-group rg-bbva-dashboard `
    --query workspaceUrl -o tsv

$headers = @{
    "Authorization" = "Bearer $DATABRICKS_TOKEN"
    "Content-Type" = "application/json"
}

$body = @{
    cluster_name = "cluster-bbva"
    spark_version = "15.4.x-scala2.12"
    node_type_id = "Standard_DS3_v2"
    num_workers = 0
    autotermination_minutes = 20
    custom_tags = @{
        "ResourceClass" = "SingleNode"
    }
    enable_photon = $true
    runtime_engine = "PHOTON"
    spark_conf = @{
        "fs.azure.account.key.stbbvadatalake.dfs.core.windows.net" = $DL_KEY
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod `
    -Uri "https://$WORKSPACE_URL/api/2.1/clusters/create" `
    -Method Post `
    -Headers $headers `
    -Body $body
```

Guardar credenciales de Databricks en Key Vault
```
az keyvault secret set --vault-name kv-bbva-dashboard --name "databricks-token" --value "$DATABRICKS_TOKEN"
az keyvault secret set --vault-name kv-bbva-dashboard --name "databricks-workspace-url" --value "https://$WORKSPACE_URL"
```

Configurar Databricks CLI
```
$configContent = @"
[DEFAULT]
host = https://$WORKSPACE_URL
token = $DATABRICKS_TOKEN
"@

[System.IO.File]::WriteAllText("$env:USERPROFILE\.databrickscfg", $configContent, [System.Text.Encoding]::ASCII)
```

Subir los Notebooks (En este caso estan en el escritorio en una carpeta Notebooks)
```
$USER_EMAIL = az account show --query user.name -o tsv

databricks workspace import-dir "$env:USERPROFILE\Desktop\Notebooks" "/Workspace/Users/$USER_EMAIL"
```

Guardar el Cluster ID en Key Vault
```
$CLUSTER_ID = (databricks clusters list --output JSON | ConvertFrom-Json)[0].cluster_id

az keyvault secret set --vault-name kv-bbva-dashboard --name "databricks-cluster-id" --value "$CLUSTER_ID"
```

## 5. Crear Container Registry

```
az acr create --name acrbbvadashboard --resource-group rg-bbva-dashboard --location eastus --sku Standard `
    --admin-enabled true
```

Guardar credenciales de ACR en Key Vault
```
$ACR_PASSWORD = az acr credential show --name acrbbvadashboard --query "passwords[0].value" -o tsv

az keyvault secret set --vault-name kv-bbva-dashboard --name "acr-password" --value "$ACR_PASSWORD"
az keyvault secret set --vault-name kv-bbva-dashboard --name "acr-username" --value "acrbbvadashboard"
az keyvault secret set --vault-name kv-bbva-dashboard --name "acr-server" --value "acrbbvadashboard.azurecr.io"
```

Abrir una terminal en la carpeta del backend para:

- Construir la imagen desde tu Dockerfile
```
docker build -t bbva-backend:v1 .
```

- Loguearse al ACR
```
az acr login --name acrbbvadashboard
```

- Taguear la imagen con el ACR
```
docker tag bbva-backend:v1 acrbbvadashboard.azurecr.io/bbva-backend:v1
```

- Subirla al ACR
```
docker push acrbbvadashboard.azurecr.io/bbva-backend:v1
```

Obtenga el backend [aqui](../5_Archivos_Utilizados/backend/) y extraelo en el escritorio.

## 6. Crear Container App

Obtener el id del log-analytics workspace
```
$LAW_ID = az monitor log-analytics workspace show --resource-group rg-bbva-dashboard --workspace-name law-bbva-dashboard `
  --query customerId -o tsv

$LAW_KEY = az monitor log-analytics workspace get-shared-keys --resource-group rg-bbva-dashboard --workspace-name law-bbva-dashboard `
  --query primarySharedKey -o tsv
```

Obtener el IDs
```
$SUBNET_ID = az network vnet subnet show `
  --name snet-containerapp-infra `
  --vnet-name vnet-bbva-dashboard `
  --resource-group rg-bbva-red `
  --query id -o tsv

$LAW_ID = az monitor log-analytics workspace show `
  --resource-group rg-bbva-dashboard `
  --workspace-name law-bbva-dashboard `
  --query customerId -o tsv

$LAW_KEY = az monitor log-analytics workspace get-shared-keys `
  --resource-group rg-bbva-dashboard `
  --workspace-name law-bbva-dashboard `
  --query primarySharedKey -o tsv
```

# Crear el nuevo environment con VNET integration
```
az containerapp env create `
  --name managedEnvironment-vnet `
  --resource-group rg-bbva-dashboard `
  --location eastus `
  --infrastructure-subnet-resource-id $SUBNET_ID `
  --internal-only false `
  --logs-workspace-id $LAW_ID `
  --logs-workspace-key $LAW_KEY
```

Crear variables
```
$DB_HOST = az keyvault secret show --vault-name kv-bbva-dashboard --name "db-host" --query value -o tsv
$DATABRICKS_WORKSPACE_URL = az keyvault secret show --vault-name kv-bbva-dashboard --name "databricks-workspace-url" --query value -o tsv
$AZURE_STORAGE_CONNECTION_STRING = az keyvault secret show --vault-name kv-bbva-dashboard --name "azure-storage-connection-string" --query value -o tsv
$ACR_PASSWORD = az keyvault secret show --vault-name kv-bbva-dashboard --name "acr-password" --query value -o tsv
$CLUSTER_ID = az keyvault secret show --vault-name kv-bbva-dashboard --name "databricks-cluster-id" --query value -o tsv
$DATABRICKS_TOKEN = az keyvault secret show --vault-name kv-bbva-dashboard --name "databricks-token" --query value -o tsv
$DB_PASSWORD = az keyvault secret show --vault-name kv-bbva-dashboard --name "db-password" --query value -o tsv
```

Crear el contenedor
```
$DB_HOST = az keyvault secret show --vault-name kv-bbva-dashboard --name "db-host" --query value -o tsv

# Crear el Container App
az containerapp create --name bbva-backend-api --resource-group rg-bbva-dashboard --environment managedEnvironment-vnet `
  --image acrbbvadashboard.azurecr.io/bbva-backend:v1 --registry-server acrbbvadashboard.azurecr.io `
  --registry-username acrbbvadashboard --registry-password $ACR_PASSWORD --target-port 5000 --ingress external `
  --cpu 0.5 --memory 1.0Gi --system-assigned --min-replicas 1 --max-replicas 1 `
  --env-vars `
    "DB_HOST=$DB_HOST" `
    "DB_PORT=5432" `
    "DB_USER=adminuser" `
    "DB_PASSWORD=$DB_PASSWORD" `
    "DB_NAME_PRACTITIONER=data_oro_practitioner" `
    "DB_NAME_CI=data_oro_ci" `
    "DATABRICKS_WORKSPACE_URL=$DATABRICKS_WORKSPACE_URL" `
    "DATABRICKS_TOKEN=$DATABRICKS_TOKEN" `
    "FLASK_ENV=production" `
    "AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING" `
    "DATABRICKS_CLUSTER_ID=$CLUSTER_ID" `
    "KEY_VAULT_NAME=kv-bbva-dashboard"
```

Configurar permisos de Key Vault para Container App
```
$CONTAINER_APP_PRINCIPAL_ID = az containerapp show --name bbva-backend-api --resource-group rg-bbva-dashboard `
     --query identity.principalId -o tsv
$KV_ID = az keyvault show --name kv-bbva-dashboard --query id -o tsv

az role assignment create --assignee $CONTAINER_APP_PRINCIPAL_ID --role "Key Vault Secrets User" --scope $KV_ID
```

Actualizar la imagen
```
az containerapp update --name bbva-backend-api --resource-group rg-bbva-dashboard `
    --image acrbbvadashboard.azurecr.io/bbva-backend:v1
```

## 7. Crear Static Web App

```
az staticwebapp create --name bbva-dashboard-frontend --resource-group rg-bbva-dashboard --location eastus2 --sku Free
```

Obtener el URL del backend para reemplazarlo en el config del frontend
```
$API_BASE_URL = "https://$(az containerapp show --name bbva-backend-api --resource-group rg-bbva-dashboard `
  --query properties.configuration.ingress.fqdn -o tsv)"

Write-Host $API_BASE_URL
```

Obtenga el frontend [aqui](../5_Archivos_Utilizados/frontend/) y extraelo en el escritorio.

Abrir una terminal en la carpeta del frontend para contruir la carpeta dist
```
npm install
npm run build
```

Subir la carpeta dist
```
$token = az staticwebapp secrets list --name bbva-dashboard-frontend --resource-group rg-bbva-dashboard `
    --query properties.apiKey -o tsv

swa deploy --app-location "$env:USERPROFILE\Desktop\frontend\dist" --deployment-token "$token" --env "production"
```

## 8. Crear Logs Analitics WorkSpace

```bash
az monitor log-analytics workspace create `
  --resource-group rg-bbva-dashboard `
  --workspace-name law-bbva-dashboard `
  --location eastus
```

# Ruta para ejecutar cualquier archivo

Para los demas 

Obtenga los KQLs [aqui](../5_Archivos_Utilizados/frontend/) y ejecutelos.

Para el Databricks (Desde el CLI)

- Cluster Events
  
```bash
databricks clusters events 1129-051945-6zvtepb6
```

- Para Jobs

```bash
databricks jobs list
databricks jobs list-runs --job-id <ID>
databricks jobs get-run-output --run-id <RUN_ID>
```
  
# 9. Crear Alertas

```bash
az group create --name rg-bbva-alerts --location eastus
```

## Para el Datalake 

- Error rate anormal (transacciones fallidas)
```bash
az monitor metrics alert create `
  --name alert-storage-errors `
  --resource-group rg-bbva-alerts `
  --scopes $STORAGE_ID `
  --condition "total Transactions > 5 where ResponseType includes Error" `
  --description "Errores de Storage > 5 en 5 minutos" `
  --evaluation-frequency 1m `
  --window-size 5m `
  --severity 2
```

- Latencia alta
```bash
az monitor metrics alert create `
  --name alert-storage-latency `
  --resource-group rg-bbva-alerts `
  --scopes $STORAGE_ID `
  --condition "avg SuccessE2ELatency > 0.2" `
  --description "Latencia del Storage > 200ms" `
  --evaluation-frequency 5m `
  --window-size 15m `
  --severity 3
```

- Costo inesperado por datos salientes
```bash
az monitor metrics alert create `
  --name alert-storage-egress `
  --resource-group rg-bbva-alerts `
  --scopes $STORAGE_ID `
  --condition "total Egress > 200" `
  --description "Egress del Storage mayor a 200 MB (posible fuga de datos)" `
  --evaluation-frequency 30m `
  --window-size 24h `
  --severity 3
```

## Para el container app

- Error rate en el backend
```bash
$API_ID = az containerapp show --name bbva-backend-api --resource-group rg-bbva-dashboard --query id -o tsv

az monitor metrics alert create `
  --name alert-backend-5xx `
  --resource-group rg-bbva-alerts `
  --scopes $API_ID `
  --condition "total Requests > 5 where statusCodeCategory includes 5XX" `
  --description 'Más de 5 errores HTTP 5xx en 5 min' `
  --evaluation-frequency 1m `
  --window-size 5m `
  --severity 1
```

- Backend sin requests (posible caída)
```bash
az monitor metrics alert create `
  --name alert-backend-no-requests `
  --resource-group rg-bbva-alerts `
  --scopes $API_ID `
  --condition "total Requests < 1" `
  --description "0 requests por 15 minutos → posible caída del backend" `
  --evaluation-frequency 5m `
  --window-size 15m `
  --severity 2
```

- CPU muy alta (>70%)
```bash
az monitor metrics alert create `
  --name alert-backend-cpu-high `
  --resource-group rg-bbva-alerts `
  --scopes $API_ID `
  --condition "avg CpuPercentage > 70" `
  --description "CPU del backend mayor al 70%" `
  --evaluation-frequency 1m `
  --window-size 5m `
  --severity 2
```

## Para el postgresql

- Consumo de CPU alto
```bash
$PG_ID = az postgres flexible-server show --name pg-bbva-dashboard --resource-group rg-bbva-dashboard --query id -o tsv

az monitor metrics alert create `
  --name alert-postgres-cpu-high `
  --resource-group rg-bbva-alerts `
  --scopes $PG_ID `
  --condition "avg cpu_percent > 70" `
  --description "CPU de PostgreSQL mayor al 70%" `
  --evaluation-frequency 5m `
  --window-size 15m `
  --severity 2
```

- Conexiones máximas (>80%)
```bash
az monitor metrics alert create `
  --name alert-postgres-connections-high `
  --resource-group rg-bbva-alerts `
  --scopes $PG_ID `
  --condition "avg active_connections > 80" `
  --description 'Conexiones activas por encima del 80% del máximo permitido' `
  --evaluation-frequency 5m `
  --window-size 15m `
  --severity 2
```

- Espacio en disco bajo (<20%)
```bash
az monitor metrics alert create `
  --name alert-postgres-storage-low `
  --resource-group rg-bbva-alerts `
  --scopes $PG_ID `
  --condition "avg storage_percent > 80" `
  --description "PostgreSQL está usando más del 80% del almacenamiento" `
  --evaluation-frequency 30m `
  --window-size 1h `
  --severity 2
```

10. Virtual Network

- Crear la Virtual Network con la primera subnet

```
az network vnet create `
  --name vnet-bbva-dashboard `
  --resource-group rg-bbva-red `
  --location eastus `
  --address-prefix 10.0.0.0/16 `
  --subnet-name snet-containerapp `
  --subnet-prefix 10.0.1.0/24
```

Explicación de parámetros:
•	--address-prefix 10.0.0.0/16: Rango total de IPs (65,536 direccionesdisponibles)
•	--subnet-prefix 10.0.1.0/24: Subred para Container Apps (256 IPs)

- Crear subnet para el enviroment del ACR
```
az network vnet subnet create  
  --name snet-containerapp-infra  
  --resource-group rg-bbva-red 
  --vnet-name vnet-bbva-dashboard 
  --address-prefix 10.0.8.0/23
  --delegations Microsoft.App/environments
```

# Crear subnet para PostgreSQL
```
az network vnet subnet create `
  --name snet-postgresql `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --address-prefix 10.0.2.0/24
```

# Crear subnet para Databricks (necesita 2 subnets)
```
az network vnet subnet create `
  --name snet-databricks-public `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --address-prefix 10.0.3.0/24
```
```
az network vnet subnet create `
  --name snet-databricks-private `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --address-prefix 10.0.4.0/24
```

# Crear subnet para Storage Account (Private Endpoints)
```
az network vnet subnet create `
  --name snet-storage `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --address-prefix 10.0.5.0/24
```

# Crear subnet para Azure Firewall
```
az network vnet subnet create `
  --name AzureFirewallSubnet `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --address-prefix 10.0.6.0/24
```

Nota: El nombre AzureFirewallSubnet es obligatorio para el firewall.

# Crear subnet para Key Vault (Private Endpoint)
```
az network vnet subnet create `
  --name snet-keyvault `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --address-prefix 10.0.7.0/24
```

11. Network Security Groups

- NSG para Container App

Crear NSG
```
az network nsg create `
  --name nsg-containerapp `
  --resource-group rg-bbva-red `
  --location eastus
```

Regla 1: Permitir HTTPS desde internet (puerto 443)
```
az network nsg rule create `
  --name AllowHTTPS `
  --nsg-name nsg-containerapp `
  --resource-group rg-bbva-red `
  --priority 100 `
  --source-address-prefixes Internet `
  --destination-port-ranges 443 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir tráfico HTTPS público"
```
Explicación:
•	--priority 100: Menor número = mayor prioridad (rango: 100-4096)
•	--source-address-prefixes Internet: Desde cualquier IP pública
•	--destination-port-ranges 443: Puerto HTTPS

Regla 2: Permitir HTTP desde internet (puerto 80)
```
az network nsg rule create `
  --name AllowHTTP `
  --nsg-name nsg-containerapp `
  --resource-group rg-bbva-red `
  --priority 110 `
  --source-address-prefixes Internet `
  --destination-port-ranges 80 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir tráfico HTTP público"
```

Regla 3: Permitir puerto 5000 para el backend Flask
```
az network nsg rule create `
  --name AllowBackendPort `
  --nsg-name nsg-containerapp `
  --resource-group rg-bbva-red `
  --priority 120 `
  --source-address-prefixes 10.0.0.0/16 `
  --destination-port-ranges 5000 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir puerto 5000 del backend desde VNET"
```

Asociar NSG a la subnet
```
az network vnet subnet update `
  --name snet-containerapp `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --network-security-group nsg-containerapp
```

- NSG para PostgreSQL

Crear NSG
```
az network nsg create `
  --name nsg-postgresql `
  --resource-group rg-bbva-red `
  --location eastus
```

Permitir conexiones PostgreSQL solo desde la VNET
```
az network nsg rule create `
  --name AllowPostgreSQL `
  --nsg-name nsg-postgresql `
  --resource-group rg-bbva-red `
  --priority 100 `
  --source-address-prefixes 10.0.0.0/16 `
  --destination-port-ranges 5432 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir PostgreSQL solo desde la VNET"
```

Explicación:
•	--source-address-prefixes 10.0.0.0/16: Solo desde tu VNET, NO desde internet
•	Puerto 5432 es el puerto estándar de PostgreSQL

Denegar todo el tráfico público entrante
```
az network nsg rule create `
  --name DenyAllInbound `
  --nsg-name nsg-postgresql `
  --resource-group rg-bbva-red `
  --priority 4096 `
  --source-address-prefixes '*' `
  --destination-port-ranges '*' `
  --protocol '*' `
  --access Deny `
  --direction Inbound `
  --description "Denegar todo el tráfico público"
```

Asociar NSG a la subnet
```
az network vnet subnet update `
  --name snet-postgresql `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --network-security-group nsg-postgresql
```

- NSG para Storage Account

Crear NSG
```
az network nsg create `
  --name nsg-storage `
  --resource-group rg-bbva-red `
  --location eastus
```

Permitir acceso HTTPS solo desde la VNET
```
az network nsg rule create `
  --name AllowStorageFromVNET `
  --nsg-name nsg-storage `
  --resource-group rg-bbva-red `
  --priority 100 `
  --source-address-prefixes 10.0.0.0/16 `
  --destination-port-ranges 443 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir Storage solo desde VNET"
```

Denegar acceso público
```
az network nsg rule create `
  --name DenyPublicAccess `
  --nsg-name nsg-storage `
  --resource-group rg-bbva-red `
  --priority 4096 `
  --source-address-prefixes Internet `
  --destination-port-ranges '*' `
  --protocol '*' `
  --access Deny `
  --direction Inbound `
  --description "Denegar acceso público al Storage"
```

Asociar NSG a la subnet
```
az network vnet subnet update `
  --name snet-storage `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --network-security-group nsg-storage
```

- NSG para Databricks

Crear NSG
```
az network nsg create `
  --name nsg-databricks `
  --resource-group rg-bbva-red `
  --location eastus
```

Regla 1: Permitir comunicación con el control plane de Databricks
```
az network nsg rule create `
  --name AllowDatabricksControlPlane `
  --nsg-name nsg-databricks `
  --resource-group rg-bbva-red `
  --priority 100 `
  --source-address-prefixes AzureDatabricks `
  --destination-port-ranges 443 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir comunicación con control plane de Databricks"
```

Regla 2: Permitir comunicación interna entre nodos de Databricks
```
az network nsg rule create `
  --name AllowDatabricksInternal `
  --nsg-name nsg-databricks `
  --resource-group rg-bbva-red `
  --priority 110 `
  --source-address-prefixes VirtualNetwork `
  --destination-address-prefixes VirtualNetwork `
  --destination-port-ranges '*' `
  --protocol '*' `
  --access Allow `
  --direction Inbound `
  --description "Permitir comunicación interna de Databricks"
```

Asociar NSG a ambas subnets de Databricks
```
az network vnet subnet update `
  --name snet-databricks-public `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --network-security-group nsg-databricks
```
```
az network vnet subnet update `
  --name snet-databricks-private `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --network-security-group nsg-databricks
```

- NSG para Key Vault

Crear NSG
```
az network nsg create `
  --name nsg-keyvault `
  --resource-group rg-bbva-red `
  --location eastus
```

Permitir HTTPS solo desde la VNET
```
az network nsg rule create `
  --name AllowKeyVaultFromVNET `
  --nsg-name nsg-keyvault `
  --resource-group rg-bbva-red `
  --priority 100 `
  --source-address-prefixes 10.0.0.0/16 `
  --destination-port-ranges 443 `
  --protocol Tcp `
  --access Allow `
  --direction Inbound `
  --description "Permitir Key Vault solo desde VNET"
```

Denegar acceso público
```
az network nsg rule create `
  --name DenyPublicAccess `
  --nsg-name nsg-keyvault `
  --resource-group rg-bbva-red `
  --priority 4096 `
  --source-address-prefixes Internet `
  --destination-port-ranges '*' `
  --protocol '*' `
  --access Deny `
  --direction Inbound `
  --description "Denegar acceso público al Key Vault"
```

Asociar NSG a la subnet
```
az network vnet subnet update `
  --name snet-keyvault `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --network-security-group nsg-keyvault
```

12. Private DNS Zone

- DNS Zone para Storage Account (Blob)

Crear Private DNS Zone para Blob Storage
```
az network private-dns zone create `
  --name privatelink.blob.core.windows.net `
  --resource-group rg-bbva-red
```

Vincular la DNS Zone a la VNET
```
az network private-dns link vnet create `
  --name link-blob-to-vnet `
  --resource-group rg-bbva-red `
  --zone-name privatelink.blob.core.windows.net `
  --virtual-network vnet-bbva-dashboard `
  --registration-enabled false
```

Explicación:
•	--registration-enabled false: No registra automáticamente VMs en el DNS

- DNS Zone para Storage Account (DFS - Data Lake)

Crear Private DNS Zone para Data Lake Storage (DFS)
```
az network private-dns zone create `
  --name privatelink.dfs.core.windows.net `
  --resource-group rg-bbva-red
```

Vincular la DNS Zone a la VNET
```
az network private-dns link vnet create `
  --name link-dfs-to-vnet `
  --resource-group rg-bbva-red `
  --zone-name privatelink.dfs.core.windows.net `
  --virtual-network vnet-bbva-dashboard `
  --registration-enabled false
```

- DNS Zone para PostgreSQL

Crear Private DNS Zone para PostgreSQL
```
az network private-dns zone create `
  --name privatelink.postgres.database.azure.com `
  --resource-group rg-bbva-red
```

Vincular la DNS Zone a la VNET
```
az network private-dns link vnet create `
  --name link-postgres-to-vnet `
  --resource-group rg-bbva-red `
  --zone-name privatelink.postgres.database.azure.com `
  --virtual-network vnet-bbva-dashboard `
  --registration-enabled false
```

- DNS Zone para Key Vault

Crear Private DNS Zone para Key Vault
```
az network private-dns zone create `
  --name privatelink.vaultcore.azure.net `
  --resource-group rg-bbva-red
```

Vincular la DNS Zone a la VNET
```
az network private-dns link vnet create `
  --name link-keyvault-to-vnet `
  --resource-group rg-bbva-red `
  --zone-name privatelink.vaultcore.azure.net `
  --virtual-network vnet-bbva-dashboard `
  --registration-enabled false
```

- DNS Zone para Container Registry

Crear Private DNS Zone para ACR
```
az network private-dns zone create `
  --name privatelink.azurecr.io `
  --resource-group rg-bbva-red
```

Vincular la DNS Zone a la VNET
```
az network private-dns link vnet create `
  --name link-acr-to-vnet `
  --resource-group rg-bbva-red `
  --zone-name privatelink.azurecr.io `
  --virtual-network vnet-bbva-dashboard `
  --registration-enabled false
```

13. Private Endpoints

- Deshabilitar acceso público a los servicios

Para las llaves
```
az keyvault update `
  --name kv-bbva-dashboard `
  --resource-group rg-bbva-dashboard `
  --public-network-access Disabled
```

Para el contenedor
```
az acr update `
  --name acrbbvadashboard `
  --resource-group rg-bbva-dashboard `
  --sku Premium
  --public-network-enabled false  
```

- Private Endpoint para Storage Account (Blob)

Deshabilitar políticas de red en la subnet (requerido para Private Endpoints)
```
az network vnet subnet update `
  --name snet-storage `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --disable-private-endpoint-network-policies true
```

Crear Private Endpoint para Blob
```
az network private-endpoint create `
  --name pe-storage-blob `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --subnet snet-storage `
  --private-connection-resource-id $(az storage account show --name stbbvadatalake --resource-group rg-bbva-dashboard --query id -o tsv) `
  --group-id blob `
  --connection-name conn-storage-blob `
  --location eastus
```

Explicación:
•	--group-id blob: Tipo de servicio (blob, dfs, table, queue, file)
•	--private-connection-resource-id: ID del Storage Account

Crear registro DNS automático para Blob
```
az network private-endpoint dns-zone-group create `
  --name zg-storage-blob `
  --resource-group rg-bbva-red `
  --endpoint-name pe-storage-blob `
  --private-dns-zone privatelink.blob.core.windows.net `
  --zone-name blob
```

- Private Endpoint para Storage Account (DFS - Data Lake)

Crear Private Endpoint para DFS
```
az network private-endpoint create `
  --name pe-storage-dfs `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --subnet snet-storage `
  --private-connection-resource-id $(az storage account show --name stbbvadatalake --resource-group rg-bbva-dashboard --query id -o tsv) `
  --group-id dfs `
  --connection-name conn-storage-dfs `
  --location eastus
```

Crear registro DNS automático para DFS
```
az network private-endpoint dns-zone-group create `
  --name zg-storage-dfs `
  --resource-group rg-bbva-red `
  --endpoint-name pe-storage-dfs `
  --private-dns-zone privatelink.dfs.core.windows.net `
  --zone-name dfs
```

- Private Endpoint para PostgreSQL

Deshabilitar políticas de red en la subnet de PostgreSQL
```
az network vnet subnet update `
  --name snet-postgresql `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --disable-private-endpoint-network-policies true
```

Crear Private Endpoint para PostgreSQL
```
az network private-endpoint create `
  --name pe-postgresql `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --subnet snet-postgresql `
  --private-connection-resource-id $(az postgres flexible-server show --name pg-bbva-dashboard --resource-group rg-bbva-dashboard --query id -o tsv) `
  --group-id postgresqlServer `
  --connection-name conn-postgresql `
  --location eastus
```

Crear registro DNS automático
```
az network private-endpoint dns-zone-group create `
  --name zg-postgresql `
  --resource-group rg-bbva-red `
  --endpoint-name pe-postgresql `
  --private-dns-zone privatelink.postgres.database.azure.com `
  --zone-name postgres
```

- Private Endpoint para Key Vault

Deshabilitar políticas de red en la subnet de Key Vault
```
az network vnet subnet update `
  --name snet-keyvault `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --disable-private-endpoint-network-policies true
```

Crear Private Endpoint para Key Vault
```
az network private-endpoint create `
  --name pe-keyvault `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --subnet snet-keyvault `
  --private-connection-resource-id $(az keyvault show --name kv-bbva-dashboard --resource-group rg-bbva-dashboard --query id -o tsv) `
  --group-id vault `
  --connection-name conn-keyvault `
  --location eastus
```

Crear registro DNS automático

```
az network private-endpoint dns-zone-group create `
  --name zg-keyvault `
  --resource-group rg-bbva-red `
  --endpoint-name pe-keyvault `
  --private-dns-zone privatelink.vaultcore.azure.net `
  --zone-name vault
```

- Private Endpoint para Container Registry

Crear Private Endpoint para ACR
```
az network private-endpoint create `
  --name pe-acr `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --subnet snet-storage `
  --private-connection-resource-id $(az acr show --name acrbbvadashboard --resource-group rg-bbva-dashboard --query id -o tsv) `
  --group-id registry `
  --connection-name conn-acr `
  --location eastus
```

Crear registro DNS automático
```
az network private-endpoint dns-zone-group create `
  --name zg-acr `
  --resource-group rg-bbva-red `
  --endpoint-name pe-acr `
  --private-dns-zone privatelink.azurecr.io `
  --zone-name registry
```

14. Firewall

- Crear IP Pública para el Firewall

El Firewall necesita una IP pública estática
```
az network public-ip create `
  --name pip-firewall `
  --resource-group rg-bbva-red `
  --location eastus `
  --allocation-method Static `
  --sku Standard
```

Explicación:
•	--allocation-method Static: IP fija (no cambia)
•	--sku Standard: Requerido para Firewall

- Crear Azure Firewall Policy

Crear política de firewall
```
az network firewall policy create `
  --name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --location eastus `
  --sku Standard
```

Crear colección de reglas de aplicación (URLs permitidas)
```
az network firewall policy rule-collection-group create `
  --name rcg-app-rules `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --priority 100
```

Regla 1: Permitir acceso a servicios de Azure
```
az network firewall policy rule-collection-group collection add-filter-collection `
  --name rc-allow-azure `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-priority 100 `
  --action Allow `
  --rule-name AllowAzureServices `
  --rule-type ApplicationRule `
  --target-fqdns "*.azure.com" "*.microsoft.com" "*.windows.net" `
  --source-addresses 10.0.0.0/16 `
  --protocols Https=443
```
  
Explicación:
•	--target-fqdns: Dominios permitidos
•	*.azure.com: Servicios de Azure
•	--protocols Https=443: Solo HTTPS

Regla 2: Permitir acceso a Databricks
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowDatabricks `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule ` rule-type
  --target-fqdns "*.databricks.net" "*.azuredatabricks.net" `
  --source-addresses 10.0.3.0/24 10.0.4.0/24 `
  --protocols Https=443
```

Regla 3: Permitir npm y paquetes de Python (para Databricks)
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowPackages `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule `
  --target-fqdns "*.pypi.org" "*.npmjs.org" "*.github.com" `
  --source-addresses 10.0.0.0/16 `
  --protocols Https=443
```

Regla 4: Permitir el dominio del Container App
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowContainerAppBackend `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule `
  --target-fqdns "*.azurecontainerapps.io" `
  --source-addresses 10.0.0.0/16 `
  --protocols Https=443
```

Regla 5: Permitir tráfico desde el dominio del Static Web App
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowStaticWebApp `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule `
  --target-fqdns "*.azurestaticapps.net" `
  --source-addresses "*" `
  --protocols Https=443
```

- Crear el Azure Firewall

Crear el Firewall
```
az network firewall create `
  --name fw-bbva-dashboard `
  --resource-group rg-bbva-red `
  --location eastus `
  --vnet-name vnet-bbva-dashboard `
  --firewall-policy policy-bbva-firewall
```

Explicación:
•	--enable-dns-proxy true: El Firewall actúa como servidor DNS

Asociar la IP pública al Firewall
```
az network firewall ip-config create `
  --name fw-config `
  --firewall-name fw-bbva-dashboard `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --public-ip-address pip-firewall
```

- Obtener la IP privada del Firewall

```
$FIREWALL_PRIVATE_IP = az network firewall show `
  --name fw-bbva-dashboard `
  --resource-group rg-bbva-red `
  --query 'ipConfigurations[0].privateIPAddress' -o tsv

Write-Host "Firewall Private IP: $FIREWALL_PRIVATE_IP"
```

- Crear Route Table para dirigir tráfico al Firewall

Crear Route Table
```
az network route-table create `
  --name rt-firewall `
  --resource-group rg-bbva-red `
  --location eastus
```

Crear ruta: Todo el tráfico de salida va al Firewall
```
az network route-table route create `
  --name route-to-firewall `
  --resource-group rg-bbva-red `
  --route-table-name rt-firewall `
  --address-prefix 0.0.0.0/0 `
  --next-hop-type VirtualAppliance `
  --next-hop-ip-address $FIREWALL_PRIVATE_IP
```

Explicación:
•	--address-prefix 0.0.0.0/0: Todo el tráfico de internet
•	--next-hop-type VirtualAppliance: El Firewall es un "appliance virtual"

Asociar Route Table a las subnets
```
az network vnet subnet update `
  --name snet-containerapp `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --route-table rt-firewall
```
```
az network vnet subnet update `
  --name snet-databricks-public `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --route-table rt-firewall
```
```
az network vnet subnet update `
  --name snet-databricks-private `
  --resource-group rg-bbva-red `
  --vnet-name vnet-bbva-dashboard `
  --route-table rt-firewall
```

- Configurar Diagnostic Settings para el Firewall (enviar logs a Log Analytics)

```
$FIREWALL_ID = az network firewall show `
  --name fw-bbva-dashboard `
  --resource-group rg-bbva-red `
  --query id -o tsv
```
```
$LAW_ID = az monitor log-analytics workspace show `
  --resource-group rg-bbva-dashboard `
  --workspace-name law-bbva-dashboard `
  --query id -o tsv
```
```
az monitor diagnostic-settings create `
  --name diag-firewall `
  --resource $FIREWALL_ID `
  --workspace $LAW_ID `
  --logs '[{"category":"AzureFirewallApplicationRule","enabled":true},{"category":"AzureFirewallNetworkRule","enabled":true}
  --metrics '[{"category":"AllMetrics","enabled":true}]'
```

Algunas reglas adicionales

Esto hace que el firewall deje pasar la subida de archivos.
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowBlobStorage `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule `
  --target-fqdns "*.blob.core.windows.net" "*.dfs.core.windows.net" `
  --source-addresses 10.0.0.0/16 `
  --protocols Https=443
```

Asignar permisos a la identidad del Container App
```
$CONTAINER_APP_PRINCIPAL_ID = az containerapp show `
     --name bbva-backend-api `
     --resource-group rg-bbva-dashboard `
     --query identity.principalId -o tsv
```
```
az role assignment create `
  --assignee $CONTAINER_APP_PRINCIPAL_ID `
  --role "Storage Blob Data Contributor" `
  --scope $(az storage account show --name stbbvadatalake --resource-group rg-bbva-dashboard --query
```
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowStorageADLS `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule `
  --target-fqdns "*.blob.core.windows.net" "*.dfs.core.windows.net" "login.microsoftonline.com" "*.login.microsoftonline.com" "*.aadcdn.microsoftonline-p.com" `
  --source-addresses 10.0.0.0/16 `
  --protocols Https=443
```
```
az network firewall policy rule-collection-group collection rule add `
  --name AllowAzureManagement `
  --policy-name policy-bbva-firewall `
  --resource-group rg-bbva-red `
  --rcg-name rcg-app-rules `
  --collection-name rc-allow-azure `
  --rule-type ApplicationRule `
  --target-fqdns "management.azure.com" `
  --source-addresses 10.0.0.0/16 `
  --protocols Https=443
```

- Backup Vault

Registrar los providers
```
az provider register --namespace Microsoft.DataProtection
az provider register --namespace Microsoft.RecoveryServices
```

Crear Backup Vault
```
az dataprotection backup-vault create `
  --resource-group rg-bbva-dashboard `
  --vault-name rg-bbva-dashboard-backup `
  --location eastus `
  --storage-settings type="GeoRedundant" datastore-type="VaultStore"
```

Habilitar identidad administrada (System Assigned)
```
az dataprotection backup-vault update `
  --resource-group rg-bbva-dashboard `
  --vault-name rg-bbva-dashboard-backup `
  --set identity.type="SystemAssigned"
```

Activar Soft Delete
```
az storage account blob-service-properties update `
  --account-name stbbvadatalake `
  --resource-group rg-bbva-dashboard `
  --enable-delete-retention true `
  --delete-retention-days 30
```

Container Soft Delete
```
az storage account blob-service-properties update `
  --account-name stbbvadatalake `
  --resource-group rg-bbva-dashboard `
  --enable-container-delete-retention true `
  --container-delete-retention-days 30
```

Restore Status
```
az storage container restore-status show `
  --account-name stbbvadatalake `
  --resource-group rg-bbva-dashboard
```

Account Redundancy (GRS check)
```
az storage account show `
  --name stbbvadatalake `
  --resource-group rg-bbva-dashboard `
  --query sku.name -o tsv
```
