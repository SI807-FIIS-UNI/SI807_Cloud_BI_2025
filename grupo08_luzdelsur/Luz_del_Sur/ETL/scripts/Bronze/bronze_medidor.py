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

# Script generated for node s_medidor
s_medidor_node1764608890637 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="medidor", transformation_ctx="s_medidor_node1764608890637")

# Script generated for node t_medidor
t_medidor_node1764608965832 = ApplyMapping.apply(frame=s_medidor_node1764608890637, mappings=[("id_medidor", "long", "id_medidor", "bigint"), ("id_suministro", "long", "id_suministro", "bigint"), ("marca_medidor", "string", "marca_medidor", "string"), ("tecnologia_medidor", "string", "tecnologia_medidor", "string"), ("numero_serie", "string", "numero_serie", "string"), ("fecha_instalacion", "string", "fecha_instalacion", "date"), ("fecha_retiro", "string", "fecha_retiro", "date"), ("estado_medidor", "string", "estado_medidor", "string")], transformation_ctx="t_medidor_node1764608965832")

# Script generated for node l_medidor
EvaluateDataQuality().process_rows(frame=t_medidor_node1764608965832, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764608750332", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
l_medidor_node1764609164156 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/medidor/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="l_medidor_node1764609164156")
l_medidor_node1764609164156.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_medidor")
l_medidor_node1764609164156.setFormat("glueparquet", compression="snappy")
l_medidor_node1764609164156.writeFrame(t_medidor_node1764608965832)
job.commit()