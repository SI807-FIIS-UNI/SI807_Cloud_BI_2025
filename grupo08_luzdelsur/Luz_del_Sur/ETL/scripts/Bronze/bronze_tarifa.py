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

# Script generated for node s_tarifa
s_tarifa_node1764609528142 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="tarifa", transformation_ctx="s_tarifa_node1764609528142")

# Script generated for node t_tarifa
t_tarifa_node1764609716317 = ApplyMapping.apply(frame=s_tarifa_node1764609528142, mappings=[("id_tarifa", "long", "id_tarifa", "bigint"), ("codigo_tarifa", "string", "codigo_tarifa", "string"), ("cod_tarifa", "string", "cod_tarifa", "string"), ("descripcion", "string", "descripcion", "string"), ("nivel_tension", "string", "nivel_tension", "string"), ("segmento_objetivo", "string", "segmento_objetivo", "string"), ("tipo_cliente", "string", "tipo_cliente", "string"), ("cargo_fijo", "double", "cargo_fijo", "double"), ("cargo_energia", "double", "cargo_energia", "double"), ("cargo_hp", "double", "cargo_hp", "double"), ("cargo_fp", "double", "cargo_fp", "double"), ("incluye_demanda", "string", "incluye_demanda", "boolean"), ("estado_tarifa", "string", "estado_tarifa", "string"), ("fecha_inicio_vigencia", "string", "fecha_inicio_vigencia", "date")], transformation_ctx="t_tarifa_node1764609716317")

# Script generated for node l_tarifa
EvaluateDataQuality().process_rows(frame=t_tarifa_node1764609716317, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764608750332", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
l_tarifa_node1764609982025 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/tarifa/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="l_tarifa_node1764609982025")
l_tarifa_node1764609982025.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_tarifa")
l_tarifa_node1764609982025.setFormat("glueparquet", compression="snappy")
l_tarifa_node1764609982025.writeFrame(t_tarifa_node1764609716317)
job.commit()