# Iniciamos el login


# Creamos las carpetas en la capa bronce

  <img width="2167" height="575" alt="image" src="https://github.com/user-attachments/assets/18c4ce5d-648e-4d2c-b0fb-e8d22db99d66" />

# Subimos el archivo csv. desde nuestro escritorio a la carpeta bronce/raw/

az storage blob upload `
  --account-name azuresi807miguel `
  --container-name bronce `
  --file "C:\Users\migue\Desktop\superstore.csv" `
  --name "raw/superstore.csv" `
  --auth-mode login
