import logging
from cloudevents.http import CloudEvent
from functions_framework import cloud_event
import config.paths as paths
from pipelines.sbs.ratio_liquidez import run_pipeline_ratio_liquidez
from pipelines.sbs.depositos import run_pipeline_depositos
from pipelines.sbs.patrimonio import run_pipeline_patrimonio
from pipelines.sbs.creditos import run_pipeline_creditos



@cloud_event
def bronce_dispatcher(event: CloudEvent):
    data = event.data
    bucket = data.get("bucket")
    name = data.get("name")

    logging.info(f"[GEN2] Evento recibido. bucket={bucket}, name={name}")

    if bucket != paths.BUCKET_MONITOREADO:
        logging.info(f"Ignorado: evento de bucket distinto: {bucket}")
        return

    # Dispatcher por carpeta
    if name.startswith(paths.PREFIX_RATIO_LIQUIDEZ):
        run_pipeline_ratio_liquidez(bucket, name)
        return
    
    if name.startswith(paths.PREFIX_DEPOSITOS):
        logging.info(f"Pipeline: DEPOSITOS → {name}")
        run_pipeline_depositos(bucket, name)
        return
    
    if name.startswith(paths.PREFIX_PATRIMONIO_EFECTIVO):
        logging.info(f"Pipeline: PATRIMONIO → {name}")
        run_pipeline_patrimonio(bucket, name)
        return
    
    if name.startswith(paths.PREFIX_CREDITOS_SEGUN_SITUACION):
        logging.info(f"Pipeline: CREDITROS → {name}")
        run_pipeline_creditos(bucket, name)
        return

    if name.startswith(paths.PREFIX_BCRP_TIPO_CAMBIO):
        logging.info(f"Pipeline: TIPO CAMBIO → {name}")
        run_pipeline_depositos(bucket, name)
        return
    
    logging.info(f"Ignorado: {name} no coincide con ninguna carpeta monitoreada.")
