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

# Script generated for node src_raw_tarifa
src_raw_tarifa_node1763365993881 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="raw_tarifa_csv", transformation_ctx="src_raw_tarifa_node1763365993881")

# Script generated for node trf_bronze_tarifa
trf_bronze_tarifa_node1763366008426 = ApplyMapping.apply(frame=src_raw_tarifa_node1763365993881, mappings=[("cod_tarifa", "string", "cod_tarifa", "string"), ("descripcion", "string", "descripcion", "string"), ("nivel_tension", "string", "nivel_tension", "string"), ("segmento_objetivo", "string", "segmento_objetivo", "string"), ("cargo_fijo", "double", "cargo_fijo", "double"), ("cargo_energia", "double", "cargo_energia", "double"), ("cargo_hp", "double", "cargo_hp", "double"), ("cargo_fp", "double", "cargo_fp", "double"), ("incluye_demanda", "string", "incluye_demanda", "string"), ("estado_tarifa", "string", "estado_tarifa", "string"), ("fecha_inicio_vigencia", "string", "fecha_inicio_vigencia", "date")], transformation_ctx="trf_bronze_tarifa_node1763366008426")

# Script generated for node tgt_bronze_tarifa
EvaluateDataQuality().process_rows(frame=trf_bronze_tarifa_node1763366008426, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763365096638", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
tgt_bronze_tarifa_node1763366117636 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/tarifa/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="tgt_bronze_tarifa_node1763366117636")
tgt_bronze_tarifa_node1763366117636.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_tarifa")
tgt_bronze_tarifa_node1763366117636.setFormat("glueparquet", compression="snappy")
tgt_bronze_tarifa_node1763366117636.writeFrame(trf_bronze_tarifa_node1763366008426)
job.commit()