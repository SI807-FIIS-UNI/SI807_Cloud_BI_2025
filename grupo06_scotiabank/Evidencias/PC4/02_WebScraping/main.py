"""
Cloud Function para descarga directa de reportes SBS
Descarga solo archivos nuevos usando URLs directas (sin scraping)
Versión optimizada: ~10x más rápida que el enfoque con scraping
"""
import os
import csv
import requests
from datetime import datetime
from google.cloud import storage
import functions_framework
from io import StringIO

# -----------------------------
# CONFIGURACIÓN
# -----------------------------

REPORTES_CONFIG = {
    "B-2201": "EEFF",
    "B-2315": "CREDITOS_SEGUN_SITUACION",
    "B-2344": "DEPOSITOS",
    "B-2370": "PATRIMONIO_EFECTIVO",
    "B-2340": "RATIO_LIQUIDEZ",
    "B-2402": "PATRIMONIO_REQUERIDO_RCG"
}

MESES = {
    1: "en",  2: "fe",  3: "ma",  4: "ab",
    5: "my",  6: "jn",  7: "jl",  8: "ag",
    9: "se", 10: "oc", 11: "no", 12: "di"
}

TRADUCCION_MESES = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Setiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

BUCKET_NAME = "grupo6_scotiabank_bucket"
BASE_PATH = "data/raw/SBS"
LOG_PATH = "logs/descargas_sbs.csv"

ANIO_INICIO = 2016


