"""
SCRIPT DE DESPLIEGUE DE INFRAESTRUCTURA AWS
Ejecutar en TU PC con: python deploy_infrastructure.py

Este script crea TODA la arquitectura necesaria en AWS:
- Buckets S3 (Bronce/Plata/Oro)
- Glue Database y Crawlers
- SageMaker Notebook Instance
- Roles IAM con permisos
"""

import boto3
import json
import time
from botocore.exceptions import ClientError

class AWSInfrastructureDeployer:
    def __init__(self, region='us-east-1', project_name='sin-exam'):
        """
        Inicializa el desplegador de infraestructura
        
        Args:
            region: Región de AWS (usa us-east-1 para costos más bajos)
            project_name: Nombre del proyecto (prefijo para recursos)
        """
        self.region = region
        self.project_name = project_name
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
        
        # Clientes AWS
        self.s3 = boto3.client('s3', region_name=region)
        self.glue = boto3.client('glue', region_name=region)
        self.iam = boto3.client('iam')
        self.sagemaker = boto3.client('sagemaker', region_name=region)
        
        print(f"✓ Conectado a AWS en región {region}")
        print(f"✓ Account ID: {self.account_id}")

    def create_s3_buckets(self):
        """Crea los 3 buckets para arquitectura medallion"""
        print("\n" + "="*60)
        print("PASO 1: Creando Buckets S3 (Medallion Architecture)")
        print("="*60)
        
        layers = ['bronze', 'silver', 'gold']
        bucket_names = {}
        
        for layer in layers:
            bucket_name = f"{self.project_name}-{layer}-{self.account_id}"
            bucket_names[layer] = bucket_name
            
            try:
                # Crear bucket
                if self.region == 'us-east-1':
                    self.s3.create_bucket(Bucket=bucket_name)
                else:
                    self.s3.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.region}
                    )
                
                # Habilitar versionado (buena práctica)
                self.s3.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                
                print(f"✓ Bucket creado: s3://{bucket_name}/")
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                    print(f"✓ Bucket ya existe: s3://{bucket_name}/")
                else:
                    print(f"✗ Error creando bucket {bucket_name}: {e}")
                    raise
        
        return bucket_names

    def create_iam_roles(self):
        """Crea roles IAM necesarios"""
        print("\n" + "="*60)
        print("PASO 2: Creando Roles IAM")
        print("="*60)
        
        roles = {}
        
        # 1. Rol para Glue Crawler
        glue_role_name = f"{self.project_name}-glue-role"
        glue_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "glue.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        
        try:
            glue_role = self.iam.create_role(
                RoleName=glue_role_name,
                AssumeRolePolicyDocument=json.dumps(glue_policy),
                Description="Role para Glue Crawler acceder a S3"
            )
            
            # Adjuntar políticas necesarias
            self.iam.attach_role_policy(
                RoleName=glue_role_name,
                PolicyArn='arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole'
            )
            self.iam.attach_role_policy(
                RoleName=glue_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
            )
            
            roles['glue'] = glue_role['Role']['Arn']
            print(f"✓ Rol Glue creado: {glue_role_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                roles['glue'] = f"arn:aws:iam::{self.account_id}:role/{glue_role_name}"
                print(f"✓ Rol Glue ya existe: {glue_role_name}")
            else:
                raise
        
        # 2. Rol para SageMaker Notebook
        sagemaker_role_name = f"{self.project_name}-sagemaker-role"
        sagemaker_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "sagemaker.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        
        try:
            sagemaker_role = self.iam.create_role(
                RoleName=sagemaker_role_name,
                AssumeRolePolicyDocument=json.dumps(sagemaker_policy),
                Description="Role para SageMaker acceder a S3 y Glue"
            )
            
            # Adjuntar políticas
            self.iam.attach_role_policy(
                RoleName=sagemaker_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess'
            )
            self.iam.attach_role_policy(
                RoleName=sagemaker_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess'
            )
            self.iam.attach_role_policy(
                RoleName=sagemaker_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess'
            )
            
            roles['sagemaker'] = sagemaker_role['Role']['Arn']
            print(f"✓ Rol SageMaker creado: {sagemaker_role_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'EntityAlreadyExists':
                roles['sagemaker'] = f"arn:aws:iam::{self.account_id}:role/{sagemaker_role_name}"
                print(f"✓ Rol SageMaker ya existe: {sagemaker_role_name}")
            else:
                raise
        
        # Esperar a que los roles se propaguen
        print("⏳ Esperando propagación de roles (30 seg)...")
        time.sleep(30)
        
        return roles

    def create_glue_database(self):
        """Crea base de datos en Glue Catalog"""
        print("\n" + "="*60)
        print("PASO 3: Creando Glue Database")
        print("="*60)
        
        db_name = f"{self.project_name}_db"
        
        try:
            self.glue.create_database(
                DatabaseInput={
                    'Name': db_name,
                    'Description': 'Database para examen de BI - Medallion Architecture'
                }
            )
            print(f"✓ Database creada: {db_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'AlreadyExistsException':
                print(f"✓ Database ya existe: {db_name}")
            else:
                raise
        
        return db_name

    def create_glue_crawlers(self, bucket_names, glue_role, db_name):
        """Crea crawlers para cada capa medallion"""
        print("\n" + "="*60)
        print("PASO 4: Creando Glue Crawlers")
        print("="*60)
        
        crawlers = {}
        
        for layer, bucket in bucket_names.items():
            crawler_name = f"{self.project_name}-{layer}-crawler"
            
            try:
                self.glue.create_crawler(
                    Name=crawler_name,
                    Role=glue_role,
                    DatabaseName=db_name,
                    Targets={
                        'S3Targets': [{
                            'Path': f"s3://{bucket}/"
                        }]
                    },
                    TablePrefix=f"{layer}_",
                    Description=f"Crawler para capa {layer.upper()}",
                    SchemaChangePolicy={
                        'UpdateBehavior': 'UPDATE_IN_DATABASE',
                        'DeleteBehavior': 'LOG'
                    }
                )
                
                crawlers[layer] = crawler_name
                print(f"✓ Crawler creado: {crawler_name}")
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'AlreadyExistsException':
                    crawlers[layer] = crawler_name
                    print(f"✓ Crawler ya existe: {crawler_name}")
                else:
                    raise
        
        return crawlers

    def create_sagemaker_notebook(self, sagemaker_role):
        """Crea instancia de SageMaker Notebook"""
        print("\n" + "="*60)
        print("PASO 5: Creando SageMaker Notebook Instance")
        print("="*60)
        
        notebook_name = f"{self.project_name}-notebook"
        
        try:
            self.sagemaker.create_notebook_instance(
                NotebookInstanceName=notebook_name,
                InstanceType='ml.t3.medium',  # Barato: $0.05/hora
                RoleArn=sagemaker_role,
                VolumeSizeInGB=10,
                DefaultCodeRepository='https://github.com/aws/amazon-sagemaker-examples.git'
            )
            
            print(f"✓ Notebook creado: {notebook_name}")
            print("⏳ Esperando que el notebook esté listo (esto toma 3-5 min)...")
            
            waiter = self.sagemaker.get_waiter('notebook_instance_in_service')
            waiter.wait(NotebookInstanceName=notebook_name)
            
            print("✓ Notebook está listo para usar!")
            
        except ClientError as e:
            if 'already exists' in str(e):
                print(f"✓ Notebook ya existe: {notebook_name}")
            else:
                raise
        
        return notebook_name

    def deploy_all(self):
        """Despliega toda la infraestructura"""
        print("\n" + "🚀 "*20)
        print("INICIANDO DESPLIEGUE DE INFRAESTRUCTURA AWS")
        print("🚀 "*20 + "\n")
        
        # Desplegar componentes
        bucket_names = self.create_s3_buckets()
        roles = self.create_iam_roles()
        db_name = self.create_glue_database()
        crawlers = self.create_glue_crawlers(bucket_names, roles['glue'], db_name)
        notebook_name = self.create_sagemaker_notebook(roles['sagemaker'])
        
        # Guardar configuración
        config = {
            'region': self.region,
            'account_id': self.account_id,
            'buckets': bucket_names,
            'glue_database': db_name,
            'crawlers': crawlers,
            'sagemaker_notebook': notebook_name,
            'roles': roles
        }
        
        with open('aws_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("\n" + "✅ "*20)
        print("DESPLIEGUE COMPLETADO EXITOSAMENTE")
        print("✅ "*20 + "\n")
        
        print("📋 RESUMEN DE RECURSOS CREADOS:")
        print(f"  • Buckets S3: {len(bucket_names)}")
        for layer, bucket in bucket_names.items():
            print(f"    - {layer.upper()}: s3://{bucket}/")
        print(f"  • Glue Database: {db_name}")
        print(f"  • Glue Crawlers: {len(crawlers)}")
        print(f"  • SageMaker Notebook: {notebook_name}")
        print(f"  • Roles IAM: {len(roles)}")
        
        print("\n📄 Configuración guardada en: aws_config.json")
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Ejecuta: python upload_csv.py tu_archivo.csv")
        print("2. Abre SageMaker en AWS Console")
        print(f"3. Inicia el notebook: {notebook_name}")
        print("4. Sube los notebooks de EDA/transformación")
        
        return config


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        AWS INFRASTRUCTURE DEPLOYER - EXAMEN BI                 ║
║        Arquitectura Medallion (Bronze/Silver/Gold)             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Verificar credenciales AWS
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print(f"✓ Autenticado como: {identity['Arn']}")
        
        # Confirmar despliegue
        print("\n⚠️  ADVERTENCIA:")
        print("Este script creará recursos en AWS que GENERAN COSTOS.")
        print("Costos estimados: ~$5-10 USD por el periodo del examen")
        print("\nRecursos a crear:")
        print("  - 3 buckets S3")
        print("  - 1 SageMaker Notebook (ml.t3.medium)")
        print("  - 3 Glue Crawlers")
        print("  - Roles IAM")
        
        confirm = input("\n¿Continuar con el despliegue? (si/no): ")
        
        if confirm.lower() in ['si', 'sí', 's', 'yes', 'y']:
            deployer = AWSInfrastructureDeployer()
            config = deployer.deploy_all()
            
            print("\n✅ ¡Todo listo para tu examen!")
            
        else:
            print("\n❌ Despliegue cancelado")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPosibles causas:")
        print("1. No tienes AWS CLI configurado (ejecuta: aws configure)")
        print("2. No tienes permisos suficientes")
        print("3. Ya alcanzaste límites de recursos en AWS")