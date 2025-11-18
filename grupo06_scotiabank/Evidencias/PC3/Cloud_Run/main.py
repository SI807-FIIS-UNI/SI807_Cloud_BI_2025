import functions_framework
from google.cloud import storage

@functions_framework.http
def create_hello_file(request):

    bucket_name = "grupo6_scotiabank_bucket"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    
    blob = bucket.blob("hello/hello.txt")
    blob.upload_from_string("hola", content_type="text/plain")

    return "Archivo hello.txt creado correctamente."
