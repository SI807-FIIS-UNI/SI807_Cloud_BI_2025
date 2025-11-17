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

# Script generated for node src_raw_asignacion_tarifa
src_raw_asignacion_tarifa_node1763366325199 = glueContext.create_dynamic_frame.from_catalog(database="raw_db", table_name="raw_asignacion_tarifa_csv", transformation_ctx="src_raw_asignacion_tarifa_node1763366325199")

# Script generated for node trf_bronze_asignacion_tarifa
trf_bronze_asignacion_tarifa_node1763366356902 = ApplyMapping.apply(frame=src_raw_asignacion_tarifa_node1763366325199, mappings=[("id_asignacion_tarifa", "long", "id_asignacion_tarifa", "long"), ("id_suministro", "long", "id_suministro", "long"), ("cod_tarifa", "string", "cod_tarifa", "string"), ("fecha_inicio", "string", "fecha_inicio", "date"), ("fecha_fin", "string", "fecha_fin", "date"), ("estado_asignacion", "string", "estado_asignacion", "string")], transformation_ctx="trf_bronze_asignacion_tarifa_node1763366356902")

# Script generated for node tgt_bronze_asignacion_tarifa
EvaluateDataQuality().process_rows(frame=trf_bronze_asignacion_tarifa_node1763366356902, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1763365096638", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
tgt_bronze_asignacion_tarifa_node1763366381825 = glueContext.getSink(path="s3://lds-s3-bucket-demo/bronze/asignacion_tarifa/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="tgt_bronze_asignacion_tarifa_node1763366381825")
tgt_bronze_asignacion_tarifa_node1763366381825.setCatalogInfo(catalogDatabase="bronze_db",catalogTableName="bronze_asignacion_tarifa")
tgt_bronze_asignacion_tarifa_node1763366381825.setFormat("glueparquet", compression="snappy")
tgt_bronze_asignacion_tarifa_node1763366381825.writeFrame(trf_bronze_asignacion_tarifa_node1763366356902)
job.commit()