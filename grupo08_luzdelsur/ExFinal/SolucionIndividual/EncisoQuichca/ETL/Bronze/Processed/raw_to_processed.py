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

# Script generated for node Accidentes_US
Accidentes_US_node1765849497482 = glueContext.create_dynamic_frame.from_catalog(database="final_db_bronze", table_name="raw", transformation_ctx="Accidentes_US_node1765849497482")

# Script generated for node Cambio de Tipo de Datos
CambiodeTipodeDatos_node1765851487278 = ApplyMapping.apply(frame=Accidentes_US_node1765849497482, mappings=[("id", "string", "id", "string"), ("source", "string", "source", "string"), ("severity", "long", "severity", "bigint"), ("start_time", "string", "start_time", "timestamp"), ("end_time", "string", "end_time", "timestamp"), ("start_lat", "double", "start_lat", "double"), ("start_lng", "double", "start_lng", "double"), ("end_lat", "double", "end_lat", "double"), ("end_lng", "double", "end_lng", "double"), ("`distance(mi)`", "double", "`distance(mi)`", "double"), ("description", "string", "description", "string"), ("street", "string", "street", "string"), ("city", "string", "city", "string"), ("county", "string", "county", "string"), ("state", "string", "state", "string"), ("zipcode", "string", "zipcode", "string"), ("country", "string", "country", "string"), ("timezone", "string", "timezone", "string"), ("airport_code", "string", "airport_code", "string"), ("weather_timestamp", "string", "weather_timestamp", "string"), ("`temperature(f)`", "double", "`temperature(f)`", "double"), ("`wind_chill(f)`", "double", "`wind_chill(f)`", "double"), ("`humidity(%)`", "double", "`humidity(%)`", "double"), ("`pressure(in)`", "double", "`pressure(in)`", "double"), ("`visibility(mi)`", "double", "`visibility(mi)`", "double"), ("wind_direction", "string", "wind_direction", "string"), ("`wind_speed(mph)`", "double", "`wind_speed(mph)`", "double"), ("`precipitation(in)`", "double", "`precipitation(in)`", "double"), ("weather_condition", "string", "weather_condition", "string"), ("amenity", "boolean", "amenity", "boolean"), ("bump", "boolean", "bump", "boolean"), ("crossing", "boolean", "crossing", "boolean"), ("give_way", "boolean", "give_way", "boolean"), ("junction", "boolean", "junction", "boolean"), ("no_exit", "boolean", "no_exit", "boolean"), ("railway", "boolean", "railway", "boolean"), ("roundabout", "boolean", "roundabout", "boolean"), ("station", "boolean", "station", "boolean"), ("stop", "boolean", "stop", "boolean"), ("traffic_calming", "boolean", "traffic_calming", "boolean"), ("traffic_signal", "boolean", "traffic_signal", "boolean"), ("turning_loop", "boolean", "turning_loop", "boolean"), ("sunrise_sunset", "string", "sunrise_sunset", "string"), ("civil_twilight", "string", "civil_twilight", "string"), ("nautical_twilight", "string", "nautical_twilight", "string"), ("astronomical_twilight", "string", "astronomical_twilight", "string")], transformation_ctx="CambiodeTipodeDatos_node1765851487278")

# Script generated for node Guardando Processed
EvaluateDataQuality().process_rows(frame=CambiodeTipodeDatos_node1765851487278, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1765849448158", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
GuardandoProcessed_node1765851741879 = glueContext.getSink(path="s3://ef-sin-bucket/bronze/processed/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="GuardandoProcessed_node1765851741879")
GuardandoProcessed_node1765851741879.setCatalogInfo(catalogDatabase="final_db_bronze",catalogTableName="processed_us_accidents")
GuardandoProcessed_node1765851741879.setFormat("glueparquet", compression="snappy")
GuardandoProcessed_node1765851741879.writeFrame(CambiodeTipodeDatos_node1765851487278)
job.commit()