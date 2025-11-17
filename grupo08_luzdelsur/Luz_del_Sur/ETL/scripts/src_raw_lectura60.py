import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node src_raw_lectura60
src_raw_lectura60_node1763367019568 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="lectura", transformation_ctx="src_raw_lectura60_node1763367019568")

# Script generated for node trf_bronze_lectura60
trf_bronze_lectura60_node1763367052222 = ApplyMapping.apply(frame=src_raw_lectura60_node1763367019568, mappings=[("id_medidor", "long", "id_medidor", "long"), ("id_suministro", "long", "id_suministro", "long"), ("fecha_lectura", "string", "fecha_lectura", "date"), ("hora_lectura", "string", "hora_lectura", "string"), ("fecha_hora_lectura", "string", "fecha_hora_lectura", "timestamp"), ("energia_activa_kwh", "double", "energia_activa_kwh", "double"), ("energia_reactiva_kvarh", "double", "energia_reactiva_kvarh", "double"), ("demanda_kw", "double", "demanda_kw", "double"), ("tipo_registro", "string", "tipo_registro", "string"), ("calidad_dato", "string", "calidad_dato", "string"), ("frecuencia_min", "long", "frecuencia_min", "int"), ("origen_lectura", "string", "origen_lectura", "string"), ("ts_ingesta", "string", "ts_ingesta", "timestamp"), ("archivo_origen", "string", "archivo_origen", "string")], transformation_ctx="trf_bronze_lectura60_node1763367052222")

# Script generated for node tgt_bronze_lectura60
EvaluateDataQuality().process_rows(frame=trf_bronze_lectura60_node1763367052222, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763365096638", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
tgt_bronze_lectura60_node1763367110288 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/lectura/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="tgt_bronze_lectura60_node1763367110288")
tgt_bronze_lectura60_node1763367110288.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_lectura")
tgt_bronze_lectura60_node1763367110288.setFormat("glueparquet", compression="snappy")
tgt_bronze_lectura60_node1763367110288.writeFrame(trf_bronze_lectura60_node1763367052222)
job.commit()