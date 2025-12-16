# Primero vas a descargar el fronted 

Link: https://drive.google.com/file/d/1UWatGW3aWJK5dbmadiidXsmLr8NycSjy/view?usp=sharing

hacer los siguientes comando dentro de la carpeta porfavor

```bash
npm install
```

```bash
npm run dev
```

# Luego vas a subirlo en un repositorio 
Es necesario para poder subirlo en el servicio de static web de azure
# Seguir los pasos para subirlo 

## 1. Crear el servicio de static web

<img width="2559" height="1402" alt="image" src="https://github.com/user-attachments/assets/a35f7f7f-b33e-4f62-8ddd-7b5dd0871a79" />

aqui completamos todo lo que se necesita para crear el servicio.

Creamos el servicio

<img width="2559" height="1400" alt="image" src="https://github.com/user-attachments/assets/72675d93-e762-4681-b9dd-6581d4ba0f93" />


## 2. 

Esperamos a que carga, 

<img width="2559" height="1400" alt="image" src="https://github.com/user-attachments/assets/9efe8961-4686-4ab0-811a-7101551ca2e8" />

Para que funcione, y use los datos de la capa de oro necesitamso hacer lo siguiente

<img width="2559" height="1342" alt="image" src="https://github.com/user-attachments/assets/c3b4a831-801f-435e-9235-cb68634a07a3" />

Completar como esta en la tercera fila. 

- https://victorious-pond-0ba9dcb0f.3.azurestaticapps.net
- Seleccionamos los 8
- *
- *
- 86400

y le damos en guardar.

## Error

Si sucede un error de que no puede lanzar el sitio , modificar el archivo azure-static-web-apps-victorious-pond-0ba9dcb0f.yml
que se encuentra dentro de la carpeta .github/workflows/

copiar y pegar el siguiente codigo para solucionar.

```bash
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
          persist-credentials: false
          lfs: false
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_VICTORIOUS_POND_0BA9DCB0F }}
          repo_token: ${{ secrets.GITHUB_TOKEN }} # Used for Github integrations (i.e. PR comments)
          action: "upload"
          ###### Repository/Build Configurations - These values can be configured to match your app requirements. ######
          # For more information regarding Static Web App workflow configurations, please visit: https://aka.ms/swaworkflowconfig
          app_location: "/" # App source code path
          api_location: "" # Api source code path - optional
          output_location: "dist" # Built app content directory - optional
          ###### End of Repository/Build Configurations ######

  close_pull_request_job:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close Pull Request Job
    steps:
      - name: Close Pull Request
        id: closepullrequest
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_VICTORIOUS_POND_0BA9DCB0F }}
          action: "close"
```

## Aqui se vera la pagina en funcionamiento

https://victorious-pond-0ba9dcb0f.3.azurestaticapps.net/

<img width="2559" height="1407" alt="image" src="https://github.com/user-attachments/assets/efe3ed44-7d1d-46fd-a593-fdc01ed6ebcb" />


<img width="2554" height="1400" alt="image" src="https://github.com/user-attachments/assets/04b4ebd2-bd78-40e3-8e7f-b2d589a8fd30" />

<img width="2559" height="1398" alt="image" src="https://github.com/user-attachments/assets/023242ee-8ad8-4e55-b41d-2b71eccbcd57" />

<img width="2559" height="1390" alt="image" src="https://github.com/user-attachments/assets/49019548-3a05-4959-a784-071919563ac2" />

