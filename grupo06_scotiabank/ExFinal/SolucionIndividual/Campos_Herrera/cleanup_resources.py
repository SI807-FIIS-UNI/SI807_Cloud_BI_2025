"""
SCRIPT DE LIMPIEZA DE RECURSOS AWS
Ejecutar DESPUÉS DEL EXAMEN para evitar costos

ADVERTENCIA: Esto eliminará TODOS los recursos creados
"""

import boto3
import json
import time

class ResourceCleaner:
    def __init__(self, config_file='aws_config.json'):
        """Carga configuración"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("❌ No se encontró aws_config.json")
            print("Deberás eliminar recursos manualmente desde AWS Console")
            return
        
        self.region = self.config['region']
        self.s3 = boto3.client('s3', region_name=self.region)
        self.glue = boto3.client('glue', region_name=self.region)
        self.sagemaker = boto3.client('sagemaker', region_name=self.region)
        self.iam = boto3.client('iam')
        
        print(f"✓ Configuración cargada")

    def delete_s3_buckets(self):
        """Elimina bucket S3 y todo su contenido"""
        print("\n" + "="*80)
        print("ELIMINANDO BUCKET S3")
        print("="*80)
        
        bucket_name = self.config['buckets']['main']
        print(f"\n⏳ Eliminando bucket: {bucket_name}")
        
        try:
            # Primero eliminar todos los objetos
            print("   • Listando objetos...")
            paginator = self.s3.get_paginator('list_object_versions')
            
            for page in paginator.paginate(Bucket=bucket_name):
                # Eliminar versiones
                if 'Versions' in page:
                    objects = [{'Key': obj['Key'], 'VersionId': obj['VersionId']} 
                             for obj in page['Versions']]
                    if objects:
                        self.s3.delete_objects(
                            Bucket=bucket_name,
                            Delete={'Objects': objects}
                        )
                        print(f"   • Eliminadas {len(objects)} versiones")
                
                # Eliminar delete markers
                if 'DeleteMarkers' in page:
                    markers = [{'Key': obj['Key'], 'VersionId': obj['VersionId']} 
                             for obj in page['DeleteMarkers']]
                    if markers:
                        self.s3.delete_objects(
                            Bucket=bucket_name,
                            Delete={'Objects': markers}
                        )
            
            # Eliminar bucket vacío
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"✓ Bucket eliminado: {bucket_name}")
            
        except Exception as e:
            print(f"⚠️  Error eliminando bucket {bucket_name}: {e}")

    def delete_glue_resources(self):
        """Elimina crawlers y database de Glue"""
        print("\n" + "="*80)
        print("ELIMINANDO RECURSOS DE GLUE")
        print("="*80)
        
        # Eliminar crawlers
        for layer, crawler_name in self.config['crawlers'].items():
            try:
                self.glue.delete_crawler(Name=crawler_name)
                print(f"✓ Crawler {layer} eliminado: {crawler_name}")
            except Exception as e:
                print(f"⚠️  Error eliminando crawler {crawler_name}: {e}")
        
        # Eliminar tablas
        db_name = self.config['glue_database']
        try:
            response = self.glue.get_tables(DatabaseName=db_name)
            for table in response['TableList']:
                table_name = table['Name']
                self.glue.delete_table(DatabaseName=db_name, Name=table_name)
                print(f"✓ Tabla eliminada: {table_name}")
        except Exception as e:
            print(f"⚠️  Error eliminando tablas: {e}")
        
        # Eliminar database
        try:
            self.glue.delete_database(Name=db_name)
            print(f"✓ Database eliminada: {db_name}")
        except Exception as e:
            print(f"⚠️  Error eliminando database: {e}")

    def delete_sagemaker_notebook(self):
        """Elimina notebook de SageMaker"""
        print("\n" + "="*80)
        print("ELIMINANDO NOTEBOOK DE SAGEMAKER")
        print("="*80)
        
        notebook_name = self.config['sagemaker_notebook']
        
        try:
            # Primero detener el notebook
            print(f"⏳ Deteniendo notebook: {notebook_name}")
            self.sagemaker.stop_notebook_instance(
                NotebookInstanceName=notebook_name
            )
            
            # Esperar a que se detenga
            print("   Esperando a que se detenga...")
            waiter = self.sagemaker.get_waiter('notebook_instance_stopped')
            waiter.wait(NotebookInstanceName=notebook_name)
            
            # Eliminar notebook
            self.sagemaker.delete_notebook_instance(
                NotebookInstanceName=notebook_name
            )
            print(f"✓ Notebook eliminado: {notebook_name}")
            
        except Exception as e:
            print(f"⚠️  Error eliminando notebook: {e}")

    def delete_iam_roles(self):
        """Elimina roles IAM"""
        print("\n" + "="*80)
        print("ELIMINANDO ROLES IAM")
        print("="*80)
        
        for role_type, role_arn in self.config['roles'].items():
            role_name = role_arn.split('/')[-1]
            
            try:
                # Primero desadjuntar políticas
                attached = self.iam.list_attached_role_policies(RoleName=role_name)
                for policy in attached['AttachedPolicies']:
                    self.iam.detach_role_policy(
                        RoleName=role_name,
                        PolicyArn=policy['PolicyArn']
                    )
                    print(f"   • Política desadjuntada: {policy['PolicyName']}")
                
                # Eliminar rol
                self.iam.delete_role(RoleName=role_name)
                print(f"✓ Rol {role_type} eliminado: {role_name}")
                
            except Exception as e:
                print(f"⚠️  Error eliminando rol {role_name}: {e}")

    def estimate_savings(self):
        """Estima costos evitados"""
        print("\n" + "="*80)
        print("ESTIMACIÓN DE COSTOS EVITADOS")
        print("="*80)
        
        costs = {
            'S3 (5 GB × 30 días)': 0.12,
            'SageMaker (ml.t3.medium × 720h)': 36.00,
            'QuickSight (30 días)': 0.00,  # Gratis primeros 30 días
            'Glue Database': 0.00,
            'Athena (queries)': 0.05
        }
        
        print("\n💰 COSTOS MENSUALES SI NO ELIMINAS:")
        total = 0
        for item, cost in costs.items():
            print(f"   • {item}: ${cost:.2f}")
            total += cost
        
        print(f"\n   TOTAL MENSUAL: ${total:.2f}")
        print(f"   AHORRO ANUAL: ${total * 12:.2f}")

    def cleanup_all(self):
        """Ejecuta limpieza completa"""
        print("\n" + "🗑️  "*20)
        print("INICIANDO LIMPIEZA DE RECURSOS AWS")
        print("🗑️  "*20)
        
        print("\n⚠️  ADVERTENCIA:")
        print("Esta acción eliminará PERMANENTEMENTE:")
        print("  • 1 bucket S3 y todos sus datos (bronze/silver/gold)")
        print("  • Glue database y tablas")
        print("  • 3 Glue crawlers")
        print("  • SageMaker notebook instance")
        print("  • 2 roles IAM")
        
        confirm = input("\n¿Estás SEGURO de continuar? (escribe 'ELIMINAR' para confirmar): ")
        
        if confirm != 'ELIMINAR':
            print("\n❌ Limpieza cancelada")
            return
        
        # Ejecutar limpieza
        self.delete_sagemaker_notebook()
        time.sleep(5)  # Dar tiempo a que SageMaker termine
        
        self.delete_glue_resources()
        self.delete_s3_buckets()
        self.delete_iam_roles()
        
        # Estimación de ahorros
        self.estimate_savings()
        
        print("\n" + "✅ "*20)
        print("LIMPIEZA COMPLETADA")
        print("✅ "*20)
        
        print("\n📋 VERIFICACIÓN FINAL:")
        print("1. Ve a S3 Console y verifica que no hay buckets bi-exam-*")
        print("   https://s3.console.aws.amazon.com/s3/buckets")
        print("\n2. Ve a SageMaker y verifica que no hay notebooks:")
        print("   https://console.aws.amazon.com/sagemaker/home#/notebook-instances")
        print("\n3. Verifica en Billing que no hay costos pendientes:")
        print("   https://console.aws.amazon.com/billing/")
        print("\n4. (Opcional) Elimina aws_config.json de tu PC")


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║           AWS RESOURCE CLEANUP - POST EXAMEN                   ║
║           ¡Evita costos innecesarios!                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    print("\n📌 IMPORTANTE:")
    print("• Ejecuta este script SOLO después de tu examen")
    print("• Asegúrate de haber exportado todos los dashboards")
    print("• Guarda copias de los notebooks con outputs")
    print("• Descarga transformation_logs.json si lo necesitas")
    
    proceed = input("\n¿Has guardado todo lo necesario? (si/no): ")
    
    if proceed.lower() not in ['si', 'sí', 's', 'yes', 'y']:
        print("\n✋ Regresa cuando hayas guardado todo")
        exit(0)
    
    try:
        cleaner = ResourceCleaner()
        cleaner.cleanup_all()
        
        print("\n🎉 ¡Recursos eliminados exitosamente!")
        print("Tu cuenta AWS está limpia y no generará más costos.")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nSi la limpieza automática falló, elimina recursos manualmente:")
        print("\n1. S3 Buckets:")
        print("   https://s3.console.aws.amazon.com/s3/buckets")
        print("\n2. SageMaker Notebooks:")
        print("   https://console.aws.amazon.com/sagemaker/home#/notebook-instances")
        print("\n3. Glue Resources:")
        print("   https://console.aws.amazon.com/glue/home")
        print("\n4. IAM Roles:")
        print("   https://console.aws.amazon.com/iam/home#/roles")