# Flujo de Implementación
## 1. Creación del Grupo de Recurso
<img width="886" height="449" alt="image" src="https://github.com/user-attachments/assets/d1ed9148-c217-4e6e-907e-37248636441f" />
## 2. Creación del Storage Account (Datalake)
<img width="886" height="433" alt="image" src="https://github.com/user-attachments/assets/ec94b23b-1e64-47d5-8e44-23faf13c3709" />
### 2.1. Creación de los Contenedores en el Datalake
<img width="886" height="431" alt="image" src="https://github.com/user-attachments/assets/302db43b-8f37-4b1e-8a56-229d27f596a5" />
### 2.2. Creación de las Carpetas en el Datalake
#### 2.2.1 En bronce
/raw
/processed
/curated
<img width="886" height="451" alt="image" src="https://github.com/user-attachments/assets/53e7c87d-fa38-4708-9494-2f7335845e39" />
- Usando CLI cargar CSV desde el escritorio: El archivo CSV llamado "" está en la carpeta "csv crudo"
<img width="1060" height="586" alt="image" src="https://github.com/user-attachments/assets/8fef19b0-e6f4-4f0f-81ab-ed4ddb99797b" />
```
az login
az storage blob upload `
  --account-name azdatalakefinal `
  --container-name bronce `
  --name raw/<Retail_Transactions_Dataset.csv `
  --file "$env:USERPROFILE\Desktop\csv crudo\Retail_Transactions_Dataset.csv" `
  --auth-mode key
```
#### 2.2.2 En plata
/dimensiones
/hechos
<img width="886" height="449" alt="image" src="https://github.com/user-attachments/assets/9ca9555b-a41c-4105-a118-7f1ff84fdbef" />
#### 2.2.3 En oro
/kpis
<img width="886" height="448" alt="image" src="https://github.com/user-attachments/assets/ad87b0b4-01a6-4470-aebd-44768ba1334c" />
- Definir KPIs





## 


## 


## 

## 


## 
