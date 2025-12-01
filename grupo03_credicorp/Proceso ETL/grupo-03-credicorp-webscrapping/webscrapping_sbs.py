import pandas as pd
import io
import requests
from datetime import date
from azure.storage.blob import BlobServiceClient
from bs4 import BeautifulSoup
import datetime
import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

DRIVER = os.getenv("SQL_DRIVER","")
SERVER_NAME = os.getenv("SQL_SERVER_NAME","")
DATABASE_NAME = os.getenv("SQL_DATABASE_NAME","")
USERNAME = os.getenv("SQL_USERNAME","")
PASSWORD = os.getenv("SQL_PASSWORD","")
CONNECTION_STRING = (
    f'DRIVER={DRIVER};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    f'UID={USERNAME};'
    f'PWD={PASSWORD}'
)

inicio=datetime.datetime.now()
year = list(range(2021, date.today().year + 1))
#year = [2021,2022]
id_sector = ["B-2201"]
#id_sector = ["B-2201", "B-3101", "C-1101", "C-2101", "C-4103"]
month = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre","Diciembre"]
code_month = ["en", "fe", "ma", "ab", "my", "jn", "jl", "ag", "se", "oc", "no", "di"]

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "trusteddata"

def path_constructor(year, id_sector, month ,code_month):
    file_path = "https://intranet2.sbs.gob.pe/estadistica/financiera/"+str(year)+"/"+month+"/"+id_sector+"-"+code_month+str(year)+".XLS"
    return file_path

def subir_dataframe_a_blob(df, blob_filename):

    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME, 
            blob=blob_filename
        )

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        blob_client.upload_blob(csv_data, overwrite=True)

        print(f"Éxito: El archivo '{blob_filename}' ha sido subido a '{CONTAINER_NAME}'.")

    except Exception as ex:
        print(f"Error al subir el blob: {ex}")

def data_cleaning(df):
    df = (df.astype(str)
          .str.strip()
          .str.lower()
          .str.replace("   ", "  ")
          .str.replace("  ", " ")
          .str.replace(" ", "_")
          .str.replace("á", "a")
          .str.replace("é", "e")
          .str.replace("í", "i")
          .str.replace("ó", "o")
          .str.replace("ú", "u")
          .str.replace(r"[^\w]", "", regex=True))
    return df
