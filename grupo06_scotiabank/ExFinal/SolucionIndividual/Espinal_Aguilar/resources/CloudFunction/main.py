import logging
from cloudevents.http import CloudEvent
from functions_framework import cloud_event
import config.paths as paths
from pipelines.proceso_elt import run_pipeline

@cloud_event
def final_dispatcher(event: CloudEvent):
    data = event.data
    bucket = data.get("bucket")
    name = data.get("name")

    logging.info(f"[GEN2] Evento recibido. bucket={bucket}, name={name}")

    if bucket != paths.BUCKET_MONITOREADO:
        logging.info(f"Ignorado: evento de bucket distinto: {bucket}")
        return

    # Dispatcher
    if name.startswith(paths.ROOT_RAW):
        run_pipeline(bucket, name)
        return
    
    logging.info(f"Ignorado: {name} no coincide con ninguna carpeta monitoreada.")
