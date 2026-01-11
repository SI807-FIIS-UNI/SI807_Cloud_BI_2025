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

# Script generated for node s_asig_tarifa
s_asig_tarifa_node1764610295057 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="asignacion_tarifa", transformation_ctx="s_asig_tarifa_node1764610295057")

# Script generated for node t_asig_tarifa
t_asig_tarifa_node1764610322561 = ApplyMapping.apply(frame=s_asig_tarifa_node1764610295057, mappings=[("id_asignacion_tarifa", "long", "id_asignacion_tarifa", "bigint"), ("id_suministro", "long", "id_suministro", "bigint"), ("id_tarifa", "long", "id_tarifa", "bigint")], transformation_ctx="t_asig_tarifa_node1764610322561")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=t_asig_tarifa_node1764610322561, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764610280407", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1764610339945 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/asignacion_tarifa/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1764610339945")
AmazonS3_node1764610339945.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_asig_tarifa")
AmazonS3_node1764610339945.setFormat("glueparquet", compression="snappy")
AmazonS3_node1764610339945.writeFrame(t_asig_tarifa_node1764610322561)
job.commit()