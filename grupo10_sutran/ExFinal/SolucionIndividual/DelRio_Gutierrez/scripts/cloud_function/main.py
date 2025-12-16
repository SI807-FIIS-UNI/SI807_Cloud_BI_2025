def trigger_etl(event, context):
    import base64
    import datetime

    file_name = event['name']
    bucket = event['bucket']
    timestamp = datetime.datetime.utcnow().isoformat()

    log_line = f"[{timestamp}] Archivo recibido: gs://{bucket}/{file_name}\n"

    # Guardar log en archivo temporal
    with open('/tmp/upload_log.txt', 'a') as log_file:
        log_file.write(log_line)

    # (Opcional) Subir log a Cloud Storage
    from google.cloud import storage
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob('docs/upload_log.txt')
    blob.upload_from_filename('/tmp/upload_log.txt')

    print(f"Archivo procesado: {file_name}")
