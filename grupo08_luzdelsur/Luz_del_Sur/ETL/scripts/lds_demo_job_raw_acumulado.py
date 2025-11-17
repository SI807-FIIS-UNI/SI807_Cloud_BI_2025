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
AWSGlueDataCatalog_node1763359520400 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="acumulado", transformation_ctx="AWSGlueDataCatalog_node1763359520400")

# Script generated for node trf_bronze_acumulado
trf_bronze_acumulado_node1763360752280 = ApplyMapping.apply(frame=AWSGlueDataCatalog_node1763359520400, mappings=[("id_suministro", "long", "id_suministro", "long"), ("id_medidor", "long", "id_medidor", "long"), ("anio_mes", "string", "anio_mes", "string"), ("energia_total_kwh", "double", "energia_total_kwh", "double"), ("demanda_max_kw", "double", "demanda_max_kw", "double"), ("n_registros", "long", "n_registros", "int"), ("n_registros_error", "long", "n_registros_error", "int")], transformation_ctx="trf_bronze_acumulado_node1763360752280")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=trf_bronze_acumulado_node1763360752280, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763359454645", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1763361089962 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/acumulado/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1763361089962")
AmazonS3_node1763361089962.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_acumulado")
AmazonS3_node1763361089962.setFormat("glueparquet", compression="snappy")
AmazonS3_node1763361089962.writeFrame(trf_bronze_acumulado_node1763360752280)
job.commit()