import azure.functions as func
import pandas as pd
from azure.storage.blob import BlobServiceClient, ContentSettings
from io import StringIO
import os
import logging

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

@app.blob_trigger(arg_name="myblob", 
                  path="dataexamenfinal/data/rawdata/US_Accidents_March23.csv",
                  connection="AzureWebJobsStorage")

def process_csv_blob(myblob: func.InputStream):
    logging.info(f"Procesando blob: {myblob.name}, Tamaño: {myblob.length} bytes")
    
    # Configuración
    connection_string = os.environ["AzureWebJobsStorage"]
    container_name = "dataexamenfinal"
    output_path = "data/processeddata"
    chunk_size = 300000
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        logging.info("Iniciando procesamiento por chunks...")
        total_rows = 0
        
        # Procesar el CSV por chunks
        for i, chunk in enumerate(pd.read_csv(myblob, chunksize=chunk_size, low_memory=False)):
            
            chunk_rows = len(chunk)
            total_rows += chunk_rows
            
            logging.info(f"Procesando chunk {i+1}: {chunk_rows:,} filas (Total acumulado: {total_rows:,})")
            
            is_first_chunk = (i == 0)
            
            # Procesar dim_ubicacion
            dim_ubicacion = chunk[['Street', 'City', 'County', 'State', 'Zipcode', 
                                   'Country', 'Timezone', 'Airport_Code']]
            append_to_blob(blob_service_client, container_name, 
                          f"{output_path}/dim_ubicacion.csv", dim_ubicacion, is_first_chunk)
            
            # Procesar dim_clima
            dim_clima = chunk[['Temperature(F)', 'Wind_Chill(F)', 'Humidity(%)', 
                              'Pressure(in)', 'Visibility(mi)', 'Wind_Direction', 
                              'Wind_Speed(mph)', 'Precipitation(in)', 'Weather_Condition']].copy()
            dim_clima.columns = ['Temperature_F', 'Wind_Chill_F', 'Humidity_Percent', 
                                'Pressure_In', 'Visibility_Mi', 'Wind_Direction', 
                                'Wind_Speed_Mph', 'Precipitation_In', 'Weather_Condition']
            append_to_blob(blob_service_client, container_name, 
                          f"{output_path}/dim_clima.csv", dim_clima, is_first_chunk)
            
            # Procesar fact_accidentes
            fact_accidentes = chunk[['Severity', 'Distance(mi)', 'Start_Lat', 'Start_Lng', 
                                    'End_Lat', 'End_Lng', 'Description', 'Amenity', 'Bump', 
                                    'Crossing', 'Give_Way', 'Junction', 'No_Exit', 'Railway', 
                                    'Roundabout', 'Station', 'Stop', 'Traffic_Calming', 
                                    'Traffic_Signal', 'Turning_Loop', 'Sunrise_Sunset', 
                                    'Civil_Twilight', 'Nautical_Twilight', 'Astronomical_Twilight']].copy()
            fact_accidentes.columns = ['severity', 'distance_mi', 'start_lat', 'start_lng', 
                                      'end_lat', 'end_lng', 'description', 'amenity', 'bump', 
                                      'crossing', 'give_way', 'junction', 'no_exit', 'railway', 
                                      'roundabout', 'station', 'stop', 'traffic_calming', 
                                      'traffic_signal', 'turning_loop', 'sunrise_sunset', 
                                      'civil_twilight', 'nautical_twilight', 'astronomical_twilight']
            append_to_blob(blob_service_client, container_name, 
                          f"{output_path}/fact_accidentes.csv", fact_accidentes, is_first_chunk)
            
            logging.info(f"✓ Chunk {i+1} procesado y guardado exitosamente")
        
        logging.info(f"¡Proceso completado! Total de filas procesadas: {total_rows:,}")
        logging.info(f"Archivos creados en {container_name}/{output_path}/:")
        logging.info("- dim_ubicacion.csv")
        logging.info("- dim_clima.csv")
        logging.info("- fact_accidentes.csv")
        
    except Exception as e:
        logging.error(f"Error en el procesamiento: {str(e)}")
        raise


def append_to_blob(blob_service_client, container_name, blob_path, dataframe, include_header):
    """
    Agrega datos de un DataFrame a un blob CSV.
    """
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)
        
        # Convertir DataFrame a CSV
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer, index=False, header=include_header)
        csv_data = csv_buffer.getvalue()
        
        if include_header:
            # Primer chunk: crear el blob
            blob_client.upload_blob(
                csv_data, 
                overwrite=True,
                content_settings=ContentSettings(content_type='text/csv')
            )
            logging.info(f"Blob {blob_path} creado con headers")
        else:
            # Chunks siguientes: agregar al blob existente
            existing_data = blob_client.download_blob().readall().decode('utf-8')
            combined_data = existing_data + csv_data
            
            blob_client.upload_blob(
                combined_data, 
                overwrite=True,
                content_settings=ContentSettings(content_type='text/csv')
            )
            logging.info(f"Datos agregados a {blob_path}")
            
    except Exception as e:
        logging.error(f"Error al escribir en blob {blob_path}: {str(e)}")
        raise