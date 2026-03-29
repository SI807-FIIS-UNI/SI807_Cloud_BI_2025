import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrameCollection
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame

# Script generated for node Custom Transform
def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    import pyspark.sql.functions as F
    from awsglue.dynamicframe import DynamicFrame, DynamicFrameCollection

    # Convertir DynamicFrame de entrada a DataFrame
    dyf = dfc.select(list(dfc.keys())[0])
    df = dyf.toDF()

    # Columnas numéricas que necesitan limpieza
    numeric_cols = [
        "energia_valle",
        "energia_pico",
        "energia_media",
        "energia_total",
        "monto_facturado"
    ]

    # Convertir blancos → NULL
    for c in numeric_cols:
        df = df.withColumn(
            c,
            F.when(F.col(c) == "", None).otherwise(F.col(c))
        )

    # Convertir de vuelta a DynamicFrame
    new_dyf = DynamicFrame.fromDF(df, glueContext, "cleaned_consolidado")

    # Retornar como DynamicFrameCollection (obligatorio)
    return DynamicFrameCollection({"cleaned_consolidado": new_dyf}, glueContext)
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

# Script generated for node bronze_consolidado
bronze_consolidado_node1764610814492 = glueContext.create_dynamic_frame.from_catalog(database="lds_raw", table_name="consolidado_mensual", transformation_ctx="bronze_consolidado_node1764610814492")

# Script generated for node t_consolidado
t_consolidado_node1764610862727 = ApplyMapping.apply(frame=bronze_consolidado_node1764610814492, mappings=[("id_suministro", "long", "id_suministro", "bigint"), ("id_medidor", "long", "id_medidor", "bigint"), ("anio_mes", "string", "anio_mes", "string"), ("energia_valle", "double", "energia_valle", "double"), ("energia_pico", "double", "energia_pico", "double"), ("energia_media", "double", "energia_media", "double"), ("energia_total", "double", "energia_total", "double"), ("monto_facturado", "double", "monto_facturado", "double")], transformation_ctx="t_consolidado_node1764610862727")

# Script generated for node Custom Transform
CustomTransform_node1764611221584 = MyTransform(glueContext, DynamicFrameCollection({"t_consolidado_node1764610862727": t_consolidado_node1764610862727}, glueContext))

# Script generated for node S_collection_consolidado
S_collection_consolidado_node1764612200593 = SelectFromCollection.apply(dfc=CustomTransform_node1764611221584, key=list(CustomTransform_node1764611221584.keys())[0], transformation_ctx="S_collection_consolidado_node1764612200593")

# Script generated for node l_consolidado
EvaluateDataQuality().process_rows(frame=S_collection_consolidado_node1764612200593, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1764610280407", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
l_consolidado_node1764611941578 = glueContext.getSink(path="s3://lds-s3-bucket-final/bronze/consolidado_mensual/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="l_consolidado_node1764611941578")
l_consolidado_node1764611941578.setCatalogInfo(catalogDatabase="lds_bronze",catalogTableName="bronze_consolidado")
l_consolidado_node1764611941578.setFormat("glueparquet", compression="snappy")
l_consolidado_node1764611941578.writeFrame(S_collection_consolidado_node1764612200593)
job.commit()