class SBSDownloader:
    """
    Descargador optimizado de reportes SBS
    Usa URLs directas en lugar de scraping (mucho más rápido)
    """
    
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(BUCKET_NAME)
        self.log_buffer = StringIO()
        self.log_writer = csv.writer(self.log_buffer)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "UNI/Proyecto-Academico_SIN"
        })
        
        # Escribir cabecera del log
        self.log_writer.writerow([
            "fecha_ejecucion",
            "reporte",
            "anio",
            "mes",
            "archivo",
            "estado",
            "url"
        ])
    
    def get_existing_files(self, carpeta):
        """Obtiene conjunto de archivos ya existentes en GCS"""
        prefix = f"{BASE_PATH}/{carpeta}/"
        blobs = self.bucket.list_blobs(prefix=prefix)
        return {blob.name.split('/')[-1] for blob in blobs}
    
    def log_evento(self, reporte, anio, mes, archivo, estado, url):
        """Registra evento en el buffer de log CSV"""
        self.log_writer.writerow([
            datetime.now().isoformat(),
            reporte,
            anio,
            mes,
            archivo,
            estado,
            url
        ])
    
    def upload_to_gcs(self, file_content, carpeta, filename):
        """Sube archivo a Google Cloud Storage"""
        blob_name = f"{BASE_PATH}/{carpeta}/{filename}"
        blob = self.bucket.blob(blob_name)
        blob.upload_from_string(file_content)
    
    def save_log_to_gcs(self):
        """Guarda el log CSV en Cloud Storage"""
        log_content = self.log_buffer.getvalue()
        
        # Obtener log existente si existe
        log_blob = self.bucket.blob(LOG_PATH)
        existing_log = ""
        
        try:
            existing_log = log_blob.download_as_text()
        except:
            # Si no existe el log, crear con cabecera
            pass
        
        # Si existe log, remover cabecera del nuevo contenido
        if existing_log:
            lines = log_content.split('\n')
            log_content = '\n'.join(lines[1:])  # Saltar cabecera
            final_log = existing_log.rstrip('\n') + '\n' + log_content
        else:
            final_log = log_content
        
        log_blob.upload_from_string(final_log)
        print(f"✓ Log guardado en gs://{BUCKET_NAME}/{LOG_PATH}")
    
    def descargar_archivo(self, url, carpeta, filename, reporte, anio, mes, existing_files):
        """Descarga archivo solo si no existe en GCS"""
        
        # VALIDACIÓN 1: evitar descargar si ya existe
        if filename in existing_files:
            print(f"⏩ Ya existe: {filename}")
            self.log_evento(reporte, anio, mes, filename, "EXISTE", url)
            return False
        
        try:
            resp = self.session.get(url, timeout=15)
            
            if resp.status_code == 200:
                # Subir directamente a GCS
                self.upload_to_gcs(resp.content, carpeta, filename)
                print(f"✔ Descargado: {filename}")
                self.log_evento(reporte, anio, mes, filename, "DESCARGADO", url)
                return True
            else:
                print(f"✘ No existe: {filename} (status {resp.status_code})")
                self.log_evento(reporte, anio, mes, filename, "NO_EXISTE_EN_SERVIDOR", url)
                return False
        
        except Exception as e:
            print(f"⚠ Error descargando {filename}: {e}")
            self.log_evento(reporte, anio, mes, filename, "ERROR", url)
            return False
    
    def construir_url(self, reporte, anio, mes_num):
        """Construye la URL directa del archivo SBS"""
        mes_cod = MESES[mes_num]
        mes_en = datetime(1900, mes_num, 1).strftime("%B")
        mes_nombre = TRADUCCION_MESES[mes_en]
        
        url = (
            f"https://intranet2.sbs.gob.pe/estadistica/financiera/"
            f"{anio}/{mes_nombre}/{reporte}-{mes_cod.lower()}{anio}.XLS"
        )
        
        return url
    
    def procesar_reporte(self, reporte, carpeta):
        """Procesa un reporte completo (todos los años y meses)"""
        print(f"\n{'='*60}")
        print(f"Procesando: {reporte} → {carpeta}")
        print(f"{'='*60}")
        
        # Obtener archivos existentes
        existing_files = self.get_existing_files(carpeta)
        print(f"Archivos existentes en GCS: {len(existing_files)}")
        
        anio_fin = datetime.now().year
        descargados = 0
        
        for anio in range(ANIO_INICIO, anio_fin + 1):
            for mes_num in range(1, 13):
                mes_cod = MESES[mes_num]
                # Construir URL y nombre de archivo
                url = self.construir_url(reporte, anio, mes_num)
                filename = f"{reporte}-{mes_cod.lower()}{anio}.xls"
                
                # Descargar
                if self.descargar_archivo(url, carpeta, filename, reporte, 
                                         anio, mes_num, existing_files):
                    descargados += 1
        
        print(f"✓ Completado {reporte}: {descargados} archivos nuevos")
        return descargados
    
    def ejecutar(self, reporte_especifico=None):
        """Ejecuta la descarga de todos los reportes o uno específico"""
        start_time = datetime.now()
        print(f"Inicio: {start_time.isoformat()}")
        
        total_descargados = 0
        resultados = {}
        
        if reporte_especifico:
            # Procesar solo un reporte
            if reporte_especifico in REPORTES_CONFIG:
                carpeta = REPORTES_CONFIG[reporte_especifico]
                count = self.procesar_reporte(reporte_especifico, carpeta)
                resultados[reporte_especifico] = count
                total_descargados = count
            else:
                return None, f"Reporte '{reporte_especifico}' no válido"
        else:
            # Procesar todos los reportes
            for reporte, carpeta in REPORTES_CONFIG.items():
                try:
                    count = self.procesar_reporte(reporte, carpeta)
                    resultados[reporte] = count
                    total_descargados += count
                except Exception as e:
                    print(f"⚠ Error procesando {reporte}: {e}")
                    resultados[reporte] = f"ERROR: {str(e)}"
        
        # Guardar log en GCS
        self.save_log_to_gcs()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        response = {
            "status": "success",
            "timestamp": start_time.isoformat(),
            "duration_seconds": round(duration, 2),
            "total_archivos_descargados": total_descargados,
            "resultados_por_reporte": resultados,
            "log_guardado_en": f"gs://{BUCKET_NAME}/{LOG_PATH}"
        }
        
        print(f"\n{'='*60}")
        print(f"RESUMEN FINAL")
        print(f"{'='*60}")
        print(f"Total archivos nuevos: {total_descargados}")
        print(f"Duración: {duration:.2f} segundos")
        
        return response, None


@functions_framework.http
def sbs_downloader_http(request):
    """
    HTTP Cloud Function para descarga de reportes SBS
    
    Parámetros opcionales:
    - formato: código de reporte específico (ej: "B-2201")
    
    Ejemplo de uso:
    - Todos los reportes: POST sin parámetros
    - Un reporte: POST {"formato": "B-2201"}
    """
    
    try:
        # Obtener parámetros
        request_json = request.get_json(silent=True)
        request_args = request.args
        
        formato_especifico = None
        if request_json and 'formato' in request_json:
            formato_especifico = request_json['formato']
        elif request_args and 'formato' in request_args:
            formato_especifico = request_args['formato']
        
        # Ejecutar descarga
        downloader = SBSDownloader()
        response, error = downloader.ejecutar(formato_especifico)
        
        if error:
            return {"error": error}, 400
        
        return response, 200
    
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, 500