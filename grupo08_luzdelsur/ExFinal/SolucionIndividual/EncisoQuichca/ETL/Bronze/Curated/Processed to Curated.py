import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
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

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1765852200471 = glueContext.create_dynamic_frame.from_catalog(database="final_db_bronze", table_name="processed_us_accidents", transformation_ctx="AWSGlueDataCatalog_node1765852200471")

# Script generated for node Drop_Fields
Drop_Fields_node1765852322143 = DropFields.apply(frame=AWSGlueDataCatalog_node1765852200471, paths=["start_lat", "start_lng", "end_lat", "end_lng", "distance_mi_#0", "description", "street", "zipcode", "airport_code", "wind_direction", "amenity", "bump", "crossing", "give_way", "junction", "no_exit", "railway", "roundabout", "station", "stop", "traffic_calming", "traffic_signal", "turning_loop", "sunrise_sunset", "civil_twilight", "nautical_twilight", "astronomical_twilight"], transformation_ctx="Drop_Fields_node1765852322143")

# Script generated for node SQL Query
SqlQuery0 = '''
SELECT
  CAST(severity AS INT) AS severity,

  NULLIF(TRIM(state), '') AS state,
  NULLIF(TRIM(city), '') AS city,
  NULLIF(TRIM(timezone), '') AS timezone,

  CAST(start_time AS TIMESTAMP) AS start_time,
  CAST(weather_timestamp AS TIMESTAMP) AS weather_timestamp,

  NULLIF(TRIM(weather_condition), '') AS weather_condition,

  CAST(`temperature_f_#1` AS DOUBLE) AS temperature_f,
  CAST(`humidity_%_#3` AS DOUBLE) AS humidity_pct,
  CAST(`pressure_in_#4` AS DOUBLE) AS pressure_in,
  CAST(`visibility_mi_#5` AS DOUBLE) AS visibility_mi,
  CAST(`wind_speed_mph_#6` AS DOUBLE) AS wind_speed_mph,
  CAST(`precipitation_in_#7` AS DOUBLE) AS precipitation_in,
  CAST(`wind_chill_f_#2` AS DOUBLE) AS wind_chill_f

FROM myDataSource

'''
SQLQuery_node1765852489928 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":Drop_Fields_node1765852322143}, transformation_ctx = "SQLQuery_node1765852489928")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1765852489928, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1765851863065", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1765853486537 = glueContext.getSink(path="s3://ef-sin-bucket/bronze/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1765853486537")
AmazonS3_node1765853486537.setCatalogInfo(catalogDatabase="final_db_bronze",catalogTableName="curated_us_accidents")
AmazonS3_node1765853486537.setFormat("glueparquet", compression="snappy")
AmazonS3_node1765853486537.writeFrame(SQLQuery_node1765852489928)
job.commit()