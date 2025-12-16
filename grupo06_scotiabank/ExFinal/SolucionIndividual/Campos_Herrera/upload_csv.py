"""
SCRIPT PARA SUBIR CSV A S3 (CAPA BRONZE)
Ejecutar en TU PC con: python upload_csv.py archivo.csv

Este script:
1. Lee el CSV que te den en el examen
2. Lo sube a la capa Bronze en S3
3. Ejecuta el Glue Crawler para catalogarlo
"""

import boto3
import json
import sys
import os
from datetime import datetime

class CSVUploader:
    def __init__(self, config_file='aws_config.json'):
        """Carga configuración de AWS"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.s3 = boto3.client('s3', region_name=self.config['region'])
        self.glue = boto3.client('glue', region_name=self.config['region'])
        
        print(f"✓ Configuración cargada desde {config_file}")

    def upload_csv(self, csv_path):
        """Sube CSV a capa Bronze"""
        print("\n" + "="*60)
        print("SUBIENDO CSV A CAPA BRONZE")
        print("="*60)
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
        
        # Información del archivo
        file_name = os.path.basename(csv_path)
        file_size = os.path.getsize(csv_path) / (1024 * 1024)  # MB
        
        print(f"📄 Archivo: {file_name}")
        print(f"📊 Tamaño: {file_size:.2f} MB")
        
        # Subir a Bronze
        bronze_bucket = self.config['buckets']['bronze']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"raw/{timestamp}_{file_name}"
        
        print(f"\n⏳ Subiendo a: s3://{bronze_bucket}/{s3_key}")
        
        self.s3.upload_file(
            csv_path,
            bronze_bucket,
            s3_key,
            ExtraArgs={'ServerSideEncryption': 'AES256'}
        )
        
        print("✓ Archivo subido exitosamente!")
        
        # Guardar ruta en config
        self.config['bronze_csv_path'] = f"s3://{bronze_bucket}/{s3_key}"
        self.config['csv_filename'] = file_name
        
        with open('aws_config.json', 'w') as f:
            json.dump(self.config, f, indent=2)
        
        return f"s3://{bronze_bucket}/{s3_key}"

    def run_glue_crawler(self):
        """Ejecuta crawler de Bronze para catalogar el CSV"""
        print("\n" + "="*60)
        print("EJECUTANDO GLUE CRAWLER")
        print("="*60)
        
        crawler_name = self.config['crawlers']['bronze']
        
        print(f"🕷️  Iniciando crawler: {crawler_name}")
        
        try:
            self.glue.start_crawler(Name=crawler_name)
            print("✓ Crawler iniciado!")
            print("⏳ El crawler tardará 1-2 minutos en completar...")
            print("\nPuedes verificar el progreso en:")
            print("AWS Console → Glue → Crawlers → " + crawler_name)
            
        except Exception as e:
            if 'CrawlerRunningException' in str(e):
                print("⚠️  El crawler ya está corriendo")
            else:
                raise

    def validate_upload(self):
        """Valida que el CSV se subió correctamente"""
        print("\n" + "="*60)
        print("VALIDANDO CARGA")
        print("="*60)
        
        bronze_bucket = self.config['buckets']['bronze']
        
        # Listar objetos en Bronze
        response = self.s3.list_objects_v2(
            Bucket=bronze_bucket,
            Prefix='raw/'
        )
        
        if 'Contents' in response:
            print(f"✓ Archivos en Bronze: {len(response['Contents'])}")
            for obj in response['Contents']:
                size_mb = obj['Size'] / (1024 * 1024)
                print(f"  - {obj['Key']} ({size_mb:.2f} MB)")
        else:
            print("⚠️  No hay archivos en Bronze")

    def process_csv(self, csv_path):
        """Pipeline completo: upload + crawler"""
        print("\n" + "🚀 "*20)
        print("INICIANDO CARGA DE CSV")
        print("🚀 "*20 + "\n")
        
        # 1. Subir archivo
        s3_path = self.upload_csv(csv_path)
        
        # 2. Ejecutar crawler
        self.run_glue_crawler()
        
        # 3. Validar
        self.validate_upload()
        
        print("\n" + "✅ "*20)
        print("CARGA COMPLETADA")
        print("✅ "*20 + "\n")
        
        print("📋 RESUMEN:")
        print(f"  • CSV subido a: {s3_path}")
        print(f"  • Crawler: {self.config['crawlers']['bronze']}")
        print(f"  • Database: {self.config['glue_database']}")
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Espera 2 minutos a que el crawler termine")
        print("2. Ve a SageMaker y abre tu notebook")
        print("3. Ejecuta 1_EDA.ipynb para explorar los datos")
        print("4. Verifica en Athena que puedes hacer queries:")
        print(f"   SELECT * FROM {self.config['glue_database']}.bronze_{self.config.get('csv_filename', 'table')} LIMIT 10;")
        
        return s3_path


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║              CSV UPLOADER - CAPA BRONZE                        ║
║              Arquitectura Medallion                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) < 2:
        print("❌ ERROR: Debes proporcionar el archivo CSV")
        print("\nUso:")
        print("  python upload_csv.py archivo.csv")
        print("\nEjemplo:")
        print("  python upload_csv.py ventas_2024.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    try:
        # Verificar que existe config
        if not os.path.exists('aws_config.json'):
            print("❌ ERROR: No se encontró aws_config.json")
            print("Primero ejecuta: python deploy_infrastructure.py")
            sys.exit(1)
        
        uploader = CSVUploader()
        uploader.process_csv(csv_path)
        
        print("\n✅ ¡Listo para comenzar el EDA en SageMaker!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()