def webscrapping():
    try:
        conn = pyodbc.connect(CONNECTION_STRING) 
        query = """WITH data AS (
                SELECT *, 1 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '11'
            
                UNION ALL
                -- BLOQUE 2
                SELECT *, 2 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '11'
            
                UNION ALL
                -- BLOQUE 3
                SELECT *, 3 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '12'
            
                UNION ALL
                -- BLOQUE 4
                SELECT *, 4 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '13'
            
                UNION ALL
                -- BLOQUE 5 (ORDEN PERSONALIZADO)
                SELECT *, 5 AS numero_bloque,
                    CASE 
                        WHEN codigo_cuenta = '1301' THEN 1
                        WHEN codigo_cuenta = '1303' THEN 2
                        WHEN codigo_cuenta = '1305' THEN 3
                        WHEN codigo_cuenta = '17'   THEN 4
                        WHEN codigo_cuenta = '1306' THEN 5
                        WHEN codigo_cuenta = '1309' THEN 6
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '13'
            
                UNION ALL
                -- BLOQUE 6
                SELECT *, 6 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '14'
            
                UNION ALL
                -- BLOQUE 7
                SELECT *, 7 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1401'
            
                UNION ALL
                -- BLOQUE 8 (ORDEN PERSONALIZADO)
                SELECT *, 8 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '1401.07.02' THEN 1
                        WHEN codigo_cuenta = '1401.07.05' THEN 2
                        WHEN codigo_cuenta = '1401.07.10' THEN 3
                        WHEN codigo_cuenta = '1401.07.06' THEN 4
                        WHEN codigo_cuenta = '1401.07.11' THEN 5
                        WHEN codigo_cuenta = '1401.04'    THEN 6
                        WHEN codigo_cuenta = '1401.07.26' THEN 7
                        WHEN codigo_cuenta = '1401.07.21' THEN 8
                        WHEN codigo_cuenta = '1401.04.99' THEN 9
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '1401'
            
                UNION ALL
                -- BLOQUE 9
                SELECT *, 9 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1403'
            
                UNION ALL
                -- BLOQUE 10
                SELECT *, 10 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1404'
            
                UNION ALL
                -- BLOQUE 11
                SELECT *, 11 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '1404'
            
                UNION ALL
                -- BLOQUE 12
                SELECT *, 12 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1409'
            
                UNION ALL
                -- BLOQUE 13
                SELECT *, 13 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1410'
            
                UNION ALL
                -- BLOQUE 14
                SELECT *, 14 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '15'
            
                UNION ALL
                -- BLOQUE 15
                SELECT *, 15 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1508'
            
                UNION ALL
                -- BLOQUE 16
                SELECT *, 16 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '1508'
            
                UNION ALL
                -- BLOQUE 17
                SELECT *, 17 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '16'
            
                UNION ALL
                -- BLOQUE 18
                SELECT *, 18 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '18'
            
                UNION ALL
                -- BLOQUE 19
                SELECT *, 19 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '19'
            
                UNION ALL
                -- BLOQUE 20
                SELECT *, 20 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '1'
            
                UNION ALL
                -- BLOQUE 21
                SELECT *, 21 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '21'
            
                UNION ALL
                -- BLOQUE 22
                SELECT *, 22 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('2101','2102','2103')
            
                UNION ALL
                -- BLOQUE 23
                SELECT *, 23 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '2103'
            
                UNION ALL
                -- BLOQUE 24
                SELECT *, 24 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('2107','2108')
            
                UNION ALL
                -- BLOQUE 25
                SELECT *, 25 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '2108'
            
                UNION ALL
                -- BLOQUE 26
                SELECT *, 26 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '23'
            
                UNION ALL
                -- BLOQUE 27
                SELECT *, 27 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '23'
            
                UNION ALL
                -- BLOQUE 28
                SELECT *, 28 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('22','24')
            
                UNION ALL
                -- BLOQUE 29
                SELECT *, 29 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '24'
            
                UNION ALL
                -- BLOQUE 30
                SELECT *, 30 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '2808'
            
                UNION ALL
                -- BLOQUE 31
                SELECT *, 31 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '2808'
            
                UNION ALL
                -- BLOQUE 32
                SELECT *, 32 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '25'
            
                UNION ALL
                -- BLOQUE 33
                SELECT *, 33 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '2001'
            
                UNION ALL
                -- BLOQUE 34 (ORDEN PERSONALIZADO)
                SELECT *, 34 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '2001.21' THEN 1
                        WHEN codigo_cuenta = '2001.23' THEN 2
                        WHEN codigo_cuenta = '2001.22' THEN 3
                        WHEN codigo_cuenta = '2001.24' THEN 4
                        WHEN codigo_cuenta = '2001.28' THEN 5
                        WHEN codigo_cuenta = '2001.25' THEN 6
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '2001'
            
                UNION ALL
                -- BLOQUE 35
                SELECT *, 35 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '29'
            
                UNION ALL
                -- BLOQUE 36
                SELECT *, 36 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '27'
            
                UNION ALL
                -- BLOQUE 37
                SELECT *, 37 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '27'
            
                UNION ALL
                -- BLOQUE 38
                SELECT *, 38 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '28'
            
                UNION ALL
                -- BLOQUE 39
                SELECT *, 39 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '2'
            
                UNION ALL
                -- BLOQUE 40
                SELECT *, 40 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '3'
            
                UNION ALL
                -- BLOQUE 41
                SELECT *, 41 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '3'
            
                UNION ALL
                -- BLOQUE 42
                SELECT *, 42 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '7'
            
                UNION ALL
                -- BLOQUE 43
                SELECT *, 43 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '7'
            
                UNION ALL
                -- BLOQUE 44
                SELECT *, 44 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '51'
            
                UNION ALL
                -- BLOQUE 45
                SELECT *, 45 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '51'
            
                UNION ALL
                -- BLOQUE 46
                SELECT *, 46 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '41'
            
                UNION ALL
                -- BLOQUE 47 (ORDEN PERSONALIZADO)
                SELECT *, 47 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '4102' THEN 1
                        WHEN codigo_cuenta = '4104' THEN 2
                        WHEN codigo_cuenta = '4106' THEN 3
                        WHEN codigo_cuenta = '4105' THEN 4
                        WHEN codigo_cuenta = '4109.01' THEN 5
                        WHEN codigo_cuenta = '4109.04' THEN 6
                        WHEN codigo_cuenta = '4109.05' THEN 7
                        WHEN codigo_cuenta = '4108'    THEN 8
                        WHEN codigo_cuenta = '4109.02' THEN 9
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN (
                    '4101','4103','4102','4104','4105','4106','4109.01','4109.04','4109.05','4108','4109.02'
                )
            
                UNION ALL
                -- BLOQUE 48
                SELECT *, 48 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '4109.99'
            
                UNION ALL
                -- BLOQUE 49 (ORDEN PERSONALIZADO)
                SELECT *, 49 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '61' THEN 1
                        WHEN codigo_cuenta = '62' THEN 2
                        WHEN codigo_cuenta = '63' THEN 3
                        WHEN codigo_cuenta = '52' THEN 4
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('61','62','63','52')
            
                UNION ALL
                -- BLOQUE 50
                SELECT *, 50 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '5202.02' THEN 1
                        WHEN codigo_cuenta = '5201'    THEN 2
                        WHEN codigo_cuenta = '5202.04' THEN 3
                        WHEN codigo_cuenta = '5202'    THEN 4
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '52'
            
                UNION ALL
                -- BLOQUE 51
                SELECT *, 51 AS numero_bloque, NULL AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta = '42'
            
                UNION ALL
                -- BLOQUE 52
                SELECT *, 52 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '4202.02' THEN 1
                        WHEN codigo_cuenta = '4202.07' THEN 2
                        WHEN codigo_cuenta = '4202.04' THEN 3
                        WHEN codigo_cuenta = '4202.3'  THEN 4
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '42'
            
                UNION ALL
                -- BLOQUE 53
                SELECT *, 53 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '64' THEN 1
                        WHEN codigo_cuenta = '65' THEN 2
                        WHEN codigo_cuenta = '45' THEN 3
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('64','65','45')
            
                UNION ALL
                -- BLOQUE 54
                SELECT *, 54 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '45'
            
                UNION ALL
                -- BLOQUE 55
                SELECT *, 55 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '6901' THEN 1
                        WHEN codigo_cuenta = '43'   THEN 2
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('6901','43')
            
                UNION ALL
                -- BLOQUE 56
                SELECT *, 56 AS numero_bloque,
                    CASE
                        WHEN codigo_cuenta = '4302'     THEN 1
                        WHEN codigo_cuenta = '4301'     THEN 2
                        WHEN codigo_cuenta = '4303'     THEN 3
                        WHEN codigo_cuenta = '4304'     THEN 4
                        WHEN codigo_cuenta = '4305'     THEN 5
                        WHEN codigo_cuenta = '8109.01'  THEN 6
                        WHEN codigo_cuenta = '8109.02'  THEN 7
                        ELSE 999
                    END AS orden_interno
                FROM cuentas_contables WHERE cuenta_padre = '43'
            
                UNION ALL
                -- BLOQUE 57
                SELECT *, 57 AS numero_bloque,
                    TRY_CAST(codigo_cuenta AS DECIMAL(18,5)) AS orden_interno
                FROM cuentas_contables WHERE codigo_cuenta IN ('56','66','68','69')
            
            )
            
            SELECT 
                codigo_cuenta,
                nombre_cuenta,
                nivel_cuenta,
                tipo_cuenta,
                cuenta_padre
            FROM data
            ORDER BY numero_bloque, orden_interno;"""
        df_bd = pd.read_sql(query, conn)
        conn.close()
        df_bd["nombre_cuenta"] = data_cleaning(df_bd["nombre_cuenta"])
        df_eeff = pd.DataFrame(
            columns=["codigo_cuenta", "nombre_cuenta", "valor_cuenta", "tipo_cuenta", "tipo_estado_financiero",
                    "nombre_empresa", "fecha"])

        cuentas_contables = pd.DataFrame()
        for id_sector in id_sector:
            for year in year:
                for i in range(12):
                    file_path = path_constructor(year, id_sector, month[i], code_month[i])
                    print(file_path)
                    r = requests.get(file_path)
                    soup = BeautifulSoup(r.text, "html.parser")
                    if r.status_code == 200:
                        excel_file = io.BytesIO(r.content)
                        with pd.ExcelFile(excel_file, engine="openpyxl") as xls:
                            for sheet in xls.sheet_names:
                                if sheet == "bg_cm" or sheet == "bg_cr" or sheet == "bg_edp" or sheet == "1":
                                    hoja = "bg"
                                elif sheet == "gyp_cm" or sheet == "gyp_cr" or sheet == "gyp_edp" or sheet == "2":
                                    hoja = "gyp"
                                df = pd.read_excel(xls, sheet_name=sheet, header=None)
                                dfaux = df
                                for j in range(dfaux.shape[1] // 4):
                                    columna = (4 * (j + 1) - 1)
                                    columnas = [12, columna]
                                    df = dfaux.iloc[:, columnas]
                                    df = df.dropna(how="all")
                                    if dfaux.iloc[5, 0] == "Activo":
                                        if id_sector == "C-1101" or id_sector == "C-4103":
                                            if dfaux.shape[0]==144:
                                                filas = list(range(5, 47)) + list(range(54,105))
                                            elif dfaux.shape[0]==143:
                                                filas = list(range(5, 47)) + list(range(53, 105))
                                        if id_sector == "C-2101":
                                            if dfaux.shape[0] == 144:
                                                filas = list(range(5, 47)) + list(range(54, 105))
                                            elif dfaux.shape[0] == 143:
                                                filas = list(range(5, 47)) + list(range(53, 105))
                                        if id_sector == "B-3101" or id_sector == "B-2201":
                                            if dfaux.shape[0] == 144:
                                                filas = list(range(5, 47)) + list(range(54, 105))
                                            elif dfaux.shape[0] == 143:
                                                filas = list(range(5, 47)) + list(range(53, 105))
                                    else:
                                        filas = list(range(4, 60))
                                    if len(df) != 0:
                                        df = df.reset_index(drop=True)
                                        df = df.iloc[filas,:]
                                        df.columns = ["cuenta", "valor"]
                                        df["cuenta"] = data_cleaning(df["cuenta"])
                                        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
                                        df['valor'] = df['valor'].fillna(0)
                                        df['tipo_estado_financiero'] = hoja
                                        df["empresa"] = dfaux.iloc[5, columna-2]
                                        df["empresa"] = data_cleaning(df["empresa"])
                                        df["fecha"] = dfaux.iloc[2, 0]
                                        df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m")
                                        if hoja == "bg":
                                            fila = list(range(93))
                                        if hoja == "gyp":
                                            fila = list(range(93, 149))
                                        df = df.reset_index(drop=True)
                                        df_eeff['codigo_cuenta'] = df_bd['codigo_cuenta'].iloc[fila].reset_index(drop=True)
                                        df_eeff['nombre_cuenta'] = df_bd["nombre_cuenta"].iloc[fila].reset_index(drop=True)
                                        df_eeff['valor_cuenta'] = df["valor"]
                                        df_eeff['tipo_cuenta'] = df_bd['tipo_cuenta'].iloc[fila].reset_index(drop=True)
                                        df_eeff['tipo_estado_financiero'] = df['tipo_estado_financiero']
                                        df_eeff['nombre_empresa'] = df["empresa"]
                                        df_eeff['fecha'] = df["fecha"]
                                        df_eeff.reset_index(drop=True)
                                        cuentas_contables = pd.concat([cuentas_contables, df_eeff], ignore_index=True)
                    else:
                        print("No se ha podido encontrar el archivo")
            cuentas_contables = cuentas_contables.dropna(how="all")
            destiny_path = "cuentas_contables.csv"
            subir_dataframe_a_blob(cuentas_contables,destiny_path)
            fin = datetime.datetime.now()
            print(fin - inicio)
    except Exception as e:
        print(e)
    return print("Proceso Terminado")