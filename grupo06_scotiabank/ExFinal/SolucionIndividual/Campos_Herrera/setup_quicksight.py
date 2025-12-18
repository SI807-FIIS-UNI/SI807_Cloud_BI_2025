"""
SCRIPT DE CONFIGURACIÓN DE QUICKSIGHT
Ejecutar en TU PC con: python setup_quicksight.py

NOTA IMPORTANTE: QuickSight requiere configuración manual en AWS Console
Este script proporciona las instrucciones y verifica los requisitos previos
"""

import boto3
import json
import sys

class QuickSightSetup:
    def __init__(self, config_file='aws_config.json'):
        """Carga configuración"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.region = self.config['region']
        self.account_id = self.config['account_id']
        self.database = self.config['glue_database']
        
        self.athena = boto3.client('athena', region_name=self.region)
        self.glue = boto3.client('glue', region_name=self.region)
        
        print(f"✓ Configuración cargada")
        print(f"  • Región: {self.region}")
        print(f"  • Account: {self.account_id}")
        print(f"  • Database: {self.database}")

    def verify_athena_setup(self):
        """Verifica que Athena está configurado correctamente"""
        print("\n" + "="*80)
        print("VERIFICANDO CONFIGURACIÓN DE ATHENA")
        print("="*80)
        
        # Verificar que existen tablas en Glue
        try:
            response = self.glue.get_tables(DatabaseName=self.database)
            tables = response['TableList']
            
            if len(tables) == 0:
                print("❌ No se encontraron tablas en Glue")
                print("   Asegúrate de haber ejecutado los crawlers")
                return False
            
            print(f"✓ Se encontraron {len(tables)} tablas en Glue:")
            
            gold_tables = []
            for table in tables:
                table_name = table['Name']
                print(f"  • {table_name}")
                if table_name.startswith('gold_'):
                    gold_tables.append(table_name)
            
            if len(gold_tables) == 0:
                print("\n⚠️  ADVERTENCIA: No se encontraron tablas Gold")
                print("   Ejecuta primero el notebook 3_Oro.ipynb")
                return False
            
            print(f"\n✓ {len(gold_tables)} tablas Gold disponibles para QuickSight")
            return True
            
        except Exception as e:
            print(f"❌ Error al verificar Glue: {e}")
            return False

    def test_athena_query(self):
        """Prueba una query en Athena"""
        print("\n" + "="*80)
        print("PROBANDO QUERY EN ATHENA")
        print("="*80)
        
        # Crear bucket para resultados de Athena si no existe
        athena_bucket = f"aws-athena-query-results-{self.account_id}-{self.region}"
        s3 = boto3.client('s3')
        
        try:
            s3.head_bucket(Bucket=athena_bucket)
            print(f"✓ Bucket de resultados existe: {athena_bucket}")
        except:
            print(f"⏳ Creando bucket de resultados: {athena_bucket}")
            if self.region == 'us-east-1':
                s3.create_bucket(Bucket=athena_bucket)
            else:
                s3.create_bucket(
                    Bucket=athena_bucket,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            print("✓ Bucket creado")
        
        # Ejecutar query de prueba
        query = f"SELECT * FROM {self.database}.gold_kpi_global LIMIT 5;"
        
        print(f"\n⏳ Ejecutando query de prueba...")
        print(f"   {query}")
        
        try:
            response = self.athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={
                    'OutputLocation': f's3://{athena_bucket}/'
                }
            )
            
            query_id = response['QueryExecutionId']
            print(f"✓ Query ejecutada (ID: {query_id})")
            
            # Esperar resultado
            import time
            for i in range(30):
                status = self.athena.get_query_execution(QueryExecutionId=query_id)
                state = status['QueryExecution']['Status']['State']
                
                if state == 'SUCCEEDED':
                    print("✓ Query completada exitosamente")
                    return True
                elif state in ['FAILED', 'CANCELLED']:
                    print(f"❌ Query falló: {state}")
                    return False
                
                time.sleep(1)
            
            print("⚠️  Timeout esperando resultado")
            return False
            
        except Exception as e:
            print(f"❌ Error ejecutando query: {e}")
            return False

    def print_quicksight_instructions(self):
        """Imprime instrucciones para configurar QuickSight"""
        print("\n" + "="*80)
        print("INSTRUCCIONES PARA CONFIGURAR QUICKSIGHT")
        print("="*80)
        
        instructions = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                     CONFIGURACIÓN DE QUICKSIGHT                            ║
║                     (Paso a paso detallado)                                ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 PASO 1: HABILITAR QUICKSIGHT (Primera vez)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Ve a AWS Console: https://console.aws.amazon.com/quicksight
2. Haz clic en "Sign up for QuickSight" (si es primera vez)
3. Selecciona "Standard Edition" (GRATIS durante 30 días)
4. Configuración:
   • QuickSight account name: {self.config.get('project_name', 'bi-exam')}
   • Email: tu correo AWS
   • Region: {self.region}
   
5. Permisos importantes:
   ✅ Marca "Amazon Athena"
   ✅ Marca "Amazon S3"
   ✅ Selecciona tus buckets:
      - {self.config['buckets']['bronze']}
      - {self.config['buckets']['silver']}
      - {self.config['buckets']['gold']}
      - aws-athena-query-results-{self.account_id}-{self.region}

6. Haz clic en "Finish"

⚠️  IMPORTANTE: Si ya tienes QuickSight habilitado, verifica permisos:
   QuickSight → Manage QuickSight → Security & permissions → 
   QuickSight access to AWS services → Add/Remove → 
   Selecciona S3 y Athena

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PASO 2: CREAR DATASET DESDE ATHENA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. En QuickSight, haz clic en "Datasets" (menú izquierdo)
2. Haz clic en "New dataset"
3. Selecciona "Athena" como fuente de datos
4. Configuración de conexión:
   • Data source name: "BI_Exam_Gold_Data"
   • Athena workgroup: [primary]
   
5. Haz clic en "Validate connection" → debe decir "Successful"
6. Haz clic en "Create data source"

7. Seleccionar tablas:
   • Database: {self.database}
   • Tables: Selecciona TODAS las tablas que empiezan con "gold_"
     ✅ gold_kpi_mensual
     ✅ gold_kpi_top_n
     ✅ gold_kpi_segmentacion
     ✅ gold_kpi_global
     ✅ gold_kpi_tendencias (si existe)

8. Para cada tabla:
   • Haz clic en "Edit/Preview data"
   • Verifica que los datos se carguen correctamente
   • Ajusta tipos de datos si es necesario
   • Haz clic en "Save & publish"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 PASO 3: CREAR DASHBOARD 1 - OVERVIEW EJECUTIVO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. En QuickSight, haz clic en "Analyses" → "New analysis"
2. Selecciona el dataset "gold_kpi_global"
3. Haz clic en "Create analysis"

VISUALIZACIONES RECOMENDADAS:

┌─────────────────────────────────────────────────────────────┐
│ A) KPI CARDS (Números principales)                         │
└─────────────────────────────────────────────────────────────┘
   • Agrega visual → KPI
   • Value: "Total"
   • Formato: Número con separadores de miles
   • Repite para: Promedio, Máximo, Total Registros

┌─────────────────────────────────────────────────────────────┐
│ B) GRÁFICO DE TENDENCIA TEMPORAL                           │
└─────────────────────────────────────────────────────────────┘
   • Usa dataset: gold_kpi_mensual
   • Visual type: Line chart
   • X axis: mes/año
   • Value: total
   • Color: Por año (opcional)
   • Agrega forecast line si disponible

┌─────────────────────────────────────────────────────────────┐
│ C) TOP N RANKING                                            │
└─────────────────────────────────────────────────────────────┘
   • Usa dataset: gold_kpi_top_n
   • Visual type: Horizontal bar chart
   • Y axis: categoría (o ID con nombre)
   • Value: total
   • Sort: Descendente

┌─────────────────────────────────────────────────────────────┐
│ D) DISTRIBUCIÓN POR SEGMENTO                                │
└─────────────────────────────────────────────────────────────┘
   • Usa dataset: gold_kpi_segmentacion
   • Visual type: Pie chart o Donut chart
   • Group: primera dimensión categórica
   • Value: total

4. Ajusta diseño:
   • Haz clic en "Format visual" para personalizar colores
   • Agrega título descriptivo a cada visual
   • Ordena los visuales de manera lógica

5. Guarda como Dashboard:
   • File → Save as → "Dashboard 1 - Executive Overview"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PASO 4: CREAR DASHBOARD 2 - ANÁLISIS DETALLADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Crea nuevo análisis
2. Usa múltiples datasets (puedes agregar joins)

VISUALIZACIONES RECOMENDADAS:

┌─────────────────────────────────────────────────────────────┐
│ A) COMPARATIVA TEMPORAL (MES A MES)                         │
└─────────────────────────────────────────────────────────────┘
   • Visual: Clustered bar chart
   • X axis: mes
   • Value: total y promedio
   • Color: Por métrica

┌─────────────────────────────────────────────────────────────┐
│ B) HEATMAP DE SEGMENTACIÓN                                  │
└─────────────────────────────────────────────────────────────┘
   • Visual: Heat map
   • Rows: dimensión 1
   • Columns: dimensión 2
   • Values: total (suma)

┌─────────────────────────────────────────────────────────────┐
│ C) TABLA DETALLADA CON FILTROS                              │
└─────────────────────────────────────────────────────────────┘
   • Visual: Table
   • Columns: Todas las dimensiones + métricas clave
   • Agrega filtros interactivos arriba

┌─────────────────────────────────────────────────────────────┐
│ D) CRECIMIENTO % PERIODO A PERIODO                          │
└─────────────────────────────────────────────────────────────┘
   • Visual: Line + Bar combo chart
   • X axis: periodo
   • Bars: total
   • Line: crecimiento_pct

3. Agrega FILTROS globales:
   • Filter → Add filter
   • Aplica a: All visuals
   • Filtros recomendados: fecha, categoría principal

4. Guarda como Dashboard:
   • "Dashboard 2 - Detailed Analysis"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 PASO 5: PUBLICAR Y COMPARTIR (Para el profesor)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. En cada análisis:
   • Share → Publish dashboard
   • Name: "Dashboard X - [Nombre]"
   • Haz clic en "Publish"

2. Compartir con el profesor (si tiene AWS account):
   • Share → Share dashboard
   • Invite users → Ingresa email del profesor
   • Permission level: "Viewer"

3. ALTERNATIVA (sin compartir):
   • Export → PDF
   • Guarda como "Dashboard_1.pdf" y "Dashboard_2.pdf"
   • O toma screenshots de alta calidad

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 TIPS PARA IMPRESIONAR AL PROFESOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Usa colores consistentes en todos los dashboards
✅ Agrega tooltips descriptivos en cada visual
✅ Incluye fecha de última actualización
✅ Usa nombres claros y descriptivos
✅ Agrega filtros interactivos
✅ Usa drill-downs cuando sea posible
✅ Exporta a PDF para la presentación

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 ENLACES ÚTILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QuickSight Console:
https://console.aws.amazon.com/quicksight

Athena Console (para verificar queries):
https://{self.region}.console.aws.amazon.com/athena

Glue Console (para verificar tablas):
https://{self.region}.console.aws.amazon.com/glue

Documentación oficial:
https://docs.aws.amazon.com/quicksight/latest/user/welcome.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  RECORDATORIO DE COSTOS:
QuickSight Standard: GRATIS primeros 30 días
Después: $9 USD/mes por usuario

Asegúrate de cancelar la suscripción después del examen:
QuickSight → Manage QuickSight → Account settings → 
Unsubscribe
        """
        
        print(instructions)

    def generate_athena_queries(self):
        """Genera queries de ejemplo para probar"""
        print("\n" + "="*80)
        print("QUERIES DE EJEMPLO PARA ATHENA")
        print("="*80)
        
        queries = [
            {
                'name': 'Ver métricas globales',
                'query': f"SELECT * FROM {self.database}.gold_kpi_global;"
            },
            {
                'name': 'Top 10 por total',
                'query': f"SELECT * FROM {self.database}.gold_kpi_top_n ORDER BY total DESC LIMIT 10;"
            },
            {
                'name': 'Tendencia últimos 12 meses',
                'query': f"SELECT año, mes, total, crecimiento_pct FROM {self.database}.gold_kpi_mensual ORDER BY año DESC, mes DESC LIMIT 12;"
            },
            {
                'name': 'Resumen por categoría',
                'query': f"SELECT * FROM {self.database}.gold_kpi_segmentacion LIMIT 100;"
            }
        ]
        
        print("\n📝 Usa estas queries para probar en Athena Console:\n")
        for i, q in enumerate(queries, 1):
            print(f"{i}. {q['name']}:")
            print(f"   {q['query']}\n")
        
        # Guardar queries en archivo
        with open('athena_queries.sql', 'w') as f:
            f.write("-- QUERIES DE EJEMPLO PARA ATHENA --\n\n")
            for q in queries:
                f.write(f"-- {q['name']}\n")
                f.write(f"{q['query']}\n\n")
        
        print("✓ Queries guardadas en: athena_queries.sql")

    def run(self):
        """Ejecuta el setup completo"""
        print("\n" + "🚀 "*20)
        print("CONFIGURACIÓN DE QUICKSIGHT")
        print("🚀 "*20)
        
        # Verificar Athena
        if not self.verify_athena_setup():
            print("\n❌ Athena no está configurado correctamente")
            print("Asegúrate de haber ejecutado los notebooks y crawlers")
            return False
        
        # Probar query
        if not self.test_athena_query():
            print("\n⚠️  Athena funciona pero no se pudieron ejecutar queries")
            print("Verifica manualmente en Athena Console")
        
        # Generar queries de ejemplo
        self.generate_athena_queries()
        
        # Mostrar instrucciones
        self.print_quicksight_instructions()
        
        print("\n" + "✅ "*20)
        print("CONFIGURACIÓN COMPLETADA")
        print("✅ "*20)
        
        return True


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          QUICKSIGHT SETUP - CONFIGURACIÓN GUIADA               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        setup = QuickSightSetup()
        setup.run()
        
        print("\n🎯 PRÓXIMOS PASOS:")
        print("1. Sigue las instrucciones arriba para configurar QuickSight")
        print("2. Crea los 2 dashboards")
        print("3. Exporta a PDF o toma screenshots")
        print("4. ¡Listo para tu examen!")
        
    except FileNotFoundError:
        print("❌ ERROR: No se encontró aws_config.json")
        print("Primero ejecuta: python deploy_infrastructure.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)