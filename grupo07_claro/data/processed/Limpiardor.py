import pandas as pd
import numpy as np
import sys
import os

# --- Configuración ---
script_dir = os.path.dirname(__file__)
input_file = os.path.join(script_dir, "../raw/sot_historico.csv")
output_file = os.path.join(script_dir, "sot_historico_limpio.csv")
replacement_text = "Sin información"

# --- Inicio del Script ---
print(f"Iniciando la limpieza de '{input_file}'...")

try:
    df = pd.read_csv(input_file, delimiter=',', dtype='str')
    print(f"Archivo cargado. {len(df)} filas y {len(df.columns)} columnas encontradas.")

except FileNotFoundError:
    print(f"--- ERROR ---")
    print(f"No se pudo encontrar el archivo: '{input_file}'")
    sys.exit()
except Exception as e:
    print(f"Ocurrió un error inesperado al leer el archivo: {e}")
    sys.exit()

# 2. Analizar y procesar las columnas
print("Analizando columnas y aplicando limpieza...")

for col in df.columns:
    
    es_texto = False
    try:
        pd.to_numeric(df[col])
        es_texto = False 
    except ValueError:
        es_texto = True 

    if es_texto:
        print(f"  > Procesando columna de texto: '{col}'")
        
        # Paso A: Rellenar nulos (NaN) y reemplazar strings vacíos ('')
        df[col] = df[col].fillna(replacement_text)
        df[col] = df[col].replace(r'^\s*$', replacement_text, regex=True)
        
        # -----------------------------------------------------------
        # Paso B: Convertir a formato "Nombre Propio" (Title Case)
        # ¡ESTA ES LA LÍNEA CORREGIDA!
        df[col] = df[col].str.title()
        # -----------------------------------------------------------

# 3. Guardar el archivo limpio
try:
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n¡Proceso completado exitosamente!")
    print(f"El archivo limpio ha sido guardado como: '{output_file}'")

except Exception as e:
    print(f"--- ERROR ---")
    print(f"Ocurrió un error al intentar guardar el archivo: {e}")