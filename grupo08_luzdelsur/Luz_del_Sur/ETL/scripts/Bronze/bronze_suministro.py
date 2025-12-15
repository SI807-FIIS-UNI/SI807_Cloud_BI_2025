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

# Script generated for node s_suministro
s_suministro_node1764608440396 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="suministro", transformation_ctx="s_suministro_node1764608440396")

# Script generated for node t_suministro
t_suministro_node1764608475548 = ApplyMapping.apply(frame=s_suministro_node1764608440396, mappings=[("id_suministro", "long", "id_suministro", "bigint"), ("id_cliente", "long", "id_cliente", "bigint"), ("id_ubicacion", "long", "id_ubicacion", "int"), ("direccion_suministro", "string", "direccion_suministro", "string"), ("nivel_tension", "string", "nivel_tension", "string"), ("id_sist_electrico", "long", "id_sist_electrico", "bigint"), ("fecha_alta_suministro", "string", "fecha_alta_suministro", "date"), ("estado_suministro", "string", "estado_suministro", "string")], transformation_ctx="t_suministro_node1764608475548")

# Script generated for node l_suministro
EvaluateDataQuality().process_rows(frame=t_suministro_node1764608475548, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764608407637", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
l_suministro_node1764608622607 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/suministro/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="l_suministro_node1764608622607")
l_suministro_node1764608622607.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_suministro")
l_suministro_node1764608622607.setFormat("glueparquet", compression="snappy")
l_suministro_node1764608622607.writeFrame(t_suministro_node1764608475548)
job.commit()