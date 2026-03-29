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

# Script generated for node s_ubicacion
s_ubicacion_node1764610385894 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="ubicacion", transformation_ctx="s_ubicacion_node1764610385894")

# Script generated for node t_ubicacion
t_ubicacion_node1764610577728 = ApplyMapping.apply(frame=s_ubicacion_node1764610385894, mappings=[("id_ubicacion", "long", "id_ubicacion", "bigint"), ("distrito", "string", "distrito", "string"), ("zona", "string", "zona", "string"), ("ubigeo", "long", "ubigeo", "bigint")], transformation_ctx="t_ubicacion_node1764610577728")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=t_ubicacion_node1764610577728, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764610280407", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1764610612008 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/ubicacion/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1764610612008")
AmazonS3_node1764610612008.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_ubicacion")
AmazonS3_node1764610612008.setFormat("glueparquet", compression="snappy")
AmazonS3_node1764610612008.writeFrame(t_ubicacion_node1764610577728)
job.commit()