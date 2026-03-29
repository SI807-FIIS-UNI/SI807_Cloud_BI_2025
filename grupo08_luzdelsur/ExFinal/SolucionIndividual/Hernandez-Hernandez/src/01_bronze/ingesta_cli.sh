# --- CONFIGURACIÓN DE VARIABLES ---
# Usamos el nombre de tu storage creado: datalakemichi1
# Usamos el nombre de tu container creado: bronce
account_name="datalakemichi1"
container_name="bronce"

echo "--- INICIANDO CONFIGURACIÓN DE ESTRUCTURA BRONCE ---"

# 1. Crear la estructura de carpetas obligatoria (raw, processed, curated)
# El examen pide explícitamente estas 3 carpetas.
az storage fs directory create -n raw -f $container_name --account-name $account_name --auth-mode login
az storage fs directory create -n processed -f $container_name --account-name $account_name --auth-mode login
az storage fs directory create -n curated -f $container_name --account-name $account_name --auth-mode login

echo "Carpetas creadas exitosamente."

echo "--- SUBIENDO ARCHIVOS CSV A LA CAPA RAW ---"

# 2. Subir los 5 archivos CSV a la carpeta 'raw'
# Asumimos que los archivos ya están subidos en el directorio actual de Cloud Shell
az storage fs file upload -s "city_day.csv" -p "raw/city_day.csv" -f $container_name --account-name $account_name --auth-mode login
az storage fs file upload -s "city_hour.csv" -p "raw/city_hour.csv" -f $container_name --account-name $account_name --auth-mode login
az storage fs file upload -s "station_day.csv" -p "raw/station_day.csv" -f $container_name --account-name $account_name --auth-mode login
az storage fs file upload -s "station_hour.csv" -p "raw/station_hour.csv" -f $container_name --account-name $account_name --auth-mode login
az storage fs file upload -s "stations.csv" -p "raw/stations.csv" -f $container_name --account-name $account_name --auth-mode login

echo "--- ¡INGESTA COMPLETADA! ---"