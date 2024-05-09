from jobs.demand_prediction.demand_prediction import demand_prediction


def analyze(spark, format="parquet", gcs_input_path=None, gcs_output_path=None):
    df = spark.read.format(format).load(gcs_input_path)
    demand_prediction(df, gcs_output_path)
    spark.stop()
