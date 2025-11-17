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

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1763363280605 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="cliente", transformation_ctx="AWSGlueDataCatalog_node1763363280605")

# Script generated for node trf_bronze_cliente
trf_bronze_cliente_node1763363331830 = ApplyMapping.apply(frame=AWSGlueDataCatalog_node1763363280605, mappings=[("id_cliente", "long", "id_cliente", "long"), ("tipo_documento", "string", "tipo_documento", "string"), ("nro_documento", "string", "nro_documento", "string"), ("nombre_cliente", "string", "nombre_cliente", "string"), ("tipo_cliente", "string", "tipo_cliente", "string"), ("fecha_alta", "string", "fecha_alta", "date"), ("estado_cliente", "string", "estado_cliente", "string"), ("email", "string", "email", "string"), ("telefono", "string", "telefono", "string")], transformation_ctx="trf_bronze_cliente_node1763363331830")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=trf_bronze_cliente_node1763363331830, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763363274803", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1763364257769 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/cliente/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1763364257769")
AmazonS3_node1763364257769.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_cliente")
AmazonS3_node1763364257769.setFormat("glueparquet", compression="snappy")
AmazonS3_node1763364257769.writeFrame(trf_bronze_cliente_node1763363331830)
job.commit()