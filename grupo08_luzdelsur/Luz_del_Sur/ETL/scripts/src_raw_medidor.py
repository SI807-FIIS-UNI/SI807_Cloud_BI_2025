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

# Script generated for node src_raw_medidor
src_raw_medidor_node1763365099704 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="medidor", transformation_ctx="src_raw_medidor_node1763365099704")

# Script generated for node trf_bronze_medidor
trf_bronze_medidor_node1763365141553 = ApplyMapping.apply(frame=src_raw_medidor_node1763365099704, mappings=[("id_medidor", "long", "id_medidor", "long"), ("nro_medidor", "string", "nro_medidor", "string"), ("id_suministro", "long", "id_suministro", "long"), ("tipo_medidor", "string", "tipo_medidor", "string"), ("tecnologia", "string", "tecnologia", "string"), ("modelo", "string", "modelo", "string"), ("marca", "string", "marca", "string"), ("constante", "double", "constante", "double"), ("tension_nominal", "string", "tension_nominal", "string"), ("fecha_instalacion", "string", "fecha_instalacion", "date"), ("fecha_retiro", "string", "fecha_retiro", "date"), ("estado_medidor", "string", "estado_medidor", "string"), ("es_principal", "string", "es_principal", "string")], transformation_ctx="trf_bronze_medidor_node1763365141553")

# Script generated for node tgt_bronze_medidor
EvaluateDataQuality().process_rows(frame=trf_bronze_medidor_node1763365141553, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763365096638", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
tgt_bronze_medidor_node1763365363469 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/medidor/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="tgt_bronze_medidor_node1763365363469")
tgt_bronze_medidor_node1763365363469.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_medidor")
tgt_bronze_medidor_node1763365363469.setFormat("glueparquet", compression="snappy")
tgt_bronze_medidor_node1763365363469.writeFrame(trf_bronze_medidor_node1763365141553)
job.commit()