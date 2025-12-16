import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import logging

connection_string = "DefaultEndpointsProtocol=https;AccountName=examenfinal1512;AccountKey=1nWT9DVHwDWOt4UsQmxAOAnuIKEF2igankmfroLzT7ujpqhx6Rdu/wFiJMFSDUOCMlaSZb+Kzcl/+AStBfoxMQ==;EndpointSuffix=core.windows.net"
container_name = "dataexamenfinal"
blob_name = "dataexamenfinal/data/rawdata/US_Accidents_March23.csv"

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        lector_main()
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def data_cleaning (df):
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

def lector_main():
    FilePath = "https://examenfinal1512.blob.core.windows.net/dataexamenfinal/data/rawdata/US_Accidents_March23.csv"
    df_aux = pd.DataFrame
    dim_ubicacion = pd.DataFrame()
    dim_clima = pd.DataFrame()
    dim_tiempo = pd.DataFrame()
    fact_accidentes = pd.DataFrame()
    df_aux = pd.ExcelFile(FilePath, engine="openpyxl")
    print (df_aux)
    return 0