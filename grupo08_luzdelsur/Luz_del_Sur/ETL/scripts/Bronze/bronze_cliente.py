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

# Script generated for node s_cliente
s_cliente_node1764606614917 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="cliente", transformation_ctx="s_cliente_node1764606614917")

# Script generated for node t_cliente
t_cliente_node1764606652166 = ApplyMapping.apply(frame=s_cliente_node1764606614917, mappings=[("id_cliente", "long", "id_cliente", "bigint"), ("tipo_cliente", "string", "tipo_cliente", "string"), ("dni", "string", "dni", "string"), ("celular", "string", "celular", "string"), ("email", "string", "email", "string"), ("id_ubicacion", "long", "id_ubicacion", "int"), ("fecha_alta", "string", "fecha_alta", "date"), ("estado_cliente", "string", "estado_cliente", "string")], transformation_ctx="t_cliente_node1764606652166")

# Script generated for node l_cliente
EvaluateDataQuality().process_rows(frame=t_cliente_node1764606652166, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764605765790", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
l_cliente_node1764606740904 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/cliente/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="l_cliente_node1764606740904")
l_cliente_node1764606740904.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_cliente")
l_cliente_node1764606740904.setFormat("glueparquet", compression="snappy")
l_cliente_node1764606740904.writeFrame(t_cliente_node1764606652166)
job.commit()