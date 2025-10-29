import pandas as pd
import numpy as np
import sys
import os

# --- Configuración ---
script_dir = os.path.dirname(__file__)
# Simplemente asigna la ruta absoluta
input_file = r"C:\Users\jesus\OneDrive\Documentos\Sistemas de Inteligencia de negocios\sot_historico.csv"

# Esta línea ya estaba perfecta
output_file = r"C:\Users\jesus\OneDrive\Documentos\Sistemas de Inteligencia de negocios\SI807_Cloud_BI_2025\grupo07_claro\data\processed\sot_historico_limpio.csv"

replacement_text = "Sin información"

# --- LISTA DE NOMBRES DE COLUMNAS ---
nombres_columnas = [
    'ID_SOT', 
    'Estado SOT', 
    'Fecha Creacion', 
    'Fecha Factibilidad', 
    'Fecha Atendido Rechazado', 
    'ID Rechazo', 
    'Departamento', 
    'Provincia', 
    'Distrito', 
    'Region'
]
# -------------------------------------

# --- Inicio del Script ---
print(f"Iniciando la limpieza de '{input_file}'...")

try:
    # --- MODIFICADO: Añadido header=None ---
    df = pd.read_csv(input_file, delimiter=',', dtype='str', header=None)
    # --------------------------------------
    print(f"Archivo cargado. {len(df)} filas y {len(df.columns)} columnas encontradas.")

except FileNotFoundError:
    print(f"--- ERROR ---")
    print(f"No se pudo encontrar el archivo: '{input_file}'")
    sys.exit()
except Exception as e:
    print(f"Ocurrió un error inesperado al leer el archivo: {e}")
    sys.exit()

# --- NUEVO: Asignar y verificar nombres de columnas ---
if len(nombres_columnas) == len(df.columns):
    df.columns = nombres_columnas
    print("Nombres de columna asignados correctamente.")
else:
    print(f"--- ERROR FATAL ---")
    print(f"La lista de nombres ({len(nombres_columnas)}) no coincide con las columnas del archivo ({len(df.columns)}).")
    sys.exit()
# --------------------------------------------------

# 2. Analizar y procesar las columnas
print("Analizando columnas y aplicando limpieza...")

for col in df.columns:
    
    es_texto = False
    try:
        # Intenta convertir a numérico (para identificar cols de texto)
        pd.to_numeric(df[col])
        es_texto = False 
    except ValueError:
        es_texto = True 

    if es_texto:
        # Ahora el print usará los nombres correctos (ej. 'Estado SOT')
        print(f"  > Procesando columna de texto: '{col}'")
        
        # Paso A: Rellenar nulos (NaN) y reemplazar strings vacíos ('')
        df[col] = df[col].fillna(replacement_text)
        df[col] = df[col].replace(r'^\s*$', replacement_text, regex=True)
        
        # -----------------------------------------------------------
        # Paso B: Convertir a formato "Nombre Propio" (Title Case)
        df[col] = df[col].str.title()
        # -----------------------------------------------------------

# 3. Guardar el archivo limpio
try:
    # --- NUEVO: Crear directorio de salida si no existe ---
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    # -------------------------------------------------

    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("\n¡Proceso completado exitosamente!")
    print(f"El archivo limpio ha sido guardado como: '{output_file}'")

except Exception as e:
    print(f"--- ERROR ---")
    print(f"Ocurrió un error al intentar guardar el archivo: {e}")