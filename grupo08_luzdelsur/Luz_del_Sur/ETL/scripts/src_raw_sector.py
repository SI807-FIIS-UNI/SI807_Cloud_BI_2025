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

# Script generated for node src_raw_sector
src_raw_sector_node1763365819321 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="sector", transformation_ctx="src_raw_sector_node1763365819321")

# Script generated for node trf_bronze_sector
trf_bronze_sector_node1763365855439 = ApplyMapping.apply(frame=src_raw_sector_node1763365819321, mappings=[("cod_sector", "string", "cod_sector", "string"), ("distrito", "string", "distrito", "string"), ("zona", "string", "zona", "string"), ("sucursal", "long", "sucursal", "string"), ("sector_tipico", "long", "sector_tipico", "long"), ("fecha_creacion", "string", "fecha_creacion", "date"), ("estado_sector", "string", "estado_sector", "string")], transformation_ctx="trf_bronze_sector_node1763365855439")

# Script generated for node tgt_bronze_sector
EvaluateDataQuality().process_rows(frame=trf_bronze_sector_node1763365855439, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763365096638", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
tgt_bronze_sector_node1763365903375 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/sector/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="tgt_bronze_sector_node1763365903375")
tgt_bronze_sector_node1763365903375.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_sector")
tgt_bronze_sector_node1763365903375.setFormat("glueparquet", compression="snappy")
tgt_bronze_sector_node1763365903375.writeFrame(trf_bronze_sector_node1763365855439)
job.commit()